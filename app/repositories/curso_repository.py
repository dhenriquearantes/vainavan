from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.curso import Curso, CursoCampus


class CursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, ativo: Optional[bool] = None) -> List[Curso]:
        query = self.db.query(Curso)
        if ativo is not None:
            query = query.filter(Curso.bo_ativo == ativo)
        return query.all()

    def get_by_id(self, id: int) -> Optional[Curso]:
        return self.db.query(Curso).filter(Curso.id == id).first()

    def create(self, curso_data: dict) -> Curso:
        curso = Curso(**curso_data)
        self.db.add(curso)
        self.db.commit()
        self.db.refresh(curso)
        return curso

    def update(self, id: int, curso_data: dict) -> Optional[Curso]:
        curso = self.get_by_id(id)
        if not curso:
            return None
        for key, value in curso_data.items():
            if value is not None:
                setattr(curso, key, value)
        self.db.commit()
        self.db.refresh(curso)
        return curso

    def disable(self, id: int) -> bool:
        curso = self.get_by_id(id)
        if not curso:
            return False
        curso.bo_ativo = False
        self.db.commit()
        return True


class CursoCampusRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, campus: Optional[int] = None, curso: Optional[int] = None) -> List[CursoCampus]:
        query = self.db.query(CursoCampus)
        if campus is not None:
            query = query.filter(CursoCampus.id_campus == campus)
        if curso is not None:
            query = query.filter(CursoCampus.id_curso == curso)
        query = query.filter(CursoCampus.bo_ativo == True)
        return query.all()

    def get_by_id(self, id: int) -> Optional[CursoCampus]:
        return self.db.query(CursoCampus).filter(CursoCampus.id == id).first()

    def create(self, curso_campus_data: dict) -> CursoCampus:
        # Verificar se já existe a relação ativa
        existing = self.db.query(CursoCampus).filter(
            CursoCampus.id_campus == curso_campus_data["id_campus"],
            CursoCampus.id_curso == curso_campus_data["id_curso"],
            CursoCampus.bo_ativo == True
        ).first()
        
        if existing:
            return existing
        
        curso_campus = CursoCampus(**curso_campus_data)
        self.db.add(curso_campus)
        self.db.commit()
        self.db.refresh(curso_campus)
        return curso_campus

    def disable(self, id: int) -> bool:
        curso_campus = self.get_by_id(id)
        if not curso_campus:
            return False
        curso_campus.bo_ativo = False
        self.db.commit()
        return True

