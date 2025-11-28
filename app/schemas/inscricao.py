from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class EventoInscricaoCreate(BaseModel):
    id_pessoa: int


class EventoInscricaoResponse(BaseModel):
    id: int
    id_evento: int
    id_pessoa: int
    created_at: datetime
    bo_ativo: bool

    class Config:
        from_attributes = True


class PessoaInscricaoRelatorio(BaseModel):
    """Dados da pessoa no relatório"""
    id: int
    nome: str
    email: str
    dt_nascimento: date
    bo_ativo: bool

    class Config:
        from_attributes = True


class EventoInscricaoRelatorioResponse(BaseModel):
    """Resposta do relatório de inscrições com dados completos da pessoa"""
    id_inscricao: int
    id_evento: int
    data_inscricao: datetime
    pessoa: PessoaInscricaoRelatorio

    class Config:
        from_attributes = True
