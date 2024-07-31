import pandas as pd
from pymongo import MongoClient

# Substitua o caminho abaixo pelo caminho do seu arquivo CSV
csv_file_path = 'C:/Users/Danielle/Downloads/movielist_1.csv'
client = MongoClient("mongodb://localhost:27017/")
db = client["EspecificacaoPiorFilme"]
collection = db["filmes"]
# Ler o arquivo CSV usando pandas
try:
    # Tenta ler o arquivo CSV
    df = pd.read_csv(csv_file_path, encoding='utf-8', delimiter=';')
    df['winner'] = df['winner'].apply(lambda x: True if x == 'yes' else False)

    # Converter o DataFrame em uma lista de dicionários
    dctFilmes = df.to_dict(orient='records')
   
    

    for doc in dctFilmes:
        print(doc['winner'])
        # collection.insert_one(doc)
  
    print('inseriu')
except FileNotFoundError:
    print(f"Erro: O arquivo {csv_file_path} não foi encontrado.")