# Feature: classify_query_node Implementation

## Context

The `classify_query_node` in `src/agent/nodes.py:10` is a live-coding stub — currently hardcoded to always return `"rag"`. It needs to use the LLM to classify user queries into `"rag"`, `"scrape"`, or `"both"` and pick the most relevant scrape URL from `NBG_SCRAPE_URLS`. The classification prompt will be enhanced to return JSON (action + URL) instead of a single word.

## Key Files

| File | Action | Role |
|------|--------|------|
| `src/agent/nodes.py` | Modify | Replace stub at lines 10-22 with LLM-based classification |
| `config/prompts/classification.txt` | Modify | Enhance prompt to return JSON with action + URL |
| `config/settings.py` | Modify | Add `scrape_max_chars` and `vector_store_collection` settings |
| `.env.example` | Modify | Add `SCRAPE_MAX_CHARS` and `VECTOR_STORE_COLLECTION` |
| `src/tools/rag_retrieval.py` | Modify | Wire `settings.retrieval_top_k` instead of hardcoded `k=5` |
| `src/tools/live_scraper.py` | Modify | Wire `settings.crawl_timeout` and `settings.scrape_max_chars` |
| `src/rag/vector_store.py` | Modify | Wire `settings.vector_store_collection` instead of hardcoded `"nbg_docs"` |
| `tests/test_nodes.py` | Create | Unit tests for classify_query_node |

### Existing utilities to reuse
- `src/agent/llm.ask_llm(prompt: str) -> str` — Azure OpenAI wrapper (`src/agent/llm.py:19`)
- `src/agent/prompts.CLASSIFICATION_PROMPT` — loaded from `config/prompts/classification.txt` (`src/agent/prompts.py:5`)
- `config.settings.settings.nbg_scrape_urls` — list of 20 scrape URLs (`config/settings.py:33`)

## Requirements

1. **Update `classification.txt`** to instruct the LLM to return JSON: `{"action": "rag"|"scrape"|"both", "url": "<selected_url_or_null>"}` — include `{scrape_urls}` placeholder so the LLM sees all available URLs
2. **Implement `classify_query_node`**:
   - Format `CLASSIFICATION_PROMPT` with `{query}` and `{scrape_urls}` (JSON-encoded list)
   - Call `ask_llm()` with the formatted prompt
   - Parse JSON response; extract `action` and `url`
   - Fallback to `"rag"` + first URL on any parse error or invalid values
   - Return `{"user_query": ..., "next_action": ..., "scrape_url": ..., "tool_calls": 0}`
3. All 13 existing tests must continue to pass
4. New tests validate parsing, fallback, and prompt formatting

## Implementation Phases

### Phase 0: Wire hardcoded runtime config through settings

Four hardcoded values need to use `config/settings.py` instead:

**0a. `src/tools/rag_retrieval.py` line 16** — `k=5` → `settings.retrieval_top_k`
```python
from config.settings import settings
results = search(query, k=settings.retrieval_top_k)
```

**0b. `src/tools/live_scraper.py` line 29** — `timeout=30` → `settings.crawl_timeout`
```python
from config.settings import settings
response = httpx.get(url, timeout=settings.crawl_timeout, follow_redirects=True)
```

**0c. `src/tools/live_scraper.py` line 32** — `content[:5000]` → `settings.scrape_max_chars`

Add new setting to `config/settings.py`:
```python
scrape_max_chars: int
```
Add to `.env.example`:
```
SCRAPE_MAX_CHARS=5000
```
Update the scraper:
```python
return content[:settings.scrape_max_chars] if content else "Could not retrieve content from the page."
```

**0d. `src/rag/vector_store.py` line 10** — `"nbg_docs"` → `settings.vector_store_collection`

Add new setting to `config/settings.py`:
```python
vector_store_collection: str
```
Add to `.env.example`:
```
VECTOR_STORE_COLLECTION=nbg_docs
```
Update vector_store.py to use `settings.vector_store_collection`.

### Phase 1: Update prompt template
File: `config/prompts/classification.txt`

Replace the current prompt with:
```
You are a query classifier for the National Bank of Greece (NBG) banking assistant.

Given a user query, classify it and respond with a JSON object:

Categories:
- "rag": General banking products, services, rates, or historical information from the knowledge base
- "scrape": Real-time information like current promotions, latest news, or live website content
- "both": Requires both knowledge base context AND live website data

If the action is "scrape" or "both", select the most relevant URL from this list:
{scrape_urls}

Respond with ONLY valid JSON, no other text:
{{"action": "rag"|"scrape"|"both", "url": "<selected_url_or_null>"}}

Example: {{"action": "scrape", "url": "https://www.nbg.gr/en/go4more"}}
Example: {{"action": "rag", "url": null}}

User query: {query}
```

### Phase 2: Implement the node
File: `src/agent/nodes.py` lines 10-22

```python
def classify_query_node(state: AgentState) -> dict:
    messages = state.get("messages", [])
    user_query = messages[-1].content if messages else ""

    prompt = CLASSIFICATION_PROMPT.format(
        query=user_query,
        scrape_urls=json.dumps(settings.nbg_scrape_urls, indent=2),
    )
    raw = ask_llm(prompt)

    # Parse LLM response
    try:
        parsed = json.loads(raw.strip())
        action = parsed.get("action", "rag")
        url = parsed.get("url")
    except (json.JSONDecodeError, AttributeError):
        action = "rag"
        url = None

    # Validate
    if action not in ("rag", "scrape", "both"):
        action = "rag"
    if not url or url not in settings.nbg_scrape_urls:
        url = settings.nbg_scrape_urls[0]

    return {"user_query": user_query, "next_action": action, "scrape_url": url, "tool_calls": 0}
```

Add `import json` at the top of the file.

### Phase 3: Write tests
File: `tests/test_nodes.py` (new file)

Mock `ask_llm` using `unittest.mock.patch` to avoid real API calls. Test cases:

1. Valid `{"action": "rag", "url": null}` → `next_action="rag"`, `scrape_url=first_url`
2. Valid `{"action": "scrape", "url": "https://www.nbg.gr/en/go4more"}` → correct action + URL
3. Valid `{"action": "both", "url": "https://www.nbg.gr/en/go4more/offers"}` → both + URL
4. Malformed response (plain text "rag") → fallback `"rag"` + first URL
5. Invalid action `{"action": "invalid"}` → fallback `"rag"`
6. URL not in allowed list `{"action": "scrape", "url": "https://evil.com"}` → first URL

## Tests

| Test File | Count | Validates |
|-----------|-------|-----------|
| `tests/test_nodes.py` | 6 | JSON parsing, action validation, URL validation, fallback behavior |

## Test Validation

```bash
uv run pytest tests/ -v
```

Expected: 13 existing + 6 new = 19 tests pass.

## Success Criteria

- [ ] `classify_query_node` calls `ask_llm()` with the enhanced prompt
- [ ] Valid LLM responses route correctly (`rag`/`scrape`/`both`)
- [ ] Malformed or unexpected responses fall back to `"rag"` + first URL
- [ ] Selected `scrape_url` is always from `NBG_SCRAPE_URLS`
- [ ] All 19 tests pass (`uv run pytest tests/ -v`)
- [ ] E2E: queries route to correct graph branch in `langgraph dev`

## Team Structure

| Role | Responsibility | Phases |
|------|---------------|--------|
| Implementer | Update prompt + implement node | 1, 2 |
| Tester | Write tests with mocked `ask_llm` | 3 |
| Reviewer | Code review: JSON parsing safety, no regressions, prompt quality | All |
