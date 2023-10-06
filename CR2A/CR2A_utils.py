from CR2A.CR2A_func import *
from CR2A.CR2A_effectiveness import *
from pyUDLF.utils import readData
import os, csv
import pandas as pd


def get_all_eval(input_path: str, N=5):
    fl = input_path.split("/")[-1]

    try:
        files = os.listdir(input_path)
    except:
        # If file couldn't be oppened return a message
        print(f"The way {input_path} couldn't be found!")
        exit()

    print(fl)
    output_file_path = os.path.join("./output", fl)

    files_list_txt = [flt for flt in files if "_lists.txt" in flt]
    for flt in files_list_txt:
        list_file_path = os.path.join(input_path, flt)

    files_classes_txt = [fct for fct in files if "_classes.txt" in fct]
    for fct in files_classes_txt:
        classes_file_path = os.path.join(input_path, fct)

    # Setting dataset
    dataset_size = get_dataset_size(classes_file_path)

    input_path = input_path + "/ranked_lists"

    files = os.listdir(input_path)

    header = ["descriptor", "precision", "recall", "MAP"]

    if not os.path.exists("./output"):
        os.makedirs("./output")

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

        precision, precision_list, recall, recall_list = get_precion_and_recall(
            ranked_list, class_list, N
        )
        MAP, MAP_list = get_MAP(ranked_list, class_list, dataset_size)

        result = [file.split(".")[0], precision, recall, MAP]

        with open(output_file_path + ".csv", "a", newline="") as csv_file:
            csv_writter = csv.writer(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            csv_writter.writerow(result)

    return


def aggregate_ranked_lists(
    dataset_name: str,
):
    file = f"./output/{dataset_name}"

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
    df_score = pd.DataFrame(list(score.items()), columns=["descriptor", "score"])

    # Ordene os elementos por pontuação em ordem decrescente
    df_score = df_score.sort_values(by="score")
    df_score = df_score.reset_index(drop=True)

    # print(df_score)

    df_score.to_csv(f"{file}_evall_borda.txt", sep=",")

    return


def aggregate_ranked_lists_effectiveness(
    dataset_name: str,
):
    file = f"./output/{dataset_name}"

    try:
        data_frame = pd.read_csv(f"{file}.csv")
    except:
        # If file couldn't be oppened return a message
        print(f"{file}.csv couldn't be found!")
        exit()

    authority_sort = data_frame.sort_values(by="authority", ascending=False)
    authority_sort = authority_sort.reset_index(drop=True)

    authority_sort[["descriptor", "authority"]].to_csv(
        f"{file}_effectiveness_authority.txt", sep=","
    )

    print(f"{file}_effectiveness_authority.txt sucefully created")

    reciprocal_sort = data_frame.sort_values(by="reciprocal", ascending=False)
    reciprocal_sort = reciprocal_sort.reset_index(drop=True)

    reciprocal_sort[["descriptor", "reciprocal"]].to_csv(
        f"{file}_effectiveness_reciprocal.txt", sep=","
    )

    print(f"{file}_effectiveness_reciprocal.txt sucefully created")

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
    df_score = pd.DataFrame(list(score.items()), columns=["descriptor", "score"])

    # Ordene os elementos por pontuação em ordem decrescente
    df_score = df_score.sort_values(by="score")
    df_score = df_score.reset_index(drop=True)

    # print(df_score)

    df_score.to_csv(f"{file}_effectiveness_borda.txt", sep=",")
    print(f"{file}_effectiveness_borda.txt sucefully created")
    return


def save_effectiveness_scores(
    dataset_name: str, authority_score: dict, reciprocal_score: dict
):
    file = f"./output/{dataset_name}.csv"

    try:
        data_frame = pd.read_csv(f"{file}")
    except:
        # If file couldn't be oppened return a message
        print(f"{file}.csv couldn't be found!")
        exit()

    if "authority" not in data_frame.columns:
        data_frame["authority"] = None

    if "reciprocal" not in data_frame.columns:
        data_frame["reciprocal"] = None

    data_frame["authority"] = authority_score.values()
    data_frame["reciprocal"] = reciprocal_score.values()

    data_frame.to_csv(file)

    print(f"File {file.split('/')[-1]} updated successfully!")

    return
