import pandas as pd
import matplotlib.pyplot as plt

def plot_dot_graph(output_dataset_path: str, dataset_name: str, top_k: int, top_m: int): 

    try:
        # Carrega os dados do CSV de descritores isolados
        descriptors_dataset = pd.read_csv(f"{output_dataset_path}/{dataset_name}.csv")
    except:
        print(f"Não foi possível localizar o arquivo {dataset_name}.csv")
    
    try:
        # Carrega os dados do CSV de descritores isolados
        fusion_values = pd.read_csv(f"{output_dataset_path}/{dataset_name}_cascade.csv")
    except:
        print(f"Não foi possível localizar o arquivo {dataset_name}_cascade.csv")
    
    # Encontrando o maior valor da coluna "MAP" no arquivo de descritores isolados
    best_MAP = descriptors_dataset["MAP"].max()

    # Lê os campos "descriptor" e "borda score" do dataframe e em seguida ordena pela coluna "borda score"
    borda_values = fusion_values[["descriptor", "borda score"]]
    #borda_values = borda_values.sort_values(by="borda score")

    # Criando uma lista vazia para armazenar as cores
    colors = []  

    # Criar uma lista numerada para os elementos
    enumerated_elements = [f"{i+1}. {txt}" for i, txt in enumerate(borda_values["descriptor"])]

    # Adicionando o valor do ponto e definindo a cor
    for i, txt in enumerate(fusion_values["descriptor"]):
        
        if fusion_values["MAP"][i] >= best_MAP:
            # Adicionando 'green' para valores maiores que best_MAP
            colors.append('green')  
        else:
            # Adicionando 'blue' para valores menores que best_MAP
            colors.append('blue')  

    #name_txt = txt.split(f"{dataset_name}_")[1].split(f"_topK={top_k}")[0]

    # Crie rótulos personalizados com números e name_txt
    legend_labels = [f"{i+1}. {txt}" for i, txt in enumerate(borda_values["descriptor"])]
    #legend_labels = [f"{i+1}. {txt.split(f'{dataset_name}_')[1].split(f'_topK={top_k}')[0]}" for i, txt in enumerate(fusion_values["descriptor"])]

     # Crie uma lista de handles para cada ponto no gráfico
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green' if color == 'green' else 'blue', markersize=10) for color in colors]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 12))
    
    plt.rc('font', size=22)

    # Gráfico no primeiro subplot (ax1)
    scatter = ax1.scatter(borda_values["borda score"], fusion_values["MAP"], c=colors)
    ax1.axhline(y=best_MAP, color='red', linestyle='--', label="Melhor descritor isolado")
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
        ax1.annotate(i+1, (borda_values["borda score"][i], fusion_values["MAP"][i]), textcoords="offset points", xytext=(5,5), ha='center')

    # Configuração global do tamanho da fonte
 

    # Crie uma lista de handles para cada ponto no gráfico
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green' if color == 'green' else 'blue', markersize=10) for color in colors]

    # Criando legend_labels modificados
    modify_legend_labels = []

    for txt in legend_labels:
        # Substituindo '_' por espaço
        txt = txt.replace('_', ' ')
        txt = txt.replace("+", " + ")

        # Substituindo termos específicos por novos valores
        txt = txt.replace('swimtf', 'Swintf')
        txt = txt.replace('swintf', 'Swintf')
        txt = txt.replace('vit-b16', 'VIT-B16')

        # Removendo termos indesejados
        regex_terms = ['rks', 'original', 'corel5k', 'flowers', 'CNN-','cnn-', 'base224']
        for word in regex_terms:
            txt = txt.replace(word, '')

        # Removendo espaços extras
        txt = ' '.join(txt.split())

        modify_legend_labels.append(txt)

    
    # Verificando se o top_m é maior que 7 para dividir em colunas
    if top_m > 5:
        num_linhas = len(modify_legend_labels) // 2 + len(modify_legend_labels) % 2
        colunas = 2
        legenda_em_colunas = []
        for i in range(colunas):
            start = i * num_linhas
            end = min((i + 1) * num_linhas, len(modify_legend_labels))
            legenda_em_colunas.append(modify_legend_labels[start:end])

        # Legenda personalizada no segundo subplot (ax2) em múltiplas colunas
        ax2.axis('off')
        ax2.set_title('Descritores',verticalalignment='center',horizontalalignment='center', fontsize= 24)

        for i, coluna in enumerate(legenda_em_colunas):
            ax2.text(i * 0.5, 0.5, '\n'.join(coluna), verticalalignment='center', transform=ax2.transAxes, fontsize= 23)


    # Caso contrário, se o top_k for menor ou igual a 7, manter uma coluna normal na legenda
    else:
        ax2.axis('off')
        ax2.legend(handles, modify_legend_labels, loc='center')
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