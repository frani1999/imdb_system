from sqlalchemy import Column, String, Integer, Text
from system_module_1.db import Base


class Person(Base):
    __tablename__ = "people"

    id = Column(String, primary_key=True, index=True)  # nconst
    name = Column(String, index=True)
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)
    primary_professions = Column(Text, nullable=True)


class Title(Base):
    __tablename__ = "titles"

    id = Column(String, primary_key=True, index=True)  # tconst
    title = Column(String, index=True)
    original_title = Column(String)
    year = Column(Integer, nullable=True)
    genres = Column(String, nullable=True)
    type = Column(String, nullable=True)
