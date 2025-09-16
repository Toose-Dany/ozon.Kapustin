from repository import ozonRepository
from ozon import ozon

class ozonService:
    def __init__(self,repository:ozonRepository):
        self.repository = repository

    def create_ozon(self, ozon:ozon):
        """Добавление рейса"""
        return self.repository.create_ozon(ozon)
    
    def get_all(self):
        '''Получить все полёты'''
        return self.repository.get_all()
        
    def get_by_id(self,ozon_id:int):
        '''Получить полёт по id'''
        return self.repository.get_by_id(ozon_id)
    
    def update_ozon(self, ozon:ozon):
        """Изменить существующий рейс. 
            Если рейса не существует, ничего не делать."""
        return self.repository.update_ozon(ozon)
    
    def delete_ozon(self,ozon_id:int):
        """Удалить существующий рейс.
            Если рейса не существует, ничего не делать."""
        return self.repository.delete_ozon(ozon_id)