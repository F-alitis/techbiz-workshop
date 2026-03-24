# Feature: LangGraph NBG Banking Agent

## Context

Building a hands-on demo for a 1-hour university presentation. The agent accesses NBG.gr subsites via pre-crawled RAG + live scraping and provides answers through a chat interface. LangSmith provides tracing, LangGraph Studio provides visual debugging. 70% pre-built scaffolding, 30% live-coded during presentation (classify_query_node, generate_answer_node).

## Tech Stack

| Component | Choice | Details |
|-----------|--------|---------|
| Language | Python 3.10+ | LangGraph's primary SDK |
| Package Manager | uv | Fast Python package manager |
| LLM | Azure OpenAI (o4-mini) | Via Responses API (`/openai/responses`) |
| Embeddings | Azure OpenAI (text-embedding-3-small) | Deployment: `uniko-poc-embeddings` |
| Framework | LangGraph v0.3+ | Graph-based agent orchestration |
| Vector Store | ChromaDB | Via `langchain-chroma` |
| Web Scraping | Crawl4AI | AI-optimized async crawler |
| CLI | Rich | Beautiful terminal output |
| Observability | LangSmith | Auto-tracing for LangGraph |
| Dev UI | LangGraph Studio | Visual graph debugging |

## Azure OpenAI Configuration

Two separate API configurations (same endpoint, different deployments/versions):

| API | Deployment | API Version | SDK |
|-----|-----------|-------------|-----|
| LLM (Responses API) | `o4-mini` | `2025-04-01-preview` | `openai.AzureOpenAI` (direct) |
| Embeddings | `uniko-poc-embeddings` | `2024-12-01-preview` | `langchain_openai.AzureOpenAIEmbeddings` |

Note: LangChain's `AzureChatOpenAI` does NOT support the Responses API. The LLM is accessed via a thin wrapper (`src/agent/llm.py`) using the `openai` SDK directly.

## Project Structure

```
nbg-banking-agent/
├── .env                          # API keys (not committed)
├── .env.example                  # Template for env vars
├── .gitignore
├── CLAUDE.md                     # Project instructions for Claude
├── README.md
├── pyproject.toml                # Dependencies (uv)
├── langgraph.json                # LangGraph Server config
├── main.py                       # CLI entry point
├── config/
│   └── settings.py               # Pydantic BaseSettings
├── data/
│   ├── raw/                      # Crawled markdown (gitignored)
│   ├── processed/                # Chunked documents (gitignored)
│   └── vector_store/             # ChromaDB storage (gitignored)
├── src/
│   ├── crawl/
│   │   ├── nbg_config.py         # NBG target URLs and crawl settings
│   │   └── crawler.py            # Crawl4AI AsyncWebCrawler
│   ├── rag/
│   │   ├── chunker.py            # RecursiveCharacterTextSplitter
│   │   ├── embeddings.py         # AzureOpenAIEmbeddings wrapper
│   │   └── vector_store.py       # ChromaDB via langchain-chroma
│   ├── tools/
│   │   ├── rag_retrieval.py      # @tool: vector search
│   │   └── live_scraper.py       # @tool: live Crawl4AI scrape
│   ├── agent/
│   │   ├── state.py              # InputState + AgentState
│   │   ├── llm.py                # Azure OpenAI Responses API wrapper
│   │   ├── prompts.py            # Classification + generation prompts
│   │   ├── nodes.py              # 4 nodes (2 stubs for live-coding)
│   │   └── graph.py              # StateGraph with input schema
│   └── cli/
│       └── chat.py               # Rich-based CLI chat loop
├── scripts/
│   ├── 01_crawl_nbg.py           # Pre-demo: crawl NBG subsites
│   ├── 02_build_vector_store.py  # Pre-demo: build ChromaDB
│   └── 03_test_retrieval.py      # Pre-demo: validate RAG
└── tests/
    ├── test_state.py             # AgentState schema tests
    ├── test_graph.py             # Graph compilation + routing tests
    ├── test_chunker.py           # Chunking tests
    └── test_vector_store.py      # ChromaDB operation tests
```

## Key Architecture Decisions

### State Design (InputState + AgentState)

