# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Kanban board app with an AI chat assistant. The backend (FastAPI/Python) serves both the REST API and the built frontend as static files. The AI assistant can read and mutate board state via OpenRouter.

## Running the App

Requires Docker Desktop and a valid `OPENROUTER_API_KEY` in `.env`.

```bash
scripts/start.bat   # Windows — starts Docker Compose
scripts/stop.bat    # Windows — stops services
scripts/start.sh    # Mac/Linux
scripts/stop.sh     # Mac/Linux
```

App is available at `http://localhost:8000`. Login: `user` / `password`.

## Development Commands

### Backend (Python/FastAPI)

```bash
cd backend
python -m pytest              # run all tests
python -m pytest test_foo.py  # run a single test file
```

Dependencies are managed with `uv` inside Docker. The backend runs on port 8000 via uvicorn.

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev           # local dev server (not connected to backend)
npm run build         # static export to frontend/out/
npm run lint          # ESLint
npm run test:unit     # Vitest unit tests
npm run test:e2e      # Playwright E2E tests
npm run test:all      # both
```

The frontend is built as a static export (`next.config.ts` sets `output: "export"`). FastAPI serves the `frontend/out/` directory at the root path — so after `npm run build`, the Docker container picks up the new build.

## Architecture

### Request Flow

```
Browser → FastAPI (/api/*) → SQLite (kanban.db)
                           → OpenRouter LLM (ai_service.py)
Browser → FastAPI (/)      → Static files (frontend/out/)
```

### Backend (`backend/`)

- **`main.py`** — FastAPI app, all routes, CORS config, mounts static frontend
- **`database.py`** — SQLite init; single table `boards(username PK, board_data TEXT)` where `board_data` is the full board JSON
- **`ai_service.py`** — OpenRouter chat via OpenAI SDK; injects current board JSON into system prompt; expects `{text_response, updated_board?}` JSON back

Key routes: `GET/PUT /api/board`, `POST /api/chat`, `GET /api/health`, `GET /api/ai_test`

### Frontend (`frontend/src/`)

- **`app/page.tsx`** — root: shows `<Login>` or `<KanbanBoard>` + `<ChatSidebar>` based on auth state
- **`lib/auth.tsx`** — auth context; credentials validated client-side, token stored in localStorage
- **`lib/kanban.ts`** — `BoardData` type (`columns`, `cards`), utility functions
- **`components/KanbanBoard.tsx`** — owns board state, fetches/persists via `/api/board`, orchestrates dnd-kit drag-drop
- **`components/ChatSidebar.tsx`** — floating chat widget; POSTs to `/api/chat`; if response includes `updated_board`, updates board state

### Board Data Shape

```typescript
type Card   = { id: string; title: string; details: string }
type Column = { id: string; title: string; cardIds: string[] }
type BoardData = { columns: Column[]; cards: Record<string, Card> }
```

This same shape is stored as JSON in SQLite and passed as context to the LLM.
