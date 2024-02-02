from pyUDLF.utils import readData
import os, csv, shutil, json, math
import pandas as pd
import PyCascadeAggreg.pca_evaluation as evall
import PyCascadeAggreg.pca_savefiles as savefiles

# Função que valida o valor minimo do top m e o valor setado para a estimativa de eficácia
def validate_data(top_m: int, number_combinations: int, evall_mode: str):
    
    #Validação do valor minimo para a agregação por cascata
    if top_m > 2:
        cascade_size = math.comb(top_m, number_combinations)
    else:
        print("O cálculo da agregação por cascateamento não pode ser efetuado com um top m menor que 3!")
        exit()
    
    #Switch para definição e validação do modo de estimativa a ser considerado
    match evall_mode.upper():
        case "B":
            evall_mode = "borda score"
        case "A":
            evall_mode = "authority"
        case "R":
            evall_mode = "reciprocal"
        case _:
            print("\nOpção de estimativa de eficácia (Borda (b), Authority(a) ou Reciprocal(r)) não reconhecida!")
            exit()    

    return cascade_size, evall_mode

# Função responsável por criar as pastas necessárias
def paths_creations(dataset_name: str, top_k: int, top_m: int, outlayer: str, mode: str, agg_method_layer_one: str,agg_method_layer_two: str):

    if mode == "borda score":
        mode="borda_score"

    rootDir = os.getcwd()
    output_path = f"{rootDir}/output"
    output_dataset_path = f"{output_path}/output_{dataset_name}_layerone-{agg_method_layer_one}_layertwo-{agg_method_layer_two}_{outlayer}_topk{top_k}_topm{top_m}_{mode}"
    output_rk_fusion_path = f"{output_dataset_path}/rk_fusions_{dataset_name}"
    output_final_result = f"{output_dataset_path}/rk_cascaded_{dataset_name}_topk={top_k}"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists("./output"):
        os.makedirs("./output")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists(output_rk_fusion_path):
        os.makedirs(output_rk_fusion_path)

    if not os.path.exists(output_final_result):
        os.mkdir(output_final_result)


    return output_dataset_path, output_rk_fusion_path, output_final_result

# Função responsável por obter e armazenar o endereço dos arquivos de listas e classes
def get_lists_and_classes_txt(input_path: str):

    print("\nIdentificando arquivos de listas e classes...")

    # Tenta localizar o caminho informado
    try:
        files = os.listdir(input_path)
    except:
        # Caso não consiga localizar o caminho retorna uma mensagem
        print(f"O Caminho {input_path} não foi localizado!")
        exit()

    # Armazena em um vetor todos os arquivos txt que contenham "_lists.txt" 
    files_list_txt = [
        file_list_txt for file_list_txt in files if "_lists.txt" in file_list_txt]
    # Armazena em uma variavél o valor do último arquivo do vetor gerado anteriormente (Apenas deve conter um arquivo com o nome de lists e classes no dataset)
    for file_list_txt in files_list_txt:
        list_file_path = os.path.join(input_path, file_list_txt)

     # Armazena em um vetor todos os arquivos txt que contenham "_classes.txt" 
    files_classes_txt = [
        file_classes_txt for file_classes_txt in files if "_classes.txt" in file_classes_txt]
    # Armazena em uma variavél o valor do último arquivo do vetor gerado anteriormente (Apenas deve conter um arquivo com o nome de lists e classes no dataset)
    for file_classes_txt in files_classes_txt:
        classes_file_path = os.path.join(input_path, file_classes_txt)

    print("Done!")

    return list_file_path, classes_file_path

# Função que calcula o tamanho do dataset
def get_dataset_size(lists_file_path: str):

    # Tenta abrir o arquivo de de listas informado
    try:
        data = open(lists_file_path, "r")
    except:
        # Caso o arquivo não seja localizado retorna a mensagem
        fileName = lists_file_path.split("/")[-1]
        print(f"\nO arquivo {fileName} não pode ser localizado para a função de cálculo do tamanho do dataset!")
        exit()

    # Cria uma lista com todos os elementos do arquivo de listas
    elements = []
    [elements.append(element) for element in data]

    # Calcula a quantidade de elementos contidos nessa lista, o resultado é o tamanho do dataset
    dataset_size = len(elements)

    # limpa o vetor de elementos
    elements.clear()

    return dataset_size

