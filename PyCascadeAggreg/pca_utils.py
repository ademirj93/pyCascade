from pyUDLF.utils import readData
import os, csv, shutil, json, math
import pandas as pd


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
            evall_mode = "borda"
        case "A":
            evall_mode = "authority"
        case "R":
            evall_mode = "reciprocal"
        case _:
            print("\nOpção de estimativa de eficácia (Borda (b), Authority(a) ou Reciprocal(r)) não reconhecida!")
            exit()    

    return cascade_size, evall_mode

def paths_creations(dataset_name: str, top_k: int, top_m: int, outlayer: str, mode: str, agg_method_layer_one: str,agg_method_layer_two: str):

    rootDir = os.getcwd()
    output_path = f"{rootDir}/output"
    output_dataset_path = f"{output_path}/output_{dataset_name}_layerone-{agg_method_layer_one}_layertwo-{agg_method_layer_two}_{outlayer}_topk={top_k}_topm={top_m}{mode}"
    output_log_path = f"{output_dataset_path}/logs_{dataset_name}_topk={top_k}"
    output_rk_fusion_path = f"{output_dataset_path}/rk_fusions_{dataset_name}_topk={top_k}"
    output_final_result = f"{output_dataset_path}/rk_cascaded_{dataset_name}_topk={top_k}"
    output_top_m_results = f"{output_dataset_path}/topm_rk_cascaded_{dataset_name}_topk={top_k}"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists("./output"):
        os.makedirs("./output")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists(output_log_path):
        os.makedirs(output_log_path)

    if not os.path.exists(output_rk_fusion_path):
        os.makedirs(output_rk_fusion_path)

    if not os.path.exists(output_final_result):
        os.mkdir(output_final_result)

    if not os.path.exists(output_top_m_results):
        os.mkdir(output_top_m_results)

    return output_log_path, output_dataset_path, output_rk_fusion_path, output_final_result, output_top_m_results