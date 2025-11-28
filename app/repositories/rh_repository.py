from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime, timezone, date
from app.models.rh import Pessoa

class PessoaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, ativo: Optional[bool] = None) -> List[Pessoa]:
        query = self.db.query(Pessoa)
        if ativo is not None:
            query = query.filter(Pessoa.bo_ativo == ativo)
        return query.all()
    
    def get_by_id(self, id: int) -> Optional[Pessoa]:
        return self.db.query(Pessoa).filter(Pessoa.id == id).first()
    
    def create(self, pessoa_data: dict) -> Pessoa:
        pessoa = Pessoa(**pessoa_data)
        self.db.add(pessoa)
        self.db.commit()
        self.db.refresh(pessoa)
        return pessoa
    
    def update(self, id: int, pessoa_data: dict) -> Optional[Pessoa]:
        pessoa = self.get_by_id(id)
        if not pessoa:
            return None
        for key, value in pessoa_data.items():
            if value is not None:
                setattr(pessoa, key, value)
        pessoa.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(pessoa)
        return pessoa
    
    def disable(self, id: int) -> bool:
        pessoa = self.get_by_id(id)
        if not pessoa:
            return False
        pessoa.bo_ativo = False
        self.db.commit()
        return True
    
    def enable(self, id: int) -> bool:
        pessoa = self.get_by_id(id)
        if not pessoa:
            return False
        pessoa.bo_ativo = True
        pessoa.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        return True
