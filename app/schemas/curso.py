from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CursoCreate(BaseModel):
    no_curso: str


class CursoUpdate(BaseModel):
    no_curso: Optional[str] = None


class CursoResponse(BaseModel):
    id: int
    no_curso: str
    bo_ativo: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CursoCampusCreate(BaseModel):
    id_campus: int
    id_curso: int


class CursoCampusResponse(BaseModel):
    id: int
    id_campus: int
    id_curso: int
    bo_ativo: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

