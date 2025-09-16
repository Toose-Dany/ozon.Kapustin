from database import DatabaseConfig, DatabaseConnection
from migrations import MigrationManager
from repository import ozonRepository
from service import ozonService
from fastapi import FastAPI, HTTPException
from ozon import ozon

#Initialize
## DB config
db_config= DatabaseConfig(
    'ozonsdb',
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
repository = ozonRepository(db_connection)
service = ozonService(repository)

app = FastAPI(
    title="ozon API"
)

@app.get("/")
async def root():
    return {"message":"Hello from FastAPI"}

@app.get("/ozons")
async def get_ozons():
    try:
        return service.get_all()
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при получении полётов: {str(e)}")

@app.post("/ozons")
async def create_ozon(ozon_data: dict):
    try:
        #Validation
        required_fields = ["price","plane"]
        for field in required_fields:
            if field not in ozon_data:
                raise HTTPException(status_code=400,detail=f"Отсутствует обязательное поле {field}")
        
        ozon = ozon(
            price=ozon_data['price'],
            plane=ozon_data['plane']
        )

        created_ozon = service.create_ozon(ozon)
        return created_ozon

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при добавлении полёта: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8080)