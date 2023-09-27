from CR2A.CR2A_func import *
from pyUDLF.utils import readData
import os
import csv


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

    header = ["file", "precision", "recall", "MAP"]

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

        result = [file, precision, recall, MAP]

        with open(output_file_path + ".csv", "a", newline="") as csv_file:
            csv_writter = csv.writer(
                csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            csv_writter.writerow(result)

    return
