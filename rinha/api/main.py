from typing import Any, List, Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from rinha import crud
from rinha.api import deps
from rinha.db.cache import Cache
from rinha.schemas.pessoa import Pessoa, PessoaCreate

app = FastAPI(title="Rinha de backend 2023")


@app.on_event("startup")
def startup():
    global cache
    cache = Cache()


@app.get("/pessoas/{pessoa_id}", response_model=Pessoa)
async def read_pessoa(
    pessoa_id: UUID, 
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    if cached_user := await cache.get(f"pessoa:{pessoa_id}"):
        return cached_user
    
    if db_user := await crud.pessoa.get(db, id=pessoa_id):
        return db_user
    
    raise HTTPException(status_code=404, detail="User not found")



@app.post("/pessoas", status_code=201)
async def create_user(
    pessoa_in: PessoaCreate,
    response: Response,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    if await cache.get(f"nickname:{pessoa_in.apelido}"):
        raise HTTPException(
            status_code=422,
            detail="Unprocessable Entity",
        )

    user = await crud.pessoa.create(db, obj_in=pessoa_in)
    await cache.set(f"nickname:{user.apelido}", "1")
    # TODO: make the id insertion transparent
    pessoa_dict = {**pessoa_in.model_dump(), "id": str(user.id)}
    pessoa_dict["stack"] = user.stack
    await cache.set(f"pessoa:{user.id}", pessoa_dict)

    response.headers["Location"] = f"/pessoas/{user.id}"


@app.get("/pessoas", response_model=List[Pessoa])
async def search_pessoas(
    t: Optional[str] = None,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    if t is None:
        raise HTTPException(status_code=400, detail="Missing search term 't'")
    search_results = await crud.pessoa.search(db, term=t)
    return search_results

@app.get("/contagem-pessoas", response_model=int)
async def count_pessoas(
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    person_count = await crud.pessoa.count(db)
    return person_count


@app.get("/")
def read_root():
    return {"status": "ok"}
