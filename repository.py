from product import Product  # Исправленный импорт
from database import DatabaseConnection


class ProductRepository:
    '''Класс-репозиторий для доступа к БД склада Ozon'''

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def create_product(self, product: Product):
        """Добавление товара на склад"""

        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO products 
                        (name, sku, quantity, price, category)
                        VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            ''', (product.name, product.sku, product.quantity, product.price, product.category))
        
        product_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        product.id = product_id
        return product
    
    def get_all(self):
        """Получить все товары"""
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, sku, quantity, price, category FROM products ORDER BY id")
        rows = cursor.fetchall()

        products = []
        for row in rows:
            products.append(Product(
                id=row[0],
                name=row[1],
                sku=row[2],
                quantity=row[3],
                price=row[4],
                category=row[5]
            ))
              
        cursor.close()
        conn.close()
        return products
        
    def get_by_id(self, product_id: int):
        """Получить товар по id"""
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, sku, quantity, price, category FROM products WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if row:
            return Product(
                id=row[0],
                name=row[1],
                sku=row[2],
                quantity=row[3],
                price=row[4],
                category=row[5]
            )
        return None
    
    def get_by_sku(self, sku: str):
        """Получить товар по артикулу (SKU)"""
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, sku, quantity, price, category FROM products WHERE sku = %s", (sku,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if row:
            return Product(
                id=row[0],
                name=row[1],
                sku=row[2],
                quantity=row[3],
                price=row[4],
                category=row[5]
            )
        return None
    
    def update_product(self, product: Product):
        """Изменить существующий товар."""
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products
            SET name = %s, sku = %s, quantity = %s, price = %s, category = %s
            WHERE id = %s
            ''', (product.name, product.sku, product.quantity, product.price, product.category, product.id))
        
        conn.commit()

        cursor.close()
        conn.close()

        return product
    
    def update_stock(self, product_id: int, new_quantity: int):
        """Обновить количество товара на складе"""
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products
            SET quantity = %s
            WHERE id = %s
            ''', (new_quantity, product_id))
        
        conn.commit()
        updated = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return updated
    
    def delete_product(self, product_id: int):
        """Удалить товар со склада"""
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM products WHERE id = %s
            ''', (product_id,))
        conn.commit()
        deleted = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return deleted