"""
Модуль описывает валидацию каждой позиции продуктов из 1С.
Формируется статистика валидных продуктов и с ошибками
"""


from typing import Optional, List, Tuple
from app.production_needs.schemas import OneStringErrorDetail, OneStringValid


def validate_product(product: dict) -> Optional[str]:
    """
    Функция проверяет одну строку продукта
    и возвращает сообщение об ошибке валидации
    """

    # Проверка наличия обязательных полей
    required_fields = ["id_prod", "version_prod", "num_order", "count_apply", "entry_type"]
    for field in required_fields:
        if field not in product:
            return f"Отсутствует поле: {field}"

    # Проверка типов данных полей
    if not isinstance(product["id_prod"], int):
        return f"id_prod должно быть целым числом"
    if not isinstance(product["version_prod"], int):
        return f"version_prod должно быть целым числом"
    if not isinstance(product["num_order"], str):
        return f"num_order должно быть строкой"
    if not isinstance(product["count_apply"], int):
        return f"count_apply должно быть целым числом"
    if not isinstance(product["entry_type"], int):
        return f"entry_type должно быть целым числом"

    # Проверка значений полей
    if product["version_prod"] != 0:
        return f"version_prod должно быть нулем 0"
    if product["entry_type"] != 1:
        return f"entry_type должно быть 1"
    if product["count_apply"] < 0:
        return f"count_apply должно быть больше 0"
    if not product["num_order"].strip():
        return f"num_order не может быть пустой строкой"

    # Все ок
    return None


def proccess_batch_data(products: List[dict]) -> Tuple[List[OneStringValid], List[OneStringErrorDetail]]:
    valide_products = []
    error_product = []

    for idx, product in enumerate(products):
        error_message = validate_product(product)
        if error_message:
            error_product.append(OneStringErrorDetail(
                id_prod=product["id_prod"],
                index=idx,
                error=error_message
                )
            )
        else:
            valide_products.append(OneStringValid(**product))
    return (valide_products, error_product)

