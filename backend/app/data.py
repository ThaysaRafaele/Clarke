from typing import List
from app.models import Fornecedor, Estado, SolucaoTipo


ESTADOS: List[Estado] = [
    Estado(uf="SP", nome="São Paulo", tarifa_base_kwh=0.92),
    Estado(uf="RJ", nome="Rio de Janeiro", tarifa_base_kwh=0.98),
    Estado(uf="MG", nome="Minas Gerais", tarifa_base_kwh=0.87),
    Estado(uf="RS", nome="Rio Grande do Sul", tarifa_base_kwh=0.85),
    Estado(uf="PR", nome="Paraná", tarifa_base_kwh=0.83),
    Estado(uf="SC", nome="Santa Catarina", tarifa_base_kwh=0.81),
    Estado(uf="BA", nome="Bahia", tarifa_base_kwh=0.79),
    Estado(uf="CE", nome="Ceará", tarifa_base_kwh=0.77),
]


FORNECEDORES: List[Fornecedor] = [
    Fornecedor(
        id="f1",
        nome="Energia Solar SP",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=solar",
        estado="SP",
        solucoes=[SolucaoTipo.GD],
        custo_kwh_gd=0.65,
        total_clientes=1523,
        avaliacao_media=4.7
    ),
    Fornecedor(
        id="f2",
        nome="PowerTrade Brasil",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=power",
        estado="SP",
        solucoes=[SolucaoTipo.MERCADO_LIVRE],
        custo_kwh_ml=0.58,
        total_clientes=892,
        avaliacao_media=4.5
    ),
    Fornecedor(
        id="f3",
        nome="GreenEnergy Soluções",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=green",
        estado="SP",
        solucoes=[SolucaoTipo.GD, SolucaoTipo.MERCADO_LIVRE],
        custo_kwh_gd=0.68,
        custo_kwh_ml=0.61,
        total_clientes=2341,
        avaliacao_media=4.8
    ),
    Fornecedor(
        id="f4",
        nome="Rio Solar Energia",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=rio",
        estado="RJ",
        solucoes=[SolucaoTipo.GD],
        custo_kwh_gd=0.71,
        total_clientes=1102,
        avaliacao_media=4.6
    ),
    Fornecedor(
        id="f5",
        nome="Mercado Livre RJ",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=livre",
        estado="RJ",
        solucoes=[SolucaoTipo.MERCADO_LIVRE],
        custo_kwh_ml=0.64,
        total_clientes=745,
        avaliacao_media=4.4
    ),
    Fornecedor(
        id="f6",
        nome="Minas Energia Limpa",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=minas",
        estado="MG",
        solucoes=[SolucaoTipo.GD, SolucaoTipo.MERCADO_LIVRE],
        custo_kwh_gd=0.62,
        custo_kwh_ml=0.56,
        total_clientes=1876,
        avaliacao_media=4.9
    ),
    Fornecedor(
        id="f7",
        nome="Sul Energia Renovável",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=sul",
        estado="RS",
        solucoes=[SolucaoTipo.GD],
        custo_kwh_gd=0.60,
        total_clientes=1234,
        avaliacao_media=4.7
    ),
    Fornecedor(
        id="f8",
        nome="Paraná Power",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=parana",
        estado="PR",
        solucoes=[SolucaoTipo.MERCADO_LIVRE],
        custo_kwh_ml=0.54,
        total_clientes=934,
        avaliacao_media=4.5
    ),
    Fornecedor(
        id="f9",
        nome="Santa Catarina Solar",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=sc",
        estado="SC",
        solucoes=[SolucaoTipo.GD],
        custo_kwh_gd=0.58,
        total_clientes=987,
        avaliacao_media=4.6
    ),
    Fornecedor(
        id="f10",
        nome="Bahia Energia Limpa",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=bahia",
        estado="BA",
        solucoes=[SolucaoTipo.GD, SolucaoTipo.MERCADO_LIVRE],
        custo_kwh_gd=0.56,
        custo_kwh_ml=0.52,
        total_clientes=1456,
        avaliacao_media=4.8
    ),
    Fornecedor(
        id="f11",
        nome="Ceará Renovável",
        logo="https://api.dicebear.com/7.x/shapes/svg?seed=ceara",
        estado="CE",
        solucoes=[SolucaoTipo.MERCADO_LIVRE],
        custo_kwh_ml=0.50,
        total_clientes=823,
        avaliacao_media=4.5
    ),
]


def get_estado(uf: str) -> Estado | None:
    return next((e for e in ESTADOS if e.uf == uf), None)


def get_fornecedores_por_estado(uf: str) -> List[Fornecedor]:
    return [f for f in FORNECEDORES if f.estado == uf]