import requests
import json
import os


def load_humanizer_prompt(prompt_file="humanizer.txt"):
    """
    Load the humanizer prompt from a text file.
    
    :param prompt_file: path to the humanizer prompt file
    :return: the prompt text
    """
    # Try to load from file if it exists
    if os.path.exists(prompt_file):
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    # Fallback to simpler embedded prompt
    return """Rewrite the following text to make it sound more natural and human-like. 
Keep the same meaning and key information, but vary the sentence structure, 
use more casual language where appropriate, and make it feel like a person wrote it naturally.
Do not add any preamble or explanation, just provide the rewritten text."""


def humanize_with_ollama(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434", 
                        temperature=0.7, max_tokens=2000, prompt_file="humanizer.txt",
                        use_system_prompt=True):
    """
    Uses Ollama to humanize text by making it sound more natural and less AI-generated.
    
    :param text: the text to be humanized
    :param model: the Ollama model to use (default: cogito-2.1:671b-cloud)
    :param ollama_url: the URL of the Ollama API (default: http://localhost:11434)
    :param temperature: controls randomness (0.0-1.0, higher = more creative)
    :param max_tokens: maximum number of tokens in the response
    :param prompt_file: path to the humanizer prompt file
    :param use_system_prompt: whether to use system/user message format (better for chat models)
    :return: the humanized text
    """
    
    # Load the system prompt
    system_prompt = load_humanizer_prompt(prompt_file)
    
    try:
        if use_system_prompt:
            # Use chat format with system and user messages (more reliable)
            response = requests.post(
                f"{ollama_url}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": f"Rewrite this text:\n\n{text}"
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=120
            )
        else:
            # Use generate format (fallback)
            prompt = f"{system_prompt}\n\nText to rewrite:\n{text}\n\nRewritten text:"
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=120
            )
        
        if response.status_code == 200:
            result = response.json()
            
            if use_system_prompt:
                # Extract from chat format
                return result.get("message", {}).get("content", "").strip()
            else:
                # Extract from generate format
                return result.get("response", "").strip()
        else:
            error_msg = f"Ollama API returned status code {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f": {error_detail}"
            except:
                error_msg += f": {response.text}"
            raise Exception(error_msg)
            
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to Ollama. Make sure Ollama is running at " + ollama_url)
    except requests.exceptions.Timeout:
        raise Exception("Request to Ollama timed out")
    except Exception as e:
        raise Exception(f"Error calling Ollama: {str(e)}")


def humanize_with_ollama_streaming(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434", 
                                   temperature=0.7, max_tokens=2000, callback=None, prompt_file="humanizer.txt",
                                   use_system_prompt=True):
    """
    Uses Ollama to humanize text with streaming output.
    
    :param text: the text to be humanized
    :param model: the Ollama model to use (default: cogito-2.1:671b-cloud)
    :param ollama_url: the URL of the Ollama API (default: http://localhost:11434)
    :param temperature: controls randomness (0.0-1.0, higher = more creative)
    :param max_tokens: maximum number of tokens in the response
    :param callback: optional callback function that receives each chunk of text
    :param prompt_file: path to the humanizer prompt file
    :param use_system_prompt: whether to use system/user message format
    :return: the complete humanized text
    """
    
    # Load the system prompt
    system_prompt = load_humanizer_prompt(prompt_file)
    
    try:
        if use_system_prompt:
            # Use chat format with streaming
            response = requests.post(
                f"{ollama_url}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": f"Rewrite this text:\n\n{text}"
                        }
                    ],
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                stream=True,
                timeout=120
            )
        else:
            # Use generate format with streaming
            prompt = f"{system_prompt}\n\nText to rewrite:\n{text}\n\nRewritten text:"
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                stream=True,
                timeout=120
            )
        
        if response.status_code == 200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        
                        if use_system_prompt:
                            # Extract from chat format
                            text_chunk = chunk.get("message", {}).get("content", "")
                        else:
                            # Extract from generate format
                            text_chunk = chunk.get("response", "")
                        
                        full_response += text_chunk
                        
                        if callback and text_chunk:
                            callback(text_chunk)
                        
                        if chunk.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            return full_response.strip()
        else:
            error_msg = f"Ollama API returned status code {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f": {error_detail}"
            except:
                error_msg += f": {response.text}"
            raise Exception(error_msg)
            
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to Ollama. Make sure Ollama is running at " + ollama_url)
    except requests.exceptions.Timeout:
        raise Exception("Request to Ollama timed out")
    except Exception as e:
        raise Exception(f"Error calling Ollama: {str(e)}")


def set_custom_prompt(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434",
                     temperature=0.7, max_tokens=2000, custom_system_prompt=None,
                     use_system_prompt=True):
    """
    Uses Ollama with a custom system prompt instead of the default humanizer prompt.
    
    :param text: the text to be processed
    :param model: the Ollama model to use
    :param ollama_url: the URL of the Ollama API
    :param temperature: controls randomness
    :param max_tokens: maximum number of tokens in the response
    :param custom_system_prompt: custom system prompt to use
    :param use_system_prompt: whether to use system/user message format
    :return: the processed text
    """
    
    if not custom_system_prompt:
        raise ValueError("custom_system_prompt must be provided")
    
    try:
        if use_system_prompt:
            response = requests.post(
                f"{ollama_url}/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": custom_system_prompt
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=120
            )
        else:
            prompt = f"{custom_system_prompt}\n\nText to process:\n{text}\n\nOutput:"
            
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=120
            )
        
        if response.status_code == 200:
            result = response.json()
            
            if use_system_prompt:
                return result.get("message", {}).get("content", "").strip()
            else:
                return result.get("response", "").strip()
        else:
            error_msg = f"Ollama API returned status code {response.status_code}"
            try:
                error_detail = response.json()
                error_msg += f": {error_detail}"
            except:
                error_msg += f": {response.text}"
            raise Exception(error_msg)
            
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to Ollama. Make sure Ollama is running at " + ollama_url)
    except requests.exceptions.Timeout:
        raise Exception("Request to Ollama timed out")
    except Exception as e:
        raise Exception(f"Error calling Ollama: {str(e)}")