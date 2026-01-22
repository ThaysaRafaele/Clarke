import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
class TestGraphQLAPI:
    """Testes de integração da API GraphQL"""
    
    async def test_health_endpoint(self):
        """Testa endpoint de health check"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    async def test_root_endpoint(self):
        """Testa endpoint raiz"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "online"
            assert "graphql" in data
    
    async def test_query_estados(self):
        """Testa query de estados"""
        query = """
            query {
                estados {
                    uf
                    nome
                    tarifaBaseKwh
                }
            }
        """
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/graphql",
                json={"query": query}
            )
            assert response.status_code == 200
            data = response.json()
            
            assert "data" in data
            assert "estados" in data["data"]
            assert len(data["data"]["estados"]) > 0
            
            # Verifica estrutura do primeiro estado
            estado = data["data"]["estados"][0]
            assert "uf" in estado
            assert "nome" in estado
            assert "tarifaBaseKwh" in estado
    
    async def test_query_simular_economia_valid(self):
        """Testa simulação de economia com dados válidos"""
        query = """
            query {
                simularEconomia(uf: "SP", consumoKwh: 30000) {
                    estado {
                        uf
                        nome
                    }
                    consumoKwh
                    custoAtualMensal
                    custoAtualAnual
                    solucoesDisponiveis {
                        tipo
                        fornecedores {
                            id
                            nome
                            avaliacaoMedia
                        }
                        melhorEconomia {
                            economiaMensal
                            economiaAnual
                            economiaPercentual
                        }
                    }
                    totalFornecedores
                }
            }
        """
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/graphql",
                json={"query": query}
            )
            assert response.status_code == 200
            data = response.json()
            
            assert "data" in data
            assert "simularEconomia" in data["data"]
            
            resultado = data["data"]["simularEconomia"]
            assert resultado is not None
            assert resultado["estado"]["uf"] == "SP"
            assert resultado["consumoKwh"] == 30000
            assert resultado["custoAtualMensal"] > 0
            assert resultado["custoAtualAnual"] > 0
            assert len(resultado["solucoesDisponiveis"]) > 0
            assert resultado["totalFornecedores"] > 0
    
    async def test_query_simular_economia_invalid_uf(self):
        """Testa simulação com UF inválida"""
        query = """
            query {
                simularEconomia(uf: "XX", consumoKwh: 30000) {
                    estado {
                        uf
                    }
                }
            }
        """
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/graphql",
                json={"query": query}
            )
            assert response.status_code == 200
            data = response.json()
            
            # Deve retornar null para UF inválida
            assert data["data"]["simularEconomia"] is None
    
    async def test_query_simular_economia_zero_consumo(self):
        """Testa simulação com consumo zero ou negativo"""
        query = """
            query {
                simularEconomia(uf: "SP", consumoKwh: 0) {
                    estado {
                        uf
                    }
                }
            }
        """
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/graphql",
                json={"query": query}
            )
            assert response.status_code == 200
            data = response.json()
            
            # Deve retornar null para consumo inválido
            assert data["data"]["simularEconomia"] is None
    
    async def test_query_simular_economia_structure(self):
        """Testa estrutura completa da resposta de simulação"""
        query = """
            query {
                simularEconomia(uf: "SP", consumoKwh: 30000) {
                    solucoesDisponiveis {
                        tipo
                        melhorEconomia {
                            fornecedor {
                                id
                                nome
                                logo
                                solucoes
                            }
                            solucao
                            custoAtual
                            custoComFornecedor
                            economiaMensal
                            economiaPercentual
                            economiaAnual
                        }
                    }
                }
            }
        """
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/graphql",
                json={"query": query}
            )
            assert response.status_code == 200
            data = response.json()
            
            solucoes = data["data"]["simularEconomia"]["solucoesDisponiveis"]
            assert len(solucoes) > 0
            
            for solucao in solucoes:
                assert "tipo" in solucao
                assert "melhorEconomia" in solucao
                
                economia = solucao["melhorEconomia"]
                assert "fornecedor" in economia
                assert "economiaMensal" in economia
                assert "economiaAnual" in economia
                assert "economiaPercentual" in economia
                
                # Valida que economia anual = economia mensal * 12
                mensal = economia["economiaMensal"]
                anual = economia["economiaAnual"]
                assert abs(anual - (mensal * 12)) < 1.0
    
    async def test_cors_headers(self):
        """Testa se headers CORS estão configurados"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.options(
                "/graphql",
                headers={
                    "Origin": "http://localhost:5173",
                    "Access-Control-Request-Method": "POST"
                }
            )
            # Verifica se CORS está habilitado
            assert response.status_code in [200, 204]