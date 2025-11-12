from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class PessoaCreate(BaseModel):
    nome: str
    dt_nascimento: date
    email: EmailStr

class PessoaResponse(BaseModel):
    id: int
    nome: str
    dt_nascimento: date
    email: str
    bo_ativo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

