from fastapi import APIRouter
from system_module_2.server.services.queries import get_person_info
from system_module_1.db import SessionLocal

router = APIRouter()


@router.get("/{name}")
async def read_person(name: str):
    db = SessionLocal()
    result = get_person_info(name, db)
    db.close()
    if result:
        return {"summary": result}
    return {"error": "Person not found"}
