from CR2A.CR2A_utils import *
from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
import pandas as pd
from enum import Enum
import os
import json


def read_list_top_m(dataset_path: str, list_complement: str, top_k: int, top_m: int):

    dataset_name = dataset_path.split("/")[-1]

    file = f"./dataset/{dataset_name}/outlayer.txt"

    try:
        with open(file, "r") as data:
            outlayer = [element.strip() for element in data.readlines()]
        print("The outlayer list has been read successfully!")
    except:
        print(
            f"Outlayer {file} not found, then the process will run without filtering!")
        outlayer = []

    file = f"./output/{dataset_name}_effectiveness_{list_complement}_topk={top_k}.txt"

    data_frame = pd.DataFrame(pd.read_csv(file))

    descriptors = []

    descriptors = data_frame['descriptor'].values

    descriptors = [
        element for element in descriptors if element not in outlayer]

    descriptors = descriptors[:top_m]

    return descriptors


def cascade_aggregate(dataset_path: str, option: str, top_k: int, top_m: int):

    match option.upper():
        case "B":
            aggregate_file_type = "borda"
        case "A":
            aggregate_file_type = "authority"
        case "R":
            aggregate_file_type = "reciprocal"
        case _:
            print("Unknown option for effectiveness topk file!")

    input_data = inputType.InputType()
    rootDir = os.getcwd()

    udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
    udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

    dataset_name = dataset_path.split("/")[-1]
    if not os.path.exists(f"./output/output_{dataset_name}"):
        os.makedirs(f"./output/output_{dataset_name}")

    if not os.path.exists(f"./output/logs_{dataset_name}"):
        os.makedirs(f"./output/logs_{dataset_name}")

    lists_file_path, classes_file_path = get_lists_and_classes_txt(
        dataset_path)

    dataset_size = get_dataset_size(classes_file_path)

    input_data.set_task("FUSION")
    input_data.set_ranked_lists_size(dataset_size)
    input_data.set_dataset_size(dataset_size)
    input_data.set_output_rk_format("NUM")
    input_data.set_output_file_format("RK")
    input_data.list_method_info("CPRR")
    input_data.set_classes_file(classes_file_path)
    input_data.set_lists_file(lists_file_path)
    input_data.write_config(f"./output/config_{dataset_name}.ini")

    descriptors = read_list_top_m(
        dataset_path, aggregate_file_type, top_k, top_m)

    dataset_path = dataset_path + "/ranked_lists/"

    for index_one, layer_one_descriptor in enumerate(descriptors):
        file_layer_one = dataset_path + f"{layer_one_descriptor}.txt"

        for index_two, layer_two_descriptor in enumerate(descriptors[index_one + 1:]):
            file_layer_two = dataset_path + f"{layer_two_descriptor}.txt"

            file_one = file_layer_one.split("/")[-1].split(".")[0]
            file_two = file_layer_two.split("/")[-1].split(".")[0]
            input_data.set_output_file_path(
                f"./output/output_{dataset_name}/{dataset_name}_{file_one}+{file_two}_topK={top_k}_topM={top_m}")

            input_data.set_input_files([file_layer_one, file_layer_two])

            output = udlf.run(input_data, get_output=True)

            # Getting the log values from the output
            return_values = output.get_log()



            with open(f"./output/logs_{dataset_name}/{dataset_name}_{file_one}+{file_two}_topK={top_k}_topM={top_m}.json", "w") as file:
                file.write(json.dumps(return_values))

    return
