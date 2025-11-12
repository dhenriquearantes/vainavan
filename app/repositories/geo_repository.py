from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.geo import Municipio, Estado

class MunicipioRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Municipio]:
        return self.db.query(Municipio).filter(Municipio.bo_ativo == True).all()
    
    def get_by_id(self, id: int) -> Optional[Municipio]:
        return self.db.query(Municipio).filter(Municipio.id == id).first()
    
    def get_by_estado(self, id_estado: int) -> List[Municipio]:
        return self.db.query(Municipio).filter(Municipio.uf == id_estado).all()

class EstadoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Estado]:
        return self.db.query(Estado).filter(Estado.bo_ativo == True).all()
    
    def get_by_id(self, id: int) -> Optional[Estado]:
        return self.db.query(Estado).filter(Estado.id == id).first()

