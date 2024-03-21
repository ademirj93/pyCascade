import os
import PyCascadeAggreg.pca_calls as pca_calls

rootDir = os.getcwd()

datasets = {"corel5k":(100, [5000, 2500])}

#NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE
methods_layer_one = ["rdpac"]
methods_layer_two = ["cprr"]

methods_topm_lt = ["exit_fusions", "alpha_m", "m_raw"]
# Opções de outlayer: Utilizando o arquivo txt de validação ("outlayer_file")/ Considerar apenas redes neurais ("only_nn_descriptors")/ Considerar apenas os descritors classicos ("only_classic_descriptors")
outlayer = "only_nn_descriptors"

# Número de elementos que serão combinados durante a primeira camada de fusão em cada iteração
number_combinations = 2

# Método a ser considerado na estimativa de eficácia b - borda / a - authority / r - reciprocal
evall_mode = "b"

# Percentagem de listas combinadas que serão consideradas na segunda etapa de fusão
alpha_start = 0.2
alpha_end = 0.9

def exec_calls(dataset_name: str, top_k: int, agg_method_layer_one: str, agg_method_layer_two:str , outlayer: str, number_combinations: int, evall_mode:str , alpha: float, l_size: int, method_topm_lt: str):


    for top_m in range(3, 10, 1):   

        pca_calls.cascade_execute(dataset_name, top_k, top_m, agg_method_layer_one, agg_method_layer_two, outlayer, number_combinations, evall_mode, float(alpha), int(l_size), method_topm_lt)

    return

for dataset_name, values in datasets.items():
    
    top_k = values[0]
    l_sizes = values[1]

    for l_size in l_sizes:
        for agg_method_layer_one in methods_layer_one:

            for agg_method_layer_two in methods_layer_two:
                
                for method_topm_lt in methods_topm_lt:
                    
                    alpha_start = 0.2
                    alpha_end = 0.9


                    if methods_topm_lt == "m_raw":
                        alpha = 0.1
                        exec_calls(dataset_name, top_k, agg_method_layer_one, agg_method_layer_two, outlayer, number_combinations, evall_mode , alpha , l_size, method_topm_lt)
                    else:
                        
                        if methods_topm_lt == "alpha_m":
                            alpha_end = alpha_end + 1
                        
                        alpha = alpha_start
                        while alpha <= alpha_end:
                            exec_calls(dataset_name, top_k, agg_method_layer_one, agg_method_layer_two, outlayer, number_combinations, evall_mode , alpha , l_size, method_topm_lt)
                            alpha = alpha + 0.1
        
        old_way = f"{rootDir}/dataset/{dataset_name}/ranked_lists"
        new_way = f"{rootDir}/dataset/{dataset_name}/ranked_lists_l_size{l_size}"

        if os.path.exists(old_way):
            try:
                os.rename(old_way, new_way)
                print("Pasta renomeada com sucesso!")
            except OSError as e:
                print(f"Erro ao renomear a pasta: {e}")