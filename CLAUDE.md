# NBG Banking Agent

Demo project: an AI-powered banking assistant for National Bank of Greece (NBG) using LangGraph.

## Architecture

- **LangGraph** - Agent orchestration and state management
- **ChromaDB** - Vector store for document retrieval (RAG)
- **Crawl4AI** - Web crawling of NBG website content
- **OpenAI** - LLM (GPT-4o) and embeddings (text-embedding-3-small)
- **LangSmith** - Tracing and observability

## Build & Run

```bash
uv sync
cp .env.example .env  # then fill in API keys
uv run python main.py
```

## Tests

```bash
uv run pytest tests/ -v
```

## Project Structure

- `config/` - Settings and configuration (Pydantic BaseSettings)
- `src/crawl/` - Web crawling pipeline
- `src/rag/` - RAG pipeline (chunking, embedding, retrieval)
- `src/tools/` - LangGraph tools
- `src/agent/` - Agent graph definition
- `src/cli/` - CLI chat interface
- `data/` - Raw, processed, and vector store data
