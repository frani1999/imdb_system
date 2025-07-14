from system_module_1.models import Person, Title
from system_module_1.db import SessionLocal


def get_person_info(name: str) -> str | None:
    db = SessionLocal()
    person = db.query(Person).filter(Person.name.ilike(name)).first()  # f"%{name}%"
    db.close()
    if person:
        summary = f"{person.name} was born in {person.birth_year or 'unknown'}"
        if person.primary_professions:
            summary += f" and was {person.primary_professions.replace(',', ' and ')}"
        return summary + "."
    return None


def get_film_info(title: str) -> str | None:
    db = SessionLocal()
    film = db.query(Title).filter(Title.title.ilike(title)).first()  # f"%{title}%"
    db.close()
    if film:
        return f"{film.title}, originally titled '{film.original_title}', is a {film.type}."
    return None
