import pandas as pd
import matplotlib.pyplot as plt

def plot_dot_graph(output_dataset_path: str, dataset_name: str, top_k: int, top_m: int): 

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
    
    plt.rc('font', size=22)

    # Gráfico no primeiro subplot (ax1)
    scatter = ax1.scatter(borda_values["score"], fusion_values["MAP"], c=colors)
    ax1.axhline(y=maior_valor_MAP, color='red', linestyle='--', label="Melhor descritor isolado")
    # Configurações do gráfico...
    ax1.legend()
    ax1.set_xlabel("Borda Score", fontsize=24)
    ax1.set_ylabel("MAP", fontsize=24)
    ax1.set_title("Gráfico de Pontos - MAP vs Borda Score")
    ax1.grid(True)

    # Ajustando o tamanho da fonte nos valores dos eixos
    ax1.tick_params(axis='x', labelsize=18)  # Tamanho da fonte no eixo x
    ax1.tick_params(axis='y', labelsize=18)  # Tamanho da fonte no eixo y

    # Adicionando os números aos pontos no gráfico
    for i, txt in enumerate(enumerated_elements):
        ax1.annotate(i+1, (borda_values["score"][i], fusion_values["MAP"][i]), textcoords="offset points", xytext=(5,5), ha='center')

    # Configuração global do tamanho da fonte
 

    # Crie uma lista de handles para cada ponto no gráfico
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green' if color == 'green' else 'blue', markersize=10) for color in colors]

    # Criando legend_labels modificados
    legend_labels_modificados = []

    for txt in legend_labels:
        # Substituindo '_' por espaço
        txt = txt.replace('_', ' ')

        # Substituindo termos específicos por novos valores
        txt = txt.replace('swimtf', 'Swintf')
        txt = txt.replace('swintf', 'Swintf')
        txt = txt.replace('vit-b16', 'VIT-B16')

        # Removendo termos indesejados
        termos_indesejados = ['rks', 'original', 'corel5k', 'flowers', 'CNN-', 'base224']
        for termo in termos_indesejados:
            txt = txt.replace(termo, '')

        # Removendo espaços extras
        txt = ' '.join(txt.split())

        legend_labels_modificados.append(txt)

    
    # Verificando se o top_k é maior que 7 para dividir em colunas
    if top_m > 5:
        num_linhas = len(legend_labels_modificados) // 2 + len(legend_labels_modificados) % 2
        colunas = 2
        legenda_em_colunas = []
        for i in range(colunas):
            start = i * num_linhas
            end = min((i + 1) * num_linhas, len(legend_labels_modificados))
            legenda_em_colunas.append(legend_labels_modificados[start:end])

        # Legenda personalizada no segundo subplot (ax2) em múltiplas colunas
        ax2.axis('off')
        ax2.set_title('Descritores',verticalalignment='center',horizontalalignment='center', fontsize= 24)

        for i, coluna in enumerate(legenda_em_colunas):
            ax2.text(i * 0.5, 0.5, '\n'.join(coluna), verticalalignment='center', transform=ax2.transAxes, fontsize= 23)


    # Caso contrário, se o top_k for menor ou igual a 7, manter uma coluna normal na legenda
    else:
        ax2.axis('off')
        ax2.legend(handles, legend_labels_modificados, loc='center')
        ax2.set_title('Descritores',verticalalignment='center')
        # Legenda personalizada no segundo subplot (ax2)

    

    # Ajustando o layout para evitar sobreposição
    plt.tight_layout()
    plotname = output_dataset_path.split("/")[-1]
    # Depois de criar o gráfico, use savefig para salvar como imagem
    plt.savefig(f'{output_dataset_path}/{plotname}.png')

    # Mostrando os subplots
    #plt.show()


    return