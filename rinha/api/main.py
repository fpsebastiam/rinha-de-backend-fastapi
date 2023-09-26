from typing import Any, List, Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Response
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
    user = crud.pessoa.get(db, id=pessoa_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/pessoas", status_code=201)
def create_user(
    pessoa_in: PessoaCreate,
    response: Response,
    db: Session = Depends(deps.get_db),
) -> Any:
    user = crud.pessoa.exists_by_apelido(db, apelido=pessoa_in.apelido)
    if user:
        raise HTTPException(
            status_code=422,
            detail="Unprocessable Entity",
        )
    user = crud.pessoa.create(db, obj_in=pessoa_in)
    response.headers["Location"] = f"/pessoas/{user.id}"


@app.get("/pessoas", response_model=List[Pessoa])
def search_pessoas(
    t: Optional[str] = None,
    db: Session = Depends(deps.get_db),
) -> Any:
    if t is None:
        raise HTTPException(status_code=400, detail="Missing search term 't'")
    return crud.pessoa.search(db, term=t)


@app.get("/contagem-pessoas", response_model=int)
def count_pessoas(
    db: Session = Depends(deps.get_db),
) -> Any:
    return crud.pessoa.count(db)


@app.get("/")
def read_root():
    return {"status": "ok"}
