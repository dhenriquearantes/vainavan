from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.repositories.rh_repository import PessoaRepository
from app.schemas.rh import PessoaCreate, PessoaUpdate, PessoaResponse

router = APIRouter(prefix="/recursos-humanos", tags=["Recursos Humanos"])

@router.get("/pessoa", response_model=List[PessoaResponse])
def listar_pessoas_ativas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    pessoas = repo.get_all(ativo=True)
    return pessoas[skip:skip+limit]

@router.get("/pessoa/inativas")
def listar_pessoas_inativas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    pessoas = repo.get_all(ativo=False)
    total = len(pessoas)
    pessoas_slice = pessoas[skip:skip+limit]
    return {
        "pessoas": pessoas_slice,
        "total": total
    }

@router.get("/pessoa/todas")
def listar_todas_pessoas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    pessoas = repo.get_all(ativo=None)
    total = len(pessoas)
    pessoas_slice = pessoas[skip:skip+limit]
    return {"pessoas": pessoas_slice, "total": total}

@router.get("/pessoa/{id}", response_model=PessoaResponse)
def obter_pessoa(id: int, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    pessoa = repo.get_by_id(id)
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return pessoa

@router.post("/pessoa", response_model=PessoaResponse, status_code=status.HTTP_201_CREATED)
def criar_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    return repo.create(pessoa.model_dump())

@router.put("/pessoa/{id}", response_model=PessoaResponse)
def atualizar_pessoa(id: int, pessoa: PessoaUpdate, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    updated = repo.update(id, pessoa.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return updated

@router.delete("/pessoa/{id}")
def desativar_pessoa(id: int, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    if not repo.disable(id):
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return {"message": "Pessoa desativada com sucesso"}


@router.post("/pessoa/{id}/reativar", response_model=PessoaResponse)
def reativar_pessoa(id: int, db: Session = Depends(get_db)):
    repo = PessoaRepository(db)
    if not repo.enable(id):
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    pessoa = repo.get_by_id(id)
    return pessoa
