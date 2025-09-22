from ozon import ozon
from database import DatabaseConnection


class ozonRepository:
    '''Класс-репозиторий для доступа к БД'''

    def __init__(self,connection: DatabaseConnection):
        self.connection=connection

    def create_ozon(self, ozon:ozon):
        """Добавление заказа"""

        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO ozons
                        (name,price)
                        VALUES (%s,%s)
            ''',(ozon.name,ozon.price))
        conn.commit()

        cursor.close()
        conn.close()

        return ozon
    
    def get_all(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ozons ORDER BY id")
        rows = cursor.fetchall()

        ozons = []
        for row in rows:
            ozons.append(ozon(
                row[0],
                row[1],
                row[2]
            ))
              
        cursor.close()
        conn.close()
        return ozons
        
    def get_by_id(self,ozon_id:int):
        """Получить хзаказ по id"""
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ozons WHERE id = %s",(ozon_id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if row:
            return ozon(
                row[0],
                row[1],
                row[2]
            )
        return None
    
    def update_ozon(self, ozon:ozon):
        """Изменить существующий заказ. 
            Если заказа не существует, ничего не делать."""
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE ozons
            SET price = %s, name = %s
            WHERE id = %s
            ''',(ozon.price, ozon.name, ozon.id))
        
        result = cursor.fetchone()
        ozon.id = result[0]
        conn.commit()

        cursor.close()
        conn.close()

        return ozon
    
    def delete_ozon(self,ozon_id:int):
        """Удалить существующий заказ.
            Если заказа не существует, ничего не делать."""
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM ozons WHERE id = %s
            ''',(ozon_id,))
        conn.commit()
        deleted = cursor.rowcount

        cursor.close()
        conn.close()

        return deleted >0