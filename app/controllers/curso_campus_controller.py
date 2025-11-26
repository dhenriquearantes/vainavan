from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.repositories.curso_repository import CursoCampusRepository
from app.schemas.curso import CursoCampusCreate, CursoCampusResponse

router = APIRouter(prefix="/instituicao/curso-campus", tags=["Curso-Campus"])


@router.get("", response_model=List[CursoCampusResponse])
def listar_curso_campus(
    skip: int = 0,
    limit: int = 100,
    campus: Optional[int] = Query(None, description="ID do campus"),
    curso: Optional[int] = Query(None, description="ID do curso"),
    db: Session = Depends(get_db)
):
    repo = CursoCampusRepository(db)
    curso_campus_list = repo.get_all(campus=campus, curso=curso)
    return curso_campus_list[skip:skip+limit]


@router.post("", response_model=CursoCampusResponse, status_code=status.HTTP_201_CREATED)
def criar_curso_campus(curso_campus: CursoCampusCreate, db: Session = Depends(get_db)):
    repo = CursoCampusRepository(db)
    return repo.create(curso_campus.model_dump())

