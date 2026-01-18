"""
Модуль описывает бизнес логику обновления таблицы production_needs
"""


from app.database import get_session
from app.production_needs.schemas import Product1CModel
from sqlalchemy import text
from typing import List


class ProductionNeedsService:
    """Класс описывает бизнес-логику обновления таблицы production_needs данными из 1С"""

    def process_upload_from_1c(self, data_from_1c: List[Product1CModel]):
        """
        Метод реализует полную логику загрузки данных
        о производственных заказов из 1С в таблицу production_needs
        """
        print("Начинается главный метод загрузки")
        with get_session() as session:
            self._create_temporary_tables(session)
            self._load_data_to_temp_table(session, data_from_1c)
            self._extract_unique_orders(session)
            self._find_removed_items(session)
            deleted_count = self._cleanup_old_uploads(session)
            inserted_count = self._insert_new_data(session)
            updated_count = self._update_entry_statuses(session)

    def _create_temporary_tables(self, session) -> None:
        """Создание табличных переменных @data и @num_orders"""

        print("Начало создание временных таблиц")
        query_for_data = text("""
                            IF OBJECT_ID('temp..#data') IS NOT NULL
                                DROP TABLE #data;
                                
                            CREATE TABLE #data(
                            [id_prod] INT
                            ,[version_prod] INT
                            ,[num_order] VARCHAR(50)
                            ,[count_apply] INT
                            ,[entry_type] INT
                            ,[date] DATETIME)
                            """)

        session.execute(query_for_data)
        print("Создана временная таблица #data")

        query_for_num_orders = text("""
                                    IF OBJECT_ID('temp..#num_orders') IS NOT NULL
                                        DROP TABLE #num_orders;
                                        
                                    CREATE TABLE #num_orders(
                                    [num_order] VARCHAR(50)
                                                            )
                                    """)
        session.execute(query_for_num_orders)
        print("Создана временная таблица #num_order")

    def _load_data_to_temp_table(self, session, data_from_1c: List[Product1CModel]):
        """Метод загрузки данных из 1С во временную таблицу #data"""
        print("Начинается метод заполнения временной табл. #data")
        if not data_from_1c:
            return 0
        loaded_counter = 0

        for item in data_from_1c:
            try:
                print("Извлекаем id_prod из текущей записи")
                product_id = item.id_prod
                print("Получение актуальной версии продукта из таблицы product")
                actual_version = self._get_product_version(session, product_id)
                print("Начинается вставка данных во временную таблицу #data")
                insert_sql = text(
                    """
                    INSERT INTO #data(
                    [id_prod], [version_prod], [num_order], [count_apply], [entry_type], [date])
                    VALUES(:id_prod, :version_prod, :num_order, :count_apply, :entry_type, GETDATE()
                    )
                    """
                )
                params = {
                    "id_prod": product_id,
                    "version_prod": actual_version,
                    "num_order": item.num_order,
                    "count_apply": item.count_apply,
                    "entry_type": item.entry_type,
                }
                session.execute(insert_sql, params)
                loaded_counter += 1
            except Exception as e:
                raise
        print(f"Загружено во временную таблицу #data записей: {loaded_counter}")
        return loaded_counter




    def _get_product_version(self, session, product_id):
        print("Начинается метод получения версии продукта из таблицы product")
        sql = text("""
        SELECT version_prod 
        FROM product
        WHERE id_prod =:product_id
        """)
        params = {'product_id': product_id}
        try:
            result = session.execute(sql, params)
            row = result.fetchone()
            if row:
                print(f"Получена версия продукта {row.version_prod}")
                return row.version_prod
            else:
                return 0
        except Exception as e:
            print(f"Ошибка {e}")


    def _extract_unique_orders(self, session):
        """"""
        print("Начинается метод извлечения уникальных заказов в #num_orders")
        sql = text(
            """
            INSERT INTO #num_orders
            SELECT DISTINCT [num_order] 
            FROM #data
            """
        )
        session.execute(sql)
        print("Извлекли уникальные заказы из #data в #num_orders")

    def _find_removed_items(self, session):
        """Метод находит позиции, которые были в плане, но удалены из новых данных"""
        print("Начинается метод поиска удаленных позиций из новых данных")
        sql = text("""
            -- Добавляем позиции, которые ушли из плана
            INSERT INTO #data (
                [id_prod], 
                [version_prod], 
                [num_order], 
                [count_apply], 
                [entry_type], 
                [date]
            )
            SELECT 
                t1.[id_prod],
                t1.[version_prod],
                t1.[num_order],
                0,
                1,
                GETDATE()
            FROM [kn51_2c_production_needs] AS t1
            LEFT JOIN #data AS t2 ON 
                t1.id_prod = t2.id_prod AND
                t1.version_prod = t2.version_prod AND
                t1.num_order = t2.num_order
            WHERE 
                t1.entry_type = 0  
                AND t1.num_order IN (SELECT num_order FROM #num_orders)
                AND t2.id_prod IS NULL
            """)

        session.execute(sql)
        print("Закончился метод поиска удаленных позиций")

    def _cleanup_old_uploads(self, session):
        """Метод удаляет старые незавершенные загрузки"""
        print("Начинается метод старых незавершенных загрузок")
        sql = text(
            """
            DELETE FROM [kn51_2c_production_needs]
            WHERE [entry_type] = 1
            AND [num_order] IN (SELECT [num_order] FROM #num_orders)
            """
        )
        result = session.execute(sql)
        deleted_count = result.rowcount
        if deleted_count > 0:
            print(f"Удалено старых или незавершенных записей: {deleted_count}")
        else:
            print("Старых или незавершенных записей не найдено")

        print("Конец метода удаления старых и незавершенных записей")
        return deleted_count


    def _insert_new_data(self, session):
        """Метод вставляет данные из временной таблицы #data в основную таблицу"""
        print("Начинается метод вставки данных из временной таблицы #data в основную")
        sql = text(
            """
            INSERT INTO [kn51_2c_production_needs]
            (
                [id_prod], 
                [version_prod], 
                [num_order], 
                [count_apply], 
                [entry_type], 
                [date]
            )
            SELECT 
                [id_prod],
                [version_prod],
                [num_order],
                [count_apply],
                [entry_type],
                [date]
            FROM #data
            """
        )
        result = session.execute(sql)
        inserted_count = result.rowcount
        print(f"Вставлено {inserted_count} записей")
        print("Конец метода вставки данных из временной таблицы в основную")
        return inserted_count

    def _update_entry_statuses(self, session):
        """Метод обновляет entry_type для всех записей заказов"""
        print("Начинается метод обновления поля entry_type")
        sql = text(
            """
            UPDATE [kn51_2c_production_needs]
            SET [entry_type] = [entry_type] - 1
            WHERE [num_order] IN (SELECT [num_order] FROM #num_orders)
            """
        )
        result = session.execute(sql)
        updated_count = result.rowcount
        print(f"Обновлено записей {updated_count} (entry_type - 1)")
        print(f"Конец метода обновления поля entry_type")
        return updated_count

uploader = ProductionNeedsService()




