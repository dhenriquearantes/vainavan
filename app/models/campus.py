from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Campus(Base):
    __tablename__ = "campus"
    __table_args__ = {"schema": "instituicao"}

    id = Column(Integer, primary_key=True, index=True)
    id_municipio = Column(Integer, ForeignKey("geo.municipio.id"), nullable=False)
    no_campus = Column(Text, nullable=False)
    bo_ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento
    municipio = relationship("Municipio", foreign_keys=[id_municipio])

