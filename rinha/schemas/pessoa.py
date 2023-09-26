from typing import List, Optional
import uuid

from pydantic import BaseModel, constr


BirthDate = constr(pattern=r'^\d{4}-\d{2}-\d{2}$')


class PessoaBase(BaseModel):
    apelido: constr(max_length=32)
    nome: constr(max_length=100)
    nascimento: BirthDate
    stack: Optional[List[constr(max_length=32)]] = None

    @property
    def stack(self) -> str:
        return ','.join(self.stack) if self.stack else None


class PessoaCreate(PessoaBase):
    pass


class PessoaInDBBase(PessoaBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# properties to return to client
class Pessoa(PessoaInDBBase):
    stack: Optional[str] = None
