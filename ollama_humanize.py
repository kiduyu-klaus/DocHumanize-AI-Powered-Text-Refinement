import requests
import json


def humanize_with_ollama(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434", temperature=0.7, max_tokens=2000):
    """
    Uses Ollama to humanize text by making it sound more natural and less AI-generated.
    
    :param text: the text to be humanized
    :param model: the Ollama model to use (default: cogito-2.1:671b-cloud)
    :param ollama_url: the URL of the Ollama API (default: http://localhost:11434)
    :param temperature: controls randomness (0.0-1.0, higher = more creative)
    :param max_tokens: maximum number of tokens in the response
    :return: the humanized text
    """
    
    prompt = f"""Rewrite the following text to make it sound more natural and human-like. 
Keep the same meaning and key information, but vary the sentence structure, 
use more casual language where appropriate, and make it feel like a person wrote it naturally.
Don't add any preamble or explanation, just provide the rewritten text.

Text to rewrite:
{text}

Rewritten text:"""

    try:
        # Call Ollama API
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
            return result.get("response", "").strip()
        else:
            raise Exception(f"Ollama API returned status code {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to Ollama. Make sure Ollama is running at " + ollama_url)
    except requests.exceptions.Timeout:
        raise Exception("Request to Ollama timed out")
    except Exception as e:
        raise Exception(f"Error calling Ollama: {str(e)}")


def humanize_with_ollama_streaming(text, model="cogito-2.1:671b-cloud", ollama_url="http://localhost:11434", 
                                   temperature=0.7, max_tokens=2000, callback=None):
    """
    Uses Ollama to humanize text with streaming output.
    
    :param text: the text to be humanized
    :param model: the Ollama model to use (default: cogito-2.1:671b-cloud)
    :param ollama_url: the URL of the Ollama API (default: http://localhost:11434)
    :param temperature: controls randomness (0.0-1.0, higher = more creative)
    :param max_tokens: maximum number of tokens in the response
    :param callback: optional callback function that receives each chunk of text
    :return: the complete humanized text
    """
    
    prompt = f"""Rewrite the following text to make it sound more natural and human-like. 
Keep the same meaning and key information, but vary the sentence structure, 
use more casual language where appropriate, and make it feel like a person wrote it naturally.
Don't add any preamble or explanation, just provide the rewritten text.

Text to rewrite:
{text}

Rewritten text:"""

    try:
        # Call Ollama API with streaming
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
                    chunk = json.loads(line)
                    text_chunk = chunk.get("response", "")
                    full_response += text_chunk
                    
                    if callback:
                        callback(text_chunk)
                    
                    if chunk.get("done", False):
                        break
            
            return full_response.strip()
        else:
            raise Exception(f"Ollama API returned status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to Ollama. Make sure Ollama is running at " + ollama_url)
    except requests.exceptions.Timeout:
        raise Exception("Request to Ollama timed out")
    except Exception as e:
        raise Exception(f"Error calling Ollama: {str(e)}")