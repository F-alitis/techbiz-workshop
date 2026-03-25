# NBG Banking Agent — Presentation Summary

## What We Built

An AI-powered banking assistant for National Bank of Greece (NBG) using **LangGraph** — a graph-based agent orchestration framework. The agent accesses NBG.gr subsites via two strategies: pre-crawled RAG (Retrieval-Augmented Generation) and live web scraping, then answers user questions through a chat interface.

The project is designed as a **1-hour hands-on university demo**: 70% pre-built scaffolding, 30% live-coded during the presentation.

---

## Architecture Overview

### The Agent Graph

```
START → classify_query → [conditional routing]
  ├─→ retrieve_from_rag → generate_answer → END
  ├─→ scrape_live → generate_answer → END
  └─→ retrieve_from_rag → scrape_live → generate_answer → END
```

Four nodes, two routing paths, one conditional decision point:

1. **classify_query_node** (STUB) — Analyzes the user's question and decides: should we search the knowledge base (`rag`), scrape the live website (`scrape`), or do both (`both`)? Also picks the most relevant `scrape_url` from `NBG_SCRAPE_URLS`.
2. **retrieve_from_rag_node** — Queries ChromaDB vector store for relevant pre-crawled content (from `NBG_CRAWL_URLS`)
3. **scrape_live_node** — Fetches live content from the selected `scrape_url` using httpx + BeautifulSoup
4. **generate_answer_node** (STUB) — Takes all gathered context and generates a final answer using the LLM

### Why Two Stubs?

The two stub nodes (`classify_query` and `generate_answer`) are intentionally left as placeholders. During the live demo, students will implement them step by step, experiencing the process of:
- Calling an LLM (Azure OpenAI Responses API)
- Prompt engineering (classification + generation)
- Seeing the graph come alive in LangGraph Studio

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Orchestration** | LangGraph v0.3+ | Graph-based agent with conditional routing |
| **LLM** | Azure OpenAI (o4-mini) | Via Responses API (`/openai/responses`) |
| **Embeddings** | Azure OpenAI (text-embedding-3-small) | Deployment: `uniko-poc-embeddings` |
| **Vector Store** | ChromaDB | Document storage and similarity search |
| **Pre-Crawling** | Crawl4AI | Full JS-rendered web scraping (scripts only) |
| **Live Scraping** | httpx + BeautifulSoup | Lightweight HTTP scraper (LangGraph-compatible) |
| **CLI** | Rich | Beautiful terminal output with spinner |
| **Observability** | LangSmith | Auto-tracing for every node and edge |
| **Dev UI** | LangGraph Studio | Visual graph debugging and testing |
| **Package Manager** | uv | Fast Python dependency management |
| **Config** | Pydantic Settings | Type-safe config from `.env` |

---

## Key Design Decisions

### 1. Single Source of Truth (`.env`)

All configuration lives in `.env` — no defaults hardcoded in Python. The `config/settings.py` file only declares types and validates. If any variable is missing, the app fails at startup with a clear error.

Sections in `.env`:
- **Azure OpenAI — LLM** (endpoint, API key, deployment, API version)
- **Azure OpenAI — Embeddings** (separate deployment and API version)
- **LangSmith** (tracing, API key, project name)
- **RAG** (chunk size, overlap, retrieval top-k)
- **Crawling** (target URLs, rate limit, timeout, allowed domain)
  - `NBG_CRAWL_URLS` — 20 static product/service pages for offline RAG indexing
  - `NBG_SCRAPE_URLS` — 20 frequently updated pages (promotions, press, rewards) for live scraping
- **Paths** (data directory, vector store path)

### 2. Prompts as Config Files

Prompts are not hardcoded in Python — they live as text files in `config/prompts/`:
- `classification.txt` — Query classification prompt
- `generation.txt` — Answer generation prompt

This allows editing prompts without touching code and makes prompt engineering more visible during the demo.

### 3. InputState vs AgentState (LangGraph Studio)

```python
class InputState(TypedDict):
    """What the user provides — shown in LangGraph Studio."""
    messages: Annotated[Sequence[BaseMessage], add_messages]

class AgentState(InputState, total=False):
    """Full internal state — not shown in Studio input."""
    user_query: str
    rag_context: str
    live_content: str
    next_action: str
    scrape_url: str
    final_answer: str
    tool_calls: int
```

