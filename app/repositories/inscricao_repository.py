from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.models.inscricao import EventoInscricao
from app.models.rh import Pessoa


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

    def get_relatorio_pessoas_por_evento(self, id_evento: int) -> List[dict]:
        """
        Busca todas as pessoas cadastradas em um evento para relatório.
        Retorna uma lista de dicionários com dados da inscrição e da pessoa.
        """
        resultados = self.db.query(
            EventoInscricao.id.label('id_inscricao'),
            EventoInscricao.id_evento,
            EventoInscricao.created_at.label('data_inscricao'),
            Pessoa.id.label('pessoa_id'),
            Pessoa.nome.label('pessoa_nome'),
            Pessoa.email.label('pessoa_email'),
            Pessoa.dt_nascimento.label('pessoa_dt_nascimento'),
            Pessoa.bo_ativo.label('pessoa_bo_ativo')
        ).join(
            Pessoa, EventoInscricao.id_pessoa == Pessoa.id
        ).filter(
            EventoInscricao.id_evento == id_evento,
            EventoInscricao.bo_ativo == True
        ).order_by(
            Pessoa.nome
        ).all()

        # Transformar os resultados em dicionários estruturados
        relatorio = []
        for row in resultados:
            relatorio.append({
                'id_inscricao': row.id_inscricao,
                'id_evento': row.id_evento,
                'data_inscricao': row.data_inscricao,
                'pessoa': {
                    'id': row.pessoa_id,
                    'nome': row.pessoa_nome,
                    'email': row.pessoa_email,
                    'dt_nascimento': row.pessoa_dt_nascimento,
                    'bo_ativo': row.pessoa_bo_ativo
                }
            })
        
        return relatorio
