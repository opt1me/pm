import os
import sqlite3
import unittest
import json
from unittest.mock import patch
from fastapi.testclient import TestClient

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app
from database import DB_PATH, init_db

VALID_BOARD = {
    "columns": [
        {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-new"]},
    ],
    "cards": {
        "card-new": {"id": "card-new", "title": "Buy milk", "details": ""}
    }
}


class TestChatEndpoint(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        self.client = TestClient(app)

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_chat_returns_text_without_board_update(self):
        with patch("ai_service.chat_with_board_context") as mock_chat:
            mock_chat.return_value = {
                "text_response": "Hello! How can I help?",
                "updated_board": None,
            }
            response = self.client.post("/api/chat", json={"message": "Hello"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["text_response"], "Hello! How can I help?")
        self.assertFalse(data["updated"])

    def test_chat_with_valid_board_update_saves_to_db(self):
        with patch("ai_service.chat_with_board_context") as mock_chat:
            mock_chat.return_value = {
                "text_response": "Added a card to buy milk.",
                "updated_board": VALID_BOARD,
            }
            response = self.client.post(
                "/api/chat", json={"message": "Add a card to buy milk"}
            )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["updated"])
        self.assertEqual(data["board_data"], VALID_BOARD)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT board_data FROM boards WHERE username='user'")
        saved = json.loads(cursor.fetchone()[0])
        conn.close()
        self.assertEqual(saved, VALID_BOARD)

    def test_chat_with_malformed_board_rejects_update(self):
        with patch("ai_service.chat_with_board_context") as mock_chat:
            mock_chat.return_value = {
                "text_response": "I tried to update.",
                "updated_board": {"columns": []},  # missing required "cards" key
            }
            response = self.client.post("/api/chat", json={"message": "Do something"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["updated"])
        self.assertIn("corrupted", data["text_response"])


if __name__ == "__main__":
    unittest.main()
