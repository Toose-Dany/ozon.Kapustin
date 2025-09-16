import sqlite3


class ozonService:
    def __init__(self, db_name: str = ""):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Иницилизация таблиц"""
        with self.get_connection as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS ozons(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         plane TEXT NOT NULL,
                         price REAL NOT NULL
                         )
                ''')