from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from rinha.db.base_class import Base


class Pessoa(Base):
    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    apelido = Column(String(length=32))
    nascimento = Column(String(length=10), nullable=False)
    nome = Column(String(length=100))
    stack = Column(String(length=1024))
