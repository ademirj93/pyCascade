import os
from itertools import zip_longest
import PyCascadeAggreg.pca_utils as utils

def cascade_execute(dataset_name: str,top_k: int, top_m: int, agg_method_layer_one: str, agg_method_layer_two: str, outlayer: str, number_combinations: int, evall_mode: str):
    
    # Valida o valor minimo do top M, calcula o tamanho da saida da cascata e valida o modo de estimativa de eficácia
    # cascade_size: int -> Número de elementos resultante da combinações da cascata
    # evall_mode: str
    cascade_size, evall_mode = utils.validate_data(top_m, number_combinations, evall_mode)
    
    # rootDir: str -> Pasta raiz do código
    rootDir = os.getcwd()

    # dataset-path: Str -> Caminho para pasta do dataset
    dataset_path = f"{rootDir}/dataset/{dataset_name}"

    # Cria as pastas caso necessário e armazena os caminhos nas varíaveis 
    output_log_path, output_dataset_path, output_rk_fusion_path, output_result, output_top_m_results = utils.paths_creations(
        dataset_name, top_k, top_m, outlayer, evall_mode, agg_method_layer_one.upper(), agg_method_layer_two.upper())
    
    

    return