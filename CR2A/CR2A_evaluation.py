from pyUDLF.utils import evaluation


def get_precion_and_recall(ranked_lists: list, class_list: list, N: int):
    precion, precion_list = evaluation.compute_precision(ranked_lists, class_list, N)
    recall, recall_list = evaluation.compute_recall(ranked_lists, class_list, N)

    return precion, precion_list, recall, recall_list


def get_MAP(ranked_lists: list, class_list: list, dataset_size: int):
    MAP, MAP_list = evaluation.compute_map(ranked_lists, class_list, dataset_size)

    return MAP, MAP_list

#def get_gain()
