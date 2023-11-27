import CR2A.CR2A_evaluation as evall
from pyUDLF.utils import readData
import os, csv, shutil, json
import pandas as pd


def paths_validations(dataset_name: str, top_k: int, top_m: int, outlayer: str, mode: str, list_method_cascade: str,list_method_final: str):

    rootDir = os.getcwd()
    output_path = f"{rootDir}/output"
    output_dataset_path = f"{output_path}/output_{dataset_name}_layerone-{list_method_cascade}_layertwo-{list_method_final}_{outlayer}_topk={top_k}_topm={top_m}{mode}"
    output_log_path = f"{output_dataset_path}/logs_{dataset_name}_topk={top_k}"
    output_rk_fusion_path = f"{output_dataset_path}/rk_fusions_{dataset_name}_topk={top_k}"
    output_final_result = f"{output_dataset_path}/rk_cascaded_{dataset_name}_topk={top_k}"
    output_top_m_results = f"{output_dataset_path}/topm_rk_cascaded_{dataset_name}_topk={top_k}"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists("./output"):
        os.makedirs("./output")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists(output_log_path):
        os.makedirs(output_log_path)

    if not os.path.exists(output_rk_fusion_path):
        os.makedirs(output_rk_fusion_path)

    if not os.path.exists(output_final_result):
        os.mkdir(output_final_result)

    if not os.path.exists(output_top_m_results):
        os.mkdir(output_top_m_results)

    return output_log_path, output_dataset_path, output_rk_fusion_path, output_final_result, output_top_m_results


def set_mode_file(option: str):

    match option.upper():
        case "B":
            aggregate_file_type = "borda"
        case "A":
            aggregate_file_type = "authority"
        case "R":
            aggregate_file_type = "reciprocal"
        case _:
            print("\nUnknown option for effectiveness topk file!")
            exit()

    return aggregate_file_type


def get_dataset_size(classes_file_path: str):

    # Try open text file to count the classes
    try:
        data = open(classes_file_path, "r")
    except:
        # If file couldn't be oppened return a message
        fileName = classes_file_path.split("/")[-1]
        print(f"\nThe file {fileName} couldn't be found to count function!")
        exit()

    # Create a list for all elements in the file
    elements = []
    [elements.append(element) for element in data]

    # Compute number of classes, the result is the dataset size
    dataset_size = len(elements)

    # Clear the elements list
    elements.clear()

    return dataset_size


def get_lists_and_classes_txt(input_path: str):

    print("\nGetting lists and classes files...")

    try:
        files = os.listdir(input_path)
    except:
        # If file couldn't be oppened return a message
        print(f"The way {input_path} couldn't be found!")
        exit()

    files_list_txt = [
        file_list_txt for file_list_txt in files if "_lists.txt" in file_list_txt]
    for file_list_txt in files_list_txt:
        list_file_path = os.path.join(input_path, file_list_txt)

    files_classes_txt = [
        file_classes_txt for file_classes_txt in files if "_classes.txt" in file_classes_txt]
    for file_classes_txt in files_classes_txt:
        classes_file_path = os.path.join(input_path, file_classes_txt)

    print("Done!")

    return list_file_path, classes_file_path