The graph uses `StateGraph(AgentState, input=InputState)` so LangGraph Studio only shows the `messages` input field — keeping the UI clean while the internal state carries all the agent's working data.

### 4. LLM Wrapper (Why Not LangChain?)

LangChain's `AzureChatOpenAI` does **NOT** support Azure OpenAI's newer Responses API. We built a thin wrapper (`src/agent/llm.py`) using the `openai` SDK directly:

```python
def ask_llm(prompt: str) -> str:
    client = AzureOpenAI(...)
    response = client.responses.create(model="o4-mini", input=prompt)
    return response.output_text
```

### 5. Dual Scraping Strategy

| Use Case | Tool | Why |
|----------|------|-----|
| Pre-crawl (scripts) | Crawl4AI | Full JS rendering, writes to disk, populates ChromaDB |
| Live scraping (agent) | httpx + BeautifulSoup | No browser needed, synchronous, LangGraph-compatible |

Crawl4AI uses Playwright/Chromium which conflicts with LangGraph's async server runtime (blocking OS calls). The live scraper uses plain HTTP — NBG.gr returns ~5000 chars of usable content even without JS rendering.

---

## Project Structure

```
nbg-banking-agent/
├── .env                          # All config (single source of truth)
├── .env.example                  # Template for env vars
├── pyproject.toml                # Dependencies (uv)
├── langgraph.json                # LangGraph Server config
├── main.py                       # CLI entry point
├── config/
│   ├── settings.py               # Pydantic BaseSettings (no defaults)
│   └── prompts/
│       ├── classification.txt    # Query classification prompt
│       └── generation.txt        # Answer generation prompt
├── src/
│   ├── crawl/
│   │   ├── nbg_config.py         # Reads URLs from settings
│   │   └── crawler.py            # Crawl4AI AsyncWebCrawler
│   ├── rag/
│   │   ├── chunker.py            # 1000-char chunks, 200-char overlap
│   │   ├── embeddings.py         # Azure OpenAI Embeddings wrapper
│   │   └── vector_store.py       # ChromaDB operations
│   ├── tools/
│   │   ├── rag_retrieval.py      # @tool: vector search
│   │   └── live_scraper.py       # @tool: httpx+BS4 live scrape
│   ├── agent/
│   │   ├── state.py              # InputState + AgentState
│   │   ├── llm.py                # Azure OpenAI Responses API wrapper
│   │   ├── prompts.py            # Loads from config/prompts/
│   │   ├── nodes.py              # 4 nodes (2 stubs for live-coding)
│   │   └── graph.py              # StateGraph with conditional routing
│   └── cli/
│       └── chat.py               # Rich CLI chat loop
├── scripts/
│   ├── 01_crawl_nbg.py           # Pre-crawl 7 NBG subsites
│   ├── 02_build_vector_store.py  # Chunk + embed (batched for rate limits)
│   └── 03_test_retrieval.py      # Validate RAG retrieval
└── tests/                        # 13 tests across 4 files
```

---

## Data Pipeline

### Step 1: Crawl (Crawl4AI)
- 20 NBG subsites crawled with full JS rendering (static product/service pages)
- Output: markdown files in `data/raw/`

### Step 2: Chunk (LangChain Text Splitters)
- RecursiveCharacterTextSplitter: 1000-char chunks, 200-char overlap
- Metadata preserved: source URL, title, timestamp
- Result: 582 document chunks

### Step 3: Embed & Store (Azure OpenAI + ChromaDB)
- Embeddings: `text-embedding-3-small` (1536 dimensions)
- Batched in groups of 20 with 2s delays and retry logic for Azure S0 rate limits
- Stored in ChromaDB with cosine similarity search

---

## Development Workflow

### How We Built It

1. **Plan** — Created detailed plan document (`docs/plans/2026-03-24-langgraph-nbg-agent.md`)
2. **Team-based implementation** — Used Claude Code's team feature with 4 parallel agents (scaffolder, data-pipeline, agent-builder, cli-tester)
3. **Verification** — Rebuilt entire project from plan in a temp directory to prove the plan is complete and accurate
4. **Iterative refinement** — Configuration evolved from hardcoded → settings.py defaults → `.env` as single source of truth

### Git History

