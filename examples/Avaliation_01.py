# -----------------
# Calculates precision, recall, and mean average precision (MAP) for a given ranked list.
# ATTENTION: Please check and modify the paths according to the file locations on your system.
# -----------------

from pyUDLF import run_calls as udlf
from pyUDLF.utils import evaluation as ev
from pyUDLF.utils import readData as rd

# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath('.../UDLF/bin/udlf')
udlf.setConfigPath('.../UDLF/bin/config.ini')

# Path to the ranked list file
RksPath = "../Dataset/ranked_list/CNN-Resnet152.txt"
# Path to the list file
pListFile = "../Dataset/flowers_lists.txt"
# Path to the classes file
pClassesFile = "../Dataset/flowers_classes.txt"
# Size dataset
pN = 1360

# Reading the class list and ranked list from the files
class_list = rd.read_classes(pListFile, pClassesFile)
rk = rd.read_ranked_lists_file_numeric(RksPath, top_k=pN)

# Setting the value of N for precision and recall calculation
N = 5

# Computing precision, recall, and MAP
precision, precision_list = ev.compute_precision(rk, class_list, N)
recall, recall_list = ev.compute_recall(rk, class_list, N)
MAP = ev.compute_map(rk, class_list, pN)

# Printing the results
print("Precision:", precision)
print("Precision list:", precision_list[:5])
print("Recall:", recall)
print("Recall list:", recall_list[:5])
print("Mean Average Precision (MAP):", MAP[0])
