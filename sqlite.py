import sqlite3


class ProductService:
    def __init__(self, db_name: str = ""):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Инициализация таблиц для склада Ozon"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS products(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         sku TEXT NOT NULL UNIQUE,
                         quantity INTEGER NOT NULL,
                         price REAL NOT NULL,
                         category TEXT,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                         )
                ''')
            