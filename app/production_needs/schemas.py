"""Модуль описывает схемы входных и выходных данных"""


from pydantic import BaseModel, validator
from typing import List, Any, Optional


class Product1CModel(BaseModel):
    """Класс описывает схему одной строки таблицы заказов из 1С"""

    id_prod: Any
    version_prod: Any
    num_order: Any
    count_apply: Any
    entry_type: Any


class ProductNeeeds1CModel(BaseModel):
    """Класс описывает схему данных продуктов и заказов, переданных из 1С"""

    data: List[Product1CModel]
    batch_id: str
    total_batches: int
    current_batch: int


class OneStringErrorDetail(BaseModel):
    """Класс описывает схему одного продукта из 1С, если будет ошибка валидации"""

    id_prod: Optional[int]
    index: int
    error: List[str]


class OneStringValid(Product1CModel):
    """Класс описывает валидную запись продукта из 1С"""
    pass