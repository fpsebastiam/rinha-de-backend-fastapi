from typing import Any, List
from uuid import UUID

from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from rinha import crud
from rinha.schemas.pessoa import PessoaCreate, Pessoa
from rinha.api import deps


app = FastAPI(title="Rinha de backend 2023")


@app.get("/pessoas/{pessoa_id}", response_model=Pessoa)
def read_pessoa(
    pessoa_id: UUID, 
    db: Session = Depends(deps.get_db),
) -> Any:
    users = crud.pessoa.get(db, id=pessoa_id)
    return users


@app.post("/pessoas", response_model=Pessoa)
def create_user(
    pessoa_in: PessoaCreate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create new user.
    """
    user = crud.pessoa.exists_by_apelido(db, apelido=pessoa_in.apelido)
    if user:
        raise HTTPException(
            status_code=422,
            detail="Unprocessable Entity",
        )
    user = crud.pessoa.create(db, obj_in=pessoa_in)
    return user


@app.get("/pessoas", response_model=List[Pessoa])
def search_pessoas(
    t: str = None,
    db: Session = Depends(deps.get_db),
) -> Any:
    return crud.pessoa.search(db, term=t)


@app.get("/contagem-pessoas", response_model=int)
def count_pessoas(
    db: Session = Depends(deps.get_db),
) -> Any:
    return crud.pessoa.count(db)


@app.get("/")
def read_root():
    return {"status": "ok"}