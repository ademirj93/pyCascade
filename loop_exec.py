import os
import PyCascadeAggreg.pca_calls as pca_calls

rootDir = os.getcwd()

datasets = {"corel5k":100}

#NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE
methods_layer_one = ["rdpac"]
methods_layer_two = ["cprr"]

# Opções de outlayer: Utilizando o arquivo txt de validação ("outlayer_file")/ Considerar apenas redes neurais ("only_nn_descriptors")/ Considerar apenas os descritors classicos ("only_classic_descriptors")
outlayer = "only_nn_descriptors"

# Número de elementos que serão combinados durante a primeira camada de fusão em cada iteração
number_combinations = 2

# Método a ser considerado na estimativa de eficácia b - borda / a - authority / r - reciprocal
evall_mode = "b"

# Percentagem de listas combinadas que serão consideradas na segunda etapa de fusão
alpha_values = [0.3]

# Parâmetro L responsável pela seleção do comprimento da ranked list
l_sizes = [5000]
    
for dataset_name, top_k in datasets.items():
    for l_size in l_sizes:
        for agg_method_layer_one in methods_layer_one:

            for agg_method_layer_two in methods_layer_two:

                for alpha in alpha_values:

                    for top_m in range(8, 10, 1):   
                
                        pca_calls.cascade_execute(dataset_name, top_k, top_m, agg_method_layer_one, agg_method_layer_two, outlayer, number_combinations, evall_mode, float(alpha), int(l_size))
    
        old_way = f"{rootDir}/dataset/{dataset_name}/ranked_lists"
        new_way = f"{rootDir}/dataset/{dataset_name}/ranked_lists_l_size{l_size}"

        if os.path.exists(old_way):
            try:
                os.rename(old_way, new_way)
                print("Pasta renomeada com sucesso!")
            except OSError as e:
                print(f"Erro ao renomear a pasta: {e}")