import sqlite3
import os
from datetime import datetime

class LeadManager:
    def __init__(self, db_path="data/oryon.db"):
        # Garante que a pasta data existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Aqui adicionamos a coluna updated_at que faltava!
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT,
                phone_raw TEXT,
                phone_clean TEXT UNIQUE,
                lead_type TEXT,
                status TEXT DEFAULT 'NEW',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
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
            return True 
        except sqlite3.IntegrityError:
            return False

    def get_leads_to_contact(self, limit=5):
        """Pega apenas celulares novos"""
        self.cursor.execute("""
            SELECT id, business_name, phone_clean 
            FROM leads 
            WHERE status = 'NEW' AND lead_type = 'mobile'
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def mark_hello_sent(self, phone_clean):
        """Atualiza status para SENT_HELLO e marca a hora"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            UPDATE leads 
            SET status = 'SENT_HELLO', updated_at = ?
            WHERE phone_clean = ?
        """, (now, phone_clean))
        self.conn.commit()

    def close(self):
        self.conn.close()