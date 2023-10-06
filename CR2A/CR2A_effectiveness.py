from multiprocessing import Pool
import os, csv
from pyUDLF.utils import readData


def list_descriptors(path):
    return [x[:-4] for x in sorted(os.listdir(path))]


def read_ranked_lists_file(descriptor: str, path_rks: str, top_k: int):
    file_path = os.path.join(path_rks, descriptor) + ".txt"
    print("\tReading file", file_path)
    with open(file_path, "r") as file:
        return [
            [int(rank) for rank in line.strip().split(" ")][:top_k]
            for line in file.readlines()
        ]


def load_ranked_lists(descriptors: list, path_rks: str, top_k: int):
    ranked_lists = {}

    print("\n Loading ranked lists...")
    for descriptor in descriptors:
        ranked_lists[descriptor] = read_ranked_lists_file(descriptor, path_rks, top_k)
    print(" Done!")

    return ranked_lists


# acho que ta pronto puta
# deixei brilhantemente explicado para n ter duvida
# quem tiver duvida é viado
# mama me olhando


def compute_authority_score(ranked_lists: list, index: int, top_k: int):
    score = 0

    query = ranked_lists[index]

    for query_rank in query[1:]:
        comparative = ranked_lists[query_rank]

        score += sum(comparative_rank in query for comparative_rank in comparative)

    return score / (top_k**2)


def compute_reciprocal_score(ranked_lists: list, index: int, top_k: int):
    result_score = 0

    query = ranked_lists[index]

    weights = [(weight + 1) for weight in list(range(top_k))]

    for query_rank in query[1:]:
        comparative = ranked_lists[query_rank]

        scores = [comparative_rank in query for comparative_rank in comparative]

        result_score += sum(
            score / weights[index] for index, score in enumerate(scores)
        )

    return result_score / (top_k**2)


def compute_rk_effectiveness(
    descriptors: list, ranked_lists: dict, effectiveness_function, top_k: int
):
    result = {}

    for descriptor in descriptors:
        result[descriptor] = 0

        count = int(len(ranked_lists[descriptor]))

        for index in range(count):
            result[descriptor] += effectiveness_function(
                ranked_lists[descriptor], index, top_k
            )

        result[descriptor] = result[descriptor] / count

    return result


def get_effectiveness_rk(effectivenes_function: str, input_path: str, top_k: int):
    input_path = input_path + "/ranked_lists"

    descriptors = list_descriptors(input_path)

    ranked_lists = load_ranked_lists(descriptors, input_path, top_k)

    if effectivenes_function == "authority":
        print("Computing authorithy score...")
        effectivenes_function = compute_authority_score
        authority = compute_rk_effectiveness(
            descriptors, ranked_lists, effectivenes_function, top_k
        )
        print("Complete!")
        return authority
    elif effectivenes_function == "reciprocal":
        print("Computing reciprocal score...")
        effectivenes_function = compute_reciprocal_score
        reciprocal = compute_rk_effectiveness(
            descriptors, ranked_lists, effectivenes_function, top_k
        )
        print("Complete!")

        return reciprocal

    elif effectivenes_function == "both":
        print("Computing authorithy and reciprocal score...")
        effectivenes_function = compute_authority_score

        authority = compute_rk_effectiveness(
            descriptors, ranked_lists, effectivenes_function, top_k
        )

        effectivenes_function = compute_reciprocal_score

        reciprocal = compute_rk_effectiveness(
            descriptors, ranked_lists, effectivenes_function, top_k
        )
        print("Complete!")
        return authority, reciprocal
    else:
        print(f"Effectiveness {effectivenes_function} coudn't be found! ")
        return
