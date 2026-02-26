import os
import sqlite3
import unittest
# Import from the specific filepath relative to this test
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import DB_PATH, init_db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Ensure fresh DB for each test by deleting if exists
        test_db_path = DB_PATH
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            
    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_database_initialization(self):
        # Running init_db should create the file and the default user
        init_db()
        
        self.assertTrue(os.path.exists(DB_PATH))
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verify the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='boards'")
        table = cursor.fetchone()
        self.assertIsNotNone(table)
        
        # Verify default user is populated
        cursor.execute("SELECT username, board_data FROM boards WHERE username='user'")
        user_row = cursor.fetchone()
        self.assertIsNotNone(user_row)
        self.assertEqual(user_row[0], "user")
        self.assertIn("columns", user_row[1]) # basic JSON validation check
        
        conn.close()

if __name__ == '__main__':
    unittest.main()
