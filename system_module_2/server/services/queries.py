from system_module_1.models import Person, Title
from sqlalchemy.orm import Session


def get_person_info(name: str, db: Session) -> str | None:
    person = db.query(Person).filter(Person.name.ilike(name)).first()
    if person:
        summary = f"{person.name} was born in {person.birth_year or 'unknown'}"
        if person.primary_professions:
            summary += f" and was {person.primary_professions.replace(',', ' and ')}"
        return summary + "."
    return None


def get_film_info(title: str, db: Session) -> str | None:
    film = db.query(Title).filter(Title.title.ilike(title)).first()
    if film:
        return f"{film.title}, originally titled '{film.original_title}', is a {film.genres}."
    return None
