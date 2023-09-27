from pyUDLF import run_calls as udlf
from CR2A.CR2A_utils import *
import os


# rootDir: str -> root path of code
rootDir = os.getcwd()

dataset_name = "corel5k"

# Setting UDLF files (udlf/config.ini)
udlf.setBinaryPath(f"{rootDir}/UDLF/bin/udlf")
udlf.setConfigPath(f"{rootDir}/UDLF/bin/config.ini")

dataset_path = f"{rootDir}/dataset/{dataset_name}"

get_all_eval(dataset_path)
