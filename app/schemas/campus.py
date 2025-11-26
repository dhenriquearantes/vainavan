from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CampusCreate(BaseModel):
    id_municipio: int  # ID do município na API do IBGE (cod_ibge)
    no_campus: str


class CampusUpdate(BaseModel):
    id_municipio: Optional[int] = None
    no_campus: Optional[str] = None


class CampusResponse(BaseModel):
    id: int
    id_municipio: int
    no_campus: str
    bo_ativo: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

