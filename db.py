import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

#DATABASE_URL = "postgresql://username:password@localhost/dbname"
#DATABASE_URL = "postgresql://postgres:6400@localhost/time_management_db"



# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)

# Base = declarative_base()#




# Path to the database file in the same directory as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "time_management.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

# SQLite needs this for multithreaded Flask/Gunicorn
connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()