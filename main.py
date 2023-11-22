import CR2A.CR2A_calls as call

#datasets = {"oxford17flowers": 80, "corel5k":100}
#methods = ["rlsim", "lhrr", "cprr", "rdpac"]

# outlayer options "outlayer_file"/"only_nn_descriptors"/"only_classic_descriptors"
#outlayer = "only_nn_descriptors"
#list_method_final = "cprr"
#for dataset_name, top_k in datasets.items():

#    for list_method_cascade in methods:

#        for top_m in range(3, 10, 2):   
    
#            call.call_cascating_aggregagtion(dataset_name,top_k, top_m, list_method_cascade, list_method_final, outlayer)

dataset_name = "oxford17flowers"
top_k = 80
top_m = 10


#NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE
list_method_cascade = "rdpac"
list_method_final = "cprr"

# b - borda / a - authority / r - reciprocal {For default mode is "b" to calculate borda ranking}
# mode = "a" 

# outlayer options "outlayer_file"/"only_nn_descriptors"/"only_classic_descriptors"
outlayer = "only_nn_descriptors"

call.call_cascating_aggregagtion(dataset_name,top_k, top_m, list_method_cascade, list_method_final, outlayer)