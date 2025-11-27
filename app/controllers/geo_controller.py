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
        if estado:
            municipios = await IBGEService.get_municipios_by_estado(estado.upper())
        else:
            municipios = await IBGEService.get_all_municipios()
        
        # Filtrar por nome se fornecido (case-insensitive, busca parcial)
        if nome:
            nome_lower = nome.lower().strip()
            municipios = [
                m for m in municipios 
                if m.get("nome") and nome_lower in m.get("nome", "").lower()
            ]
        
        result = []
        for m in municipios:
            microrregiao = m.get("microrregiao") or {}
            mesorregiao = microrregiao.get("mesorregiao") or {}
            uf = mesorregiao.get("UF") or {}
            regiao = uf.get("regiao") or {}
            
            result.append({
                "id": m.get("id"),
                "nome": m.get("nome"),
                "microrregiao": microrregiao.get("nome"),
                "mesorregiao": mesorregiao.get("nome"),
                "uf": uf.get("sigla"),
                "regiao": regiao.get("nome")
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar municípios: {str(e)}")

@router.get("/municipio/{id}")
async def obter_municipio(id: int):
    try:
        municipio = await IBGEService.get_municipio_by_id(id)
        if not municipio:
            raise HTTPException(status_code=404, detail="Município não encontrado")
        
        microrregiao = municipio.get("microrregiao") or {}
        mesorregiao = microrregiao.get("mesorregiao") or {}
        uf = mesorregiao.get("UF") or {}
        regiao = uf.get("regiao") or {}
        
        return {
            "id": municipio.get("id"),
            "nome": municipio.get("nome"),
            "microrregiao": microrregiao.get("nome"),
            "mesorregiao": mesorregiao.get("nome"),
            "uf": uf.get("sigla"),
            "regiao": regiao.get("nome")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar município: {str(e)}")

@router.get("/municipio/estado/{sigla_uf}")
async def listar_municipios_por_estado(sigla_uf: str):
    try:
        municipios = await IBGEService.get_municipios_by_estado(sigla_uf.upper())
        result = []
        for m in municipios:
            microrregiao = m.get("microrregiao") or {}
            mesorregiao = microrregiao.get("mesorregiao") or {}
            
            result.append({
                "id": m.get("id"),
                "nome": m.get("nome"),
                "microrregiao": microrregiao.get("nome"),
                "mesorregiao": mesorregiao.get("nome"),
                "uf": sigla_uf.upper()
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar municípios: {str(e)}")
