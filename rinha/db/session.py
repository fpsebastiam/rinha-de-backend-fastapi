from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rinha.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
