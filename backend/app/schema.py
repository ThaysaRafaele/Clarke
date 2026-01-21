import strawberry
from typing import List, Optional
from app.models import SolucaoTipo, EconomiaFornecedor, Fornecedor, Estado
from app.data import ESTADOS, get_estado, get_fornecedores_por_estado


@strawberry.type
class FornecedorType:
    id: str
    nome: str
    logo: str
    estado: str
    solucoes: List[str]
    custo_kwh_gd: Optional[float]
    custo_kwh_ml: Optional[float]
    total_clientes: int
    avaliacao_media: float


@strawberry.type
class EstadoType:
    uf: str
    nome: str
    tarifa_base_kwh: float


@strawberry.type
class EconomiaFornecedorType:
    fornecedor: FornecedorType
    solucao: str
    custo_atual: float
    custo_com_fornecedor: float
    economia_mensal: float
    economia_percentual: float
    economia_anual: float


@strawberry.type
class SolucaoDisponivel:
    tipo: str
    fornecedores: List[FornecedorType]
    melhor_economia: Optional[EconomiaFornecedorType]


@strawberry.type
class ResultadoSimulacao:
    estado: EstadoType
    consumo_kwh: float
    custo_atual_mensal: float
    custo_atual_anual: float
    solucoes_disponiveis: List[SolucaoDisponivel]
    total_fornecedores: int


def calcular_economia(
    fornecedor: Fornecedor,
    solucao: SolucaoTipo,
    consumo_kwh: float,
    tarifa_base: float
) -> EconomiaFornecedor:
    custo_atual = consumo_kwh * tarifa_base
    
    custo_kwh_fornecedor = (
        fornecedor.custo_kwh_gd if solucao == SolucaoTipo.GD 
        else fornecedor.custo_kwh_ml
    ) or 0
    
    custo_com_fornecedor = consumo_kwh * custo_kwh_fornecedor
    economia_mensal = custo_atual - custo_com_fornecedor
    economia_percentual = (economia_mensal / custo_atual * 100) if custo_atual > 0 else 0
    economia_anual = economia_mensal * 12
    
    return EconomiaFornecedor(
        fornecedor=fornecedor,
        solucao=solucao,
        custo_atual=custo_atual,
        custo_com_fornecedor=custo_com_fornecedor,
        economia_mensal=economia_mensal,
        economia_percentual=economia_percentual,
        economia_anual=economia_anual
    )


def converter_fornecedor(fornecedor: Fornecedor) -> FornecedorType:
    return FornecedorType(
        id=fornecedor.id,
        nome=fornecedor.nome,
        logo=fornecedor.logo,
        estado=fornecedor.estado,
        solucoes=[s.value for s in fornecedor.solucoes],
        custo_kwh_gd=fornecedor.custo_kwh_gd,
        custo_kwh_ml=fornecedor.custo_kwh_ml,
        total_clientes=fornecedor.total_clientes,
        avaliacao_media=fornecedor.avaliacao_media
    )


def converter_economia(economia: EconomiaFornecedor) -> EconomiaFornecedorType:
    return EconomiaFornecedorType(
        fornecedor=converter_fornecedor(economia.fornecedor),
        solucao=economia.solucao.value,
        custo_atual=round(economia.custo_atual, 2),
        custo_com_fornecedor=round(economia.custo_com_fornecedor, 2),
        economia_mensal=round(economia.economia_mensal, 2),
        economia_percentual=round(economia.economia_percentual, 2),
        economia_anual=round(economia.economia_anual, 2)
    )


@strawberry.type
class Query:
    
    @strawberry.field
    def estados(self) -> List[EstadoType]:
        return [
            EstadoType(uf=e.uf, nome=e.nome, tarifa_base_kwh=e.tarifa_base_kwh)
            for e in ESTADOS
        ]
    
    @strawberry.field
    def simular_economia(self, uf: str, consumo_kwh: float) -> Optional[ResultadoSimulacao]:
        if consumo_kwh <= 0:
            return None
        
        estado = get_estado(uf)
        if not estado:
            return None
        
        fornecedores = get_fornecedores_por_estado(uf)
        if not fornecedores:
            return None
        
        custo_atual_mensal = consumo_kwh * estado.tarifa_base_kwh
        custo_atual_anual = custo_atual_mensal * 12
        
        solucoes_map: dict[SolucaoTipo, List[Fornecedor]] = {
            SolucaoTipo.GD: [],
            SolucaoTipo.MERCADO_LIVRE: []
        }
        
        for fornecedor in fornecedores:
            for solucao in fornecedor.solucoes:
                solucoes_map[solucao].append(fornecedor)
        
        solucoes_disponiveis: List[SolucaoDisponivel] = []
        
        for solucao_tipo, fornecedores_solucao in solucoes_map.items():
            if not fornecedores_solucao:
                continue
            
            economias = [
                calcular_economia(f, solucao_tipo, consumo_kwh, estado.tarifa_base_kwh)
                for f in fornecedores_solucao
            ]
            
            melhor = max(economias, key=lambda e: e.economia_mensal)
            
            solucoes_disponiveis.append(
                SolucaoDisponivel(
                    tipo=solucao_tipo.value,
                    fornecedores=[converter_fornecedor(f) for f in fornecedores_solucao],
                    melhor_economia=converter_economia(melhor)
                )
            )
        
        return ResultadoSimulacao(
            estado=EstadoType(
                uf=estado.uf,
                nome=estado.nome,
                tarifa_base_kwh=estado.tarifa_base_kwh
            ),
            consumo_kwh=consumo_kwh,
            custo_atual_mensal=round(custo_atual_mensal, 2),
            custo_atual_anual=round(custo_atual_anual, 2),
            solucoes_disponiveis=solucoes_disponiveis,
            total_fornecedores=len(fornecedores)
        )


schema = strawberry.Schema(query=Query)