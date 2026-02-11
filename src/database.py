import sqlite3
import os

class LeadManager:
    def __init__(self, db_path="data/oryon.db"):
        # Garante que a pasta data existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT,
                phone_raw TEXT,
                phone_clean TEXT UNIQUE,
                lead_type TEXT,
                status TEXT DEFAULT 'NEW',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_lead(self, name, phone_raw, phone_clean, lead_type):
        try:
            self.cursor.execute("""
                INSERT INTO leads (business_name, phone_raw, phone_clean, lead_type)
                VALUES (?, ?, ?, ?)
            """, (name, phone_raw, phone_clean, lead_type))
            self.conn.commit()
            return True # Sucesso
        except sqlite3.IntegrityError:
            return False # Duplicado

    def close(self):
        self.conn.close()