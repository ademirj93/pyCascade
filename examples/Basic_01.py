# --------------
# Executes the UDLF
# ATTENTION: Please check and modify the paths according to the file locations on your system.
# --------------


from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType


# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath("./UDLF/bin/udlf")
udlf.setConfigPath = "./UDLF/bin/config.ini"

# Method to be used
method = "CPRR"  # NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC

# Path to the ranked list file
RksPath = "./Dataset/ranked_list/CNN-Resnet152.txt"
# Path to the list file
pListFile = "./Dataset/flowers_lists.txt"
# Path to the classes file
pClassesFile = "./Dataset/flowers_classes.txt"
# Size dataset
pN = 1360


# Creating an instance of InputType
input_data = inputType.InputType()

# Setting parameters for input_data
# input_data.set_task("FUSION")
input_data.set_param("SIZE_DATASET", pN)  # Setting the size of the dataset
input_data.set_ranked_lists_size(pN)  # Setting the size of the ranked listss
input_data.set_method_name(method)  # Setting the method name
input_data.set_input_files(RksPath)  # Setting the input files (ranked lists)
input_data.set_lists_file(pListFile)  # Setting the list file
input_data.set_classes_file(pClassesFile)  # Setting the classes file
# input_data.input_files([path1,path2,path3..])

# Setting the output file to "FALSE" to disable output file generation
input_data.set_param("OUTPUT_FILE", "FALSE")

# Running the UDLF with the input_data and getting the results
output = udlf.run(input_data, get_output=True)

# Printing the log from the output
output.print_log()

# Getting the log values from the output
return_values = output.get_log()
