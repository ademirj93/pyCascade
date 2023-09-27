# -----------------
# Runs the Correlation Graph algorithm with varying end thresholds and collects the MAP values for each threshold.
# ATTENTION: Please check and modify the paths according to the file locations on your system.
# -----------------

from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType

# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath('.../files/UDLF/bin/udlf')
udlf.setConfigPath('.../files/UDLF/bin/config.ini')

# Method to be used
# NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC
method = "CORGRAPH"

# Path to the ranked list file
RksPath = ".../files/Dataset/ranked_list/CNN-Resnet152.txt"
# Path to the list file
pListFile = ".../files/Dataset/flowers_lists.txt"
# Path to the classes file
pClassesFile = ".../files/Dataset/flowers_classes.txt"
# Size dataset
pN = 1360

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

# Setting thresholds
th_start = 0.05
th_inc = 0.005
# Setting the starting threshold value
input_data.set_param("PARAM_CORGRAPH_THRESHOLD_START", th_start)
# Setting the threshold increment value
input_data.set_param("PARAM_CORGRAPH_THRESHOLD_INC", th_inc)

# List that contains results
results = []

# Run UDLF for each threshold
th_end = th_start

while th_end < 1:
    print("Run for th_end = {}".format(th_end))
    # Setting the end threshold value
    input_data.set_param("PARAM_CORGRAPH_THRESHOLD_END", th_end)
    output = udlf.run(input_data, get_output=True)
    # Getting the MAP value from the output log
    result_map = output.get_log()["MAP"]["After"]
    results.append(result_map)
    print("MAP = {}".format(result_map))
    # output.print_log()
    th_end += th_inc

print(results)
