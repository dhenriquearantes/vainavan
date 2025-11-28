from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class PessoaCreate(BaseModel):
    nome: str
    dt_nascimento: date
    email: EmailStr

class PessoaUpdate(BaseModel):
    nome: Optional[str] = None
    dt_nascimento: Optional[date] = None
    email: Optional[EmailStr] = None

class PessoaResponse(BaseModel):
    id: int
    nome: str
    dt_nascimento: date
    email: str
    bo_ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

