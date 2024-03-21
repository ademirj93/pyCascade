import pandas as pd
import os, csv
from pyUDLF.utils import readData
import PyCascadeAggreg.pca_utils as utils
import PyCascadeAggreg.pca_evaluation as evall


def save_results_evalluation(output_file_path: str, files: list, input_path: str,list_file_path: str, classes_file_path:str, dataset_size: int,l_size: int, N=5):
        
    header = ["descriptor", "precision", "recall", "MAP"]

    with open(output_file_path + ".csv", "w", newline="") as csv_file:
        csv_writter = csv.writer(
            csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONE
        )

        csv_writter.writerow(header)

    for file in files:
        input_file_path = os.path.join(input_path, file)

        with open(input_file_path, "r") as input_file:
            content = input_file.read()

        # Reading the class and ranked lists from the files
        class_list = readData.read_classes(list_file_path, classes_file_path)
        ranked_list = readData.read_ranked_lists_file_numeric(
            input_file_path, top_k=dataset_size
        )

        precision, precision_list, recall, recall_list = evall.get_precion_and_recall(
            ranked_list, class_list, N)
        MAP, MAP_list = evall.get_MAP(ranked_list, class_list, l_size)

        result = [file.split(".")[0], precision, recall, MAP]

        with open(output_file_path + ".csv", "a", newline="") as csv_file:
            csv_writter = csv.writer(
                csv_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONE
            )

            csv_writter.writerow(result)
    return

def save_effectiveness_scores(file_name: str, authority_score: dict, reciprocal_score: dict, output_dataset_path: str):

    file = f"{output_dataset_path}/{file_name}.csv"

    try:
        data_frame = pd.read_csv(file, delimiter=";")
    except:
        # If file couldn't be oppened return a message
        print(f"\n{file} não localizado!")
        exit()

    if "authority" not in data_frame.columns:
        data_frame["authority"] = None

    if "reciprocal" not in data_frame.columns:
        data_frame["reciprocal"] = None

    data_frame["authority"] = authority_score.values()
    data_frame["reciprocal"] = reciprocal_score.values()

    data_frame.to_csv(file, index=False, sep=';')

    print(f"Arquivo {file.split('/')[-1]} atualizado com sucesso!")

    return

def save_borda_score(file_name: str, borda_score: list):

    file = f"{file_name}.csv"

    try:
        # Abre o arquivo CSV em modo de leitura para ler as linhas existentes
        with open(file, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            lines = list(csv_reader)
            fieldnames = csv_reader.fieldnames

        # Coluna na qual os valores serão inseridos
        column_name = 'borda score'

        # Adiciona a nova coluna ao fieldnames se não existir
        if column_name not in fieldnames:
            fieldnames.append(column_name)

        # Atualiza as linhas existentes com os valores da lista na coluna especificada
        for line, value in zip(lines, borda_score):
            line[column_name] = value

        # Escreve as linhas atualizadas de volta no arquivo CSV
        with open(file, 'w', newline='') as csv_file:
            escritor_csv = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            escritor_csv.writeheader()
            escritor_csv.writerows(lines)

        print(f"Dados atualizados em {file}")

    except FileNotFoundError:
        print(f"Arquivo {file} não localizado!")
    
    
    
def save_layer_one_aggreg(output_dataset_path: str, dataset_name: str, field_keys: list, return_values: list):


    output_file_path = f"{output_dataset_path}/{dataset_name}_cascade.csv"
    with open(output_file_path, "w") as file:        
        csv_writer = csv.DictWriter(file, fieldnames= field_keys, delimiter=";")
        csv_writer.writeheader()
        

    for value in return_values:
   
        with open(output_file_path, "a") as file:
                
            csv_writer = csv.DictWriter(file, fieldnames= field_keys, delimiter=";")
            csv_writer.writerow(value)


    try:
        data_frame = pd.read_csv(output_file_path, delimiter=";")
        
        # Ordena o DataFrame pelo valor da coluna "descriptor"
        data_frame_sorted = data_frame.sort_values(by="descriptor", ascending=True)

        # Salva o DataFrame ordenado de volta no arquivo CSV original
        data_frame_sorted.to_csv(output_file_path, index=False, sep=';')  # Não inclui o índice no arquivo CSV

    except:
        # If file couldn't be oppened return a message
        file = output_file_path.split("/")[-1]
        print(f"{file} não localizado!")
        exit()

    return

def save_index(date_ex: str, csv_index_file: str, agg_index: str, dataset_name: str, agg_method_layer_one: str, agg_method_layer_two: str, outlayer: str, top_k: int, top_m: int,top_m_lt_type: str, top_m_lt: int, alpha: float , effectiveness_mode: str,  l_size: int, map_result: float, run_time: float ,data_full_path: str):

    with open(csv_index_file, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([date_ex ,agg_index, dataset_name, agg_method_layer_one, agg_method_layer_two, outlayer, top_k, top_m, top_m_lt_type, top_m_lt, alpha, effectiveness_mode, l_size, map_result, run_time,data_full_path]) 

    return