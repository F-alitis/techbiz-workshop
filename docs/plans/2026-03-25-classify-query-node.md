# Feature: classify_query_node Implementation

## Context

The `classify_query_node` in `src/agent/nodes.py:10` is a live-coding stub — currently hardcoded to always return `"rag"`. It needs to use the LLM to classify user queries into `"rag"`, `"scrape"`, or `"both"` and pick the most relevant scrape URLs (up to `SCRAPE_MAX_URLS`) from `NBG_SCRAPE_URLS`. The classification prompt will be enhanced to return JSON (action + URLs list) instead of a single word.

## Key Files

| File | Action | Role |
|------|--------|------|
| `src/agent/nodes.py` | Modify | Replace stub at lines 10-22 with LLM-based classification |
| `src/agent/state.py` | Modify | Change `scrape_url: str` to `scrape_urls: list[str]` |
| `config/prompts/classification.txt` | Modify | Enhance prompt to return JSON with action + URLs list |
| `config/settings.py` | Modify | Add `scrape_max_chars`, `vector_store_collection`, and `scrape_max_urls` settings |
| `.env.example` | Modify | Add `SCRAPE_MAX_CHARS`, `VECTOR_STORE_COLLECTION`, and `SCRAPE_MAX_URLS` |
| `src/tools/rag_retrieval.py` | Modify | Wire `settings.retrieval_top_k` instead of hardcoded `k=5` |
| `src/tools/live_scraper.py` | Modify | Wire `settings.crawl_timeout` and `settings.scrape_max_chars` |
| `src/rag/vector_store.py` | Modify | Wire `settings.vector_store_collection` instead of hardcoded `"nbg_docs"` |
| `tests/test_nodes.py` | Create | Unit tests for classify_query_node |

### Existing utilities to reuse
- `src/agent/llm.ask_llm(prompt: str) -> str` — Azure OpenAI wrapper (`src/agent/llm.py:19`)
- `src/agent/prompts.CLASSIFICATION_PROMPT` — loaded from `config/prompts/classification.txt` (`src/agent/prompts.py:5`)
- `config.settings.settings.nbg_scrape_urls` — list of 20 scrape URLs (`config/settings.py:33`)

## Requirements

1. **Update `classification.txt`** to instruct the LLM to return JSON: `{"action": "rag"|"scrape"|"both", "urls": ["<url1>", "<url2>", ...] or []}` — include `{scrape_urls}` placeholder so the LLM sees all available URLs, and `{max_urls}` so it knows the limit
2. **Update `src/agent/state.py`** — change `scrape_url: str` to `scrape_urls: list[str]`
3. **Implement `classify_query_node`**:
   - Format `CLASSIFICATION_PROMPT` with `{query}`, `{scrape_urls}` (JSON-encoded list), and `{max_urls}`
   - Call `ask_llm()` with the formatted prompt
   - Parse JSON response; extract `action` and `urls` list
   - Validate each URL against allowed list, filter invalid ones
   - Truncate to `settings.scrape_max_urls`
   - Fallback to `"rag"` + `[first_url]` on any parse error or invalid values
   - Return `{"user_query": ..., "next_action": ..., "scrape_urls": [...], "tool_calls": 0}`
4. **Update `scrape_live_node`** to loop over `scrape_urls` and concatenate results
5. All 13 existing tests must continue to pass
6. New tests validate parsing, fallback, multi-URL handling, and prompt formatting

## Implementation Phases

### Phase 0: Wire hardcoded runtime config through settings

Four hardcoded values need to use `config/settings.py` instead, plus new settings:

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

**0e. Add `scrape_max_urls` setting**

Add new setting to `config/settings.py`:
```python
scrape_max_urls: int
```
Add to `.env.example`:
```
SCRAPE_MAX_URLS=3
```

**0f. Update `src/agent/state.py`** — change `scrape_url: str` to `scrape_urls: list[str]`

Also update `scrape_live_node` in `src/agent/nodes.py` to read `scrape_urls` (list) from state and use the first URL as default:
```python
url = state.get("scrape_url", settings.nbg_scrape_urls[0])
```
becomes:
```python
urls = state.get("scrape_urls", [settings.nbg_scrape_urls[0]])
```

