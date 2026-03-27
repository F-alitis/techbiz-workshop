---
name: feature-builder
description: End-to-end feature implementation with research, planning, TDD, and mandatory code review. Use when the user asks to build a feature, implement functionality, or requests a structured development workflow. Enforces disciplined phases — analyze, research, plan, implement, test, and review.
---

You are using the **feature-builder** skill. Announce this at the start:

> "I'm using the feature-builder skill to implement this feature."

Follow these 4 phases strictly and in order. Do NOT skip phases. Do NOT commit changes until the user explicitly agrees.

---

## Phase 1: Analyze

Read the project's `CLAUDE.md` and everything in `docs/` to understand:
- Project architecture, conventions, and patterns
- Existing utilities, shared code, and reusable modules
- Any prior planning documents or specs related to the feature

Then explore the codebase:
- Identify files and modules related to the requested feature
- Understand the current structure, naming conventions, and test patterns
- Note any existing tests, CI configuration, or build tooling

Summarize findings before moving to Phase 2.

---

## Phase 2: Research

Use `WebSearch` to research:
- Best practices and patterns relevant to the feature
- Libraries or tools that could help (check if already in project dependencies first)
- Known pitfalls or edge cases for this type of feature

Review the project's existing dependencies (`package.json`, `requirements.txt`, `go.mod`, etc.) to avoid adding redundant packages.

Produce a short research summary with recommendations for the planning phase.

---

## Phase 3: Plan

Enter plan mode using `EnterPlanMode`.

1. **Clarify ambiguities** — use `AskUserQuestion` for any open questions about requirements, scope, or approach before writing the plan
2. **Create the planning document** at `docs/plans/YYYY-MM-DD-<feature-name>.md` (use today's date and a kebab-case feature name)
3. If `docs/PROMPT_TEMPLATE.md` exists, use it as the base structure. Otherwise, use the structure below.

### Planning Document Structure

The document MUST include ALL of these sections:

```markdown
# Feature: <Feature Name>

## Context
- Problem statement
- Goal
- Research findings summary

## Key Files

| File | Action | Role |
|------|--------|------|
| `path/to/file` | Create / Modify / Remove | What this file does |

## Requirements
- Numbered list of what needs to be built
- Acceptance criteria for each requirement

## Implementation Phases
1. Step-by-step breakdown
2. Each step should be small and independently testable
3. Order matters — dependencies first

## Tests
- Exact test files to create
- What each test validates
- Edge cases to cover

## Test Validation
- How to run the tests (exact commands)
- Expected outcomes

## Success Criteria
- Measurable targets (e.g., "all tests pass", "API returns 200 for valid input")
- Definition of done

## Team Structure
- Agent roles and responsibilities (e.g., lead, implementer, tester, reviewer)
- Task assignments mapped to implementation phases
```

4. **Persist the plan** — the planning document at `docs/plans/YYYY-MM-DD-<feature-name>.md` MUST be written to disk before exiting plan mode. This is the source of truth for Phase 4 and must exist as a file in the project's `docs/` directory. If the `docs/plans/` directory does not exist, create it.
5. Exit plan mode with `ExitPlanMode` and get user approval before proceeding

---

## Phase 4: Implement, Test & Review

**MANDATORY: You MUST spawn a team for this phase. This is non-negotiable — never execute implementation, testing, or review as a single agent. Always use `TeamCreate` before any code is written.**

### Setup

1. Use `TeamCreate` to spin up a team — this step is REQUIRED, do not skip it regardless of feature size or complexity
2. Define roles dynamically based on the feature (e.g., lead, implementer, tester, reviewer — adapt to the demand)
3. Create tasks with `TaskCreate` covering:
   - **Implementation tasks** — matching the implementation phases from the plan document, following TDD (write test first, verify it fails, implement code, verify test passes)
   - **Test & validate task** — run ALL tests (new + existing), validate against every success criterion in the plan, fix and re-run until all pass, confirm no regressions
   - **Code review task** — review ALL changes for: best practices, simplification opportunities, reusability (extract shared utilities), no regressions, and security (OWASP top 10)
4. Assign tasks to teammates and coordinate execution

### Review loop

If the code review identifies issues:
1. Create new implementation tasks for the fixes
2. Re-run all tests
3. Re-review
4. Repeat until the reviewer passes all checks

### After review passes

1. Shut down the team
2. Update the plan document (`docs/plans/YYYY-MM-DD-<feature-name>.md`) with a final **"Review Notes"** section documenting:
   - What was refactored during review
   - Any patterns extracted to shared utilities
   - Final assessment
3. Present the summary to the user
4. Ask the user to approve committing the changes
5. Do NOT commit — only commit when the user explicitly agrees
