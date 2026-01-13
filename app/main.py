from fastapi import FastAPI
from app.database import get_session
import  datetime
from sqlalchemy import text


app = FastAPI()




@app.get("/health")
def health_check():
    """Проверка здоровья приложения и подключения к БД"""
    with get_session() as session:
        try:
            session.execute(text("SELECT 1"))
            return {"status": "connected"}
        except Exception as e:
            return {"status": "disconnected"}