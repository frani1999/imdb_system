import gzip
import csv
import os
import requests
from sqlalchemy.orm import Session
from system_module_1.db import SessionLocal, engine
from system_module_1.models import Base, Person, Title

IMDB_BASE_URL = "https://datasets.imdbws.com/"

FILES = {"name.basics.tsv.gz": "people", "title.basics.tsv.gz": "titles"}

TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp")
os.makedirs(TMP_DIR, exist_ok=True)


def download_file(filename: str) -> str:
    url = IMDB_BASE_URL + filename
    local_path = os.path.join(TMP_DIR, filename)
    if not os.path.exists(local_path):
        print(f"Downloading {filename} ...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    return local_path


def load_names(session: Session, filepath: str, batch_size: int = 10000):
    print("Loading names...")
    with gzip.open(filepath, mode='rt', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        batch = []
        count = 0

        for row in reader:
            birth = int(row['birthYear']) if row['birthYear'].isdigit() else None
            death = int(row['deathYear']) if row['deathYear'].isdigit() else None
            person = Person(
                id=row['nconst'],
                name=row['primaryName'],
                birth_year=birth,
                death_year=death,
                primary_professions=row['primaryProfession']
            )
            batch.append(person)
            count += 1

            if len(batch) >= batch_size:
                session.bulk_save_objects(batch)
                session.commit()
                print(f"   → {count} people inserted...")
                batch.clear()

        if batch:
            session.bulk_save_objects(batch)
            session.commit()
            print(f"   → {count} people inserted (final).")

    print(f"Number of people loaded: {count}")


def load_titles(session: Session, filepath: str, batch_size: int = 10000):
    print("Loading titles...")
    with gzip.open(filepath, mode='rt', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        batch = []
        count = 0

        for row in reader:
            year = int(row['startYear']) if row['startYear'].isdigit() else None
            title = Title(
                id=row['tconst'],
                title=row['primaryTitle'],
                original_title=row['originalTitle'],
                year=year,
                genres=row['genres'] if row['genres'] != '\\N' else None,
                type=row['titleType']
            )
            batch.append(title)
            count += 1

            if len(batch) >= batch_size:
                session.bulk_save_objects(batch)
                session.commit()
                print(f"   → {count} titles inserted...")
                batch.clear()

        if batch:
            session.bulk_save_objects(batch)
            session.commit()
            print(f"   → {count} titles inserted (final).")

    print(f"Number of titles loaded: {count}")


def setup_database():
    print("Restarting database...")
    Base.metadata.drop_all(bind=engine)  # Delete all database content
    Base.metadata.create_all(bind=engine)  # Create tables: Person, Title
    print("Database ready.")


def ingest_all():
    setup_database()
    db = SessionLocal()
    try:
        # Names
        people_file = download_file("name.basics.tsv.gz")
        load_names(db, people_file)

        # Titles
        titles_file = download_file("title.basics.tsv.gz")
        load_titles(db, titles_file)

        print("Ingest Completed.")
    finally:
        db.close()


def interleaved_ingest(db: Session, people_file: str, titles_file:str, batch_size: int = 10000):
    try:
        print("Starting interleaved ingestion...")

        with gzip.open(people_file, mode='rt', encoding='utf-8') as pf, \
             gzip.open(titles_file, mode='rt', encoding='utf-8') as tf:

            people_reader = csv.DictReader(pf, delimiter='\t')
            titles_reader = csv.DictReader(tf, delimiter='\t')

            people_batch = []
            titles_batch = []
            people_count = 0
            titles_count = 0

            while True:
                try:
                    person_row = next(people_reader)
                    birth = int(person_row['birthYear']) if person_row['birthYear'].isdigit() else None
                    death = int(person_row['deathYear']) if person_row['deathYear'].isdigit() else None
                    person = Person(
                        id=person_row['nconst'],
                        name=person_row['primaryName'],
                        birth_year=birth,
                        death_year=death,
                        primary_professions=person_row['primaryProfession']
                    )
                    people_batch.append(person)
                    people_count += 1
                except StopIteration:
                    person_row = None

                try:
                    title_row = next(titles_reader)
                    year = int(title_row['startYear']) if title_row['startYear'].isdigit() else None
                    title = Title(
                        id=title_row['tconst'],
                        title=title_row['primaryTitle'],
                        original_title=title_row['originalTitle'],
                        year=year,
                        genres=title_row['genres'] if title_row['genres'] != '\\N' else None,
                        type=title_row['titleType']
                    )
                    titles_batch.append(title)
                    titles_count += 1
                except StopIteration:
                    title_row = None

                # Save batches when they reach size
                if len(people_batch) >= batch_size:
                    db.bulk_save_objects(people_batch)
                    db.commit()
                    print(f"   → {people_count} people inserted...")
                    people_batch.clear()

                if len(titles_batch) >= batch_size:
                    db.bulk_save_objects(titles_batch)
                    db.commit()
                    print(f"   → {titles_count} titles inserted...")
                    titles_batch.clear()

                if person_row is None and title_row is None:
                    break

            # # Insert rest
            if people_batch:
                db.bulk_save_objects(people_batch)
                db.commit()
                print(f"   → {people_count} people inserted (final).")

            if titles_batch:
                db.bulk_save_objects(titles_batch)
                db.commit()
                print(f"   → {titles_count} titles inserted (final).")

        print("Interleaved ingestion completed.")

    finally:
        db.close()


if __name__ == "__main__":
    # Load first people, next titles
    # ingest_all()
    # Load interleaved between people and titles
    setup_database()
    db_ses = SessionLocal()
    people_fil = download_file("name.basics.tsv.gz")
    titles_fil = download_file("title.basics.tsv.gz")
    interleaved_ingest(db_ses, people_fil, titles_fil)
