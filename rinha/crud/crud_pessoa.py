from typing import Any, Dict, Optional, Union
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import any_, literal, func, select, or_, column

from rinha.crud.base import CRUDBase
from rinha.models.pessoa import Pessoa
from rinha.schemas.pessoa import PessoaCreate


class CRUDPessoa(CRUDBase[Pessoa, PessoaCreate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Pessoa]:
        return db.query(Pessoa).filter(Pessoa.email == email).first()

    def create(self, db: Session, *, obj_in: PessoaCreate) -> Pessoa:
        db_obj = Pessoa(
            id=uuid.uuid4(),
            nome=obj_in.nome,
            apelido=obj_in.apelido,
            nascimento=obj_in.nascimento,
            stack=obj_in.stack,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    def count(self, db: Session) -> int:
        return db.query(Pessoa).count()


    def search(self, db: Session, *, term: str) -> int:
        # TODO: this is very clunky, but will be replaced by an index
        subquery = select(func.count().label("count")).\
            select_from(func.unnest(Pessoa.stack).alias("stack_el")).\
                where(column("stack_el").ilike(f"%{term}%")).\
                    subquery().as_scalar()

        return db.query(Pessoa).filter(or_(
            Pessoa.nome.ilike(f"%{term}%"),
            Pessoa.apelido.ilike(f"%{term}%"),
            subquery > 0,
        )).limit(50).all()
    
    def exists_by_apelido(self, db: Session, *, apelido: str) -> bool:
        return db.query(Pessoa).filter(Pessoa.apelido == apelido).count() > 0


pessoa = CRUDPessoa(Pessoa)
