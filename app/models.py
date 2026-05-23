import os
import mysql.connector

class ItemModel:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'db'),
            'user': os.getenv('DB_USER', 'taskuser'),
            'password': os.getenv('DB_PASS', 'taskpass'),
            'database': os.getenv('DB_NAME', 'taskdb')
        }
        print(f"DB Config: host={self.config['host']}, user={self.config['user']}, database={self.config['database']}")

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def get_all_items(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT id, name FROM items')
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            return items
        except Exception as e:
            print(f"Error in get_all_items: {e}")
            return []
