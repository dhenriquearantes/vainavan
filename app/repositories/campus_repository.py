from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.campus import Campus
from app.models.geo import Municipio
from app.repositories.geo_repository import MunicipioRepository
from app.services.geo_service import IBGEService


class CampusRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self, 
        ativo: Optional[bool] = None, 
        municipio: Optional[int] = None,
        nome: Optional[str] = None
    ) -> List[Campus]:
        query = self.db.query(Campus)
        if ativo is not None:
            query = query.filter(Campus.bo_ativo == ativo)
        if municipio is not None:
            query = query.filter(Campus.id_municipio == municipio)
        if nome:
            # Busca parcial (case-insensitive)
            query = query.filter(Campus.no_campus.ilike(f"%{nome}%"))
        return query.all()
    
    def get_by_estado(self, uf: str, ativo: Optional[bool] = None) -> List[Campus]:
        """Busca campus por estado (UF) através do relacionamento com município"""
        query = self.db.query(Campus).join(Municipio, Campus.id_municipio == Municipio.id)
        query = query.filter(Municipio.uf == uf.upper())
        if ativo is not None:
            query = query.filter(Campus.bo_ativo == ativo)
        return query.all()
    
    def get_by_municipio(self, cod_ibge: int, ativo: Optional[bool] = None) -> List[Campus]:
        """Busca campus por município (código IBGE)"""
        query = self.db.query(Campus).filter(Campus.id_municipio == cod_ibge)
        if ativo is not None:
            query = query.filter(Campus.bo_ativo == ativo)
        return query.all()

    def get_by_id(self, id: int) -> Optional[Campus]:
        return self.db.query(Campus).filter(Campus.id == id).first()

    async def _get_or_create_municipio(self, cod_ibge: str) -> int:
        """Busca ou cria município pelo código IBGE. Retorna o código IBGE (que é o ID)."""
        municipio_repo = MunicipioRepository(self.db)
        
        # Verificar se o município já existe no banco (ID = código IBGE)
        municipio = municipio_repo.get_by_cod_ibge(cod_ibge)
        
        if not municipio:
            # Buscar o município na API do IBGE
            municipio_ibge = await IBGEService.get_municipio_by_id(int(cod_ibge))
            if not municipio_ibge:
                raise ValueError(f"Município com código IBGE {cod_ibge} não encontrado na API do IBGE")
            
            # Extrair dados do município
            microrregiao = municipio_ibge.get("microrregiao") or {}
            mesorregiao = microrregiao.get("mesorregiao") or {}
            uf = mesorregiao.get("UF") or {}
            
            # Criar o município no banco (ID será o código IBGE)
            municipio_data = {
                "no_municipio": municipio_ibge.get("nome", ""),
                "uf": uf.get("sigla", ""),
                "cod_ibge": cod_ibge,
                "bo_ativo": True
            }
            municipio = municipio_repo.create(municipio_data)
        
        # Retorna o código IBGE que é o próprio ID
        return municipio.id
    
    async def create(self, campus_data: dict) -> Campus:
        # O id_municipio recebido é o código IBGE (que também é o ID na tabela)
        cod_ibge = str(campus_data["id_municipio"])
        
        # Buscar ou criar município (não cria se já existir)
        id_municipio = await self._get_or_create_municipio(cod_ibge)
        
        # Usar o código IBGE como id_municipio (que é o ID da tabela)
        campus_data["id_municipio"] = id_municipio
        
        campus = Campus(**campus_data)
        self.db.add(campus)
        self.db.commit()
        self.db.refresh(campus)
        return campus

    async def update(self, id: int, campus_data: dict) -> Optional[Campus]:
        campus = self.get_by_id(id)
        if not campus:
            return None
        
        # Se id_municipio for fornecido, precisa ser tratado como código IBGE
        if "id_municipio" in campus_data and campus_data["id_municipio"] is not None:
            cod_ibge = str(campus_data["id_municipio"])
            id_municipio_local = await self._get_or_create_municipio(cod_ibge)
            campus_data["id_municipio"] = id_municipio_local
        
        for key, value in campus_data.items():
            if value is not None:
                setattr(campus, key, value)
        self.db.commit()
        self.db.refresh(campus)
        return campus

    def disable(self, id: int) -> bool:
        campus = self.get_by_id(id)
        if not campus:
            return False
        campus.bo_ativo = False
        self.db.commit()
        return True

