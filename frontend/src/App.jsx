import { useState } from 'react';
import { useQuery, useLazyQuery } from '@apollo/client';
import { GET_ESTADOS, SIMULAR_ECONOMIA } from './graphql/queries';
import './App.css';

function App() {
  const [selectedUf, setSelectedUf] = useState('');
  const [consumo, setConsumo] = useState('');
  const [resultado, setResultado] = useState(null);

  const { loading: loadingEstados, error: errorEstados, data: dataEstados } = useQuery(GET_ESTADOS);
  
  const [simularEconomia, { loading: loadingSimulacao }] = useLazyQuery(SIMULAR_ECONOMIA, {
    onCompleted: (data) => {
      setResultado(data.simularEconomia);
    },
    onError: (error) => {
      console.error('Erro na simulação:', error);
      alert('Erro ao simular. Verifique se o backend está rodando.');
    }
  });

  const handleSimular = () => {
    if (!selectedUf || !consumo || consumo <= 0) {
      alert('Por favor, preencha todos os campos corretamente.');
      return;
    }

    simularEconomia({
      variables: {
        uf: selectedUf,
        consumoKwh: parseFloat(consumo)
      }
    });
  };

  if (loadingEstados) return <div className="loading">Carregando estados...</div>;
  if (errorEstados) return <div className="error">Erro ao carregar estados</div>;

  return (
    <div className="app">
      <header className="header">
        <img 
          src="/src/assets/logo2.png" 
          alt="Clarke Energia" 
          className="logo"
        />
        <p>Simule sua economia com energia renovável</p>
      </header>

      <main className="main">
        <div className="form-container">
          <div className="form-group">
            <label htmlFor="estado">Selecione seu estado:</label>
            <select 
              id="estado"
              value={selectedUf} 
              onChange={(e) => setSelectedUf(e.target.value)}
              className="select"
            >
              <option value="">Escolha um estado</option>
              {dataEstados.estados.map((estado) => (
                <option key={estado.uf} value={estado.uf}>
                  {estado.nome} ({estado.uf})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="consumo">Consumo mensal (kWh):</label>
            <input
              id="consumo"
              type="number"
              value={consumo}
              onChange={(e) => setConsumo(e.target.value)}
              placeholder="Ex: 30000"
              className="input"
              min="1"
            />
          </div>

          <button 
            className="btn-simular"
            onClick={handleSimular}
            disabled={!selectedUf || !consumo || loadingSimulacao}
          >
            {loadingSimulacao ? 'Simulando...' : 'Simular Economia'}
          </button>
        </div>

        {resultado && (
          <div className="resultados">
            <div className="resultado-header">
              <h2>Resultado da Simulação</h2>
              <p className="estado-info">
                {resultado.estado.nome} - Tarifa base: R$ {resultado.estado.tarifaBaseKwh.toFixed(2)}/kWh
              </p>
            </div>

            <div className="custos-atuais">
              <div className="custo-card">
                <span className="label">Custo Atual Mensal</span>
                <span className="valor">R$ {resultado.custoAtualMensal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
              </div>
              <div className="custo-card">
                <span className="label">Custo Atual Anual</span>
                <span className="valor">R$ {resultado.custoAtualAnual.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
              </div>
            </div>

            {resultado.solucoesDisponiveis.map((solucao) => (
              <div key={solucao.tipo} className="solucao-section">
                <h3 className="solucao-titulo">{solucao.tipo}</h3>
                
                {solucao.melhorEconomia && (
                  <div className="melhor-economia">
                    <div className="economia-destaque">
                      <h4>Melhor Economia</h4>
                      <p className="fornecedor-nome">{solucao.melhorEconomia.fornecedor.nome}</p>
                      <div className="economia-valores">
                        <div className="economia-item">
                          <span className="economia-label">Economia Mensal</span>
                          <span className="economia-valor positivo">
                            R$ {solucao.melhorEconomia.economiaMensal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                          </span>
                        </div>
                        <div className="economia-item">
                          <span className="economia-label">Economia Anual</span>
                          <span className="economia-valor positivo">
                            R$ {solucao.melhorEconomia.economiaAnual.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                          </span>
                        </div>
                        <div className="economia-item">
                          <span className="economia-label">Economia %</span>
                          <span className="economia-percentual">
                            {solucao.melhorEconomia.economiaPercentual.toFixed(2)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <div className="fornecedores-list">
                  <h4>Fornecedores Disponíveis ({solucao.fornecedores.length})</h4>
                  <div className="fornecedores-grid">
                    {solucao.fornecedores.map((fornecedor) => (
                      <div key={fornecedor.id} className="fornecedor-card">
                        <img src={fornecedor.logo} alt={fornecedor.nome} className="fornecedor-logo" />
                        <h5>{fornecedor.nome}</h5>
                        <div className="fornecedor-info">
                          <span>⭐ {fornecedor.avaliacaoMedia.toFixed(1)}</span>
                          <span>👥 {fornecedor.totalClientes.toLocaleString('pt-BR')} clientes</span>
                        </div>
                        <div className="fornecedor-custos">
                          {fornecedor.custoKwhGd && (
                            <span>GD: R$ {fornecedor.custoKwhGd.toFixed(2)}/kWh</span>
                          )}
                          {fornecedor.custoKwhMl && (
                            <span>ML: R$ {fornecedor.custoKwhMl.toFixed(2)}/kWh</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
            <div className="selo-energia">
              <img 
                src="/src/assets/3.png" 
                alt="Energia do Futuro - Empresa comprometida com sustentabilidade" 
                className="selo-img"
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;