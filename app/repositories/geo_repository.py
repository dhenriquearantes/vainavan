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
    
    def get_by_cod_ibge(self, cod_ibge: str) -> Optional[Municipio]:
        # Como o ID é o código IBGE, buscar diretamente pelo ID
        try:
            return self.db.query(Municipio).filter(Municipio.id == int(cod_ibge)).first()
        except ValueError:
            return None
    
    def get_by_estado(self, id_estado: int) -> List[Municipio]:
        return self.db.query(Municipio).filter(Municipio.uf == id_estado).all()
    
    def create(self, municipio_data: dict) -> Municipio:
        # O ID do município é o código IBGE (não auto-incremento)
        cod_ibge = municipio_data.pop("cod_ibge")
        municipio_data["id"] = int(cod_ibge)  # Define o ID como o código IBGE
        municipio_data["cod_ibge"] = cod_ibge  # Mantém cod_ibge também para referência
        
        # Verificar se já existe antes de criar
        existing = self.get_by_id(int(cod_ibge))
        if existing:
            return existing  # Retorna o existente, não cria duplicado
        
        municipio = Municipio(**municipio_data)
        self.db.add(municipio)
        try:
            self.db.commit()
            self.db.refresh(municipio)
        except Exception:
            self.db.rollback()
            # Se der erro (provavelmente já existe), buscar novamente
            return self.get_by_id(int(cod_ibge))
        return municipio

class EstadoRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Estado]:
        return self.db.query(Estado).filter(Estado.bo_ativo == True).all()
    
    def get_by_id(self, id: int) -> Optional[Estado]:
        return self.db.query(Estado).filter(Estado.id == id).first()

