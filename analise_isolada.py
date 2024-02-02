from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
import os


def get_lists_and_classes_txt(input_path: str):

    print("\nIdentificando arquivos de listas e classes...")

    # Tenta localizar o caminho informado
    try:
        files = os.listdir(input_path)
    except:
        # Caso não consiga localizar o caminho retorna uma mensagem
        print(f"O Caminho {input_path} não foi localizado!")
        exit()

    # Armazena em um vetor todos os arquivos txt que contenham "_lists.txt" 
    files_list_txt = [
        file_list_txt for file_list_txt in files if "_lists.txt" in file_list_txt]
    # Armazena em uma variavél o valor do último arquivo do vetor gerado anteriormente (Apenas deve conter um arquivo com o nome de lists e classes no dataset)
    for file_list_txt in files_list_txt:
        list_file_path = os.path.join(input_path, file_list_txt)

     # Armazena em um vetor todos os arquivos txt que contenham "_classes.txt" 
    files_classes_txt = [
        file_classes_txt for file_classes_txt in files if "_classes.txt" in file_classes_txt]
    # Armazena em uma variavél o valor do último arquivo do vetor gerado anteriormente (Apenas deve conter um arquivo com o nome de lists e classes no dataset)
    for file_classes_txt in files_classes_txt:
        classes_file_path = os.path.join(input_path, file_classes_txt)

    print("Done!")

    return list_file_path, classes_file_path

input_data = inputType.InputType()
rootDir = os.getcwd()

udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

dataset_name = "corel5k"
dataset_path = f"{rootDir}/dataset/{dataset_name}"

lists_file_path, classes_file_path = get_lists_and_classes_txt(dataset_path)
list_method = "RDPAC"
dataset_size = 5000

ranked_list_one = f"{dataset_path}/rks_VIT-B16_original_corel5k.txt"
ranked_list_two = f"{dataset_path}/rks_swimtf_base224_original_corel5k.txt"


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
input_data.set_param("OUTPUT_LOG_FILE_PATH",f"{rootDir}/analise_log.txt")

if list_method.upper() == "RDPAC":
    rdpac_l = int(dataset_size//2)
    input_data.set_param("PARAM_RDPAC_L", dataset_size/2)

input_data.set_output_file_path(
    f"analise_{dataset_name}")
input_data.set_input_files([ranked_list_one,ranked_list_two])
input_data.write_config(
    f"{rootDir}/config_analise_{dataset_name}_cascaded.ini")


output = udlf.run(input_data, get_output=True)


# Getting the log values from the output
return_values = output.get_log()