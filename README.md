# Project Management MVP

A beautifully designed, minimalist Kanban board featuring a built-in OpenRouter AI assistant.

## Architecture

- Frontend: NextJS (static export).
- Backend: Python FastAPI.
- Database: SQLite local database for state persistence.
- AI: Chat sidebar that intelligently parses requested commands and mutates the current board state.

## Setup

1. Copy `.env.example` to `.env` (if applicable) and ensure your `OPENROUTER_API_KEY` is set.
2. Ensure Docker Desktop is running.

## Running Locally

Use the provided scripts to start and stop the Docker environment:

- **Windows**: `scripts\start.bat` to start, `scripts\stop.bat` to stop.
- **Mac/Linux**: `scripts/start.sh` to start, `scripts/stop.sh` to stop.

Once running, access the application at `http://localhost:8000`.
Login with username "user" and password "password".
