import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import get_db_connection, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Project Management MVP API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

import json
from pydantic import BaseModel

from ai_service import test_ai_connection

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/ai_test")
def ai_test():
    """Test endpoint for verifying OpenRouter LLM connectivity."""
    result = test_ai_connection()
    return {"result": result}

class BoardUpdate(BaseModel):
    board_data: dict

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    """Chat with the AI and optionally update the board state."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT board_data FROM boards WHERE username = ?", ("user",))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"error": "Board not found"}

    current_board = json.loads(row["board_data"])

    from ai_service import chat_with_board_context
    ai_response = chat_with_board_context(req.message, current_board)

    updated_board = ai_response.get("updated_board")

    is_valid_board = (
        isinstance(updated_board, dict) and
        "columns" in updated_board and isinstance(updated_board["columns"], list) and
        "cards" in updated_board and isinstance(updated_board["cards"], dict)
    )

    if updated_board and is_valid_board:
        cursor.execute(
            "UPDATE boards SET board_data = ? WHERE username = ?",
            (json.dumps(updated_board), "user")
        )
        conn.commit()
    elif updated_board and not is_valid_board:
        updated_board = None
        current_text = ai_response.get("text_response", "")
        ai_response["text_response"] = f"{current_text} (Note: I attempted to change the board but my output was corrupted, so the update was aborted to protect your data.)"

    conn.close()

    return {
        "text_response": ai_response.get("text_response", "An error occurred with the AI response."),
        "updated": bool(updated_board),
        "board_data": updated_board if updated_board else current_board
    }

@app.get("/api/board")
def get_board():
    """Retrieve the JSON board data for the default user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT board_data FROM boards WHERE username = ?", ("user",))
    row = cursor.fetchone()
    conn.close()

    if row:
        return json.loads(row["board_data"])
    return {"error": "Board not found"}

@app.put("/api/board")
def update_board(update: BoardUpdate):
    """Update the JSON board data for the default user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE boards SET board_data = ? WHERE username = ?",
        (json.dumps(update.board_data), "user")
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

# Mount the static Next.js frontend files
frontend_out = os.path.join(os.path.dirname(__file__), "..", "frontend", "out")
if os.path.exists(frontend_out):
    app.mount("/", StaticFiles(directory=frontend_out, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"error": "Frontend build not found. Please run 'npm run build' in the frontend directory."}
