from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional


class EventoInscricaoPessoaResponse(BaseModel):
    id: int
    id_pessoa: int
    created_at: datetime
    bo_ativo: bool

    class Config:
        from_attributes = True


class EventoCreate(BaseModel):
    titulo: str
    descricao: str
    dt_inicio: date
    dt_fim: date
    id_criador: int


class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    dt_inicio: Optional[date] = None
    dt_fim: Optional[date] = None


class EventoResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    dt_inicio: date
    dt_fim: date
    id_criador: int
    created_at: datetime
    updated_at: Optional[datetime]
    bo_ativo: bool
    inscricoes: List[EventoInscricaoPessoaResponse] = []

    class Config:
        from_attributes = True

