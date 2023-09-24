from sqlalchemy import ARRAY, Column, String
from sqlalchemy.dialects.postgresql import UUID

from rinha.db.base_class import Base


class Pessoa(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    apelido = Column(String(length=32), unique=True, nullable=False, index=True)
    nascimento = Column(String)
    nome = Column(String(length=100))
    stack = Column(ARRAY(String(length=32)))
