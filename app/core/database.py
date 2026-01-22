import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from fastapi import Request, Depends
from typing import Generator

load_dotenv()

DATABASE_URL = os.getenv(
    "MASTER_DB_URL",
    "postgresql+psycopg://apple:admin123@localhost:5432/school_masters"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_public_db(request: Request) -> Generator:
    db = SessionLocal()
    try:
        schema = request.state.schema_name
        print(f"→ Setting search_path to schema: {schema}")
        db.execute(text(f'SET search_path TO "{schema}", public'))
        yield db
    finally:
        db.close()