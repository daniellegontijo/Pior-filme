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

# import re
# from .models import Movie

# def split_producers(producers):
#     """
#     Divide a string de produtores em uma lista de produtores individuais.
#     """
#     return [producer.strip() for producer in re.split(r', |, and | and ', producers)]

# def calcular_intervalos_premios():
#     try:
#         # Obter todos os filmes
#         todos_filmes = Filme.objects.all()

#         # Verificar se há filmes vencedores manualmente
#         vencedores = [filme for filme in todos_filmes if filme.vencedor]

#         if not vencedores:
#             print("Nenhum filme vencedor encontrado.")
#         else:
#             print(f"Total de filmes vencedores encontrados: {len(vencedores)}")
#             for filme in vencedores:
#                 print(f"Título: {filme.titulo}")
#                 print(f"Ano: {filme.ano}")
#                 print(f"Estúdios: {filme.estudios}")
#                 print(f"Produtores: {filme.produtores}")
#                 print("")  # Linha em branco para separar cada filme

#         # Dicionário para armazenar os anos dos prêmios dos produtores
#         intervalos = {}

#         for filme in vencedores:
#             produtores = split_producers(filme.produtores)
#             for produtor in produtores:
#                 if produtor not in intervalos:
#                     intervalos[produtor] = []
#                 intervalos[produtor].append(filme.ano)

#         print(intervalos)

#         # Calcular intervalos
#         resultados = []
#         for produtor, anos in intervalos.items():
#             if len(anos) > 1:
#                 anos.sort()
#                 for i in range(len(anos) - 1):
#                     intervalo = anos[i + 1] - anos[i]
#                     resultados.append({
#                         'produtor': produtor,
#                         'intervalo': intervalo,
#                         'previousWin': anos[i],
#                         'followingWin': anos[i + 1]
#                     })

#         # Encontrar os produtores com o maior e menor intervalo
#         if resultados:
#             max_intervalo = max(resultados, key=lambda x: x['intervalo'])['intervalo']
#             min_intervalo = min(resultados, key=lambda x: x['intervalo'])['intervalo']

#             produtores_maior_intervalo = [res for res in resultados if res['intervalo'] == max_intervalo]
#             produtores_menor_intervalo = [res for res in resultados if res['intervalo'] == min_intervalo]

#             return {
#                 'min': produtores_menor_intervalo,
#                 'max': produtores_maior_intervalo
#             }

#     except Exception as e:
#         print(f"Erro ao calcular intervalos: {e}")

#     return {
#         'min': [],
#         'max': [],
#     }

 