# Feature: Reveal.js Intro Presentation

## Context

Create a concise 10-slide HTML presentation using reveal.js to introduce university students to AI agents and LangGraph before the hands-on coding session. This covers the ~10 min intro portion of the 1-hour NBG Banking Agent demo. The presentation must be professional with a banking aesthetic (navy + gold), include an NBG logo placeholder, and be self-contained (single HTML file, CDN-loaded).

## Key Files

| File | Action | Role |
|------|--------|------|
| `docs/presentation/index.html` | Create | The full reveal.js presentation (single file, all styles inline) |
| `docs/presentation/assets/nbg-logo.png` | Create | SVG placeholder for NBG logo (to be replaced with real logo) |
| `docs/plans/presentation-plan.md` | Modify | Update with review notes after completion |

### Reference files (read-only, content sources)
- `docs/summary.md` — full project summary, architecture, tech stack, data pipeline
- `docs/demo-todos.md` — live-coding stubs and pre-demo checklist
- `docs/plans/2026-03-24-langgraph-nbg-agent.md` — detailed plan with graph flow, state design, git history

## Requirements

1. **11 slides** as outlined below, concise and focused
2. **reveal.js v5 via CDN** — no local install, single HTML file
3. **Modern banking aesthetic** — gradient navy background (#0a1628 → #162d50), gold (#d4a843) accents, white text, Google Fonts (Playfair Display headings, Inter body, JetBrains Mono code), glass-morphism cards
4. **NBG logo placeholder** — on title slide, referenced as `assets/nbg-logo.png`
5. **Code highlighting** — reveal.js highlight plugin for Python snippets
6. **CSS diagrams** — graph flow and data pipeline as styled HTML/CSS boxes (no external dependency)
7. **Git commit history** — show actual commits from the project on the "Built with Claude Code" slide

## Slide Outline

1. **Title** — "Building AI Agents with LangGraph" / NBG Banking Agent / NBG logo placeholder
2. **Workshop Overview** — What we're building (AI banking assistant for NBG), the goal (agent that decides how to answer), how we'll do it (70% pre-built, implement 2 key functions), end result (working agent in LangGraph Studio)
3. **What are AI Agents?** — 3-4 bullets: decision-making, tool use, state, differ from simple LLM calls
3. **Why LangGraph?** — Graph-based orchestration, conditional routing, state management, observability. Brief contrast with plain chains.
4. **LangGraph Core Concepts** — Icon cards with beginner-friendly explanations: Nodes (Python functions that do work), Edges (normal vs conditional for decision-making), State (agent's "working memory" as TypedDict), Messages (HumanMessage/AIMessage with add_messages). Includes annotated code example.
5. **Architecture Overview** — Vertical centered flow diagram: START → classify_query → diamond decision → 3 branches (rag/scrape/both) → generate_answer → END. Proper alignment with SVG arrows.
6. **Tech Stack** — Grid/table: Azure OpenAI, ChromaDB, Crawl4AI, LangSmith, LangGraph Studio, uv, Pydantic
7. **RAG Data Pipeline** — Explains how the agent's knowledge base is built before the workshop. Visual: Crawl (Crawl4AI) → Chunk (1000/200) → Embed (text-embedding-3-small) → Store (ChromaDB)
8. **Built with Claude Code** — Git log showing commits: `7f0e85f feat: initial NBG banking agent...` through `1ebbd92 fix: add batching...`. Highlight AI-assisted development.
9. **What We'll Build Today** — Two stubs: `classify_query_node` (hardcoded → LLM classification) and `generate_answer_node` (placeholder → LLM generation). Show before/after code.
10. **Hands-On Setup** — Project structure tree, key commands (`langgraph dev`, `uv run pytest`), LangGraph Studio orientation.

## Implementation Phases

1. **Create directory structure** — `docs/presentation/` and `docs/presentation/assets/`
2. **Create placeholder logo** — Simple SVG-based placeholder at `assets/nbg-logo.png` (or inline SVG in HTML)
3. **Build index.html** — Single file with:
   - CDN links for reveal.js v5 CSS + JS + highlight plugin
   - Custom CSS overrides for banking theme (colors, fonts, diagrams)
   - All 10 slides as `<section>` elements
   - CSS-styled flow diagrams (flexbox boxes with arrows)
   - Python code blocks with highlight.js
   - Reveal.initialize() config at bottom

## Tests

No automated tests — this is a static HTML file.

## Test Validation

- Open `docs/presentation/index.html` in Chrome
- Verify all 10 slides render and navigate correctly
- Verify code highlighting works on Python snippets
- Verify flow diagrams display properly
- Verify NBG logo placeholder appears on title slide
- Verify colors match spec (navy bg, gold accents, white text)

## Success Criteria

- Single `index.html` file opens in browser and displays all 10 slides
- Professional banking aesthetic (navy/gold/white)
- Code blocks have syntax highlighting
- Flow diagrams render as CSS-styled visuals
- NBG logo placeholder visible on title slide
- All content is accurate per `docs/summary.md`

## Team Structure

| Role | Responsibility |
|------|---------------|
| **Implementer** | Build the full `index.html` with all slides, styles, and diagrams |
| **Reviewer** | Review HTML/CSS quality, content accuracy, visual polish |

## Review Notes

- Initial implementation used flat navy background and basic CSS — reworked to gradient background, glass-morphism cards, Google Fonts, and SVG arrows for a modern banking feel
- Slide 4 (LangGraph Core Concepts) was too abstract for beginners — rewritten with icon cards, plain-English explanations (e.g., state = "working memory"), and annotated code
- Slide 5 (Architecture) was horizontal and misaligned — redesigned as a vertical centered flow with a diamond decision node and three side-by-side branches
- All other slides verified accurate against docs/summary.md

## TODOs (post-implementation)

- [ ] Replace `docs/presentation/assets/nbg-logo.png` placeholder with the real NBG logo
