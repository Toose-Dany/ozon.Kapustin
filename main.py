from repository import ProductRepository
from database import DatabaseConfig, DatabaseConnection
from migrations import MigrationManager
from service import ProductService
from fastapi import FastAPI, HTTPException
from product import Product

# Initialize
## DB config
db_config = DatabaseConfig(
    'ozon_warehouse_db',
    'postgres',
    'postgres',
    '123Secret_a',
    5432
)
db_connection = DatabaseConnection(db_config)
## Migrations
migration_manager = MigrationManager(db_config)
migration_manager.create_tables()
# Repository and Service
repository = ProductRepository(db_connection)
service = ProductService(repository)

app = FastAPI(
    title="Ozon Warehouse API"
)

@app.get("/")
async def root():
    return {"message": "Ozon Warehouse Management System"}

@app.get("/products")
async def get_products():
    try:
        return service.get_all()
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при получении товаров: {str(e)}")

@app.post("/products")
async def create_product(product_data: dict):
    try:
        # Validation
        required_fields = ["name", "sku", "quantity", "price"]
        for field in required_fields:
            if field not in product_data:
                raise HTTPException(status_code=400, detail=f"Отсутствует обязательное поле {field}")
        
        product = Product(
            id=None,  # ID будет сгенерирован базой данных
            name=product_data['name'],
            sku=product_data['sku'],
            quantity=product_data['quantity'],
            price=product_data['price'],
            category=product_data.get('category')  # Необязательное поле
        )

        created_product = service.create_product(product)
        return created_product

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при добавлении товара: {str(e)}")

@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    try:
        product = service.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        return product
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при получении товара: {str(e)}")

@app.put("/products/{product_id}")
async def update_product(product_id: int, product_data: dict):
    try:
        product = service.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        # Обновляем поля товара
        if 'name' in product_data:
            product.name = product_data['name']
        if 'sku' in product_data:
            product.sku = product_data['sku']
        if 'quantity' in product_data:
            product.quantity = product_data['quantity']
        if 'price' in product_data:
            product.price = product_data['price']
        if 'category' in product_data:
            product.category = product_data['category']
        
        updated_product = service.update_product(product)
        return updated_product

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при обновлении товара: {str(e)}")

@app.patch("/products/{product_id}/stock")
async def update_stock(product_id: int, stock_data: dict):
    try:
        if 'quantity' not in stock_data:
            raise HTTPException(status_code=400, detail="Отсутствует поле quantity")
        
        result = service.update_stock(product_id, stock_data['quantity'])
        if not result:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        return {"message": "Количество товара успешно обновлено"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при обновлении количества: {str(e)}")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    try:
        result = service.delete_product(product_id)
        if not result:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        return {"message": "Товар успешно удален"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при удалении товара: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)