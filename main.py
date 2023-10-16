from CR2A.CR2A_calls import *


dataset_name = "oxford17flowers"
top_k = 100
top_m = 10

#mode = b - borda / a - authority / r - reciprocal {For default mode is "b" to calculate borda ranking}
call_cascating_aggregagtion(dataset_name, top_k, top_m)

