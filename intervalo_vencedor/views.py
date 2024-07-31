from django.http import JsonResponse
from .services import calcular_intervalos_premios

def maior_intervalo(request):
    """
    View que retorna os maiores e menores intervalos de prêmios para cada produtor.
    """
    intervalos = calcular_intervalos_premios()
    return JsonResponse(intervalos)
