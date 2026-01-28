"""
Модуль для подключения к БД и работой с ней
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import settings
from contextlib import  asynccontextmanager

import anyio

engine = create_engine(settings.database_url, echo=False)


@asynccontextmanager
async def get_async_session():
    """
    Функция отдает сессию для работы с БД.
    Автоматически делает ролбэки и коммиты
    """
    session = scoped_session(sessionmaker(bind=engine))
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


async def async_execute(query):
    async with get_async_session() as session:
        result = session.execute(query)
        return result.fetchall()  # Возвращаем все строки как список