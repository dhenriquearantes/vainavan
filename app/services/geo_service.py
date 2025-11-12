import httpx
from typing import List, Dict, Optional

class IBGEService:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v1"
    
    @staticmethod
    async def get_estados() -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{IBGEService.BASE_URL}/localidades/estados")
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def get_municipios_by_estado(sigla_uf: str) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{IBGEService.BASE_URL}/localidades/estados/{sigla_uf}/municipios"
            )
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def get_municipio_by_id(id: int) -> Optional[Dict]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{IBGEService.BASE_URL}/localidades/municipios/{id}"
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None
    
    @staticmethod
    async def get_all_municipios() -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{IBGEService.BASE_URL}/localidades/municipios")
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    async def search_municipio(nome: str) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{IBGEService.BASE_URL}/localidades/municipios",
                params={"nome": nome}
            )
            response.raise_for_status()
            return response.json()