```python
class InputState(TypedDict):
    """User-facing input — shown in LangGraph Studio."""
    messages: Annotated[Sequence[BaseMessage], add_messages]

class AgentState(InputState, total=False):
    """Internal state — populated by nodes, not shown in Studio input."""
    user_query: str
    rag_context: str
    live_content: str
    next_action: str
    final_answer: str
    tool_calls: int
```

The graph uses `StateGraph(AgentState, input=InputState)` so Studio only shows `messages`.

### LLM Wrapper (src/agent/llm.py)

```python
def ask_llm(prompt: str) -> str:
    client = AzureOpenAI(api_version=..., azure_endpoint=..., api_key=...)
    response = client.responses.create(model="o4-mini", input=prompt)
    return response.output_text
```

### Graph Flow

```
START → classify_query → [conditional routing]
  ├─→ retrieve_from_rag → generate_answer → END
  ├─→ scrape_live → generate_answer → END
  └─→ retrieve_from_rag → scrape_live → generate_answer → END
```

- `classify_query_node`: Extracts user_query from messages, decides routing (STUB)
- `retrieve_from_rag_node`: Queries ChromaDB, returns rag_context
- `scrape_live_node`: Crawls NBG page, returns live_content
- `generate_answer_node`: Generates answer from context (STUB)

## Environment Variables

```bash
# Azure OpenAI
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://users-direct-oai.openai.azure.com/
AZURE_OPENAI_API_VERSION=2025-04-01-preview
AZURE_OPENAI_DEPLOYMENT=o4-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=uniko-poc-embeddings
AZURE_OPENAI_EMBEDDING_API_VERSION=2024-12-01-preview

# LangSmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=nbg-banking-agent
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

## Commands

| Command | Description |
|---------|-------------|
| `uv sync` | Install dependencies |
| `uv run python main.py` | Start CLI chat |
| `langgraph dev` | Start LangGraph Server + Studio |
| `uv run pytest tests/ -v` | Run all tests |
| `uv run python scripts/01_crawl_nbg.py` | Crawl NBG website |
| `uv run python scripts/02_build_vector_store.py` | Build vector store |
| `uv run python scripts/03_test_retrieval.py` | Test retrieval |

## Live-Coding Stubs (30% of demo)

Two nodes in `src/agent/nodes.py` are stubs with TODO comments:

1. **`classify_query_node`** (line 10) — Uses `ask_llm()` with `CLASSIFICATION_PROMPT` to classify as "rag"/"scrape"/"both"
2. **`generate_answer_node`** (line 46) — Uses `ask_llm()` with `GENERATION_PROMPT` to generate contextual answers

## Tests (13 total)

| Test File | Count | Validates |
|-----------|-------|-----------|
| `tests/test_state.py` | 2 | AgentState creation and field types |
| `tests/test_graph.py` | 5 | Graph compiles, routing logic (rag/scrape/both) |
| `tests/test_chunker.py` | 4 | Chunk size, overlap, metadata, document processing |
| `tests/test_vector_store.py` | 2 | ChromaDB add/search, empty collection |

## Verification (all passing)

```
$ uv run pytest tests/ -v → 13 passed
$ python -c "from src.agent.graph import graph; ..." → Graph runs E2E
$ python -c "from src.agent.llm import ask_llm; ..." → LLM responds (o4-mini)
$ python -c "from src.rag.embeddings import ...; ..." → Embeddings: dim=1536
$ echo "/quit" | python main.py → CLI starts and exits cleanly
$ langgraph dev → Studio opens with messages-only input
```

## Demo Flow (1 hour)

| Time | Activity |
|------|----------|
| 5 min | Intro: What are AI agents, why LangGraph |
| 5 min | Architecture walkthrough (show graph in Studio) |
| 10 min | Pre-crawled data demo + LangSmith traces |
| 20 min | Live-code classify_query_node + generate_answer_node |
| 10 min | Run full agent in Studio, show traces |
| 10 min | Q&A |

## Pre-Demo Checklist

- [ ] `.env` has all API keys configured
- [ ] `uv sync` completed
- [ ] NBG data crawled (`scripts/01_crawl_nbg.py`)
- [ ] Vector store populated (`scripts/02_build_vector_store.py`)
- [ ] Retrieval tested (`scripts/03_test_retrieval.py`)
- [ ] `langgraph dev` starts and Studio loads
- [ ] LangSmith traces appear in dashboard
- [ ] All 13 tests pass
