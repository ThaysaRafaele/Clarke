from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class SolucaoTipo(str, Enum):
    """Tipos de solução energética"""
    GD = "GD"
    MERCADO_LIVRE = "Mercado Livre"

class Fornecedor(BaseModel):
    """Modelo de fornecedor de energia"""
    id: str
    nome: str
    logo: str
    estado: str
    solucoes: List[SolucaoTipo]
    custo_kwh_gd: Optional[float] = None
    custo_kwh_ml: Optional[float] = None
    total_clientes: int
    avaliacao_media: float = Field(ge=0, le=5)

class Estado(BaseModel):
    """Modelo de estado com tarifa base"""
    uf: str
    nome: str
    tarifa_base_kwh: float  # R$ por kWh

class EconomiaFornecedor(BaseModel):
    """Resultado de economia para um fornecedor específico"""
    fornecedor: Fornecedor
    solucao: SolucaoTipo
    custo_atual: float
    custo_com_fornecedor: float
    economia_mensal: float
    economia_percentual: float
    economia_anual: float