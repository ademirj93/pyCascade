import PCA_utils as utils
import os, csv, shutil, json
import pandas as pd

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

def call_save_effectiveness(dataset_name: str, authority: dict, reciprocal: dict, top_k: int, output_dataset_path: str, filtering=False, result=[]):

    if not filtering:
        save_effectiveness_scores(
            dataset_name, authority, reciprocal, output_dataset_path)

        utils.aggregate_ranked_lists_effectiveness(
            dataset_name, top_k, output_dataset_path)
    elif filtering:

        save_effectiveness_result(dataset_name, output_dataset_path, result)

        utils.aggregate_ranked_lists_effectiveness(
            f"{dataset_name}_after_cascade", top_k, output_dataset_path)

    return