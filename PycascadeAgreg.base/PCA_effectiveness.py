from multiprocessing import Pool
import PCA_utils as utils
import os
import numpy as np


def list_descriptors(path):
    files = [os.path.splitext(file)[0] for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    files.sort()
    print(files)
    return files

#def list_descriptors(path):
#    return [x[:-4] for x in sorted(os.listdir(path))]


def get_effectiveness_func(effectiveness_estimation_measure):
    if effectiveness_estimation_measure == "authority":
        return compute_authority_score

    if effectiveness_estimation_measure == "reciprocal":
        return compute_reciprocal_score

    print("\n ERROR: Unknown effec. estim. measure:",
          effectiveness_estimation_measure)
    exit(1)

def read_ranked_lists_file(descriptor: str, path_rks: str, top_k: int):
    file_path = os.path.join(path_rks, descriptor) + ".txt"
    #print("\tReading file", file_path)
    with open(file_path, "r") as file:
        return [
            [int(rank) for rank in line.strip().split(" ")][:top_k]
            for line in file.readlines()
        ]


def load_ranked_lists(descriptors: list, path_rks: str, top_k: int):
    ranked_lists = {}

    print("\n Loading ranked lists...")
    for descriptor in descriptors:
        ranked_lists[descriptor] = read_ranked_lists_file(
            descriptor, path_rks, top_k)
    print(" Done!")

    return ranked_lists


import numpy as np

def compute_authority_score(ranked_lists, index, top_k):
    score = 0
    rk1 = np.array(ranked_lists[index][:top_k])
    
    for img1 in rk1:
        rk2 = np.array(ranked_lists[img1][:top_k])
        matches = np.isin(rk2, rk1)
        score += np.sum(matches)
        
    return (score / (top_k**2))


def compute_reciprocal_score(ranked_lists, index, top_k):
    score = 0
    rk1 = np.array(ranked_lists[index][:top_k])
    
    for img1 in rk1:
        rk2 = np.array(ranked_lists[img1][:top_k])
        matches = np.isin(rk2, rk1)
        reciprocal_ranks = np.where(matches)[0] + 1
        score += np.sum(1 / reciprocal_ranks)
        
    return (score / (top_k**2))


def compute_rk_effectiveness(effectiveness_function, ranked_lists, top_k):
    n = int(len(ranked_lists))
    total = 0
    
    for index in range(n):
        total += effectiveness_function(ranked_lists, index, top_k)
        
    return total / n


def compute_descriptors_effectiveness(effectiveness_function: str, top_k: int, input_path: str, outlayer: str, n_pools = 4):
    
    descriptors = list_descriptors(input_path)

    descriptors = utils.set_filter_outlayer(descriptors, outlayer)


    ranked_lists = load_ranked_lists(descriptors, input_path, top_k)

    effectiveness_function = get_effectiveness_func(effectiveness_function)

    effectiveness = {}
    print("\n Computing effectiveness estimations...")
    pool_params = [[effectiveness_function, ranked_lists[descriptor], top_k]
                   for descriptor in descriptors]
    with Pool(n_pools) as p:
        # Some print messages may not be reported while running pool map
        output_effectiveness = p.starmap(compute_rk_effectiveness, pool_params)
    for i, descriptor in enumerate(descriptors):
        effectiveness[descriptor] = output_effectiveness[i]
    print(" Done!")
    return effectiveness
