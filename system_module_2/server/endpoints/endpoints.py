from fastapi import APIRouter
from system_module_2.server.services.queries import get_person_info
from system_module_1.db import SessionLocal
from system_module_2.server.services.queries import get_film_info

router_films = APIRouter()
router_people = APIRouter()


@router_people.get("/{name}")  # Decorator: Add base logic for complete the function (Register endpoint)
async def read_person(name: str):  # Async: Server can manage multiple clients at the same time
    db = SessionLocal()
    result = get_person_info(name, db)
    db.close()
    if result:
        return {"summary": result}
    return {"error": "Person not found"}


@router_films.get("/{title}")  # Decorator: Add base logic for complete the function (Register endpoint)
async def read_film(title: str):  # Async: Server can manage multiple clients (tasks) at the same time
    db = SessionLocal()
    result = get_film_info(title, db)
    db.close()
    if result:
        return {"summary": result}
    return {"error": "Film not found"}