# Função para aplicação dos filtros outlayer
def set_filter_outlayer(file_list: list, option: str):

    # Identificação da raiz da execução
    rootDir = os.getcwd()

    # Switch case para definir o tipo de outlayer escolhido
    match option.lower():
        
        case "outlayer_file":
            outlayer = f"{rootDir}/outlayer.txt"

            try:
                with open(outlayer, "r") as data:
                    outlayer = [element.strip() for element in data.readlines()]
                print("\nLista de outlayers lida com sucesso!")
            except:
                print(
                f"\nOutlayer {outlayer} não localizado, a execução ocorrerá sem aplicação de filtro!")
            outlayer = []
        
            descriptors = [element for element in file_list if element not in outlayer]
        
        case "only_nn_descriptors":
            
            print("\nFiltrando ranqueadores CNN e Transformers!")
            descriptors = [element for element in file_list if "CNN-" in element or "rks_" in element]
        
        case "only_classic_descriptors":

            print("\nFiltrando ranqueadores clássicos!")
            descriptors = [element for element in file_list if "CNN-" not in element and "rks_" not in element]

        case _:
            print("\nOpção de filtragem desconhecida!")
            exit()
        
    return descriptors

def get_borda_ranked_lists(dataset_name: str, output_dataset_path: str): 

    print("\nCalculando a contagem de Borda das estimativas de eficácia...")

    file = f"{output_dataset_path}/{dataset_name}"

    try:
        data_frame = pd.read_csv(f"{file}.csv")
    except:
        # If file couldn't be oppened return a message
        print(f"{file}.csv couldn't be found!")
        exit()

    authority_sort = data_frame.sort_values(by="authority", ascending=False)
    authority_sort = authority_sort.reset_index(drop=True)

    reciprocal_sort = data_frame.sort_values(by="reciprocal", ascending=False)
    reciprocal_sort = reciprocal_sort.reset_index(drop=True)

    # Crie uma estrutura de dados para armazenar a contagem de votos (pontuações) para cada elemento
    score = {}

    concat_data_frame = pd.concat([authority_sort, reciprocal_sort])

    # Calcule a pontuação de Borda Count para cada elemento
    for index, row in concat_data_frame.iterrows():
        descriptor = row[
            "descriptor"
        ]  # Substitua 'Elemento' pelo nome da coluna apropriada
        if descriptor in score:
            score[descriptor] += index  # Soma a posição
        else:
            score[descriptor] = index

    # Converta a estrutura de dados de pontuação em um DataFrame
    df_score = pd.DataFrame(list(score.items()), columns=[
                            "descriptor", "borda score"])

    
    # Ordene os elementos por pontuação em ordem decrescente
    df_score = df_score.sort_values(by="descriptor")
    df_score = df_score.reset_index(drop=True)

    #print (df_score)
    borda_score = df_score['borda score']

    savefiles.save_borda_score(file, borda_score)

    file = file.split("/")[-1]
    print(f"Arquivo {file} Atualizado com sucesso!")

    return

def get_all_eval(input_path: str,  output_dataset_path: str, outlayer: str):

    # Coletando a string do nome do dataset
    dataset_name = input_path.split("/")[-1]

    # Definindo a pasta destino de saida da execução
    output_file_path = os.path.join(output_dataset_path, dataset_name)

    # Coleta os arquivos de lista e classes
    list_file_path, classes_file_path = get_lists_and_classes_txt(input_path)

    # Calcula o tamanho do dataset
    dataset_size = get_dataset_size(list_file_path)

    # Definie a pasta de entrada
    input_path = input_path + "/ranked_lists"

    # Lê e ordena os arquivos após a aplicação do filtro
    files = set_filter_outlayer(os.listdir(input_path), outlayer)
    files.sort()

    # Chama a função de salvamento do arquivo CSV
    savefiles.save_results_evalluation(output_file_path, files, input_path,list_file_path, classes_file_path, dataset_size)

    return 