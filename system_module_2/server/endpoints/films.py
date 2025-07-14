from fastapi import APIRouter
from system_module_2.server.services.queries import get_film_info

router = APIRouter()


@router.get("/{title}")
def read_film(title: str):
    result = get_film_info(title)
    if result:
        return {"summary": result}
    return {"error": "Film not found"}