def aggregate_ranked_lists(
    dataset_name: str, output_dataset_path: str
):

    print("\nEvaluation aggregation started...")

    file = f"{output_dataset_path}/{dataset_name}"

    try:
        data_frame = pd.read_csv(f"{file}.csv")
    except:
        # If file couldn't be oppened return a message
        print(f"{file}.csv couldn't be found!")
        exit()

    map_sort = data_frame.sort_values(by="MAP", ascending=False)
    map_sort = map_sort.reset_index(drop=True)

    precision_sort = data_frame.sort_values(by="precision", ascending=False)
    precision_sort = precision_sort.reset_index(drop=True)

    recall_sort = data_frame.sort_values(by="recall", ascending=False)
    recall_sort = recall_sort.reset_index(drop=True)

    # Crie uma estrutura de dados para armazenar a contagem de votos (pontuações) para cada elemento
    score = {}

    concat_data_frame = pd.concat([map_sort, precision_sort, recall_sort])

    # Calcule a pontuação de Borda Count para cada elemento
    for index, row in concat_data_frame.iterrows():
        descriptor = row[
            "descriptor"
        ]  # Substitua 'Elemento' pelo nome da coluna apropriada
        if descriptor in score:
            score[descriptor] += index  # Soma a posição
        else:
            score[descriptor] = index

    # Converta a estrutura de dados de pontuação em um DataFrame
    df_score = pd.DataFrame(list(score.items()), columns=[
                            "descriptor", "score"])

    # Ordene os elementos por pontuação em ordem decrescente
    df_score = df_score.sort_values(by="score")
    df_score = df_score.reset_index(drop=True)

    # print(df_score)

    df_score.to_csv(f"{file}_evall_borda.txt", sep=",")

    print("Done!")

    return


def aggregate_ranked_lists_effectiveness(
    dataset_name: str, top_k: int, output_dataset_path: str
):

    print(f"\nAggregation effectiveness values started...")

    file = f"{output_dataset_path}/{dataset_name}"

    try:
        data_frame = pd.read_csv(f"{file}.csv")
    except:
        # If file couldn't be oppened return a message
        print(f"{file}.csv couldn't be found!")
        exit()

    authority_sort = data_frame.sort_values(by="authority", ascending=False)
    authority_sort = authority_sort.reset_index(drop=True)

    authority_sort[["descriptor", "authority"]].to_csv(
        f"{file}_effectiveness_authority_topk={top_k}.txt", sep=","
    )

    print(f"\n{file}_effectiveness_authority_topk={top_k}.txt sucefully created")

    reciprocal_sort = data_frame.sort_values(by="reciprocal", ascending=False)
    reciprocal_sort = reciprocal_sort.reset_index(drop=True)

    reciprocal_sort[["descriptor", "reciprocal"]].to_csv(
        f"{file}_effectiveness_reciprocal_topk={top_k}.txt", sep=","
    )

    print(f"{file}_effectiveness_reciprocal_topk={top_k}.txt sucefully created")

    # Crie uma estrutura de dados para armazenar a contagem de votos (pontuações) para cada elemento
    score = {}

    concat_data_frame = pd.concat([authority_sort, reciprocal_sort])

    # Calcule a pontuação de Borda Count para cada elemento
    for index, row in concat_data_frame.iterrows():
        descriptor = row[
            "descriptor"
        ]  # Substitua 'Elemento' pelo nome da coluna apropriada
        if descriptor in score:
            score[descriptor] += index  # Soma a posição
        else:
            score[descriptor] = index

    # Converta a estrutura de dados de pontuação em um DataFrame
    df_score = pd.DataFrame(list(score.items()), columns=[
                            "descriptor", "score"])

    # Ordene os elementos por pontuação em ordem decrescente
    df_score = df_score.sort_values(by="score")
    df_score = df_score.reset_index(drop=True)

    # print(df_score)

    df_score.to_csv(f"{file}_effectiveness_borda_topk={top_k}.txt", sep=",")
    print(f"{file}_effectiveness_borda_topk={top_k}.txt sucefully created")

    print("done")

    return


def save_effectiveness_scores(dataset_name: str, authority_score: dict, reciprocal_score: dict, output_dataset_path: str):

    file = f"{output_dataset_path}/{dataset_name}.csv"

    try:
        data_frame = pd.read_csv(file)
    except:
        # If file couldn't be oppened return a message
        print(f"\n{file} couldn't be found!")
        exit()

    if "authority" not in data_frame.columns:
        data_frame["authority"] = None

    if "reciprocal" not in data_frame.columns:
        data_frame["reciprocal"] = None

    data_frame["authority"] = authority_score.values()
    data_frame["reciprocal"] = reciprocal_score.values()

    data_frame.to_csv(file)

    print(f"\nFile {file.split('/')[-1]} updated successfully!")

    return


