from multiprocessing import Pool
import PyCascadeAggreg.pca_utils as utils
import os
import numpy as np

# Função que lista os elementos dos descritores no diretório
def list_descriptors(path: str):
    # Lista os descritores 
    return [x[:-4] for x in sorted(os.listdir(path))]

# Função de calculo da estimativa Auhority
def compute_authority_score(ranked_lists, index, top_k):
    score = 0
    rk1 = np.array(ranked_lists[index][:top_k])
    
    for img1 in rk1:
        rk2 = np.array(ranked_lists[img1][:top_k])
        matches = np.isin(rk2, rk1)
        score += np.sum(matches)
        
    return (score / (top_k**2))

# Função de calculo da estimativa Reciprocal
def compute_reciprocal_score(ranked_lists, index, top_k):
    score = 0
    rk1 = np.array(ranked_lists[index][:top_k])
    
    for img1 in rk1:
        rk2 = np.array(ranked_lists[img1][:top_k])
        matches = np.isin(rk2, rk1)
        reciprocal_ranks = np.where(matches)[0] + 1
        score += np.sum(1 / reciprocal_ranks)
        
    return (score / (top_k**2))

# Função que retorna a estimativa de eficácia a ser utilizada
def get_effectiveness_func(effectiveness_estimation_measure):
    if effectiveness_estimation_measure == "authority":
        return compute_authority_score

    if effectiveness_estimation_measure == "reciprocal":
        return compute_reciprocal_score

    print("\nERROR: Medida de estimativa de eficácia não reconhecida!:",
          effectiveness_estimation_measure)
    exit(1)

def read_ranked_lists_file(descriptor: str, path_rks: str, top_k: int):
    file_path = os.path.join(path_rks, descriptor) + ".txt"
    #print("\tReading file", file_path)
    with open(file_path, "r") as file:
        return [[int(rank) for rank in line.strip().split(" ")][:top_k] for line in file.readlines()]
    
def load_ranked_lists(descriptors: list, path_rks: str, top_k: int):
    ranked_lists = {}

    print("\nCarregando listas ranqueadas...")
    for descriptor in descriptors:
        ranked_lists[descriptor] = read_ranked_lists_file(
            descriptor, path_rks, top_k)
    print("Finalizado com sucesso!")

    return ranked_lists

def compute_rk_effectiveness(effectiveness_function, ranked_lists, top_k):
    
    n = int(len(ranked_lists))
    
    total = 0
    
    for index in range(n):
        total += effectiveness_function(ranked_lists, index, top_k)
        
    return total / n

# Função para calcular e estimativa de eficácia das listas ranqueadas
def compute_descriptors_effectiveness(effectiveness_function:str, top_k: int, ranked_lists: dict, descriptors: list, n_pools = 4):
    
    print(f"\nCalculando {effectiveness_function} score...")
    
    # Chama a função de calculo de estimativa de eficácia 
    effectiveness_function = get_effectiveness_func(effectiveness_function)

    # Criando o dicionário para receber os dados
    effectiveness = {}

    # Criando os parâmetros para o multiprocessamento
    pool_params = [[effectiveness_function, ranked_lists[descriptor], top_k]
                   for descriptor in descriptors]
    
    with Pool(n_pools) as p:
        
        # Execução dos cáculos de eficácia através de multiprocessamento pelo starmap
        output_effectiveness = p.starmap(compute_rk_effectiveness, pool_params)

    # Varre os resultados e associa cada descritor a um valor de eficácia correspondente
    for i, descriptor in enumerate(descriptors):
        effectiveness[descriptor] = output_effectiveness[i]
    
    print(f"Finalizado com sucesso!\n")
    
    return effectiveness

# Função de chamada para calculo dos valores das estimativas de eficácia, com a finalidade de economizar processamento na leitura de dados
def call_compute_descriptors_effectiveness(top_k: int, input_path: str, outlayer: str):

    # Leitura e aplicação do filtro aos descritores
    descriptors = list_descriptors(input_path)
    descriptors = utils.set_filter_outlayer(descriptors, outlayer)
    descriptors.sort()

    # Carrega as listas ranquedas de cada descritor na variavel
    ranked_lists = load_ranked_lists(descriptors, input_path, top_k)

    print("\nCalculando estimativas de eficácia...")

    # Vetor com as estimativas que serão aplicadas
    effectiveness_functions = ["authority","reciprocal"]
    
    # Iteração para cada elemento do vetor
    for effectiveness_function in effectiveness_functions:

        # Armazena o resultado do cálculo na variável "result"
        result = compute_descriptors_effectiveness(effectiveness_function, top_k, ranked_lists, descriptors)
        
        # Switch para definir em qual estimativa o código esta iterando para armazenar o resultado na variável correta
        if effectiveness_function == "authority":
                authority = result
        elif effectiveness_function == "reciprocal":
                reciprocal = result

    print("Finalizado com sucesso!")

    return authority, reciprocal