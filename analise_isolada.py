from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
import os


input_data = inputType.InputType()
rootDir = os.getcwd()

udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

dataset_name = "corel5k"

lists_file_path = f"{rootDir}/dataset/corel5k/corel5k_lists.txt"
classes_file_path = f"{rootDir}/dataset/corel5k/corel5k_classes.txt"
list_method = "rdpac"
dataset_size = 5000

ranked_list_one = f"{rootDir}/dataset/corel5k/ranked_lists/rks_swimtf_base224_original_corel5k.txt"
ranked_list_two = f"{rootDir}/dataset/corel5k/ranked_lists/rks_VIT-B16_original_corel5k.txt"


input_data.set_task("FUSION")
input_data.set_method_name(list_method.upper())
input_data.set_ranked_lists_size(dataset_size)
input_data.set_dataset_size(dataset_size)
input_data.set_param("INPUT_FILE_FORMAT", "RK")
input_data.set_output_rk_format("NUM")
input_data.set_output_file_format("RK")
input_data.set_classes_file(classes_file_path)
input_data.set_lists_file(lists_file_path)
input_data.set_param("NUM_INPUT_FUSION_FILES", 2)
input_data.set_output_file_path(
    f"analise_{dataset_name}")
input_data.set_input_files([ranked_list_one,ranked_list_two])
input_data.write_config(
    f"config_analise_{dataset_name}_cascaded.ini")
output = udlf.run(input_data, get_output=True)

# Getting the log values from the output
return_values = output.get_log()