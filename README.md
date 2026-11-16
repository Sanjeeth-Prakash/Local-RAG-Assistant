# Local RAG Assistant with Llama 3.1 and Ollama

A lightweight Retrieval Augmented Generation (RAG) system that enables conversation with local codebase documentation using Llama 3.1 running on Ollama.

## Overview

This project demonstrates a complete RAG pipeline for local codebases:
- **Retrieve**: Keyword-based search through Python files
- **Augment**: Build context from relevant code snippets
- **Generate**: Answer questions using Llama 3.1 with grounded responses

## Features

- Local LLM inference using Ollama (no API keys required)
- Keyword-based retrieval from Python codebases
- Grounded responses with source citation
- Zero external dependencies beyond Python standard library

## Prerequisites

- Python 3.11+
- Ollama installed and running
- Llama 3.1 8B model pulled via `ollama pull llama3.1`

## Installation

```bash
pip install requests
```

## Usage

```bash
python rag_chat_keyword.py
```

Ask questions about your codebase:
```
>> How does the expense extractor work?
```

The assistant retrieves relevant files and answers using only your local context.

## Architecture

```
User Question → Keyword Search → Relevant Docs → Context → Llama 3.1 → Grounded Answer
```

## Files

- `rag_chat_keyword.py` — Main RAG chat implementation
- `expense_extractor.py` — Example extraction project
- `tool_calculator.py` — Function calling demo
- `smart_git.py` — AI commit message generator

## Tech Stack

- **LLM**: Llama 3.1 8B (Ollama)
- **Retrieval**: Keyword overlap scoring
- **Language**: Python
- **Framework**: Pure Python (no heavy dependencies)

## License

MIT
