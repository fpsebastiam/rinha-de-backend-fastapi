from typing import Generator

from rinha.db.session import SessionLocal


async def get_db() -> Generator:
    async with SessionLocal() as async_session:
        yield async_session
