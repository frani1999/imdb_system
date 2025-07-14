from fastapi import APIRouter
from system_module_2.server.services.queries import get_person_info

router = APIRouter()


@router.get("/{name}")
def read_person(name: str):
    result = get_person_info(name)
    if result:
        return {"summary": result}
    return {"error": "Person not found"}
