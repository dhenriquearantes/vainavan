from sqlalchemy import Column, Integer, Date, Boolean, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Pessoa(Base):
    __tablename__ = "pessoa"
    __table_args__ = {"schema": "rh"}
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(Text, nullable=False)
    dt_nascimento = Column(Date, nullable=False)
    email = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    bo_ativo = Column(Boolean, default=True)

