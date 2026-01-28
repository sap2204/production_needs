"""Модуль содержит эндпоинты для таблицы product_needs"""


from fastapi import APIRouter
from app.production_needs.servive.valide_product import proccess_batch_data
#from app.production_needs.schemas import ProductNeeeds1CModel
#from app.production_needs.servive.service import uploader

#from app.database import get_session
import anyio
from fastapi import HTTPException
from app.database import async_execute
from sqlalchemy import text

router = APIRouter(prefix="/products", tags=["Заказы продуктов"])

# @router.post("/check_1C_data")
# def check_1C_data(request_data: ProductNeeeds1CModel):
#     data = request_data.data
#     result = proccess_batch_data(data)
#     valid_products = result[0]
#     errors_products = result[1]
#     return {
#         f"valid_products {len(valid_products)}": valid_products,
#         f"error_products": len(data) - len(valid_products),
#         f"errors {len(errors_products)}": errors_products
#     }


# @router.post("/upload_1C_data")
# def upload_1c_data(request_data: ProductNeeeds1CModel):
#     """Эндпоинт загрузки заказов с продуктами из 1С"""
#     print("Начало выполнения эндпоинта")
#     # Проведение валидации входных данных
#     data = request_data.data
#     validate_products = proccess_batch_data(data)
#     print("Получены валидные данные")
#     valid_products = validate_products[0]
#     errors_products = validate_products[1]

#     print("Начинается сервисный слой")
#     result = uploader.process_upload_from_1c(valid_products)
#     return result

#     # Вставка в таблицу production_needs только валидных данных


@router.get("/health")
async def check_db():
    try:
        query = text("SELECT 1 AS check_db FROM kn51_2c_production_needs")
        results = await async_execute(query)
        
        if results:
            # Теперь results - это список, и мы можем получить первую строку
            return {"status": "OK", "result": results[0].check_db}
        else:
            return {"status": "NO_DATA"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))