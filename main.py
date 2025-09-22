# Добавьте этот импорт в начало файла main.py
from product import Product  # ← ДОБАВЬТЕ ЭТУ СТРОКУ

from repository import ProductRepository
from database import DatabaseConfig, DatabaseConnection
from migrations import MigrationManager
from service import ProductService
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название товара")
    sku: str = Field(..., min_length=1, max_length=50, description="Артикул товара")
    quantity: int = Field(..., ge=0, description="Количество товара")
    price: float = Field(..., gt=0, description="Цена товара")
    category: Optional[str] = Field(None, max_length=50, description="Категория товара")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    id: int = Field(..., gt=0, description="ID товара")

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    quantity: int = Field(..., ge=0, description="Новое количество товара")

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
    title="Ozon Warehouse API",
    description="API для управления складом товаров Ozon"
)

@app.get("/")
async def root():
    return {"message": "Ozon Warehouse Management System"}

@app.get("/products", response_model=List[ProductResponse], summary="Получить все товары")
async def get_all_products():
    """
    Получить список всех товаров на складе.
    """
    try:
        products = service.get_all()
        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товары не найдены"
            )
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении товаров: {str(e)}"
        )

@app.get("/products/{product_id}", response_model=ProductResponse, summary="Получить товар по ID")
async def get_product_by_id(product_id: int):
    """
    Получить информацию о конкретном товаре по его ID.
    """
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID товара должен быть положительным числом"
            )
        
        product = service.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с ID {product_id} не найден"
            )
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении товара: {str(e)}"
        )

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, summary="Создать новый товар")
async def create_product(product_data: ProductCreate):
    """
    Добавить новый товар на склад.
    """
    try:
        # Проверяем, не существует ли товар с таким же SKU
        existing_product = service.get_by_sku(product_data.sku)
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Товар с артикулом {product_data.sku} уже существует"
            )
        
        product = Product(
            id=None,
            name=product_data.name,
            sku=product_data.sku,
            quantity=product_data.quantity,
            price=product_data.price,
            category=product_data.category
        )

        created_product = service.create_product(product)
        return created_product

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при добавлении товара: {str(e)}"
        )

@app.put("/products/{product_id}", response_model=ProductResponse, summary="Обновить товар")
async def update_product(product_id: int, product_data: ProductUpdate):
    """
    Обновить информацию о товаре.
    """
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID товара должен быть положительным числом"
            )
        
        if product_id != product_data.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID в пути и в теле запроса не совпадают"
            )
        
        # Проверяем существование товара
        existing_product = service.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с ID {product_id} не найден"
            )
        
        # Проверяем, не занят ли новый SKU другим товаром
        if existing_product.sku != product_data.sku:
            product_with_sku = service.get_by_sku(product_data.sku)
            if product_with_sku and product_with_sku.id != product_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Артикул {product_data.sku} уже используется другим товаром"
                )
        
        product = Product(
            id=product_id,
            name=product_data.name,
            sku=product_data.sku,
            quantity=product_data.quantity,
            price=product_data.price,
            category=product_data.category
        )

        updated_product = service.update_product(product)
        return updated_product

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении товара: {str(e)}"
        )

@app.patch("/products/{product_id}/stock", summary="Обновить количество товара")
async def update_stock(product_id: int, stock_data: StockUpdate):
    """
    Обновить количество товара на складе.
    """
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID товара должен быть положительным числом"
            )
        
        # Проверяем существование товара
        existing_product = service.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с ID {product_id} не найден"
            )
        
        result = service.update_stock(product_id, stock_data.quantity)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось обновить количество товара"
            )
        
        return {"message": "Количество товара успешно обновлено", "new_quantity": stock_data.quantity}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении количества: {str(e)}"
        )

@app.delete("/products/{product_id}", summary="Удалить товар")
async def delete_product(product_id: int):
    """
    Удалить товар со склада.
    """
    try:
        if product_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID товара должен быть положительным числом"
            )
        
        # Проверяем существование товара
        existing_product = service.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Товар с ID {product_id} не найден"
            )
        
        result = service.delete_product(product_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось удалить товар"
            )
        
        return {"message": "Товар успешно удален"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении товара: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)