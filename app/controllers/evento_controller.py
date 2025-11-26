from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.repositories.evento_repository import EventoRepository
from app.schemas.evento import EventoCreate, EventoUpdate, EventoResponse

router = APIRouter(prefix="/evento", tags=["Evento"])


@router.get("", response_model=List[EventoResponse])
def listar_eventos(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = Query(True),
    criador: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    repo = EventoRepository(db)
    eventos = repo.get_all(ativo=ativo, criador=criador)
    return eventos[skip:skip+limit]


@router.get("/{id}", response_model=EventoResponse)
def obter_evento(id: int, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    evento = repo.get_by_id(id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    return evento


@router.post("", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    return repo.create(evento.model_dump())


@router.put("/{id}", response_model=EventoResponse)
def atualizar_evento(id: int, evento: EventoUpdate, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    updated = repo.update(id, evento.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    return updated


@router.delete("/{id}")
def desativar_evento(id: int, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    if not repo.disable(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    return {"message": "Evento desativado com sucesso"}

