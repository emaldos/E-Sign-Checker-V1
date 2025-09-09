import sqlite3, hashlib, datetime
from typing import Optional, List, Tuple

class SignatureDatabase:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self._init()
    def _init(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS signatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_name TEXT NOT NULL,
                title TEXT,
                created_date TEXT NOT NULL,
                signature_data BLOB NOT NULL,
                hash_value TEXT NOT NULL,
                notes TEXT
            )
        """)
        self.conn.commit()
    def save_signature(self, owner: str, title: str, data: bytes, notes: str = "") -> bool:
        try:
            h = hashlib.sha256(data).hexdigest()
            c = self.conn.cursor()
            c.execute(
                "INSERT INTO signatures (owner_name, title, created_date, signature_data, hash_value, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (owner, title, datetime.datetime.now().isoformat(), data, h, notes)
            )
            self.conn.commit()
            return True
        except:
            return False
    def count(self, q: str = "") -> int:
        c = self.conn.cursor()
        if q:
            like = f"%{q}%"
            c.execute("""
                SELECT COUNT(*) FROM signatures
                WHERE owner_name LIKE ? OR title LIKE ? OR notes LIKE ? OR created_date LIKE ?
            """, (like, like, like, like))
        else:
            c.execute("SELECT COUNT(*) FROM signatures")
        return int(c.fetchone()[0])
    def page(self, q: str = "", limit: int = 10, offset: int = 0) -> List[Tuple[int,str,str,str,str,bytes]]:
        c = self.conn.cursor()
        if q:
            like = f"%{q}%"
            c.execute("""
                SELECT id, owner_name, title, created_date, notes, signature_data
                FROM signatures
                WHERE owner_name LIKE ? OR title LIKE ? OR notes LIKE ? OR created_date LIKE ?
                ORDER BY datetime(created_date) DESC
                LIMIT ? OFFSET ?
            """, (like, like, like, like, limit, offset))
        else:
            c.execute("""
                SELECT id, owner_name, title, created_date, notes, signature_data
                FROM signatures
                ORDER BY datetime(created_date) DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
        return c.fetchall()
    def get_signature(self, sig_id: int) -> Optional[bytes]:
        c = self.conn.cursor()
        c.execute("SELECT signature_data FROM signatures WHERE id = ?", (sig_id,))
        r = c.fetchone()
        return r[0] if r else None
    def delete(self, sig_id: int) -> bool:
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM signatures WHERE id = ?", (sig_id,))
            self.conn.commit()
            return True
        except:
            return False
