import os
import sqlite3
import unittest
import json
from fastapi.testclient import TestClient

# Import from the specific filepath relative to this test
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app
from database import DB_PATH, init_db

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        # Reset DB before each test
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        self.client = TestClient(app)

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_get_board_returns_default(self):
        response = self.client.get("/api/board")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("columns", data)
        self.assertEqual(len(data["columns"]), 5)
        self.assertEqual(data["columns"][0]["id"], "col-backlog")

    def test_update_board_modifies_data(self):
        # Create a new, modified board payload using the real schema shape
        new_board = {
            "columns": [
                {
                    "id": "col-backlog",
                    "title": "Backlog",
                    "cardIds": ["card-1", "card-new"]
                }
            ],
            "cards": {
                "card-1": {"id": "card-1", "title": "Setup project", "details": "Initialize NextJS and FastAPI"},
                "card-new": {"id": "card-new", "title": "New Card", "details": "Added via API"}
            }
        }
        
        # Call the PUT endpoint
        put_response = self.client.put("/api/board", json={"board_data": new_board})
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json(), {"status": "success"})
        
        # Verify the GET endpoint returns the new data
        get_response = self.client.get("/api/board")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json(), new_board)
        
        # Verify it persisted to SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT board_data FROM boards WHERE username='user'")
        row = cursor.fetchone()
        conn.close()
        
        saved_json = json.loads(row[0])
        self.assertEqual(saved_json, new_board)

if __name__ == '__main__':
    unittest.main()
