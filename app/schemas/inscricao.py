from pydantic import BaseModel
from datetime import datetime


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
