from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Curso(Base):
    __tablename__ = "curso"
    __table_args__ = {"schema": "instituicao"}

    id = Column(Integer, primary_key=True, index=True)
    no_curso = Column(Text, nullable=False)
    bo_ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    cursos_campus = relationship("CursoCampus", back_populates="curso", cascade="all, delete-orphan")


class CursoCampus(Base):
    __tablename__ = "curso_campus"
    __table_args__ = {"schema": "instituicao"}

    id = Column(Integer, primary_key=True, index=True)
    id_campus = Column(Integer, ForeignKey("instituicao.campus.id"), nullable=False)
    id_curso = Column(Integer, ForeignKey("instituicao.curso.id"), nullable=False)
    bo_ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    campus = relationship("Campus", foreign_keys=[id_campus])
    curso = relationship("Curso", foreign_keys=[id_curso], back_populates="cursos_campus")

