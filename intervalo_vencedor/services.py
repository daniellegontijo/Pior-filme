import re
from collections import defaultdict
from .models import Movie

def split_producers(producers_str):
    """
    Função auxiliar para separar os nomes dos produtores considerando diferentes separadores.
    """
    # Usando expressão regular para separar por ', ' e ' and '
    producers = re.split(r'\s*,\s*|\s+and\s+', producers_str)
    return [p.strip() for p in producers]

def calcular_intervalos_premios():
    """
    Calcula os maiores e menores intervalos de prêmios para cada produtor.
    """
    producer_wins = defaultdict(list)
    filmes = Movie.objects.all()

    # Organiza os anos de premiação por produtor
    for filme in filmes:
        if filme.winner:  # Verifica se o filme ganhou um prêmio
            producers = split_producers(filme.producers)
            for producer in producers:
                producer_wins[producer].append(filme.year)

    min_interval = float('inf')
    max_interval = float('-inf')
    min_interval_details = []
    max_interval_details = []

    # Calcula o menor e maior intervalo para cada produtor
    for producer, years in producer_wins.items():
        years.sort()
        if len(years) < 2:
            continue  # Ignora produtores com menos de dois prêmios

        for i in range(len(years) - 1):
            interval = years[i + 1] - years[i]
            if interval < min_interval:
                min_interval = interval
                min_interval_details = [{
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                }]
            elif interval == min_interval:
                min_interval_details.append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                })

            if interval > max_interval:
                max_interval = interval
                max_interval_details = [{
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                }]
            elif interval == max_interval:
                max_interval_details.append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                })

    # Se não há prêmios, retorna listas vazias
    if min_interval == float('inf'):
        min_interval_details = []
    if max_interval == float('-inf'):
        max_interval_details = []

    return {'min': min_interval_details, 'max': max_interval_details}