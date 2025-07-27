from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ----------------------------------------------------------------------------------------------------------------------
'''
Choose the DATABASE_URL for development or Production
    -.env.local -> contains the development DATABASE_URL
    -.env -> contains the production DATABASE_URL
'''

# Path to root directory of the project
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Path to env files
ENV_LOCAL_PATH = os.path.join(BASE_DIR, ".env.local")
ENV_PATH = os.path.join(BASE_DIR, ".env")

# .env.local (Development)
if os.path.exists(ENV_LOCAL_PATH):
    env_file = ENV_LOCAL_PATH
else:
    # .env (production / docker)
    env_file = ENV_PATH

print(env_file)

load_dotenv(env_file)

DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)
# ----------------------------------------------------------------------------------------------------------------------
'''
Create the database engine ("motor de base de datos")
-Choose database type (SQLite or PostGreSQL)
-echo: show log in terminal
-Future: Enables the modern mode of SQLAlchemy 2.0 (cleaner and more explicit).
'''
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
