# LangGraph Agent Implementation Plan - NBG Banking Assistant

## Context

We're building a hands-on demo project for a 1-hour university presentation. The goal is to showcase building a LangGraph agent that accesses NBG.gr subsites, extracts content via RAG + live scraping, and provides it through a CLI chat interface. 70% is pre-built, 30% is live-coded during the presentation. After this, a Claude Code skill will be created live to evaluate dialog quality.

---

## Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python 3.10+ | LangGraph's primary SDK |
| LLM | OpenAI GPT-4o | User requirement |
| Framework | LangGraph v0.3+ | Graph-based agent orchestration |
| Vector Store | ChromaDB | Better DX than FAISS, built-in persistence |
| Web Scraping | Crawl4AI | AI-optimized, clean markdown output |
| Embeddings | text-embedding-3-small | Cost-effective, OpenAI native |
| CLI | Rich | Beautiful terminal output |
| Observability | LangSmith | Zero-config tracing for LangGraph |

---

## Environment Variables

```bash
# OpenAI (single key for both GPT-4o and embeddings)
OPENAI_API_KEY=sk-proj-...

# LangSmith (tracing/observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...
LANGCHAIN_PROJECT=nbg-banking-agent
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

No custom OpenAI endpoint needed — `langchain-openai` uses `https://api.openai.com/v1` by default.

---

## Project Structure

```
nbg-banking-agent/
├── .env                          # API keys (OPENAI_API_KEY, LANGCHAIN_*)
├── requirements.txt
├── main.py                       # Entry point
├── config/
│   └── settings.py               # Pydantic settings
├── data/
│   ├── raw/                      # Raw scraped markdown
│   ├── processed/                # Chunked documents
│   └── vector_store/             # ChromaDB persistent storage
├── src/
│   ├── crawl/
│   │   ├── crawler.py            # Crawl4AI implementation
│   │   └── nbg_config.py         # Target URLs and rules
│   ├── rag/
│   │   ├── chunker.py            # RecursiveCharacterTextSplitter
│   │   ├── embeddings.py         # OpenAI embedding wrapper
│   │   └── vector_store.py       # ChromaDB operations
│   ├── tools/
│   │   ├── rag_retrieval.py      # Vector search tool
│   │   └── live_scraper.py       # Live web scraping tool
│   ├── agent/
│   │   ├── state.py              # AgentState TypedDict
│   │   ├── nodes.py              # Graph node functions
│   │   ├── graph.py              # LangGraph definition
│   │   └── prompts.py            # System prompts
│   └── cli/
│       └── chat.py               # Rich-based chat loop
└── scripts/
    ├── 01_crawl_nbg.py           # Pre-demo: crawl site
    ├── 02_build_vector_store.py  # Pre-demo: build ChromaDB
    └── 03_test_retrieval.py      # Pre-demo: validate RAG
```

---

## LangGraph Design

### State Schema
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add]
    user_query: str
    rag_context: str | None
    live_content: str | None
    next_action: str  # "rag", "scrape", "both"
    final_answer: str | None
    tool_calls: int
```

### Graph Flow
```
START → classify_query → [conditional routing]
  ├─→ retrieve_from_rag → generate_answer → END
  ├─→ scrape_live → generate_answer → END
  └─→ retrieve_from_rag → scrape_live → generate_answer → END
```

- Historical data (products, rates) → RAG only
- Real-time info (promotions, hours) → Live scraping
- Complex queries → RAG first, then live scraping
- Max 2 tool calls per query (prevent loops)

---

## RAG Pipeline

- **Crawl targets**: 7 NBG subsites (retail, loans, cards, accounts, business, about, contact)
- **Chunking**: RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- **Metadata**: source URL, page title, section heading, timestamp
- **Retrieval**: Top-5 cosine similarity search
- **Embeddings**: OpenAI text-embedding-3-small (1536 dims)

---

## LangSmith Integration

4 env vars in `.env` — zero code changes. Auto-traces all nodes, LLM calls, tool invocations, and state transitions.

---

## Implementation Order

### Phase 1: Pre-Build (70%)

1. **Project scaffolding** — structure, dependencies, .env
2. **Data pipeline** — crawl NBG → chunk → embed → ChromaDB
3. **Tools** — RAG retrieval tool + live scraper tool (complete)
4. **CLI** — Rich-based chat loop (complete)
5. **Graph structure** — nodes with stub implementations, edges wired

### Phase 2: Live-Code (30%) — The interesting parts

1. **`classify_query_node`** (10 min) — GPT-4o classifies query → routing decision
2. **`generate_answer_node`** (10 min) — GPT-4o generates answer with RAG context
3. **`route_query`** (10 min) — conditional edge function

---

## Demo Flow (1 hour)

| Time | Activity |
|------|----------|
| 5 min | Intro: What are AI agents, why LangGraph |
| 5 min | Architecture walkthrough + pre-crawled data demo |
| 30 min | Live-code the 3 key functions |
| 10 min | Run agent + LangSmith trace walkthrough |
| 10 min | Q&A |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| OpenAI API down | Pre-cache 3 demo responses |
| nbg.gr blocks scraper | Pre-scraped backup files in data/raw/ |
| ChromaDB corruption | Backup copy in data/vector_store_backup/ |
| Graph infinite loop | Max 2 tool calls hardcoded |

---

## Verification

1. `python scripts/03_test_retrieval.py` — confirms RAG returns relevant docs
2. Run 10 test queries covering RAG, scraping, hybrid, and edge cases
3. Verify LangSmith traces appear in dashboard
4. Full rehearsal of live-coding flow

---

## Dependencies (requirements.txt)

```txt
langgraph>=0.3.0,<0.4.0
langchain>=0.3.0
langchain-openai>=0.2.0
langsmith>=0.2.0
openai>=1.50.0
chromadb>=0.5.0
crawl4ai>=0.4.0
playwright>=1.45.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
tiktoken>=0.7.0
langchain-text-splitters>=0.3.0
rich>=13.7.0
python-dotenv>=1.0.0
pydantic>=2.8.0
pydantic-settings>=2.0.0
httpx>=0.27.0
```

---

## Files to Create/Modify

All files listed in the project structure above — created from scratch in `nbg-banking-agent/` directory.
