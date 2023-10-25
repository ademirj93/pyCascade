import CR2A.CR2A_calls as call


dataset_name = "oxford17flowers"
top_k = 80
top_m = 5


#NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE
list_method_cascade = "RFE"
list_method_final = "CPRR"

# mode = b - borda / a - authority / r - reciprocal {For default mode is "b" to calculate borda ranking}
# outlayer options "outlayer_file"/"only_nn_descriptors"/"only_classic_descriptors"
call.call_cascating_aggregagtion(dataset_name, top_k, top_m, list_method_cascade, list_method_final, number_combinations=2, outlayer="only_nn_descriptors")

