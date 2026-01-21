import { useState } from 'react';
import { useQuery } from '@apollo/client';
import { GET_ESTADOS } from './graphql/queries';
import './App.css';

function App() {
  const [selectedUf, setSelectedUf] = useState('');
  const [consumo, setConsumo] = useState('');

  const { loading, error, data } = useQuery(GET_ESTADOS);

  if (loading) return <div className="loading">Carregando estados...</div>;
  if (error) return <div className="error">Erro ao carregar estados</div>;

  return (
    <div className="app">
      <header className="header">
        <h1>Clarke Energia</h1>
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
              {data.estados.map((estado) => (
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
            disabled={!selectedUf || !consumo}
          >
            Simular Economia
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;