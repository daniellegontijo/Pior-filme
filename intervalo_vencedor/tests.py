from django.test import TestCase
from .models import Movie
from .services import calcular_intervalos_premios

class CalcularIntervalosPremiosTest(TestCase):

    def setUp(self):
        # Criação de alguns filmes de teste
        Movie.objects.create(year=2000, producers="Producer A, Producer B", winner=True)
        Movie.objects.create(year=2002, producers="Producer A", winner=True)
        Movie.objects.create(year=2005, producers="Producer A", winner=True)
        Movie.objects.create(year=2010, producers="Producer B", winner=True)
        Movie.objects.create(year=2013, producers="Producer B", winner=True)
        Movie.objects.create(year=2015, producers="Producer C", winner=True)
        Movie.objects.create(year=2017, producers="Producer C", winner=True)
    
    def test_calcular_intervalos_premios(self):
        resultado = calcular_intervalos_premios()

        esperado = {
            'min': [
                {
                    'producer': 'Producer A',
                    'interval': 3,
                    'previousWin': 2002,
                    'followingWin': 2005
                },
                {
                    'producer': 'Producer B',
                    'interval': 3,
                    'previousWin': 2010,
                    'followingWin': 2013
                }
            ],
            'max': [
                {
                    'producer': 'Producer A',
                    'interval': 5,
                    'previousWin': 2005,
                    'followingWin': 2010
                }
            ]
        }

        self.assertEqual(resultado, esperado)