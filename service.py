from repository import ProductRepository
from product import Product

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(self, product: Product):
        """Добавление товара на склад"""
        return self.repository.create_product(product)
    
    def get_all(self):
        '''Получить все товары на складе'''
        return self.repository.get_all()
        
    def get_by_id(self, product_id: int):
        '''Получить товар по id'''
        return self.repository.get_by_id(product_id)
    
    def update_product(self, product: Product):
        """Изменить существующий товар. 
            Если товара не существует, ничего не делать."""
        return self.repository.update_product(product)
    
    def delete_product(self, product_id: int):
        """Удалить существующий товар со склада.
            Если товара не существует, ничего не делать."""
        return self.repository.delete_product(product_id)
    
    def get_by_sku(self, sku: str):
        '''Получить товар по SKU (артикулу)'''
        return self.repository.get_by_sku(sku)
    
    def update_stock(self, product_id: int, new_quantity: int):
        """Обновить количество товара на складе"""
        return self.repository.update_stock(product_id, new_quantity)