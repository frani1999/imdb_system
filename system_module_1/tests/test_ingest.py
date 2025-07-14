import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from system_module_1.models import Base, Person, Title
from system_module_1.ingest import load_names, load_titles
import gzip
import os

# Setup in-memory SQLite for testing
DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def create_fake_tsv(path, header, rows):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in rows:
            f.write(row + "\n")


def test_load_people(db_session, tmp_path):
    file = tmp_path / "name.basics.tsv.gz"
    create_fake_tsv(file, "nconst\tprimaryName\tbirthYear\tdeathYear\tprimaryProfession\tknownForTitles", [
        "nm0000001\tBruce Lee\t1940\t1973\tactor,producer\ttt0000001",
    ])
    load_names(db_session, str(file))
    result = db_session.query(Person).filter_by(name="Bruce Lee").first()
    assert result is not None
    assert result.birth_year == 1940


def test_load_titles(db_session, tmp_path):
    file = tmp_path / "title.basics.tsv.gz"
    create_fake_tsv(file, "tconst\ttitleType\tprimaryTitle\toriginalTitle\tisAdult\tstartYear\tendYear\truntimeMinutes\tgenres", [
        "tt0000001\tdocumentary\tBlacksmith Scene\tLes forgerons\t0\t1895\t\\N\t1\tDocumentary",
    ])
    load_titles(db_session, str(file))
    result = db_session.query(Title).filter_by(title="Blacksmith Scene").first()
    assert result is not None
    assert result.original_title == "Les forgerons"
