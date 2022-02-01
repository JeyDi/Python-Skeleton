# define postgres sqlalchemy engine connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.src.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)