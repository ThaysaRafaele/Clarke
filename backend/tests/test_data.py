import pytest
from app.data import ESTADOS, FORNECEDORES, get_estado, get_fornecedores_por_estado
from app.schema import calcular_economia
from app.models import SolucaoTipo


class TestData:
    """Testes para funções de acesso aos dados"""
    
    def test_get_estado_exists(self):
        """Testa busca de estado existente"""
        estado = get_estado("SP")
        assert estado is not None
        assert estado.uf == "SP"
        assert estado.nome == "São Paulo"
    
    def test_get_estado_not_exists(self):
        """Testa busca de estado inexistente"""
        estado = get_estado("XX")
        assert estado is None
    
    def test_get_fornecedores_por_estado_sp(self):
        """Testa busca de fornecedores em SP"""
        fornecedores = get_fornecedores_por_estado("SP")
        assert len(fornecedores) > 0
        for f in fornecedores:
            assert f.estado == "SP"
    
    def test_get_fornecedores_por_estado_empty(self):
        """Testa busca de fornecedores em estado sem fornecedores"""
        fornecedores = get_fornecedores_por_estado("XX")
        assert len(fornecedores) == 0
    
    def test_estados_list_not_empty(self):
        """Testa se a lista de estados não está vazia"""
        assert len(ESTADOS) > 0
    
    def test_fornecedores_list_not_empty(self):
        """Testa se a lista de fornecedores não está vazia"""
        assert len(FORNECEDORES) > 0


class TestCalculoEconomia:
    """Testes para função de cálculo de economia"""
    
    def test_calcular_economia_gd(self):
        """Testa cálculo de economia com GD"""
        # Criar fornecedor de teste
        from app.models import Fornecedor
        
        fornecedor = Fornecedor(
            id="test",
            nome="Test GD",
            logo="https://example.com/logo.png",
            estado="SP",
            solucoes=[SolucaoTipo.GD],
            custo_kwh_gd=0.65,
            total_clientes=100,
            avaliacao_media=4.5
        )
        
        consumo_kwh = 30000
        tarifa_base = 0.92
        
        economia = calcular_economia(
            fornecedor=fornecedor,
            solucao=SolucaoTipo.GD,
            consumo_kwh=consumo_kwh,
            tarifa_base=tarifa_base
        )
        
        # Cálculos esperados
        custo_atual = consumo_kwh * tarifa_base  # 27600
        custo_fornecedor = consumo_kwh * 0.65  # 19500
        economia_esperada = custo_atual - custo_fornecedor  # 8100
        
        assert economia.custo_atual == custo_atual
        assert economia.custo_com_fornecedor == custo_fornecedor
        assert economia.economia_mensal == economia_esperada
        assert economia.economia_anual == economia_esperada * 12
        assert economia.economia_percentual > 0
    
    def test_calcular_economia_mercado_livre(self):
        """Testa cálculo de economia com Mercado Livre"""
        from app.models import Fornecedor
        
        fornecedor = Fornecedor(
            id="test",
            nome="Test ML",
            logo="https://example.com/logo.png",
            estado="SP",
            solucoes=[SolucaoTipo.MERCADO_LIVRE],
            custo_kwh_ml=0.58,
            total_clientes=100,
            avaliacao_media=4.5
        )
        
        consumo_kwh = 30000
        tarifa_base = 0.92
        
        economia = calcular_economia(
            fornecedor=fornecedor,
            solucao=SolucaoTipo.MERCADO_LIVRE,
            consumo_kwh=consumo_kwh,
            tarifa_base=tarifa_base
        )
        
        custo_atual = consumo_kwh * tarifa_base
        custo_fornecedor = consumo_kwh * 0.58
        economia_esperada = custo_atual - custo_fornecedor
        
        assert economia.economia_mensal == economia_esperada
        assert economia.solucao == SolucaoTipo.MERCADO_LIVRE
    
    def test_calcular_economia_percentual(self):
        """Testa se o cálculo percentual está correto"""
        from app.models import Fornecedor
        
        fornecedor = Fornecedor(
            id="test",
            nome="Test",
            logo="https://example.com/logo.png",
            estado="SP",
            solucoes=[SolucaoTipo.GD],
            custo_kwh_gd=0.50,
            total_clientes=100,
            avaliacao_media=4.5
        )
        
        economia = calcular_economia(
            fornecedor=fornecedor,
            solucao=SolucaoTipo.GD,
            consumo_kwh=1000,
            tarifa_base=1.00
        )
        
        # 1000 * 1.00 = 1000 (custo atual)
        # 1000 * 0.50 = 500 (custo fornecedor)
        # Economia = 500 (50%)
        
        assert abs(economia.economia_percentual - 50.0) < 0.1