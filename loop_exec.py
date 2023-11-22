import CR2A.CR2A_calls as call

datasets = {"oxford17flowers": 80, "corel5k":100}
methods = ["rlsim", "lhrr", "cprr", "rdpac"]

# outlayer options "outlayer_file"/"only_nn_descriptors"/"only_classic_descriptors"
outlayer = "only_nn_descriptors"
list_method_final = "cprr"
for dataset_name, top_k in datasets.items():

    for list_method_cascade in methods:

        for top_m in range(3, 10, 2):   
    
           call.call_cascating_aggregagtion(dataset_name,top_k, top_m, list_method_cascade, list_method_final, outlayer)
