from fastapi import FastAPI
from app.production_needs.router import router as product_needs_router


app = FastAPI()
app.include_router(product_needs_router)








# @app.get("/health")
# def health_check():
#     """Проверка здоровья приложения и подключения к БД"""
#     with get_session() as session:
#         try:
#             session.execute(text("SELECT 1"))
#             return {"status": "connected"}
#         except Exception as e:
#             return {"status": "disconnected"}