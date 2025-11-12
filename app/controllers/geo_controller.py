from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.geo_service import IBGEService

router = APIRouter(prefix="/geolocalizacao", tags=["Geolocalização"])

@router.get("/estado")
async def listar_estados():
    try:
        estados = await IBGEService.get_estados()
        return [
            {
                "id": estado["id"],
                "sigla": estado["sigla"],
                "nome": estado["nome"],
                "regiao": estado["regiao"]["nome"] if "regiao" in estado else None
            }
            for estado in estados
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estados: {str(e)}")

@router.get("/municipio")
async def listar_municipios(
    estado: Optional[str] = Query(None, description="Sigla do estado (ex: SP, RJ, MG)"),
    nome: Optional[str] = Query(None, description="Nome do município para busca")
):
    try:
        if nome:
            municipios = await IBGEService.search_municipio(nome)
        elif estado:
            municipios = await IBGEService.get_municipios_by_estado(estado.upper())
        else:
            municipios = await IBGEService.get_all_municipios()
        
        return [
            {
                "id": m["id"],
                "nome": m["nome"],
                "microrregiao": m.get("microrregiao", {}).get("nome"),
                "mesorregiao": m.get("microrregiao", {}).get("mesorregiao", {}).get("nome"),
                "uf": m.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {}).get("sigla"),
                "regiao": m.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {}).get("regiao", {}).get("nome")
            }
            for m in municipios
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar municípios: {str(e)}")

@router.get("/municipio/{id}")
async def obter_municipio(id: int):
    try:
        municipio = await IBGEService.get_municipio_by_id(id)
        if not municipio:
            raise HTTPException(status_code=404, detail="Município não encontrado")
        
        return {
            "id": municipio["id"],
            "nome": municipio["nome"],
            "microrregiao": municipio.get("microrregiao", {}).get("nome"),
            "mesorregiao": municipio.get("microrregiao", {}).get("mesorregiao", {}).get("nome"),
            "uf": municipio.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {}).get("sigla"),
            "regiao": municipio.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {}).get("regiao", {}).get("nome")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar município: {str(e)}")

@router.get("/municipio/estado/{sigla_uf}")
async def listar_municipios_por_estado(sigla_uf: str):
    try:
        municipios = await IBGEService.get_municipios_by_estado(sigla_uf.upper())
        return [
            {
                "id": m["id"],
                "nome": m["nome"],
                "microrregiao": m.get("microrregiao", {}).get("nome"),
                "mesorregiao": m.get("microrregiao", {}).get("mesorregiao", {}).get("nome"),
                "uf": sigla_uf.upper()
            }
            for m in municipios
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar municípios: {str(e)}")
