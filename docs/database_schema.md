# Database Schema for Kanban MVP

For this project, we are storing the core data natively as JSON payloads in an SQLite database. This ensures simplicity while conforming to the schema the frontend expects, and allows the LLM to read and write the exact shape with minimal translation logic.

## SQLite Table: `boards`

There will be a single table intended to store board state per user.

**Columns:**

- `username` (TEXT, PRIMARY KEY): The identifier for the user (for this MVP, always `"user"`).
- `board_data` (TEXT): The full JSON representation of the Kanban board at any given time.

## Board Data Shape

The `board_data` column holds a JSON object with two top-level keys:

- `columns`: ordered array of column objects, each with `id`, `title`, and `cardIds` (an ordered array of card IDs belonging to that column).
- `cards`: a flat dictionary mapping card ID to card object (`id`, `title`, `details`).

```json
{
  "columns": [
    { "id": "col-backlog",   "title": "Backlog",      "cardIds": ["card-1", "card-2"] },
    { "id": "col-discovery", "title": "Discovery",    "cardIds": ["card-3"] },
    { "id": "col-progress",  "title": "In Progress",  "cardIds": ["card-4", "card-5"] },
    { "id": "col-review",    "title": "Review",       "cardIds": ["card-6"] },
    { "id": "col-done",      "title": "Done",         "cardIds": ["card-7", "card-8"] }
  ],
  "cards": {
    "card-1": { "id": "card-1", "title": "Align roadmap themes",   "details": "Draft quarterly themes with impact statements and metrics." },
    "card-2": { "id": "card-2", "title": "Gather customer signals", "details": "Review support tags, sales notes, and churn feedback." },
    "card-3": { "id": "card-3", "title": "Prototype analytics view","details": "Sketch initial dashboard layout and key drill-downs." },
    "card-4": { "id": "card-4", "title": "Refine status language",  "details": "Standardize column labels and tone across the board." },
    "card-5": { "id": "card-5", "title": "Design card layout",      "details": "Add hierarchy and spacing for scanning dense lists." },
    "card-6": { "id": "card-6", "title": "QA micro-interactions",   "details": "Verify hover, focus, and loading states." },
    "card-7": { "id": "card-7", "title": "Ship marketing page",     "details": "Final copy approved and asset pack delivered." },
    "card-8": { "id": "card-8", "title": "Close onboarding sprint", "details": "Document release notes and share internally." }
  }
}
```

Updating the board replaces the entire `board_data` value for the given `username`.
