from PCA_effectiveness import *
from pyUDLF.utils import evaluation


def get_effectiveness_func(effectiveness_estimation_measure):
    if effectiveness_estimation_measure == "authority":
        return compute_authority_score

    if effectiveness_estimation_measure == "reciprocal":
        return compute_reciprocal_score

    print("\n ERROR: Unknown effec. estim. measure:", effectiveness_estimation_measure)
    exit(1)


def get_dataset_size(classes_file_path: str):
    # Try open text file to count the classes
    try:
        data = open(classes_file_path, "r")
    except:
        # If file couldn't be oppened return a message
        fileName = classes_file_path.split("/")[-1]
        print(f"The file {fileName} couldn't be found to count function!")
        exit()

    elements = []

    # Create a list for all elements in the file
    for el in data:
        elements.append(el)

    # Compute number of classes, the result is the dataset size
    dataset_size = len(elements)

    # Clear the elements list
    elements.clear()

    return dataset_size


def get_precion_and_recall(ranked_lists: list, class_list: list, N: int):
    precion, precion_list = evaluation.compute_precision(ranked_lists, class_list, N)
    recall, recall_list = evaluation.compute_recall(ranked_lists, class_list, N)

    return precion, precion_list, recall, recall_list


def get_MAP(ranked_lists: list, class_list: list, dataset_size: int):
    MAP, MAP_list = evaluation.compute_map(ranked_lists, class_list, dataset_size)

    return MAP, MAP_list