**0g. Update `scrape_live_node`** to loop over all URLs and concatenate results:
```python
def scrape_live_node(state: AgentState) -> dict:
    """Scrape live content from NBG website."""
    urls = state.get("scrape_urls", [settings.nbg_scrape_urls[0]])
    contents = []
    for url in urls:
        try:
            content = scrape_nbg_page.invoke(url)
            contents.append(f"[Source: {url}]\n{content}")
        except Exception as e:
            contents.append(f"[Source: {url}]\nLive scraping failed: {e}")
    return {"live_content": "\n\n---\n\n".join(contents), "tool_calls": state.get("tool_calls", 0) + 1}
```

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

If the action is "scrape" or "both", select up to {max_urls} most relevant URLs from this list:
{scrape_urls}

Respond with ONLY valid JSON, no other text:
{{"action": "rag"|"scrape"|"both", "urls": ["<url1>", "<url2>"] or []}}

Example: {{"action": "scrape", "urls": ["https://www.nbg.gr/en/go4more", "https://www.nbg.gr/en/go4more/offers"]}}
Example: {{"action": "rag", "urls": []}}

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
        max_urls=settings.scrape_max_urls,
    )
    raw = ask_llm(prompt)

    # Parse LLM response
    try:
        parsed = json.loads(raw.strip())
        action = parsed.get("action", "rag")
        urls = parsed.get("urls", [])
    except (json.JSONDecodeError, AttributeError):
        action = "rag"
        urls = []

    # Validate
    if action not in ("rag", "scrape", "both"):
        action = "rag"
    # Filter to allowed URLs and truncate to max
    urls = [u for u in urls if u in settings.nbg_scrape_urls][:settings.scrape_max_urls]
    if not urls:
        urls = [settings.nbg_scrape_urls[0]]

    return {"user_query": user_query, "next_action": action, "scrape_urls": urls, "tool_calls": 0}
```

Add `import json` at the top of the file.

### Phase 3: Write tests
File: `tests/test_nodes.py` (new file)

Mock `ask_llm` using `unittest.mock.patch` to avoid real API calls. Test cases:

1. Valid `{"action": "rag", "urls": []}` → `next_action="rag"`, `scrape_urls=[first_url]`
2. Valid `{"action": "scrape", "urls": ["https://www.nbg.gr/en/go4more"]}` → correct action + URL
3. Valid `{"action": "both", "urls": ["https://www.nbg.gr/en/go4more", "https://www.nbg.gr/en/go4more/offers"]}` → both + 2 URLs
4. Malformed response (plain text "rag") → fallback `"rag"` + `[first_url]`
5. Invalid action `{"action": "invalid"}` → fallback `"rag"`
6. URL not in allowed list `{"action": "scrape", "urls": ["https://evil.com"]}` → `[first_url]`
7. More URLs than `scrape_max_urls` → truncated to max

## Tests

| Test File | Count | Validates |
|-----------|-------|-----------|
| `tests/test_nodes.py` | 7 | JSON parsing, action validation, multi-URL validation, truncation, fallback behavior |

## Test Validation

```bash
uv run pytest tests/ -v
```

Expected: 13 existing + 7 new = 20 tests pass.

## Success Criteria

- [ ] `classify_query_node` calls `ask_llm()` with the enhanced prompt
- [ ] Valid LLM responses route correctly (`rag`/`scrape`/`both`)
- [ ] Classifier returns up to `SCRAPE_MAX_URLS` URLs (default 3)
- [ ] Malformed or unexpected responses fall back to `"rag"` + `[first_url]`
- [ ] All selected `scrape_urls` are from `NBG_SCRAPE_URLS`
- [ ] `scrape_live_node` scrapes all URLs and concatenates results
- [ ] All 20 tests pass (`uv run pytest tests/ -v`)
- [ ] E2E: queries route to correct graph branch in `langgraph dev`

## Team Structure

| Role | Responsibility | Phases |
|------|---------------|--------|
| Implementer | Update prompt + implement node | 1, 2 |
| Tester | Write tests with mocked `ask_llm` | 3 |
| Reviewer | Code review: JSON parsing safety, no regressions, prompt quality | All |
