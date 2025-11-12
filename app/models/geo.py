from sqlalchemy import Column, Integer, Text, Boolean
from app.core.database import Base

class Estado(Base):
    __tablename__ = "estados"
    __table_args__ = {"schema": "geo"}
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_uf = Column(Text, nullable=False)
    nome = Column(Text, nullable=False)
    uf = Column(Text, nullable=False)
    bo_ativo = Column(Boolean, default=True)

class Municipio(Base):
    __tablename__ = "municipio"
    __table_args__ = {"schema": "geo"}
    
    id = Column(Integer, primary_key=True, index=True)
    no_municipio = Column(Text, nullable=False)
    uf = Column(Text, nullable=False)
    cod_ibge = Column(Text, nullable=False)
    bo_ativo = Column(Boolean, default=True)

