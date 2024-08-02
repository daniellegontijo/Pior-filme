
import re
import logging
from collections import defaultdict
from .models import Movie

# Configuração do logger
logger = logging.getLogger('teste_pior_filme')

def split_producers(producers_str):
    """
    Função auxiliar para separar os nomes dos produtores considerando diferentes separadores.
    """
    producers = re.split(r',\s+and\s+|\sand\s+|,\s+', producers_str)
    return [p.strip() for p in producers]

def calcular_intervalos_premios():
    """
    Calcula os maiores e menores intervalos de prêmios para cada produtor.
    """
    logger.info("Iniciando cálculo dos intervalos de prêmios")
    producer_wins = defaultdict(list)
    filmes = Movie.objects.all()

    # Organiza os anos de premiação por produtor
    for filme in filmes:
        if filme.winner:  # Verifica se o filme ganhou um prêmio
            producers = split_producers(filme.producers)
            logger.debug(f"Produtores encontrados: {producers}")
            for producer in producers:
                producer_wins[producer].append(filme.year)
                logger.debug(f"Adicionando ano {filme.year} para o produtor {producer}")

    min_interval = float('inf')
    max_interval = float('-inf')
    min_interval_details = []
    max_interval_details = []

    # Calcula o menor e maior intervalo para cada produtor
    for producer, years in producer_wins.items():
        years.sort()
        logger.debug(f"Anos de prêmios para o produtor {producer}: {years}")
        if len(years) < 2:
            logger.info(f"Produtor {producer} tem menos de dois prêmios, ignorando.")
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
                logger.info(f"Novo menor intervalo encontrado: {min_interval} anos, para o produtor {producer}")
            elif interval == min_interval:
                min_interval_details.append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                })
                logger.info(f"Intervalo igual ao menor encontrado: {min_interval} anos, para o produtor {producer}")

            if interval > max_interval:
                max_interval = interval
                max_interval_details = [{
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                }]
                logger.info(f"Novo maior intervalo encontrado: {max_interval} anos, para o produtor {producer}")
            elif interval == max_interval:
                max_interval_details.append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                })
                logger.info(f"Intervalo igual ao maior encontrado: {max_interval} anos, para o produtor {producer}")

    # Se não há prêmios, retorna listas vazias
    if min_interval == float('inf'):
        logger.info("Nenhum menor intervalo encontrado, retornando lista vazia.")
        min_interval_details = []
    if max_interval == float('-inf'):
        logger.info("Nenhum maior intervalo encontrado, retornando lista vazia.")
        max_interval_details = []

    result = {'min': min_interval_details, 'max': max_interval_details}
    logger.info("Cálculo dos intervalos de prêmios concluído")
    return result