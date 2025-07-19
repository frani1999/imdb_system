from fastapi import APIRouter
from system_module_2.server.services.queries import get_film_info
from system_module_1.db import SessionLocal

router = APIRouter()


@router.get("/{title}")
async def read_film(title: str):
    db = SessionLocal()
    result = get_film_info(title, db)
    db.close()
    if result:
        return {"summary": result}
    return {"error": "Film not found"}
