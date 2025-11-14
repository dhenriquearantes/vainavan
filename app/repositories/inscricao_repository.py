from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.inscricao import Evento, EventoInscricao


class EventoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, ativo: Optional[bool] = None, criador: Optional[int] = None) -> List[Evento]:
        query = self.db.query(Evento)
        if ativo is not None:
            query = query.filter(Evento.bo_ativo == ativo)
        if criador is not None:
            query = query.filter(Evento.id_criador == criador)
        return query.all()

    def get_by_id(self, id: int) -> Optional[Evento]:
        return self.db.query(Evento).filter(Evento.id == id).first()

    def create(self, evento_data: dict) -> Evento:
        evento = Evento(**evento_data)
        self.db.add(evento)
        self.db.commit()
        self.db.refresh(evento)
        return evento

    def update(self, id: int, evento_data: dict) -> Optional[Evento]:
        evento = self.get_by_id(id)
        if not evento:
            return None
        for key, value in evento_data.items():
            if value is not None:
                setattr(evento, key, value)
        self.db.commit()
        self.db.refresh(evento)
        return evento

    def disable(self, id: int) -> bool:
        evento = self.get_by_id(id)
        if not evento:
            return False
        evento.bo_ativo = False
        self.db.commit()
        return True


class EventoInscricaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_evento(self, id_evento: int) -> List[EventoInscricao]:
        return self.db.query(EventoInscricao).filter(
            EventoInscricao.id_evento == id_evento,
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
        self.db.commit()
        return True
