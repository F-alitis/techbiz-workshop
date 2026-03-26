# Demo TODOs

## Live-Coding Stubs (src/agent/nodes.py)

- [ ] **`classify_query_node`** (line 10) — Implement query classification
  - Call `ask_llm()` with `CLASSIFICATION_PROMPT` and the user's query
  - Parse response to classify as `"rag"`, `"scrape"`, or `"both"`
  - Currently hardcoded to always return `"rag"`

- [ ] **`generate_answer_node`** (line 46) — Implement answer generation
  - Call `ask_llm()` with `GENERATION_PROMPT`
  - Inject `rag_context` and `live_content` into the prompt
  - Return the LLM-generated answer
  - Currently returns a placeholder string

## Presentation

- [x] Create dynamic HTML presentation for intro (content from `docs/summary.md`)
  - What are AI agents, why LangGraph
  - Architecture overview (graph flow, 4 nodes, conditional routing)
  - Tech stack (Azure OpenAI, ChromaDB, Crawl4AI, LangSmith, etc.)
  - Key design decisions (single source of truth, prompts as config, InputState vs AgentState)
  - Data pipeline overview (crawl → chunk → embed → store)

## Skill

- [ ] Build a conversation quality evaluation skill
  - Evaluate agent responses for accuracy, relevance, and completeness
  - Score or grade the quality of the conversation

## Pre-Demo Checklist

- [ ] `.env` has all API keys configured
- [ ] `uv sync` completed
- [ ] NBG data crawled (`scripts/01_crawl_nbg.py`)
- [ ] Vector store populated (`scripts/02_build_vector_store.py`)
- [ ] Retrieval tested (`scripts/03_test_retrieval.py`)
- [ ] `langgraph dev` starts and Studio loads
- [ ] LangSmith traces appear in dashboard
- [ ] All 13 tests pass
