"""Модуль описывает схемы входных и выходных данных"""


from pydantic import BaseModel, validator
from typing import List


class Product1CModel(BaseModel):
    """Класс описывает схему одной строки таблицы заказов из 1С"""

    id_prod: int
    version_prod: int
    num_order: str
    count_apply: int
    entry_type: int

    @validator('version_prod')
    def validate_version_prod(cls, value: int):
        if value != 0:
            raise ValueError(f'{value} должна быть 0')
        return value

    @validator('entry_type')
    def validate_entry_type(cls, value: int):
        if value != 1:
            raise ValueError(f'{value} должно быть 1')
        return value


class ProductNeeeds1CModel(BaseModel):
    """Класс описывает схему данных продуктов и заказов, переданных из 1С"""

    data: List[Product1CModel]
    batch_id: str
    total_batches: int
    current_batch: int


class OneStringErrorDetail(BaseModel):
    """Класс описывает схему одного продукта из 1С, если будет ошибка валидации"""

    id_prod: int
    index: int
    error: str


class OneStringValid(BaseModel):
    """Класс описывает валидную запись продукта из 1С"""
    id_prod: int
    version_prod: int
    num_order: str
    count_apply: int