import PyCascadeAggreg.pca_utils as utils
from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
import pandas as pd
from collections import OrderedDict
import os, json, csv


def read_list_top_m(dataset_path: str, output_dataset_path: str, effectiveness_score: str, top_m: int):
    
    dataset_name = dataset_path.split("/")[-1]

    file = f"{output_dataset_path}/{dataset_name}.csv"
    
    data_frame = pd.DataFrame(pd.read_csv(file))

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

def first_layer_fusion(list_method: str, dataset_path: str, evall_mode: str, top_m: int, output_dataset_path: str, output_rk_fusion_path: str):
    
    print("\nIniciado o processo de agregação da primeira camada...")

    input_data = inputType.InputType()
    rootDir = os.getcwd()

    udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
    udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

    dataset_name = dataset_path.split("/")[-1]

    lists_file_path, classes_file_path = utils.get_lists_and_classes_txt(
        dataset_path)

    dataset_size = utils.get_dataset_size(classes_file_path)

    input_data.set_task("FUSION")
    input_data.set_method_name(list_method.upper())
    input_data.set_ranked_lists_size(dataset_size)
    input_data.set_dataset_size(dataset_size)
    input_data.set_output_rk_format("NUM")
    input_data.set_output_file_format("RK")
    input_data.set_classes_file(classes_file_path)
    input_data.set_lists_file(lists_file_path)
    input_data.write_config(
        f"{output_dataset_path}/config_{dataset_name}.ini")

    descriptors = read_list_top_m(dataset_path, output_dataset_path, evall_mode, top_m)


    dataset_path = dataset_path + "/ranked_lists/"


    for index_one, layer_one_descriptor in enumerate(descriptors):
        
        file_layer_one = dataset_path + f"{layer_one_descriptor}.txt"

        for index_two, layer_two_descriptor in enumerate(descriptors[index_one + 1:]):
            
            file_layer_two = dataset_path + f"{layer_two_descriptor}.txt"

            file_one = file_layer_one.split("/")[-1].split(".")[0]
            file_two = file_layer_two.split("/")[-1].split(".")[0]

            input_data.set_output_file_path(
                f"{output_rk_fusion_path}/{dataset_name}_{file_one}_+_{file_two}")

            input_data.set_input_files([file_layer_one, file_layer_two])

            output = udlf.run(input_data, get_output=True)

            # Getting the log values from the output
            return_values = output.get_log()
            
            fusion_key = "descriptor"
            fusion_desc = f"{file_one} + {file_two}"

            order_dict = OrderedDict(return_values)
            order_dict = OrderedDict([(fusion_key, fusion_desc)] + list(order_dict.items()))
            return_values = dict(order_dict)

            field_keys = return_values.keys()

            if index_one == 1:
                with open(f"{output_dataset_path}/{dataset_name}_cascade.csv", "w") as file:
                   
                    csv_writer = csv.DictWriter(file, fieldnames= field_keys)
                    csv_writer.writeheader()
                    csv_writer.writerow(return_values)

            with open(f"{output_dataset_path}/{dataset_name}_cascade.csv", "a") as file:
                csv_writer = csv.DictWriter(file, fieldnames= field_keys)
            
                csv_writer.writerow(return_values)

    print("Finalizado com sucesso!")
    return