"""Модуль содержит эндпоинты для таблицы product_needs"""


from fastapi import APIRouter
from app.production_needs.servive.valide_product import proccess_batch_data
from app.production_needs.schemas import ProductNeeeds1CModel


router = APIRouter(prefix="/products", tags=["Заказы продуктов"])

@router.post("/check_1C_data")
def check_1C_data(request_data: ProductNeeeds1CModel):
    data = request_data.data
    result = proccess_batch_data(data)
    valide_products = result[0]
    errors_products = result[1]
    return {
        f"valide_products {len(valide_products)}": valide_products,
        f"error_products": len(data) - len(valide_products),
        f"errors {len(errors_products)}": errors_products
    }