def save_effectiveness_result(dataset_name: str, output_dataset_path: str, results: list):

    header = ["descriptor", "authority", "reciprocal"]

    with open(f"{output_dataset_path}/{dataset_name}_after_cascade.csv", "w", newline="") as csv_file:
        csv_writter = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writter.writerow(header)

    for result in results:

        with open(f"{output_dataset_path}/{dataset_name}_after_cascade.csv", "a", newline="") as csv_file:
            csv_writter = csv.writer(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            csv_writter.writerow(result)

    return

def set_filter_outlayer(file_list: list, option: str):

    rootDir = os.getcwd()

    match option.lower():
        
        case "outlayer_file":
            outlayer = f"{rootDir}/outlayer.txt"

            try:
                with open(outlayer, "r") as data:
                    outlayer = [element.strip() for element in data.readlines()]
                print("\nThe outlayer list has been read successfully!")
            except:
                print(
                f"\nOutlayer {outlayer} not found, then the process will run without filtering!")
            outlayer = []
        
        
            descriptors = [element for element in file_list if element not in outlayer]
        
        case "only_nn_descriptors":
            
            print("\nFiltering ranked lists of CNN and Transformers!")
            descriptors = [element for element in file_list if "CNN-" in element or "rks_" in element]
        
        case "only_classic_descriptors":

            print("\nFiltering ranked lists of classic descriptors!")
            descriptors = [element for element in file_list if "CNN-" not in element and "rks_" not in element]

        case _:
            print("\nUnknown option for filtering!")
            exit()
        
    return descriptors

def get_all_eval(input_path: str,  output_dataset_path: str, outlayer: str, N=5):


    dataset_name = input_path.split("/")[-1]

    output_file_path = os.path.join(output_dataset_path, dataset_name)

    list_file_path, classes_file_path = get_lists_and_classes_txt(input_path)

    # Setting dataset
    dataset_size = get_dataset_size(classes_file_path)

    input_path = input_path + "/ranked_lists"

    files = set_filter_outlayer(os.listdir(input_path), outlayer)

    files.sort()

    header = ["descriptor", "precision", "recall", "MAP"]

    with open(output_file_path + ".csv", "w", newline="") as csv_file:
        csv_writter = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
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
        MAP, MAP_list = evall.get_MAP(ranked_list, class_list, dataset_size)

        result = [file.split(".")[0], precision, recall, MAP]

        with open(output_file_path + ".csv", "a", newline="") as csv_file:
            csv_writter = csv.writer(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            csv_writter.writerow(result)

    aggregate_ranked_lists(dataset_name,  output_dataset_path)

    return 


def call_save_effectiveness(dataset_name: str, authority: dict, reciprocal: dict, top_k: int, output_dataset_path: str, filtering=False, result=[]):

    if not filtering:
        save_effectiveness_scores(
            dataset_name, authority, reciprocal, output_dataset_path)

        aggregate_ranked_lists_effectiveness(
            dataset_name, top_k, output_dataset_path)
    elif filtering:

        save_effectiveness_result(dataset_name, output_dataset_path, result)

        aggregate_ranked_lists_effectiveness(
            f"{dataset_name}_after_cascade", top_k, output_dataset_path)

    return

def call_copy_topm_files(topm_descriptors:list, output_rk_fusion_path: str, output_log_path: str,output_top_k_results: str):

    for descriptor in topm_descriptors:
        
        origin_log = os.path.join(output_log_path, descriptor.split(".")[0]+".json")
        origin_rk = os.path.join(output_rk_fusion_path, descriptor)

        destiny_log = os.path.join(output_top_k_results, descriptor.split(".")[0]+".json")
        destiny_rk = os.path.join(output_top_k_results, descriptor)

        descriptor_desc = descriptor.split('.')[0]

        try:
            shutil.copy(origin_rk, destiny_rk)
            #print(f'Files txt of {descriptor_desc} sucessfuly copied!')
        except FileNotFoundError:
            print(f'Files txt of {descriptor_desc} do not exist!' )
        except FileExistsError:
            print(f'Files txt of {descriptor_desc} already exist!')
    
        try:
            shutil.copy(origin_log, destiny_log)
            #print(f'Files json of {descriptor_desc} sucessfuly copied!')
        except FileNotFoundError:
            print(f'Files json of {descriptor_desc} do not exist!' )
        except FileExistsError:
            print(f'Files json of {descriptor_desc} already exist!')

    return

def orderbymap_csv(dataset_name: str, outuput_dataset_path: str):
    

    dataframe = pd.read_csv(f"{outuput_dataset_path}/{dataset_name}.csv")

    dataframe = dataframe.sort_values(by="MAP", ascending=False)
    dataframe = dataframe.reset_index(drop=True)

    dataframe[["descriptor","precision","recall","MAP","authority","reciprocal"]].to_csv(f"{outuput_dataset_path}/{dataset_name}.csv", index=False)
    
    best_isolated = dataframe["descriptor"].iloc[0]

    return best_isolated

def computing_gain (dataset_path: str, output_dataset_path: str, best_isolated: str, topM: int):

    print(f"Computing gain between {best_isolated} and the result of cascade process...")

    
    dataset_name = dataset_path.split("/")[-1]

    rkslist, classes_list = get_lists_and_classes_txt(dataset_path)

    dataset_size = get_dataset_size(classes_list)

    classes_list = readData.read_classes(rkslist, classes_list)

    before_rankedlist = readData.read_ranked_lists_file_numeric(f"{dataset_path}/ranked_lists/{best_isolated}.txt", dataset_size)
    after_rankedlist = readData.read_ranked_lists_file_numeric(f"{output_dataset_path}/cascaded_{dataset_name}_topM={topM}.txt", dataset_size)

    

    gain_list,gain_mean_percent, gain_mean  = evall.get_gain(before_rankedlist,after_rankedlist, classes_list, dataset_size)

    return gain_list,gain_mean_percent, gain_mean


def jsons_to_CSV(output_log_path: str, output_dataset_path: str, complement: str):
    
    # Lista para armazenar os dados a serem salvos no CSV
    csv_data = []

    # Itera pelos arquivos no diretório
    for file in os.listdir(output_log_path):
        if file.endswith('.json'):
            file_way = os.path.join(output_log_path, file)

            # Abre o arquivo JSON e lê seus dados
            with open(file_way, 'r') as f:
                json_data = json.load(f)

            # Obtém o título do arquivo
            file_title = os.path.splitext(file)[0]

            # Cria um dicionário para armazenar os valores
            values = {"descriptor": file_title}

            # Adiciona os valores das chaves ao dicionário
            for key, value in json_data.items():
                values[key] = value

            # Adiciona os valores a serem salvos no CSV
            csv_data.append(values)

    # Reorganiza a ordem das colunas para ter "descriptor" como a primeira coluna
    ordered_columns = ["descriptor"] + [col for col in csv_data[0] if col != "descriptor"]

    # Ordena os dados pela coluna "MAP"
    ordered_csv_data = sorted(csv_data, key=lambda x: float(x.get('MAP', 0)), reverse=True)

    # Caminho para salvar o arquivo CSV
    csv_way = f'{output_dataset_path}/fusion_values_{complement}.csv'

    # Salva os dados em um arquivo CSV
    with open(csv_way, 'w', newline='', encoding='utf-8') as csv_file:
        escritor_csv = csv.DictWriter(csv_file, fieldnames=ordered_columns)
        escritor_csv.writeheader()
        escritor_csv.writerows(ordered_csv_data)

    shutil.rmtree(output_log_path)

    return