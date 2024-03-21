import PyCascadeAggreg.pca_utils as utils
import PyCascadeAggreg.pca_savefiles as savefile
from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
import pandas as pd
from collections import OrderedDict
import os, math


def read_list_top_m(dataset_path: str, output_dataset_path: str, effectiveness_score: str, top_m: int):
    
    dataset_name = dataset_path.split("/")[-1]

    file = f"{output_dataset_path}/{dataset_name}.csv"
    
    data_frame = pd.DataFrame(pd.read_csv(file, delimiter=";"))

    descriptors = []

    if effectiveness_score == "borda score":
        # Ordene os elementos por pontuação em ordem decrescente
        data_frame = data_frame.sort_values(by=effectiveness_score, ascending=True)
    else:
        # Ordene os elementos por pontuação em ordem decrescente
        data_frame = data_frame.sort_values(by=effectiveness_score,ascending=False)

    descriptors = data_frame['descriptor'].values

    descriptors = [element for element in descriptors]

    descriptors = descriptors[:top_m]

    return descriptors

def first_layer_fusion(list_method: str, dataset_path: str, evall_mode: str, top_m: int, output_dataset_path: str, output_rk_fusion_path: str, lists_file_path: str, classes_file_path: str, l_size: int):
    
    print("\nIniciado o processo de agregação da primeira camada...")

    input_data = inputType.InputType()
    rootDir = os.getcwd()

    udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
    udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

    dataset_name = dataset_path.split("/")[-1]

    dataset_size = utils.get_dataset_size(classes_file_path)

    input_data.set_task("FUSION")
    input_data.set_method_name(list_method.upper())
    input_data.set_ranked_lists_size(dataset_size)
    input_data.set_dataset_size(dataset_size)
    input_data.set_param("INPUT_FILE_FORMAT", "RK")
    input_data.set_output_rk_format("NUM")
    input_data.set_output_file_format("RK")
    input_data.set_ranked_lists_size(l_size)
    input_data.set_classes_file(classes_file_path)
    input_data.set_lists_file(lists_file_path)
#    input_data.write_config(f"{output_dataset_path}/config_{dataset_name}.ini")
    if list_method.upper() == "RDPAC":
        rdpac_l = int(l_size//2)
        input_data.set_param("PARAM_RDPAC_L", rdpac_l)

    descriptors = read_list_top_m(dataset_path, output_dataset_path, evall_mode, top_m)


    dataset_path = dataset_path + "/ranked_lists/"

    data_results = []

    for index_one, layer_one_descriptor in enumerate(descriptors):
        
        file_layer_one = os.path.join(dataset_path, f"{layer_one_descriptor}.txt")

        for index_two, layer_two_descriptor in enumerate(descriptors[index_one + 1:]):
            
            file_layer_two = os.path.join(dataset_path, f"{layer_two_descriptor}.txt")

            file_one = file_layer_one.split("/")[-1].split(".")[0]
            file_two = file_layer_two.split("/")[-1].split(".")[0]

            print(f"Agregando as listas {file_one} + {file_two}")

            input_data.set_input_files([file_layer_one, file_layer_two])

            path_out = f"{output_rk_fusion_path}/{file_one}+{file_two}"
            input_data.set_output_file_path(path_out)

            input_data.write_config(f"{output_dataset_path}/config_{dataset_name}.ini")

            output = udlf.run(input_data, get_output=True)


            #print(path_out)
            #print(output.get_rks())
            # Getting the log values from the output
            return_values = output.get_log()
            
            fusion_key = "descriptor"
            fusion_desc = f"{file_one}+{file_two}"

            #output.print_log()

            order_dict = OrderedDict(return_values)
            order_dict = OrderedDict([(fusion_key, fusion_desc)] + list(order_dict.items()))
            return_values = dict(order_dict)

            data_results.append(return_values)
        
        field_keys = return_values.keys()
        savefile.save_layer_one_aggreg(output_dataset_path, dataset_name, field_keys, data_results)


    print("Finalizado com sucesso!")

    return


def second_layer_fusion(list_method: str, dataset_path: str, evall_mode: str, output_dataset_path: str, output_rk_fusion_path: str, alpha: float, lists_file_path: str, classes_file_path: str, fisrt_layer_method: str, top_m: int, l_size: int, top_m_type: str):
    
    print("\nIniciado o processo de agregação da segunda camada...")

    input_data = inputType.InputType()
    rootDir = os.getcwd()

    udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
    udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

    dataset_name = dataset_path.split("/")[-1]

    dataset_size = utils.get_dataset_size(classes_file_path)

    ranked_lists_files = [file for file in os.listdir(output_rk_fusion_path)]

    match top_m_type.lower():
        case "exit_fusions": 
            top_m = int(math.ceil(len(os.listdir(output_rk_fusion_path)) * alpha))
        case "alpha_m": 
            top_m = int(math.ceil(top_m * alpha))
        case "m_raw": 
            top_m = top_m
        case _: 
            print("\nOpção de seleção de elementos da segunda camada não identificado!")
            exit()

    descriptors = read_list_top_m(f"{dataset_path}_cascade", output_dataset_path, evall_mode, top_m)
    
    ranked_lists = []
    for rk in ranked_lists_files:
        rk_noex = rk.split(".txt")[0]
        if rk_noex in descriptors:
            ranked_lists.append(f"{output_rk_fusion_path}/{rk}")

    input_data.set_task("FUSION")
    input_data.set_method_name(list_method.upper())
    input_data.set_ranked_lists_size(l_size)
    input_data.set_dataset_size(dataset_size)
    input_data.set_param("INPUT_FILE_FORMAT", "RK")
    input_data.set_output_rk_format("NUM")
    input_data.set_output_file_format("RK")
    input_data.set_classes_file(classes_file_path)
    input_data.set_lists_file(lists_file_path)
    input_data.set_param("NUM_INPUT_FUSION_FILES", top_m)
    input_data.set_output_file_path(f"{output_dataset_path}/cascaded_{dataset_name}")
    input_data.set_input_files(ranked_lists)
    input_data.write_config(f"{output_dataset_path}/finalconfig_{dataset_name}.ini")
    input_data.set_param("OUTPUT_LOG_FILE_PATH",f"{output_dataset_path}/result_cascade.txt")
    
    if list_method.upper() == "RDPAC" and fisrt_layer_method.upper() == "RDPAC": 
        rdpac_l = int(l_size//4)
        input_data.set_param("PARAM_RDPAC_L", rdpac_l)
    elif list_method.upper() == "RDPAC" and fisrt_layer_method.upper() != "RDPAC": 
        rdpac_l = int(l_size//2)
        input_data.set_param("PARAM_RDPAC_L", rdpac_l)
    elif list_method.upper() == "CPRR" and fisrt_layer_method.upper() == "RDPAC": 
        cprr_l = int(l_size//2)
        input_data.set_param("PARAM_CPRR_L", cprr_l)
         
    output = udlf.run(input_data, get_output=True)
    return_values = output.get_log()

    MAP_value = return_values["MAP"]

    print("Finalizado com sucesso!")
    
    return MAP_value, top_m
