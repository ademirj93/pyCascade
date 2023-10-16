import CR2A.CR2A_aggregate as aggregate
import CR2A.CR2A_utils as utils
import CR2A.CR2A_effectiveness as effectiv
import CR2A.CR2A_evaluation as evall
import os

def call_cascating_aggregagtion(dataset_name: str, top_k: int, top_m: int, mode = "b"):

    # rootDir: str -> root path of code
    rootDir = os.getcwd()

    if not os.path.exists("./output"):
        os.makedirs("./output")

    dataset_path = f"{rootDir}/dataset/{dataset_name}"

    utils.get_all_eval(dataset_path)

    authority, reciprocal = effectiv.get_effectiveness_rk(dataset_path, top_k)

    utils.call_save_effectiveness(dataset_name, authority, reciprocal, top_k)

    aggregate.cascade_aggregate(dataset_path, mode,top_k, top_m)


    return