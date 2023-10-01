from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from rinha.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_size=20, max_overflow=0)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
