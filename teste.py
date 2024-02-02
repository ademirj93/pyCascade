import os
from pyUDLF.utils import readData as rd

root = os.getcwd()
dataset_name = "corel5k"
dataset_path = f"{root}/dataset/{dataset_name}/ranked_lists"

rk = rd.read_ranked_lists_file_numeric(f"{dataset_path}/rks_VIT-B16_original_corel5k.txt", 5000)

print(len(rk), len(rk[0]))
