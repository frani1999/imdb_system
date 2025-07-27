from fastapi import APIRouter
from system_module_2.server.services.queries import get_film_info
from system_module_1.db import SessionLocal

router = APIRouter()


@router.get("/{title}")  # Decorator: Add base logic for complete the function (Register endpoint)
async def read_film(title: str):  # Async: Server can manage multiple clients (tasks) at the same time
    db = SessionLocal()
    result = get_film_info(title, db)
    db.close()
    if result:
        return {"summary": result}
    return {"error": "Film not found"}
