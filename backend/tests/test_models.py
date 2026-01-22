import pytest
from pydantic import ValidationError
from app.models import Estado, Fornecedor, EconomiaFornecedor, SolucaoTipo


class TestModels:
    """Testes dos modelos de dados Pydantic"""
    
    def test_estado_criacao_valida(self):
        """Testa criação de um Estado válido"""
        estado = Estado(
            uf="SP",
            nome="São Paulo",
            tarifa_base_kwh=0.92
        )
        
        assert estado.uf == "SP"
        assert estado.nome == "São Paulo"
        assert estado.tarifa_base_kwh == 0.92
    
    def test_fornecedor_criacao_gd(self):
        """Testa criação de Fornecedor com solução GD"""
        fornecedor = Fornecedor(
            id="f1",
            nome="Energia Solar SP",
            logo="https://example.com/logo.png",
            estado="SP",
            solucoes=[SolucaoTipo.GD],
            custo_kwh_gd=0.65,
            total_clientes=1000,
            avaliacao_media=4.5
        )
        
        assert fornecedor.id == "f1"
        assert fornecedor.nome == "Energia Solar SP"
        assert SolucaoTipo.GD in fornecedor.solucoes
        assert fornecedor.custo_kwh_gd == 0.65
        assert fornecedor.total_clientes == 1000
        assert fornecedor.avaliacao_media == 4.5
    
    def test_fornecedor_criacao_mercado_livre(self):
        """Testa criação de Fornecedor com solução Mercado Livre"""
        fornecedor = Fornecedor(
            id="f2",
            nome="PowerTrade Brasil",
            logo="https://example.com/logo.png",
            estado="RJ",
            solucoes=[SolucaoTipo.MERCADO_LIVRE],
            custo_kwh_ml=0.58,
            total_clientes=500,
            avaliacao_media=4.7
        )
        
        assert SolucaoTipo.MERCADO_LIVRE in fornecedor.solucoes
        assert fornecedor.custo_kwh_ml == 0.58
    
    def test_fornecedor_multiplas_solucoes(self):
        """Testa Fornecedor com GD e Mercado Livre"""
        fornecedor = Fornecedor(
            id="f3",
            nome="GreenEnergy",
            logo="https://example.com/logo.png",
            estado="MG",
            solucoes=[SolucaoTipo.GD, SolucaoTipo.MERCADO_LIVRE],
            custo_kwh_gd=0.68,
            custo_kwh_ml=0.61,
            total_clientes=2000,
            avaliacao_media=4.8
        )
        
        assert len(fornecedor.solucoes) == 2
        assert SolucaoTipo.GD in fornecedor.solucoes
        assert SolucaoTipo.MERCADO_LIVRE in fornecedor.solucoes
    
    def test_avaliacao_media_valida(self):
        """Testa validação de avaliação (deve estar entre 0 e 5)"""
        # Avaliação válida
        fornecedor = Fornecedor(
            id="f4",
            nome="Test",
            logo="https://example.com/logo.png",
            estado="SP",
            solucoes=[SolucaoTipo.GD],
            custo_kwh_gd=0.65,
            total_clientes=100,
            avaliacao_media=5.0
        )
        assert fornecedor.avaliacao_media == 5.0
    
    def test_avaliacao_media_invalida(self):
        """Testa que avaliação acima de 5 gera erro"""
        with pytest.raises(ValidationError):
            Fornecedor(
                id="f5",
                nome="Test",
                logo="https://example.com/logo.png",
                estado="SP",
                solucoes=[SolucaoTipo.GD],
                custo_kwh_gd=0.65,
                total_clientes=100,
                avaliacao_media=5.5  # Inválido!
            )
    
    def test_economia_fornecedor_criacao(self):
        """Testa criação de EconomiaFornecedor"""
        fornecedor = Fornecedor(
            id="f1",
            nome="Test",
            logo="https://example.com/logo.png",
            estado="SP",
            solucoes=[SolucaoTipo.GD],
            custo_kwh_gd=0.65,
            total_clientes=100,
            avaliacao_media=4.5
        )
        
        economia = EconomiaFornecedor(
            fornecedor=fornecedor,
            solucao=SolucaoTipo.GD,
            custo_atual=27600.0,
            custo_com_fornecedor=19500.0,
            economia_mensal=8100.0,
            economia_percentual=29.35,
            economia_anual=97200.0
        )
        
        assert economia.fornecedor.id == "f1"
        assert economia.solucao == SolucaoTipo.GD
        assert economia.economia_mensal == 8100.0
        assert economia.economia_anual == 97200.0
    
    def test_solucao_tipo_valores(self):
        """Testa os valores do enum SolucaoTipo"""
        assert SolucaoTipo.GD.value == "GD"
        assert SolucaoTipo.MERCADO_LIVRE.value == "Mercado Livre"