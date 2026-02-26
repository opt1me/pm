import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "kanban.db")

DEFAULT_BOARD_JSON = json.dumps({
  "columns": [
    { "id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"] },
    { "id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"] },
    {
      "id": "col-progress",
      "title": "In Progress",
      "cardIds": ["card-4", "card-5"]
    },
    { "id": "col-review", "title": "Review", "cardIds": ["card-6"] },
    { "id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"] }
  ],
  "cards": {
    "card-1": {
      "id": "card-1",
      "title": "Align roadmap themes",
      "details": "Draft quarterly themes with impact statements and metrics."
    },
    "card-2": {
      "id": "card-2",
      "title": "Gather customer signals",
      "details": "Review support tags, sales notes, and churn feedback."
    },
    "card-3": {
      "id": "card-3",
      "title": "Prototype analytics view",
      "details": "Sketch initial dashboard layout and key drill-downs."
    },
    "card-4": {
      "id": "card-4",
      "title": "Refine status language",
      "details": "Standardize column labels and tone across the board."
    },
    "card-5": {
      "id": "card-5",
      "title": "Design card layout",
      "details": "Add hierarchy and spacing for scanning dense lists."
    },
    "card-6": {
      "id": "card-6",
      "title": "QA micro-interactions",
      "details": "Verify hover, focus, and loading states."
    },
    "card-7": {
      "id": "card-7",
      "title": "Ship marketing page",
      "details": "Final copy approved and asset pack delivered."
    },
    "card-8": {
      "id": "card-8",
      "title": "Close onboarding sprint",
      "details": "Document release notes and share internally."
    }
  }
})

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the boards table.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boards (
            username TEXT PRIMARY KEY,
            board_data TEXT NOT NULL
        )
    ''')
    
    # Initialize the default user if they don't exist.
    cursor.execute('SELECT username FROM boards WHERE username = ?', ('user',))
    if not cursor.fetchone():
        cursor.execute(
            'INSERT INTO boards (username, board_data) VALUES (?, ?)',
            ('user', DEFAULT_BOARD_JSON)
        )
        
    conn.commit()
    conn.close()

# Automatically initialize database when database.py is loaded.
init_db()
