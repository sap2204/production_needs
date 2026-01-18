"""
Модуль для подключения к БД и работой с ней
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from contextlib import contextmanager


engine = create_engine(settings.database_url)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)

@contextmanager
def get_session():
    """
    Функция отдает сессию для работы с БД.
    Автоматически делает ролбэки и коммиты
    """
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()