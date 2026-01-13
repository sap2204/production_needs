"""
Модуль описывает бизнес логику обновления таблицы production_needs
"""


from app.database import get_session
from schemas import ProductNeeeds1CModel
from sqlalchemy import text


class ProductionNeedsService:

    def upload_production_needs_from_1c(self, data: ProductNeeeds1CModel):
        """
        Метод реализует полную логику загрузки данных
        о производственных заказов из 1С в таблицу production_needs
        """
        with get_session() as session:
            pass

    def _create_temporary_tables(self, session) -> None:
        """Создание табличных переменных @data и @num_orders"""
        query_for_data = text("""
                             DECLARE @data TABLE(
                             [id_prod] INT
                            ,[version_prod] INT
                            ,[num_order] VARCHAR(50)
                            ,[count_apply] INT
                            ,[entry_type] INT
                            ,[date] DATETIME
                            )
                            """)
        session.execute(query_for_data)

        query_for_num_orders = text("""
                                    DECLARE @num_orders TABLE(
                                    [num_order] VARCHAR(50)
                                                            )
                                    """)
        session.execute(query_for_num_orders)

    def _load_from_1c_to_data(self, session, data_items: ProductNeeeds1CModel):
        """Метод загрузки данных из 1С в табличную переменную data"""
        if not data_items:
            return 0

        loaded_counter = 0

        for item in data_items:



