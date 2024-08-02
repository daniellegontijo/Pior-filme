from django.test import Client
from django.urls import reverse
from intervalo_vencedor.services import calcular_intervalos_premios
from intervalo_vencedor.models import Movie
from unittest.mock import patch, MagicMock
from unittest import TestCase
import unittest
import json

class CalcularIntervalosPremiosTest(TestCase):
    
    @patch('intervalo_vencedor.services.Movie')
    def test_calcular_intervalos_premios(self, MockMovie):
        # Configura o mock para retornar os filmes de teste
        MockMovie.objects.all.return_value = [
            MagicMock(year=2000, producers="Producer A", winner=True),
            MagicMock(year=2002, producers="Producer A", winner=True),
            MagicMock(year=2005, producers="Producer A", winner=True),
            MagicMock(year=2007, producers="Producer B", winner=True)
        ]

        resultado = calcular_intervalos_premios()

        esperado = {
            'min': [
                {'producer': 'Producer A', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 3, 'previousWin': 2002, 'followingWin': 2005}
            ]
        }

        # Imprime os resultados para depuração
        print("Resultado obtido:", resultado)
        print("Resultado esperado:", esperado)
        
        # Configura o maxDiff para None para ver o diff completo
        self.maxDiff = None
        self.assertEqual(resultado, esperado)

    @patch('intervalo_vencedor.services.Movie')
    def test_consecutive_wins(self, MockMovie):
        MockMovie.objects.all.return_value = [
            MagicMock(year=2000, producers="Producer A", winner=True),
            MagicMock(year=2001, producers="Producer A", winner=True),
            MagicMock(year=2002, producers="Producer A", winner=True)
        ]
        
        resultado = calcular_intervalos_premios()
        esperado = {
            'min': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2001, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2001, 'followingWin': 2002}
            ]
        }

        # Imprime os resultados para depuração
        print("Resultado obtido:", resultado)
        print("Resultado esperado:", esperado)
        self.assertEqual(resultado, esperado)

    @patch('intervalo_vencedor.services.Movie')
    def test_multiple_producers(self, MockMovie):
        MockMovie.objects.all.return_value = [
            MagicMock(year=2000, producers="Producer A", winner=True),
            MagicMock(year=2002, producers="Producer A", winner=True),
            MagicMock(year=2005, producers="Producer A", winner=True),
            MagicMock(year=2001, producers="Producer B", winner=True),
            MagicMock(year=2006, producers="Producer B", winner=True)
        ]
        
        resultado = calcular_intervalos_premios()
        esperado = {
            'min': [
                {'producer': 'Producer A', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer B', 'interval': 5, 'previousWin': 2001, 'followingWin': 2006}
            ]
        }
        print("Resultado obtido:", resultado)
        print("Resultado esperado:", esperado)
        self.assertEqual(resultado, esperado)
        
    @patch('intervalo_vencedor.services.Movie')
    def test_single_award_per_producer(self, MockMovie):
        MockMovie.objects.all.return_value = [
            MagicMock(year=2000, producers="Producer A", winner=True),
            MagicMock(year=2005, producers="Producer B", winner=True)
        ]
        
        resultado = calcular_intervalos_premios()
        esperado = {'min': [], 'max': []}
        self.assertEqual(resultado, esperado)

# class MaiorIntervaloViewTest(TestCase):
    
#     @patch('intervalo_vencedor.views.calcular_intervalos_premios')
#     def test_maior_intervalo(self, mock_calcular_intervalos_premios):
#         # Define o resultado mockado
#         mock_calcular_intervalos_premios.return_value = {
#             'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}],
#             'max': [{'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005}]
#         }
        
#         # Faz uma requisição GET para a view
#         response = self.client.get(reverse('maior_intervalo'))
        
#         # Verifica o status da resposta
#         self.assertEqual(response.status_code, 200)
        
#         # Verifica o conteúdo da resposta
#         expected_response = {
#             'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}],
#             'max': [{'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005}]
#         }
#         self.assertJSONEqual(response.content, expected_response)

class MaiorIntervaloViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_maior_intervalo(self, mock_calcular_intervalos):
        # Define o valor mockado
        mock_calcular_intervalos.return_value = {
            'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                    {'producer': 'Producer A', 'interval': 1, 'previousWin': 2001, 'followingWin': 2002}],
            'max': [{'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005}]
        }

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Dados esperados
        expected_response = {
            'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                    {'producer': 'Producer A', 'interval': 1, 'previousWin': 2001, 'followingWin': 2002}],
            'max': [{'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005}]
        }

        # Converte a resposta para dicionário
        response_data = json.loads(response.content)

        # Compara os dados
        self.assertEqual(response_data, expected_response)

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_maior_intervalo_sem_premios(self, mock_calcular_intervalos):
        # Define o valor mockado para o caso sem prêmios
        mock_calcular_intervalos.return_value = {'min': [], 'max': []}

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Dados esperados
        expected_response = {'min': [], 'max': []}

        # Converte a resposta para dicionário
        response_data = json.loads(response.content)

        # Compara os dados
        self.assertEqual(response_data, expected_response)

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_maior_intervalo_multiplos_produtores(self, mock_calcular_intervalos):
        # Define o valor mockado com múltiplos produtores e intervalos variados
        mock_calcular_intervalos.return_value = {
            'min': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer B', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005},
                {'producer': 'Producer B', 'interval': 10, 'previousWin': 2000, 'followingWin': 2010}
            ]
        }

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Dados esperados
        expected_response = {
            'min': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer B', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005},
                {'producer': 'Producer B', 'interval': 10, 'previousWin': 2000, 'followingWin': 2010}
            ]
        }

        # Converte a resposta para dicionário
        response_data = json.loads(response.content)

        # Compara os dados
        self.assertEqual(response_data, expected_response)

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_maior_intervalo_intervalos_iguais(self, mock_calcular_intervalos):
        # Define o valor mockado com intervalos iguais para vários produtores
        mock_calcular_intervalos.return_value = {
            'min': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer B', 'interval': 1, 'previousWin': 2001, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002},
                {'producer': 'Producer B', 'interval': 2, 'previousWin': 2002, 'followingWin': 2004}
            ]
        }

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Dados esperados
        expected_response = {
            'min': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer B', 'interval': 1, 'previousWin': 2001, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002},
                {'producer': 'Producer B', 'interval': 2, 'previousWin': 2002, 'followingWin': 2004}
            ]
        }

        # Converte a resposta para dicionário
        response_data = json.loads(response.content)

        # Compara os dados
        self.assertEqual(response_data, expected_response)

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_maior_intervalo_um_produtor_um_intervalo(self, mock_calcular_intervalos):
        # Define o valor mockado com um único produtor e um intervalo
        mock_calcular_intervalos.return_value = {
            'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}],
            'max': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}]
        }

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Dados esperados
        expected_response = {
            'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}],
            'max': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}]
        }

        # Converte a resposta para dicionário
        response_data = json.loads(response.content)

        # Compara os dados
        self.assertEqual(response_data, expected_response)

class MaiorIntervaloUrlTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_url_resposta(self, mock_calcular_intervalos):
        # Define o valor mockado para o cálculo de intervalos
        mock_calcular_intervalos.return_value = {'min': [], 'max': []}

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Verifica se o status da resposta é 200 (OK)
        self.assertEqual(response.status_code, 200)

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_url_conteudo_resposta(self, mock_calcular_intervalos):
        # Define o valor mockado para o cálculo de intervalos
        mock_calcular_intervalos.return_value = {
            'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}],
            'max': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}]
        }

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Dados esperados
        expected_response = {
            'min': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}],
            'max': [{'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001}]
        }

        # Converte a resposta para dicionário
        response_data = json.loads(response.content)

        # Compara os dados
        self.assertEqual(response_data, expected_response)

    @patch('intervalo_vencedor.views.calcular_intervalos_premios')
    def test_url_dados_variados(self, mock_calcular_intervalos):
        # Define o valor mockado com dados variados
        mock_calcular_intervalos.return_value = {
            'min': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer B', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005},
                {'producer': 'Producer B', 'interval': 10, 'previousWin': 2000, 'followingWin': 2010}
            ]
        }

        # Requisita a URL
        response = self.client.get(reverse('maior_intervalo'))

        # Dados esperados
        expected_response = {
            'min': [
                {'producer': 'Producer A', 'interval': 1, 'previousWin': 2000, 'followingWin': 2001},
                {'producer': 'Producer B', 'interval': 2, 'previousWin': 2000, 'followingWin': 2002}
            ],
            'max': [
                {'producer': 'Producer A', 'interval': 5, 'previousWin': 2000, 'followingWin': 2005},
                {'producer': 'Producer B', 'interval': 10, 'previousWin': 2000, 'followingWin': 2010}
            ]
        }

        # Converte a resposta para dicionário
        response_data = json.loads(response.content)

        # Compara os dados
        self.assertEqual(response_data, expected_response)