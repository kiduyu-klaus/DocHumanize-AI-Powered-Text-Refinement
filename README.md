# DocHumanize

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

✨ **AI-Powered Text Refinement** - Transform robotic text into natural, human-sounding content with the power of Ollama's LLM cloud

## Overview

DocHumanize is a command-line tool that uses Ollama's cloud-based language models to refine and humanize text content. Perfect for developers, content creators, and professionals who need to polish AI-generated text or technical documents into more natural, engaging content.

## Features

- **AI-Powered Refinement**: Leverages Ollama's cogito-2.1:671b-cloud model to rewrite and enhance text
- **Document Support**: Processes both plain text and Microsoft Word (.docx) files
- **CLI Interface**: Simple command-line tool for easy integration into workflows
- **Customizable Output**: Adjust formality, tone, and style parameters
- **Batch Processing**: Handle multiple files or directories at once
- **Preserve Formatting**: Maintains original document structure and formatting
- **Progress Tracking**: Real-time progress indicators for long documents

## Quick Start
```bash
# Install dependencies
pip install python-docx requests

# Humanize a document
python docx_processor.py input.docx

# With custom model and settings
python docx_processor.py input.docx --model cogito-2.1:671b-cloud --temperature 0.7
```

## Usage

### Basic Document Processing
```python
from docx_processor import process_docx

# Process a single document
output_path = process_docx(
    input_path="document.docx",
    ollama_model="cogito-2.1:671b-cloud",
    ollama_url="http://localhost:11434",
    temperature=0.7,
    preserve_formatting=True
)
```

### Batch Processing
```python
from docx_processor import batch_process_docx

# Process multiple documents
output_files = batch_process_docx(
    directory="./documents",
    ollama_model="cogito-2.1:671b-cloud",
    temperature=0.7
)
```

### With Progress Tracking
```python
from docx_processor import process_docx_with_progress

def progress_handler(current, total, message):
    print(f"[{current}/{total}] {message}")

output_path = process_docx_with_progress(
    input_path="document.docx",
    ollama_model="cogito-2.1:671b-cloud",
    progress_callback=progress_handler
)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ollama_model` | `cogito-2.1:671b-cloud` | The Ollama model to use for text refinement |
| `ollama_url` | `http://localhost:11434` | URL of your Ollama instance |
| `temperature` | `0.7` | Controls creativity (0.0-1.0, higher = more creative) |
| `max_tokens` | `2000` | Maximum tokens per API request |
| `preserve_formatting` | `True` | Maintain original document formatting |

## Why DocHumanize?

- **Save Time**: Automatically refine content instead of manual rewriting
- **Improve Readability**: Transform technical or AI-generated text into natural language
- **Consistent Quality**: Maintain professional tone across all your documents
- **Privacy Focused**: Choose between Ollama Cloud or self-hosted instances
- **Format Preservation**: Keep your document styling intact while improving content

## Perfect For

- Refining AI-generated content
- Improving technical documentation
- Preparing client-facing materials
- Enhancing academic writing
- Batch processing multiple documents
- Converting robotic text to natural language

## Requirements

- Python 3.7+
- Ollama installed and running
- python-docx
- requests

## TODO

- [ ] Add support for PDF files
- [ ] Implement configuration file for custom presets
- [ ] Add CLI argument parser for command-line usage
- [ ] Support for additional LLM providers (OpenAI, Anthropic)
- [ ] Web interface for non-technical users
- [ ] Plugin system for custom transformations
- [ ] Multi-language support
- [ ] Integration with popular editors (VS Code, Obsidian)
- [ ] Real-time streaming output display
- [ ] Support for markdown files
- [ ] Custom prompt templates
- [ ] Undo/redo functionality
- [ ] Document comparison view (before/after)

## License

MIT