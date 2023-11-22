import CR2A.CR2A_aggregate as aggregate
import CR2A.CR2A_utils as utils
import CR2A.CR2A_effectiveness as effectiv
import CR2A.CR2A_plotlib as plotlib
import os, math, shutil
from itertools import zip_longest

def call_cascating_aggregagtion(dataset_name: str,top_k: int, top_m: int, list_method_cascade: str, list_method_final: str, outlayer: str, number_combinations=2, mode="b"):


    # rootDir: str -> root path of code
    rootDir = os.getcwd()

    dataset_path = f"{rootDir}/dataset/{dataset_name}"

    output_log_path, output_dataset_path, output_rk_fusion_path, output_result, output_top_m_results = utils.paths_validations(
        dataset_name, top_k, top_m, outlayer, mode, list_method_cascade.upper(), list_method_final.upper())



    print("\nGetting values from precision, recall and MAP...")


    utils.get_all_eval(dataset_path, output_dataset_path, outlayer)


    #authority, reciprocal = effectiv.get_effectiveness_rk(f"{dataset_path}/ranked_lists", top_k, outlayer)

    authority = effectiv.compute_descriptors_effectiveness("authority", top_k, f"{dataset_path}/ranked_lists", outlayer)
    reciprocal = effectiv.compute_descriptors_effectiveness("reciprocal", top_k, f"{dataset_path}/ranked_lists", outlayer)

    print("\nSaving the results of authority and reciprocal...")

    utils.call_save_effectiveness(
        dataset_name, authority, reciprocal, top_k, output_dataset_path)

    print("\nFirst step of cascade aggregation started...")

    aggregate.cascade_aggregate(list_method_cascade.upper(), dataset_path, mode, top_k,
                                top_m, output_log_path, output_dataset_path, output_rk_fusion_path)

    if top_m > 2:
        cascate_size = math.comb(top_m, number_combinations)
    else:
        print("The cascading calculation cannot be performed with a top M value of less than 2!")
        exit()

    print(f"\nThe size of cascade is equals {cascate_size}")

    print("\nSecond step of cascade aggregation started...")

    aggregate.final_cascade_aggregate(list_method_final.upper(), dataset_path, top_m, output_rk_fusion_path, cascate_size, output_result)
    
    #authority,reciprocal = effectiv.get_effectiveness_rk(output_rk_fusion_path, top_k, outlayer)

    authority = effectiv.compute_descriptors_effectiveness("authority", top_k, output_rk_fusion_path, outlayer)
    reciprocal = effectiv.compute_descriptors_effectiveness("reciprocal", top_k, output_rk_fusion_path, outlayer)

    cascade_descriptors = os.listdir(output_rk_fusion_path)

    result = [[desc, auth, rec] for desc, auth, rec in zip_longest(cascade_descriptors, authority.values(), reciprocal.values(), fillvalue="NULL")]

    utils.call_save_effectiveness(dataset_name,authority, reciprocal, top_k,output_dataset_path, True, result)

    print("\nSaving the results of authority and reciprocal...")

    print("\nGetting top m descriptors")

    topm_descriptors = aggregate.read_list_top_m(dataset_path, output_dataset_path, utils.set_mode_file(mode), top_k, top_m, True)

    print("\nCoping json and txt for top m descriptors...")

    utils.call_copy_topm_files(topm_descriptors, output_rk_fusion_path, output_log_path, output_top_m_results)

    print("\nLast step of cascade aggregation started...")

    aggregate.final_cascade_aggregate(list_method_final.upper(), dataset_path, top_m,output_top_m_results, top_m, output_dataset_path)

    best_isolated = utils.orderbymap_csv(dataset_name, output_dataset_path)

    gain_list,gain_mean_percent, gain_mean = utils.computing_gain(dataset_path, output_dataset_path, best_isolated, top_m)

    print("\nThe cascade process has been complete!")

    gain_log = f"The gain between the best single descriptor and the cascade method was equal to {gain_mean} ({gain_mean_percent}%)"

    print(gain_log)

    with open(f'{output_dataset_path}/gain_log.txt', 'w') as log_file:
        log_file.write(gain_log)


    utils.jsons_to_CSV(output_log_path ,output_dataset_path, "all_fusions")

    utils.jsons_to_CSV(output_top_m_results, output_dataset_path, "top_m_fusions")
    
    shutil.rmtree(output_rk_fusion_path)

    for current_path, subpaths, files in os.walk(output_dataset_path):
        for file in files:
            file_way = os.path.join(current_path, file)
            if file.endswith('.txt') and (os.path.getsize(file_way) > (100 * 1024)):  # 100 KB em bytes:
                os.remove(file_way)
                print(f"Arquivo {file_way} removido com sucesso.")

    plotlib.plot_dot_graph(output_dataset_path, dataset_name, top_k)

    return
