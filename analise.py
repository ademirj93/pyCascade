import os
import json
import pandas as pd

caminho_pasta = 'caminho/para/sua/pasta'  # Substitua pelo caminho da sua pasta

dados = []

for nome_arquivo in os.listdir(caminho_pasta):
    if nome_arquivo.endswith('.json'):
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
        with open(caminho_arquivo, 'r') as arquivo_json:
            dados_json = json.load(arquivo_json)
            dados_json['descriptor'] = nome_arquivo  # Adicionando o título do arquivo como 'descriptor'
            dados.append(dados_json)

# Convertendo para DataFrame do pandas
df = pd.DataFrame(dados)

# Salvando como CSV
df.to_csv('resultado.csv', index=False)
