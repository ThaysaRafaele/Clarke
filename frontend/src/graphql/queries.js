import { gql } from '@apollo/client';

export const GET_ESTADOS = gql`
  query GetEstados {
    estados {
      uf
      nome
      tarifaBaseKwh
    }
  }
`;

export const SIMULAR_ECONOMIA = gql`
  query SimularEconomia($uf: String!, $consumoKwh: Float!) {
    simularEconomia(uf: $uf, consumoKwh: $consumoKwh) {
      estado {
        uf
        nome
        tarifaBaseKwh
      }
      consumoKwh
      custoAtualMensal
      custoAtualAnual
      totalFornecedores
      solucoesDisponiveis {
        tipo
        melhorEconomia {
          fornecedor {
            nome
            logo
            avaliacaoMedia
            totalClientes
          }
          economiaMensal
          economiaPercentual
          economiaAnual
        }
        fornecedores {
          id
          nome
          logo
          solucoes
          custoKwhGd
          custoKwhMl
          totalClientes
          avaliacaoMedia
        }
      }
    }
  }
`;