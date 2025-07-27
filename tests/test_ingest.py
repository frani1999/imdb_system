from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from system_module_1.models import Base, Person, Title
from system_module_1.ingest import load_names, load_titles, interleaved_ingest
import gzip
import unittest  # Python standard library for Unit Testing (pytest is external library)

# Setup in-memory SQLite for testing
DATABASE_URL = "sqlite:///:memory:"


def create_fake_tsv(path, header, rows):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write(header + "\n")
        for row in rows:
            f.write(row + "\n")


def get_testing_session_local():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(bind=engine)
    db_session = testing_session_local()
    return db_session


class TestIngest(unittest.TestCase):
    def test_load_people(self):
        db_session = get_testing_session_local()
        _file = "name.basics.tsv.gz"
        create_fake_tsv(_file, "nconst\tprimaryName\tbirthYear\tdeathYear\tprimaryProfession\tknownForTitles", [
            "nm0000001\tBruce Lee\t1940\t1973\tactor,producer\ttt0000001",
        ])
        load_names(db_session, str(_file))
        result = db_session.query(Person).filter_by(name="Bruce Lee").first()
        db_session.close()
        self.assertNotEqual(result, None)
        self.assertEqual(result.birth_year, 1940)

    def test_load_titles(self):
        db_session = get_testing_session_local()
        _file = "title.basics.tsv.gz"
        create_fake_tsv(_file, "tconst\ttitleType\tprimaryTitle\toriginalTitle\tisAdult\tstartYear\tendYear\truntimeMinutes\tgenres", [
            "tt0000001\tdocumentary\tBlacksmith Scene\tLes forgerons\t0\t1895\t\\N\t1\tDocumentary",
        ])
        load_titles(db_session, str(_file))
        result = db_session.query(Title).filter_by(title="Blacksmith Scene").first()
        db_session.close()
        self.assertNotEqual(result, None)
        self.assertEqual(result.original_title, "Les forgerons")

    def test_interleaved_ingest(self):
        db_session = get_testing_session_local()
        file_name = "name.basics.tsv.gz"
        create_fake_tsv(file_name, "nconst\tprimaryName\tbirthYear\tdeathYear\tprimaryProfession\tknownForTitles", [
            "nm0000001\tBruce Lee\t1940\t1973\tactor,producer\ttt0000001",
        ])
        file_title = "title.basics.tsv.gz"
        create_fake_tsv(file_title, "tconst\ttitleType\tprimaryTitle\toriginalTitle\tisAdult\tstartYear\tendYear\truntimeMinutes\tgenres", [
            "tt0000001\tdocumentary\tBlacksmith Scene\tLes forgerons\t0\t1895\t\\N\t1\tDocumentary",
        ])
        interleaved_ingest(db_session, file_name, file_title)
        result_person = db_session.query(Person).filter_by(name="Bruce Lee").first()
        result_film = db_session.query(Title).filter_by(title="Blacksmith Scene").first()
        db_session.close()
        self.assertNotEqual(result_person, None)
        self.assertEqual(result_person.birth_year, 1940)
        self.assertNotEqual(result_film, None)
        self.assertEqual(result_film.original_title, "Les forgerons")
