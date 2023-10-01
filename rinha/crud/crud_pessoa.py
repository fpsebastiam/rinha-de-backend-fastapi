import uuid
from uuid import UUID
from typing import Optional
import logging

from sqlalchemy import text, select, func
from sqlalchemy.orm import Session

from rinha.crud.base import CRUDBase
from rinha.models.pessoa import Pessoa
from rinha.schemas.pessoa import PessoaCreate


logger = logging.getLogger(__name__)

class CRUDPessoa(CRUDBase[Pessoa, PessoaCreate]):
    async def get(self, db: Session, *, id: UUID) -> Optional[Pessoa]:
        pessoa = await db.get(Pessoa, str(id))
        return pessoa

    async def create(self, db: Session, *, obj_in: PessoaCreate) -> Pessoa:
        db_obj = Pessoa(
            id=uuid.uuid4(),
            nome=obj_in.nome,
            apelido=obj_in.apelido,
            nascimento=obj_in.nascimento,
            stack=str(obj_in.stack),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    

    async def count(self, db: Session) -> int:
        pessoa_count = await db.scalar(select(func.count(Pessoa.id)))
        return pessoa_count


    async def search(self, db: Session, *, term: str) -> int:
        query = select(Pessoa).filter(
            text(f"busca like '%{term}%'")
        ).limit(50)
        matching_pessoas = await db.execute(query)
        return [r[0] for r in matching_pessoas.all()]


pessoa = CRUDPessoa(Pessoa)
