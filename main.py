from pyUDLF import run_calls as udlf
from CR2A.CR2A_utils import *
from CR2A.CR2A_effectiveness import *
import os


# rootDir: str -> root path of code
rootDir = os.getcwd()

# authority/reciprocal/both
function_eff = "both"

dataset_name = "oxford17flowers"

# Setting UDLF files (udlf/config.ini)
udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

dataset_path = f"{rootDir}/dataset/{dataset_name}"

get_all_eval(dataset_path)

aggregate_ranked_lists(dataset_name)
effectiveness_func = compute_authority_score


authority, reciprocal = get_effectiveness_rk(function_eff, dataset_path, 200)
# save_effectiveness_scores(dataset_name, authority, reciprocal)

save_effectiveness_scores(dataset_name, authority, reciprocal)

aggregate_ranked_lists_effectiveness(dataset_name)
