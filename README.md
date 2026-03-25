# NBG Banking Agent

An AI-powered banking assistant for National Bank of Greece (NBG), built with LangGraph, ChromaDB, Crawl4AI, and OpenAI.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- OpenAI API key
- LangSmith API key

## Installation

1. Clone the repository and navigate to the project directory.

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys.

## Usage

Run the chat interface:
```bash
uv run python main.py
```

## Pre-Demo Data Setup

```bash
uv run python scripts/01_crawl_nbg.py
uv run python scripts/02_build_vector_store.py
uv run python scripts/03_test_retrieval.py
```

## Demo Queries

Try these queries to showcase the agent's intelligent routing (RAG, live scrape, or both):

### Combined Knowledge + Live Data (the showstopper)
- "I have a Gold credit card — what rewards can I earn with go4more and are there any current offers I can use?"
- "I'm interested in a green mortgage — what are the Estia Green loan terms and is the My Home II state program still available?"

### Live Website Scraping
- "What are NBG's latest financial results?"
- "Tell me about the new Skroutz Plus Mastercard"

### Knowledge Base (RAG)
- "Compare the benefits of a savings account vs a current account"

## Tests

```bash
uv run pytest tests/ -v
```
