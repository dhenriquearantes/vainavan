from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.repositories.inscricao_repository import EventoRepository, EventoInscricaoRepository
from app.schemas.inscricao import (
    EventoCreate, EventoUpdate, EventoResponse,
    EventoInscricaoCreate, EventoInscricaoResponse
)

router = APIRouter(prefix="/inscricao", tags=["Inscrição"])

# =============== EVENTOS ===============


@router.get("/evento", response_model=List[EventoResponse])
def listar_eventos(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = Query(None),
    criador: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    repo = EventoRepository(db)
    eventos = repo.get_all(ativo=ativo, criador=criador)
    return eventos[skip:skip+limit]


@router.get("/evento/{id}", response_model=EventoResponse)
def obter_evento(id: int, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    evento = repo.get_by_id(id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return evento


@router.post("/evento", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    return repo.create(evento.model_dump())


@router.put("/evento/{id}", response_model=EventoResponse)
def atualizar_evento(id: int, evento: EventoUpdate, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    updated = repo.update(id, evento.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return updated


@router.delete("/evento/{id}")
def desativar_evento(id: int, db: Session = Depends(get_db)):
    repo = EventoRepository(db)
    if not repo.disable(id):
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return {"message": "Evento desativado com sucesso"}

# =============== INSCRIÇÕES ===============


@router.get("/evento/{id}/inscricoes", response_model=List[EventoInscricaoResponse])
def listar_inscricoes_evento(id: int, db: Session = Depends(get_db)):
    evento_repo = EventoRepository(db)
    evento = evento_repo.get_by_id(id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    inscricao_repo = EventoInscricaoRepository(db)
    return inscricao_repo.get_all_by_evento(id)


@router.post("/evento/{id}/inscricoes", response_model=EventoInscricaoResponse, status_code=status.HTTP_201_CREATED)
def inscrever_pessoa(id: int, inscricao: EventoInscricaoCreate, db: Session = Depends(get_db)):
    evento_repo = EventoRepository(db)
    evento = evento_repo.get_by_id(id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    inscricao_repo = EventoInscricaoRepository(db)
    return inscricao_repo.criar_inscricao(id, inscricao.id_pessoa)


@router.delete("/evento/{id}/inscricoes/{inscricao_id}")
def remover_inscricao(id: int, inscricao_id: int, db: Session = Depends(get_db)):
    evento_repo = EventoRepository(db)
    evento = evento_repo.get_by_id(id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    inscricao_repo = EventoInscricaoRepository(db)
    if not inscricao_repo.remover_inscricao(inscricao_id):
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")

    return {"message": "Inscrição removida com sucesso"}
