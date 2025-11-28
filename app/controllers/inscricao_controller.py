from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.repositories.evento_repository import EventoRepository
from app.repositories.inscricao_repository import EventoInscricaoRepository
from app.repositories.rh_repository import PessoaRepository
from app.schemas.inscricao import EventoInscricaoCreate, EventoInscricaoResponse, EventoInscricaoRelatorioResponse

router = APIRouter(prefix="/inscricao", tags=["Evento-Inscrição"])

@router.get("/evento/{id}/inscricoes", response_model=List[EventoInscricaoResponse])
def listar_inscricoes_evento(id: int, db: Session = Depends(get_db)):
    """Listar todas as inscrições de um evento"""
    evento_repo = EventoRepository(db)
    evento = evento_repo.get_by_id(id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )

    inscricao_repo = EventoInscricaoRepository(db)
    return inscricao_repo.get_all_by_evento(id)


@router.post("/evento/{id}/inscricoes", response_model=EventoInscricaoResponse, status_code=status.HTTP_201_CREATED)
def inscrever_pessoa(id: int, inscricao: EventoInscricaoCreate, db: Session = Depends(get_db)):
    """Inscrever uma pessoa em um evento"""
    evento_repo = EventoRepository(db)
    evento = evento_repo.get_by_id(id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    if not evento.bo_ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível inscrever em um evento desativado"
        )

    pessoa_repo = PessoaRepository(db)
    pessoa = pessoa_repo.get_by_id(inscricao.id_pessoa)
    if not pessoa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada"
        )
    
    if not pessoa.bo_ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível inscrever uma pessoa desativada"
        )

    inscricao_repo = EventoInscricaoRepository(db)
    return inscricao_repo.criar_inscricao(id, inscricao.id_pessoa)


@router.delete("/evento/{id}/inscricoes/{inscricao_id}")
def remover_inscricao(id: int, inscricao_id: int, db: Session = Depends(get_db)):
    """Remover inscrição de um evento"""
    evento_repo = EventoRepository(db)
    evento = evento_repo.get_by_id(id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )

    inscricao_repo = EventoInscricaoRepository(db)
    if not inscricao_repo.remover_inscricao(inscricao_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inscrição não encontrada"
        )

    return {"message": "Inscrição removida com sucesso"}


@router.get("/pessoa/{id_pessoa}/inscricoes", response_model=List[EventoInscricaoResponse])
def listar_inscricoes_pessoa(id_pessoa: int, db: Session = Depends(get_db)):
    """Listar todas as inscrições de uma pessoa"""
    inscricao_repo = EventoInscricaoRepository(db)
    return inscricao_repo.get_all_by_pessoa(id_pessoa)


@router.get("/evento/{id}/relatorio", response_model=List[EventoInscricaoRelatorioResponse])
def relatorio_pessoas_evento(id: int, db: Session = Depends(get_db)):
    """Relatório de todas as pessoas cadastradas em um evento"""
    evento_repo = EventoRepository(db)
    evento = evento_repo.get_by_id(id)
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado"
        )
    
    inscricao_repo = EventoInscricaoRepository(db)
    relatorio = inscricao_repo.get_relatorio_pessoas_por_evento(id)
    
    # Transformar os dicionários em objetos Pydantic
    return [
        EventoInscricaoRelatorioResponse(**item)
        for item in relatorio
    ]
