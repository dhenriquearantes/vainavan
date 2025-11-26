from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.inscricao import EventoInscricao


class EventoInscricaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_evento(self, id_evento: int) -> List[EventoInscricao]:
        return self.db.query(EventoInscricao).filter(
            EventoInscricao.id_evento == id_evento,
            EventoInscricao.bo_ativo == True
        ).all()

    def get_all_by_pessoa(self, id_pessoa: int) -> List[EventoInscricao]:
        return self.db.query(EventoInscricao).filter(
            EventoInscricao.id_pessoa == id_pessoa,
            EventoInscricao.bo_ativo == True
        ).all()

    def get_by_id(self, id: int) -> Optional[EventoInscricao]:
        return self.db.query(EventoInscricao).filter(EventoInscricao.id == id).first()

    def verificar_inscricao(self, id_evento: int, id_pessoa: int) -> Optional[EventoInscricao]:
        return self.db.query(EventoInscricao).filter(
            EventoInscricao.id_evento == id_evento,
            EventoInscricao.id_pessoa == id_pessoa,
            EventoInscricao.bo_ativo == True
        ).first()

    def criar_inscricao(self, id_evento: int, id_pessoa: int) -> EventoInscricao:
        # Verificar se já existe inscrição ativa
        existente = self.verificar_inscricao(id_evento, id_pessoa)
        if existente:
            return existente

        inscricao = EventoInscricao(id_evento=id_evento, id_pessoa=id_pessoa)
        self.db.add(inscricao)
        self.db.commit()
        self.db.refresh(inscricao)
        return inscricao

    def remover_inscricao(self, id: int) -> bool:
        inscricao = self.get_by_id(id)
        if not inscricao:
            return False
        inscricao.bo_ativo = False
        self.db.flush()
        self.db.commit()
        self.db.refresh(inscricao)
        return True
