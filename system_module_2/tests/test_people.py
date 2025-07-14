import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from system_module_1.db import Base  # usa el mismo Base
from system_module_1.models import Person
from system_module_2.server.server import app

TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    TestingSession = sessionmaker(bind=engine)

    # Crea todas las tablas sobre el Base correcto
    Base.metadata.create_all(bind=engine)

    session = TestingSession()

    # Carga un registro de prueba
    session.add(Person(
        id="nm0000045",
        name="Bruce Lee",
        birth_year=1940,
        death_year=1973,
        primary_professions="actor,producer"
    ))
    session.commit()

    yield session
    session.close()

def test_get_person(monkeypatch, db_session):
    # Monkeypatch SessionLocal usado en services/queries.py
    monkeypatch.setattr("system_module_2.server.services.queries.SessionLocal", lambda: db_session)

    client = TestClient(app)
    response = client.get("/people/Bruce Lee")
    assert response.status_code == 200
    assert "Bruce Lee was born in 1940" in response.json()["summary"]
