from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Evento(Base):
    __tablename__ = "evento"
    __table_args__ = {"schema": "inscricao"}

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    dt_inicio = Column(Date, nullable=False)
    dt_fim = Column(Date, nullable=False)
    id_criador = Column(Integer, ForeignKey("rh.pessoa.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    bo_ativo = Column(Boolean, default=True)

    # Relacionamento
    inscricoes = relationship(
        "EventoInscricao", back_populates="evento", cascade="all, delete-orphan")


class EventoInscricao(Base):
    __tablename__ = "evento_inscricao"
    __table_args__ = {"schema": "inscricao"}

    id = Column(Integer, primary_key=True, index=True)
    id_evento = Column(Integer, ForeignKey(
        "inscricao.evento.id"), nullable=False)
    id_pessoa = Column(Integer, ForeignKey("rh.pessoa.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    bo_ativo = Column(Boolean, default=True)

    # Relacionamentos
    evento = relationship("Evento", back_populates="inscricoes")
