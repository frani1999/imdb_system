from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from system_module_1.models import Base, Person, Title
from system_module_1.ingest import load_names, load_titles
import gzip
import unittest

# Setup in-memory SQLite for testing
DATABASE_URL = "sqlite:///:memory:"


def create_fake_tsv(path, header, rows):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in rows:
            f.write(row + "\n")


class TestIngest(unittest.TestCase):
    def test_load_people(self):
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        TestingSessionLocal = sessionmaker(bind=engine)
        db_session = TestingSessionLocal()
        file = "name.basics.tsv.gz"
        create_fake_tsv(file, "nconst\tprimaryName\tbirthYear\tdeathYear\tprimaryProfession\tknownForTitles", [
            "nm0000001\tBruce Lee\t1940\t1973\tactor,producer\ttt0000001",
        ])
        load_names(db_session, str(file))
        result = db_session.query(Person).filter_by(name="Bruce Lee").first()
        db_session.close()
        self.assertNotEqual(result, None)
        self.assertEqual(result.birth_year, 1940)

    def test_load_titles(self):
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        TestingSessionLocal = sessionmaker(bind=engine)
        db_session = TestingSessionLocal()
        file = "title.basics.tsv.gz"
        create_fake_tsv(file, "tconst\ttitleType\tprimaryTitle\toriginalTitle\tisAdult\tstartYear\tendYear\truntimeMinutes\tgenres", [
            "tt0000001\tdocumentary\tBlacksmith Scene\tLes forgerons\t0\t1895\t\\N\t1\tDocumentary",
        ])
        load_titles(db_session, str(file))
        result = db_session.query(Title).filter_by(title="Blacksmith Scene").first()
        db_session.close()
        self.assertNotEqual(result, None)
        self.assertEqual(result.original_title, "Les forgerons")
