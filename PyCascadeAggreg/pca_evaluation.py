from pyUDLF.utils import evaluation


# Funcão para calcular precion e recall
def get_precion_and_recall(ranked_lists: list, class_list: list, N: int):
    precion, precion_list = evaluation.compute_precision(ranked_lists, class_list, N)
    recall, recall_list = evaluation.compute_recall(ranked_lists, class_list, N)

    return precion, precion_list, recall, recall_list

# Funcão para calcular MAP (Mean Average Preciosion)
def get_MAP(ranked_lists: list, class_list: list, dataset_size: int):
    MAP, MAP_list = evaluation.compute_map(ranked_lists, class_list, dataset_size)

    return MAP, MAP_list

# Funcão para calcular ganho
def get_gain(before_rankedlist: list, after_rankedlist: list, classes_list: list, depth: int):

    gain_list,gain_mean_percent, gain_mean = evaluation.compute_gain(before_rankedlist, after_rankedlist, classes_list, depth)

    return gain_list,gain_mean_percent, gain_mean
