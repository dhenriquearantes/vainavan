from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.repositories.campus_repository import CampusRepository
from app.schemas.campus import CampusCreate, CampusUpdate, CampusResponse

router = APIRouter(prefix="/instituicao/campus", tags=["Campus"])


@router.get("", response_model=List[CampusResponse])
def listar_campus(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = Query(None),
    municipio: Optional[int] = Query(None, description="Código IBGE do município"),
    nome: Optional[str] = Query(None, description="Nome do campus para busca parcial"),
    db: Session = Depends(get_db)
):
    repo = CampusRepository(db)
    campus_list = repo.get_all(ativo=ativo, municipio=municipio, nome=nome)
    return campus_list[skip:skip+limit]


@router.get("/estado/{uf}", response_model=List[CampusResponse])
def listar_campus_por_estado(
    uf: str,
    ativo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Lista campus por estado (UF)"""
    repo = CampusRepository(db)
    campus_list = repo.get_by_estado(uf.upper(), ativo=ativo)
    if not campus_list:
        return []
    return campus_list


@router.get("/municipio/{cod_ibge}", response_model=List[CampusResponse])
def listar_campus_por_municipio(
    cod_ibge: int,
    ativo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Lista campus por município (código IBGE)"""
    repo = CampusRepository(db)
    campus_list = repo.get_by_municipio(cod_ibge, ativo=ativo)
    if not campus_list:
        return []
    return campus_list


@router.get("/{id}", response_model=CampusResponse)
def obter_campus(id: int, db: Session = Depends(get_db)):
    """Obter campus por ID"""
    repo = CampusRepository(db)
    campus = repo.get_by_id(id)
    if not campus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campus não encontrado"
        )
    return campus


@router.post("", response_model=CampusResponse, status_code=status.HTTP_201_CREATED)
async def criar_campus(campus: CampusCreate, db: Session = Depends(get_db)):
    repo = CampusRepository(db)
    try:
        return await repo.create(campus.model_dump())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar campus: {str(e)}"
        )


@router.put("/{id}", response_model=CampusResponse)
async def atualizar_campus(id: int, campus: CampusUpdate, db: Session = Depends(get_db)):
    repo = CampusRepository(db)
    try:
        updated = await repo.update(id, campus.model_dump(exclude_unset=True))
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campus não encontrado"
            )
        return updated
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar campus: {str(e)}"
        )


@router.delete("/{id}")
def desativar_campus(id: int, db: Session = Depends(get_db)):
    repo = CampusRepository(db)
    if not repo.disable(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campus não encontrado"
        )
    return {"message": "Campus desativado com sucesso"}

