"""
Модуль описывает валидацию каждой позиции продуктов из 1С.
Формируется статистика валидных продуктов и с ошибками
"""


from typing import Optional, List, Tuple
from app.production_needs.schemas import OneStringErrorDetail, OneStringValid, Product1CModel



def validate_product(product: Product1CModel) -> List[str]:
    """
    Функция проверяет одну строку продукта
    и возвращает сообщение об ошибке валидации
    """

    errors = []

    # Проверка наличия обязательных полей
    required_fields = ["id_prod", "version_prod", "num_order", "count_apply", "entry_type"]
    for field in required_fields:
        if not hasattr(product, field):
            errors.append(f"Отсутствует поле: {field}")

    # Проверка типов данных полей
    if not isinstance(product.id_prod, int):
        errors.append(f"Поле id_prod должно быть целым числом")
    if not isinstance(product.version_prod, int):
        errors.append(f"Поле version_prod должно быть целым числом")
    if not isinstance(product.num_order, str):
        errors.append(f"Поле num_order должно быть строкой")
    if not isinstance(product.count_apply, int):
        errors.append(f"Поле count_apply должно быть целым числом")
    if not isinstance(product.entry_type, int):
        errors.append(f"Поле entry_type должно быть целым числом")

    # Проверка значений полей
    if product.version_prod != 0:
        errors.append(f"Поле version_prod должно быть нулем 0")
    if product.entry_type != 1:
        errors.append(f"Поле entry_type должно быть 1")
    if isinstance(product.num_order, str):
        if not product.num_order.strip():
            errors.append(f"Поле num_order не может быть пустой строкой")

    return errors


def proccess_batch_data(products: List[Product1CModel]) -> Tuple[List[OneStringValid],
                                                           List[OneStringErrorDetail]]:
    """
    Функция проходит по списку продуктов, проводить валидацию данных.
    Собирает валидные и невалидные данные в разные списки и возвращает их
    """
    valide_products = []
    error_product = []

    for idx, product in enumerate(products):
        error_message = validate_product(product)
        if error_message:
            error_product.append(OneStringErrorDetail(
                id_prod=product.id_prod if isinstance(product.id_prod, int) else None,
                index=idx,
                error=error_message
                )
            )
        else:
            valide_products.append(product)
    return valide_products, error_product

