from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.repositories.curso_repository import CursoRepository
from app.schemas.curso import CursoCreate, CursoUpdate, CursoResponse

router = APIRouter(prefix="/instituicao/curso", tags=["Curso"])


@router.get("", response_model=List[CursoResponse])
def listar_cursos(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    repo = CursoRepository(db)
    cursos = repo.get_all(ativo=ativo)
    return cursos[skip:skip+limit]


@router.get("/{id}", response_model=CursoResponse)
def obter_curso(id: int, db: Session = Depends(get_db)):
    repo = CursoRepository(db)
    curso = repo.get_by_id(id)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    return curso


@router.post("", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def criar_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    repo = CursoRepository(db)
    return repo.create(curso.model_dump())


@router.put("/{id}", response_model=CursoResponse)
def atualizar_curso(id: int, curso: CursoUpdate, db: Session = Depends(get_db)):
    repo = CursoRepository(db)
    updated = repo.update(id, curso.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    return updated


@router.delete("/{id}")
def desativar_curso(id: int, db: Session = Depends(get_db)):
    repo = CursoRepository(db)
    if not repo.disable(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )
    return {"message": "Curso desativado com sucesso"}

