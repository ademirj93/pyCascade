import pandas as pd
import matplotlib.pyplot as plt
import os, datetime

def plot_dot_graph(output_dataset_path: str, dataset_name: str, top_k: int): 

    # Obter data e hora atuais
    current_time = datetime.datetime.now()

    # Extrair informações de data e hora
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    seconds = current_time.second



    # Carrega os dados do CSV de descritores isolados
    descriptors_dataset = pd.read_csv(f"{output_dataset_path}/{dataset_name}.csv")
    # Carregando os dados do arquivo "fusion_values_all_fusions.csv"
    fusion_values = pd.read_csv(f"{output_dataset_path}/fusion_values_all_fusions.csv")

    # Encontrando o maior valor da coluna "MAP"
    maior_valor_MAP = descriptors_dataset["MAP"].max()

    # Carregando os dados do arquivo "{dataset_name}_evall_borda.txt"
    borda_values = pd.read_csv(f"{output_dataset_path}/{dataset_name}_after_cascade_effectiveness_borda_topk={top_k}.txt")

    colors = []  # Criando uma lista vazia para armazenar as cores

    # Criar uma lista numerada para os elementos
    enumerated_elements = [f"{i+1}. {txt}" for i, txt in enumerate(fusion_values["descriptor"])]

    # Adicionando o valor do ponto e definindo a cor
    for i, txt in enumerate(fusion_values["descriptor"]):
        
        if fusion_values["MAP"][i] >= maior_valor_MAP:
            colors.append('green')  # Adicionando 'green' para valores maiores que maior_valor_MAP
        else:
            colors.append('blue')  # Adicionando 'black' para valores menores que maior_valor_MAP

    name_txt = txt.split(f"{dataset_name}_")[1].split(f"_topK={top_k}")[0]
    # Crie rótulos personalizados com números e name_txt
    #legend_labels = [f"{i+1}. {txt}" for i, txt in enumerate(fusion_values["descriptor"])]
    legend_labels = [f"{i+1}. {txt.split(f'{dataset_name}_')[1].split(f'_topK={top_k}')[0]}" for i, txt in enumerate(fusion_values["descriptor"])]

    # Crie uma lista de handles para cada ponto no gráfico
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green' if color == 'green' else 'blue', markersize=10) for color in colors]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))

    # Gráfico no primeiro subplot (ax1)
    scatter = ax1.scatter(borda_values["score"], fusion_values["MAP"], c=colors)
    ax1.axhline(y=maior_valor_MAP, color='black', linestyle='--', label="Melhor descritor isolado")
    # Configurações do gráfico...
    ax1.legend()
    ax1.set_xlabel("Borda Score")
    ax1.set_ylabel("MAP")
    ax1.set_title("Gráfico de Pontos - MAP vs Borda Score")
    ax1.grid(True)

    # Adicionando os números aos pontos no gráfico
    for i, txt in enumerate(enumerated_elements):
        ax1.annotate(i+1, (borda_values["score"][i], fusion_values["MAP"][i]), textcoords="offset points", xytext=(5,5), ha='center')

    # Crie uma lista de handles para cada ponto no gráfico
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green' if color == 'green' else 'blue', markersize=10) for color in colors]

    # Legenda personalizada no segundo subplot (ax2)
    ax2.axis('off')
    ax2.legend(handles, legend_labels, loc='center')
    ax2.set_title('Descritores')

    # Ajustando o layout para evitar sobreposição
    plt.tight_layout()

    # Depois de criar o gráfico, use savefig para salvar como imagem
    plt.savefig(f'{output_dataset_path}/{dataset_name}_graph_{day}{month}{year}.png')

    # Mostrando os subplots
    plt.show()


    return