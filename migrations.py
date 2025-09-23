import psycopg2
from database import DatabaseConfig

class MigrationManager:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config

    def get_connection(self):
        return psycopg2.connect(
            database=self.db_config.database,
            user=self.db_config.user,
            password=self.db_config.password,
            host=self.db_config.host,
            port=self.db_config.port
        )

    def create_tables(self):
        """Проверка существования таблиц (создаются через init-db.sql)"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Просто проверяем что таблицы существуют
                    cursor.execute("SELECT COUNT(*) FROM products")
                    print("✅ Таблица products существует")
                    
                    cursor.execute("SELECT COUNT(*) FROM stock_movements")
                    print("✅ Таблица stock_movements существует")
                    
            return True
        except Exception as e:
            print(f"❌ Таблицы не созданы: {e}")
            return False