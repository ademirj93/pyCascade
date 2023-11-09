import CR2A.CR2A_utils as utils
from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
import pandas as pd
import os, json


def read_list_top_m(dataset_path: str, output_dataset_path: str, list_complement: str, top_k: int, top_m: int, filtering=False):
    """
    Reads a CSV file containing a column of descriptors and returns a list of the top `top_m` descriptors.

    Args:
        dataset_path (str): The path to the dataset file.
        output_dataset_path (str): The path containing the results obtained by calculating the effectiveness estimate..
        list_complement (str): The complement of the list, i.e. which estimation mode will be considered between Authority, Reciprocall and the aggregation of both through the Borda methodology.
        top_k (int): The number of top elements considered in the effectiveness estimate.
        top_m (int): The number of top descriptors to return.
        filtering (bool, optional): Whether to apply filtering or not. Defaults to False.

    Returns:
        list: A list of the top `top_m` descriptors.
    """
    
    dataset_name = dataset_path.split("/")[-1]

    if not filtering:
        file = f"{output_dataset_path}/{dataset_name}_effectiveness_{list_complement}_topk={top_k}.txt"
    elif filtering:
        file = f"{output_dataset_path}/{dataset_name}_after_cascade_effectiveness_{list_complement}_topk={top_k}.txt"
    
    data_frame = pd.DataFrame(pd.read_csv(file))

    descriptors = []

    descriptors = data_frame['descriptor'].values

    descriptors = [element for element in descriptors]

    descriptors = descriptors[:top_m]

    return descriptors



def cascade_aggregate(list_method: str, dataset_path: str, option: str, top_k: int, top_m: int, output_log_path: str, output_dataset_path: str, output_rk_fusion_path: str):

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
    #input_data.list_method_info(list_method.upper())
    input_data.set_classes_file(classes_file_path)
    input_data.set_lists_file(lists_file_path)
    input_data.write_config(
        f"{output_dataset_path}/config_{dataset_name}.ini")

    descriptors = read_list_top_m(
        dataset_path, output_dataset_path, utils.set_mode_file(option), top_k, top_m)

    dataset_path = dataset_path + "/ranked_lists/"

    for index_one, layer_one_descriptor in enumerate(descriptors):
        file_layer_one = dataset_path + f"{layer_one_descriptor}.txt"

        for index_two, layer_two_descriptor in enumerate(descriptors[index_one + 1:]):
            file_layer_two = dataset_path + f"{layer_two_descriptor}.txt"

            file_one = file_layer_one.split("/")[-1].split(".")[0]
            file_two = file_layer_two.split("/")[-1].split(".")[0]
            input_data.set_output_file_path(
                f"{output_rk_fusion_path}/{dataset_name}_{file_one}+{file_two}_topK={top_k}_topM={top_m}")

            input_data.set_input_files([file_layer_one, file_layer_two])

            output = udlf.run(input_data, get_output=True)

            # Getting the log values from the output
            return_values = output.get_log()

            with open(f"{output_log_path}/{dataset_name}_{file_one}+{file_two}_topK={top_k}_topM={top_m}.json", "w") as file:
                file.write(json.dumps(return_values))

    return


def final_cascade_aggregate(list_method: str, dataset_path: str, top_m: int, output_rk_fusion_path: str, cascade_size: int, output_final_result: str):

    input_data = inputType.InputType()
    rootDir = os.getcwd()

    udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
    udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

    dataset_name = dataset_path.split("/")[-1]

    lists_file_path, classes_file_path = utils.get_lists_and_classes_txt(
        dataset_path)

    dataset_size = utils.get_dataset_size(classes_file_path)

    ranked_lists_files = [file for file in os.listdir(output_rk_fusion_path) if file.endswith(".txt")]
    ranked_lists = []

    for rk in ranked_lists_files:
        ranked_lists.append(f"{output_rk_fusion_path}/{rk}")

    input_data.set_task("FUSION")
    input_data.set_method_name(list_method.upper())
    input_data.set_ranked_lists_size(dataset_size)
    input_data.set_dataset_size(dataset_size)
    input_data.set_param("INPUT_FILE_FORMAT", "RK")
    input_data.set_output_rk_format("NUM")
    input_data.set_output_file_format("RK")
    #input_data.list_method_info(list_method.upper())
    input_data.set_classes_file(classes_file_path)
    input_data.set_lists_file(lists_file_path)
    input_data.set_param("NUM_INPUT_FUSION_FILES", cascade_size)
    input_data.set_output_file_path(
        f"{output_final_result}/cascaded_{dataset_name}_topM={top_m}")
    input_data.set_input_files(ranked_lists)
    input_data.write_config(
        f"{output_final_result}/config_{dataset_name}_cascaded.ini")
    output = udlf.run(input_data, get_output=True)

    # Getting the log values from the output
    return_values = output.get_log()

    with open(f"{output_final_result}/cacaded_{dataset_name}_topM={top_m}.json", "w") as file:
        file.write(json.dumps(return_values))

    return
