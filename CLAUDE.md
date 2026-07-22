# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal AI writing assistant built with Streamlit and the Gemini API. No database, no auth — single-user local app.

## Commands

```
pip install -r requirements.txt   # install deps
streamlit run app.py              # run the app (http://localhost:8501)
```

Requires a `.env` file (copy from `.env.example`) with `GEMINI_API_KEY` set. Get a key at https://aistudio.google.com/apikey.

There are no tests or lint configs in this repo currently.

## Architecture

- `app.py` — Streamlit entry point. Imports every module in `features/` and maps it to a sidebar label in the `FEATURES` dict. `main()` renders the sidebar radio, checks `GEMINI_API_KEY` presence, and calls the selected feature's `render()`.
- `core/gemini_client.py` — single shared Gemini call path. `get_client()` is `st.cache_resource`-wrapped so the `genai.Client` is constructed once per session. `generate(prompt, system_instruction=None, model=DEFAULT_MODEL, temperature=0.7)` is the only way features should call the API — it returns `response.text` as a plain string.
- `features/*.py` — one file per writing tool (blog_writer, email_reply, summarizer, document_creator, tone_rewriter, title_generator). Each file is self-contained and follows the same shape:
  1. Module-level `SYSTEM_INSTRUCTION` string defining the AI's role/persona.
  2. A `render()` function with no arguments, no return value — it draws the Streamlit widgets, builds a prompt string from the widget values, calls `generate(prompt, system_instruction=SYSTEM_INSTRUCTION)` inside `st.spinner`, then displays the result via `st.markdown` or `st.text_area` (and `st.download_button` where a file output makes sense).

### Adding a new writing feature

1. Create `features/new_feature.py` following the pattern above (`SYSTEM_INSTRUCTION` + `render()`).
2. Import it in `app.py` and add an entry to the `FEATURES` dict with a Japanese label — that's the only wiring needed; the sidebar and dispatch are generic.

### Conventions

- All user-facing text (labels, placeholders, warnings, generated system instructions) is in Japanese.
- Feature modules never call `genai` directly — always go through `core.gemini_client.generate` so the client stays a singleton and model/config stay centralized.
- Prompts are built as f-strings inline in `render()`, embedding the widget values under labeled sections (e.g. `# 受信メール`, `# トーン`); there's no separate templating layer.

## Gemini API notes

- `DEFAULT_MODEL` in `core/gemini_client.py` (`gemini-3.1-flash-lite`) is shared by every feature. Don't override `model=` per-feature unless there's a concrete reason (e.g. a task genuinely needs a different model's tradeoffs) — keep model choice centralized so it's a one-line change.
- `get_client()` is `st.cache_resource`-wrapped, so the client (and the API key it was built with) persists for the life of the Streamlit process. If `GEMINI_API_KEY` changes in `.env`, the app process must be restarted — editing `.env` alone won't take effect.
- `generate()` has no retry/timeout/exception handling — API errors (invalid key, rate limit, network) currently surface as an unhandled exception in the Streamlit UI. When touching `gemini_client.py`, keep this in mind rather than assuming errors are already handled somewhere.
- Never hardcode an API key in source. `.env` is the only place it should live, and it's already git-ignored — don't remove it from `.gitignore` or print/log the key value.

## Personal-tool operating rules

- This is a single-user local tool, not a product: no auth, no database, no multi-user session handling, no deployment config. Don't add any of these unless explicitly asked, even if they'd be "best practice" for a public app.
- Bias toward the simplest change that works over generalized abstractions — e.g. a new feature is a new `features/*.py` file following the existing pattern, not a plugin system or config-driven feature registry.
- Don't add automated tests, CI, linting config, or Docker setup speculatively — none exist today, and this repo doesn't need them unless the user asks.
