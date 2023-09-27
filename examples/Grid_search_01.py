# -----------------
# Performs a grid search to find the optimal value of the "PARAM_CPRR_K" parameter in the CPRR method.
# ATTENTION: Please check and modify the paths according to the file locations on your system.
# -----------------

from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
from pyUDLF.utils import gridSearch


# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath('.../files/UDLF/bin/udlf')
udlf.setConfigPath('.../files/UDLF/bin/config.ini')

# Method to be used
method = "CPRR"  # NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC

# Path to the ranked list file
RksPath = ".../files/Dataset/ranked_list/CNN-Resnet152.txt"
# Path to the list file
pListFile = ".../files/Dataset/flowers_lists.txt"
# Path to the classes file
pClassesFile = ".../files/Dataset/flowers_classes.txt"
# Size dataset
pN = 1360
range = '5,10,15,20,30,50,80'

# Creating an instance of InputType
input_data = inputType.InputType()

# Setting parameters for input_data
input_data.set_param("SIZE_DATASET", pN)  # Setting the size of the dataset
input_data.set_ranked_lists_size(pN)  # Setting the size of the ranked lists
input_data.set_method_name(method)  # Setting the method name
input_data.set_input_files(RksPath)  # Setting the input files (ranked lists)
input_data.set_lists_file(pListFile)  # Setting the list file
input_data.set_classes_file(pClassesFile)  # Setting the classes file

# Setting the output file to "FALSE" to disable output file generation
input_data.set_param("OUTPUT_FILE", "FALSE")

# Setting parameters for precision calculation
input_data.set_param("EFFECTIVENESS_RECALLS_TO_COMPUTE", range)
input_data.set_param("EFFECTIVENESS_PRECISIONS_TO_COMPUTE", range)

# Finding the best parameter for CPRR method using grid search
out_dict = gridSearch.find_best_param(input_data, "CPRR", "PARAM_CPRR_K", [
                                      10, 15, 20], ranked_list_size=1360, verbose=True)

# Printing the dictionary containing the best parameter value and evaluation results
print(out_dict)
