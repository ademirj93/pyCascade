import PyCascadeAggreg.pca_calls as pca_calls


dataset_name = "oxford17flowers"
top_k = 80
top_m = 3


#NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE
agg_method_layer_one = "rdpac"
agg_method_layer_two = "cprr"

# Método a ser considerado na estimativa de eficácia b - borda / a - authority / r - reciprocal
evall_mode = "b"

# Opções de outlayer: Utilizando o arquivo txt de validação ("outlayer_file")/ Considerar apenas redes neurais ("only_nn_descriptors")/ Considerar apenas os descritors classicos ("only_classic_descriptors")
outlayer = "only_nn_descriptors"

# Número de elementos que serão combinados durante a primeira camada de fusão em cada iteração
number_combinations = 2

# Chamada da execução do código
pca_calls.cascade_execute(dataset_name, top_k, top_m, agg_method_layer_one, agg_method_layer_two, outlayer, number_combinations, evall_mode)