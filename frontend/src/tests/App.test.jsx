import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MockedProvider } from '@apollo/client/testing'
import userEvent from '@testing-library/user-event'
import App from '../App'
import { GET_ESTADOS, SIMULAR_ECONOMIA } from '../graphql/queries'

// Mock dos dados de estados
const mockEstados = [
  { uf: 'SP', nome: 'São Paulo', tarifaBaseKwh: 0.92 },
  { uf: 'RJ', nome: 'Rio de Janeiro', tarifaBaseKwh: 0.98 },
  { uf: 'MG', nome: 'Minas Gerais', tarifaBaseKwh: 0.87 },
]

// Mock da simulação
const mockSimulacao = {
  estado: { uf: 'SP', nome: 'São Paulo', tarifaBaseKwh: 0.92 },
  consumoKwh: 30000,
  custoAtualMensal: 27600,
  custoAtualAnual: 331200,
  totalFornecedores: 3,
  solucoesDisponiveis: [
    {
      tipo: 'GD',
      fornecedores: [
        {
          id: 'f1',
          nome: 'Energia Solar SP',
          logo: 'https://api.dicebear.com/7.x/shapes/svg?seed=solar',
          avaliacaoMedia: 4.7,
          totalClientes: 1523,
          custoKwhGd: 0.65,
          custoKwhMl: null,
        },
      ],
      melhorEconomia: {
        fornecedor: {
          id: 'f1',
          nome: 'Energia Solar SP',
        },
        economiaMensal: 8100,
        economiaAnual: 97200,
        economiaPercentual: 29.35,
      },
    },
  ],
}

describe('App Component - Testes Reais', () => {
  
  it('deve mostrar loading ao carregar estados', () => {
    const mocks = [
      {
        request: { query: GET_ESTADOS },
        result: { data: { estados: mockEstados } },
        delay: 100, // Simula delay
      },
    ]

    render(
      <MockedProvider mocks={mocks} addTypename={false}>
        <App />
      </MockedProvider>
    )

    expect(screen.getByText(/Carregando estados/i)).toBeInTheDocument()
  })

  it('deve carregar e exibir os estados no select', async () => {
    const mocks = [
      {
        request: { query: GET_ESTADOS },
        result: { data: { estados: mockEstados } },
      },
    ]

    render(
      <MockedProvider mocks={mocks} addTypename={false}>
        <App />
      </MockedProvider>
    )

    await waitFor(() => {
      expect(screen.getByText('São Paulo (SP)')).toBeInTheDocument()
      expect(screen.getByText('Rio de Janeiro (RJ)')).toBeInTheDocument()
    })
  })

  it('deve exibir campos de formulário', async () => {
    const mocks = [
      {
        request: { query: GET_ESTADOS },
        result: { data: { estados: mockEstados } },
      },
    ]

    render(
      <MockedProvider mocks={mocks} addTypename={false}>
        <App />
      </MockedProvider>
    )

    await waitFor(() => {
      expect(screen.getByLabelText(/Selecione seu estado/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/Consumo mensal/i)).toBeInTheDocument()
      expect(screen.getByText(/Simular Economia/i)).toBeInTheDocument()
    })
  })

  it('deve permitir selecionar estado e digitar consumo', async () => {
    const user = userEvent.setup()
    const mocks = [
      {
        request: { query: GET_ESTADOS },
        result: { data: { estados: mockEstados } },
      },
    ]

    render(
      <MockedProvider mocks={mocks} addTypename={false}>
        <App />
      </MockedProvider>
    )

    await waitFor(() => {
      expect(screen.getByLabelText(/Selecione seu estado/i)).toBeInTheDocument()
    })

    const selectEstado = screen.getByLabelText(/Selecione seu estado/i)
    const inputConsumo = screen.getByLabelText(/Consumo mensal/i)

    await user.selectOptions(selectEstado, 'SP')
    await user.type(inputConsumo, '30000')

    expect(selectEstado.value).toBe('SP')
    expect(inputConsumo.value).toBe('30000')
  })

  it('deve simular economia quando clicar no botão', async () => {
    const user = userEvent.setup()
    const mocks = [
      {
        request: { query: GET_ESTADOS },
        result: { data: { estados: mockEstados } },
      },
      {
        request: {
          query: SIMULAR_ECONOMIA,
          variables: { uf: 'SP', consumoKwh: 30000 },
        },
        result: { data: { simularEconomia: mockSimulacao } },
      },
    ]

    render(
        <MockedProvider mocks={mocks} addTypename={false}>
            <App />
        </MockedProvider>
    )

    await waitFor(() => {
        expect(screen.getByLabelText(/Selecione seu estado/i)).toBeInTheDocument()
    })

    const selectEstado = screen.getByLabelText(/Selecione seu estado/i)
    const inputConsumo = screen.getByLabelText(/Consumo mensal/i)
    const btnSimular = screen.getByText(/Simular Economia/i)

    await user.selectOptions(selectEstado, 'SP')
    await user.type(inputConsumo, '30000')
    await user.click(btnSimular)

    await waitFor(() => {
        expect(screen.getByText(/Resultado da Simulação/i)).toBeInTheDocument()
        const fornecedores = screen.queryAllByText(/Energia Solar SP/i)
        expect(fornecedores.length).toBeGreaterThan(0)
    })
  })

  it('botão deve estar desabilitado quando campos vazios', async () => {
    const mocks = [
      {
        request: { query: GET_ESTADOS },
        result: { data: { estados: mockEstados } },
      },
    ]

    render(
      <MockedProvider mocks={mocks} addTypename={false}>
        <App />
      </MockedProvider>
    )

    await waitFor(() => {
      expect(screen.getByLabelText(/Selecione seu estado/i)).toBeInTheDocument()
    })

    const btnSimular = screen.getByText(/Simular Economia/i)
    expect(btnSimular).toBeDisabled()
  })
})