```
7f0e85f feat: initial NBG banking agent with LangGraph
475f743 chore: remove outdated plan document
d36531f feat: configurable crawl URLs and lightweight live scraper
ffad0c9 refactor: single source of truth for config and prompts
47ea399 chore: reset classify_query stub to rag default
1ebbd92 fix: add batching and retry logic for embedding rate limits
```

---

## Testing

13 tests across 4 files, all passing:

| Test File | Count | What It Validates |
|-----------|-------|-------------------|
| `test_state.py` | 2 | AgentState creation and field types |
| `test_graph.py` | 5 | Graph compiles, conditional routing (rag/scrape/both) |
| `test_chunker.py` | 4 | Chunk size, overlap, metadata, document processing |
| `test_vector_store.py` | 2 | ChromaDB add/search, empty collection |

---

## Observability

### LangSmith Tracing
- Every graph execution is auto-traced
- Each node appears as a span with inputs/outputs
- Conditional routing decisions are visible
- No code changes needed — just env vars

### LangGraph Studio
- Visual graph with node status
- Messages-only input (internal state hidden)
- Step-through debugging
- Real-time execution monitoring

---

## Intro Presentation

An 11-slide reveal.js presentation (`docs/presentation/index.html`) covers the intro portion of the workshop:

1. Title slide (with NBG logo placeholder)
2. Workshop Overview — what we're building, the goal, and how we'll get there
3. What are AI Agents?
4. Why LangGraph?
5. LangGraph Core Concepts (nodes, edges, state, messages — beginner-friendly with annotated code)
6. Architecture Overview (vertical flow diagram with decision diamond)
7. Tech Stack (icon grid)
8. RAG Data Pipeline — how the knowledge base is built (Crawl → Chunk → Embed → Store)
9. Built with Claude Code (git commit history)
10. What We'll Build Today (before/after code stubs)
11. Hands-On Setup (project structure + commands)

Design: modern banking aesthetic — gradient navy background, gold accents, Google Fonts (Playfair Display + Inter + JetBrains Mono), glass-morphism cards. Self-contained single HTML file, CDN-loaded.

---

## Live Demo Plan (1 hour)

| Time | Activity |
|------|----------|
| 5 min | Intro: What are AI agents, why LangGraph |
| 5 min | Architecture walkthrough (show graph in Studio) |
| 10 min | Pre-crawled data demo + LangSmith traces |
| 20 min | **Live-code**: classify_query_node + generate_answer_node |
| 10 min | Run full agent in Studio, show traces |
| 10 min | Q&A |

### What Students Will Live-Code

**1. classify_query_node** — Replace the stub with:
```python
prompt = CLASSIFICATION_PROMPT.format(query=user_query)
result = ask_llm(prompt)
next_action = result.strip().lower()
```

**2. generate_answer_node** — Replace the stub with:
```python
prompt = GENERATION_PROMPT.format(
    rag_context=state.get("rag_context", "N/A"),
    live_content=state.get("live_content", "N/A"),
    query=state.get("user_query", ""),
)
answer = ask_llm(prompt)
```

---

## Pre-Demo Checklist

- [ ] `.env` has all API keys configured
- [ ] `uv sync` completed
- [ ] NBG data crawled (`scripts/01_crawl_nbg.py`)
- [ ] Vector store populated (`scripts/02_build_vector_store.py`)
- [ ] Retrieval tested (`scripts/03_test_retrieval.py`)
- [ ] `langgraph dev` starts and Studio loads
- [ ] LangSmith traces appear in dashboard
- [ ] All 13 tests pass

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| LangChain doesn't support Azure Responses API | Thin `openai` SDK wrapper (`src/agent/llm.py`) |
| LangGraph Studio showed all state fields | Separate `InputState` (messages only) + `input=InputState` on StateGraph |
| Crawl4AI blocked in LangGraph async runtime | Dual strategy: Crawl4AI for pre-crawl, httpx+BS4 for live |
| Azure S0 rate limits on embeddings | Batched embedding (10 chunks/batch) with exponential backoff |
| Config scattered across code and env | Single source of truth: all config in `.env`, settings.py validates only |
| Prompts hardcoded in Python | External text files in `config/prompts/` |
| Live scraper hardcoded to one URL | Separate `NBG_SCRAPE_URLS` config, classifier picks target URL per query |
