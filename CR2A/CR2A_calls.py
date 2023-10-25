import CR2A.CR2A_aggregate as aggregate
import CR2A.CR2A_utils as utils
import CR2A.CR2A_effectiveness as effectiv
import os
from itertools import zip_longest

def call_cascating_aggregagtion(dataset_name: str, top_k: int, top_m: int, list_method_final: str, list_method_cascade: str, number_combinations, outlayer: str, mode="b"):

    output_log_path, output_dataset_path, output_rk_fusion_path, output_result, output_top_k_results = utils.paths_validations(
        dataset_name, top_k, top_m, outlayer, mode)

    # rootDir: str -> root path of code
    rootDir = os.getcwd()

    dataset_path = f"{rootDir}/dataset/{dataset_name}"

    utils.get_all_eval(dataset_path, output_dataset_path, outlayer)

    authority, reciprocal = effectiv.get_effectiveness_rk(f"{dataset_path}/ranked_lists", top_k, outlayer)

    utils.call_save_effectiveness(
        dataset_name, authority, reciprocal, top_k, output_dataset_path)

    aggregate.cascade_aggregate(list_method_cascade, dataset_path, mode, top_k,
                                top_m, output_log_path, output_dataset_path, output_rk_fusion_path)

    if top_m > 2:
        cascate_size = int(utils.get_factorial(top_m)/(utils.get_factorial(top_m -
                        number_combinations)*utils.get_factorial(number_combinations)))
    elif top_m == 2:
        cascate_size = 1
    else:
        print("The cascading calculation cannot be performed with a top M value of less than 2!")
        exit()

    aggregate.final_cascade_aggregate(list_method_final, dataset_path, top_m, output_rk_fusion_path, cascate_size, output_result)
    
    authority,reciprocal = effectiv.get_effectiveness_rk(output_rk_fusion_path, top_k, outlayer)
    
    cascade_descriptors = os.listdir(output_rk_fusion_path)

    result = [[desc, auth, rec] for desc, auth, rec in zip_longest(cascade_descriptors, authority.values(), reciprocal.values(), fillvalue="NULL")]

    utils.call_save_effectiveness(dataset_name,authority, reciprocal, top_k,output_dataset_path, True, result)

    topm_descriptors = aggregate.read_list_top_m(dataset_path, output_dataset_path, utils.set_mode_file(mode), top_k, top_m, True)

    utils.call_copy_topm_files(topm_descriptors, output_rk_fusion_path, output_log_path, output_top_k_results)

    aggregate.final_cascade_aggregate(list_method_final, dataset_path, top_m,output_top_k_results, top_m, output_dataset_path)

    return
