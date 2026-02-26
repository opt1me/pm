# Database Schema for Kanban MVP

For this project, we are storing the core data natively as JSON payloads in an SQLite database. This ensures simplicity while conforming to the schema the frontend expects, and allows the LLM to read and write the exact shape with minimal translation logic.

## SQLite Table: `boards`

There will be a single table intended to store board state per user.

**Columns:**

- `username` (TEXT, PRIMARY KEY): The identifier for the user (for this MVP, always `"user"`).
- `board_data` (TEXT): The full JSON representation of the Kanban board at any given time.

## Initial Board Data

When a new user is created or when the database is initialized for standard usage, the `board_data` column is populated with the following JSON structure:

```json
{
  "columns": [
    {
      "id": "col-todo",
      "title": "To Do",
      "cards": [
        { "id": "card-1", "title": "Setup project", "content": "Initialize NextJS and FastAPI" },
        { "id": "card-2", "title": "Design DB", "content": "Document SQLite approach" }
      ]
    },
    {
      "id": "col-inprogress",
      "title": "In Progress",
      "cards": [
         { "id": "card-3", "title": "Build MVP", "content": "Connect all parts together" }
      ]
    },
    {
      "id": "col-review",
      "title": "Review",
      "cards": []
    },
    {
      "id": "col-done",
      "title": "Done",
      "cards": []
    }
  ]
}
```

Updating the board drops the modified JSON snippet into the `board_data` column for that specific `username`.
