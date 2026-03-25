# Feature: generate_answer_node Implementation

## Context

The `generate_answer_node` in `src/agent/nodes.py:45` is a live-coding stub — currently returns a placeholder string. It needs to use the LLM with `GENERATION_PROMPT` to generate contextual answers from `rag_context` and `live_content`. The generation prompt will be enhanced with a formal/corporate tone of voice and structured markdown formatting instructions.

## Key Files

| File | Action | Role |
|------|--------|------|
| `src/agent/nodes.py` | Modify | Replace stub at lines 45-58 with LLM-based generation |
| `config/prompts/generation.txt` | Modify | Add tone of voice and formatting instructions |
| `tests/test_nodes.py` | Modify | Add tests for generate_answer_node |

### Existing utilities to reuse
- `src/agent/llm.ask_llm(prompt: str) -> str` — Azure OpenAI wrapper (`src/agent/llm.py:19`)
- `src/agent/prompts.GENERATION_PROMPT` — loaded from `config/prompts/generation.txt` (`src/agent/prompts.py:6`)
- Template placeholders: `{query}`, `{rag_context}`, `{live_content}` (already in `config/prompts/generation.txt`)

## Requirements

1. **Implement `generate_answer_node`**:
   - Extract `user_query`, `rag_context`, `live_content` from state
   - Use `"No information available."` as default for missing context
   - Format `GENERATION_PROMPT` with all three placeholders
   - Call `ask_llm()` with the formatted prompt
   - Return `{"final_answer": answer, "messages": [AIMessage(content=answer)]}`
2. The `messages` AIMessage must contain the actual LLM answer (not a placeholder)
3. **Update `generation.txt`** with formal/corporate tone and structured markdown formatting instructions
4. All existing + classify_query_node tests must pass

## Implementation Phases

### Phase 0: Update prompt template
File: `config/prompts/generation.txt`

Replace with:
```
You are an expert banking assistant for the National Bank of Greece (NBG).

## Instructions

Answer the user's question using ONLY the provided context. Do not infer, assume, or fabricate information beyond what is explicitly stated in the context below. If the context does not contain enough information to fully answer the question, state clearly what information is available and what is not.

## Tone

Maintain a formal, professional tone befitting a major financial institution. Use precise banking terminology where appropriate. Be authoritative yet clear — ensure complex financial concepts are explained without oversimplification.

## Formatting

Structure your response using markdown:
- Use **bold** for key terms, product names, and important figures
- Use bullet points for lists of features, requirements, or conditions
- Use ### headings to separate distinct topics when the answer covers multiple areas
- Include specific details such as rates, terms, fees, and eligibility criteria when available
- Keep paragraphs concise — prefer short, focused sections over long blocks of text

## Context

### Knowledge Base
{rag_context}

### Live Website Content
{live_content}

## User Question
{query}
```

### Phase 1: Implement the node
File: `src/agent/nodes.py` lines 45-58

```python
def generate_answer_node(state: AgentState) -> dict:
    user_query = state.get("user_query", "")
    rag_context = state.get("rag_context") or "No information available."
    live_content = state.get("live_content") or "No information available."

    prompt = GENERATION_PROMPT.format(
        query=user_query,
        rag_context=rag_context,
        live_content=live_content,
    )
    answer = ask_llm(prompt)

    return {
        "final_answer": answer,
        "messages": [AIMessage(content=answer)],
    }
```

### Phase 2: Write tests
File: `tests/test_nodes.py` (append to existing file from Plan A)

Mock `ask_llm` using `unittest.mock.patch`. Test cases:

1. **Both contexts provided** — verify `ask_llm` is called with prompt containing both `rag_context` and `live_content` values
2. **Only rag_context** (no `live_content` in state) — prompt uses `"No information available."` for live_content
3. **Only live_content** (no `rag_context` in state) — prompt uses `"No information available."` for rag_context
4. **Response structure: `final_answer`** — returned dict has `final_answer` key matching mocked LLM response
5. **Response structure: `messages`** — returned dict has `messages` list with one `AIMessage` whose `content` equals the LLM response

## Tests

| Test File | Count | Validates |
|-----------|-------|-----------|
| `tests/test_nodes.py` | 5 (added to existing) | Prompt formatting, context defaults, response structure |

## Test Validation

```bash
uv run pytest tests/ -v
```

Expected: 19 (after Plan A) + 5 new = 24 tests pass.

## Success Criteria

- [ ] `generate_answer_node` calls `ask_llm()` with properly formatted `GENERATION_PROMPT`
- [ ] Missing `rag_context` or `live_content` default to `"No information available."`
- [ ] `final_answer` matches the LLM response string
- [ ] `messages` contains `AIMessage` with the actual answer (not placeholder)
- [ ] All 24 tests pass (`uv run pytest tests/ -v`)
- [ ] E2E: full agent loop works — classify → retrieve/scrape → generate real answers

## Team Structure

| Role | Responsibility | Phases |
|------|---------------|--------|
| Implementer | Implement node logic | 1 |
| Tester | Write tests with mocked `ask_llm` | 2 |
| Reviewer | Verify prompt formatting, response structure, no regressions | All |

## Execution Dependency

This plan should be executed **after** `2026-03-25-classify-query-node.md` since both share `tests/test_nodes.py`.
