# ---------------------
# Executes the UDLF method and generates ranked lists based on input data
# ATTENTION: Please check and modify the paths according to the file locations on your system.
# ---------------------


from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
import os

currentDir = os.getcwd()
# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath(f"{currentDir}/UDLF/bin/udlf")
udlf.setConfigPath(f"{currentDir}/UDLF/bin/config.ini")

# Method to be used
method = "CPRR"  # Options: NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE

# Path to the ranked list file
RksPath = f"{currentDir}/Dataset/ranked_list/CNN-Resnet152.txt"
# Path to the list file
pListFile = f"{currentDir}/Dataset/flowers_lists.txt"
# Path to the classes file
pClassesFile = f"{currentDir}/Dataset/flowers_classes.txt"
# Output Path / do not add the extension -> .txt, .html, and others
pOut = f"{currentDir}/Examples/output"
# Size dataset
pN = 1360
# Interval to compute precision and recall
range = "5,10,15,20,30,50,80"

# Creating an instance of InputType
input_data = inputType.InputType()

# Setting parameters for input_data
input_data.set_param("SIZE_DATASET", pN)  # Setting the size of the dataset
input_data.set_ranked_lists_size(pN)  # Setting the size of the ranked lists
input_data.set_method_name(method)  # Setting the method name
input_data.set_input_files(RksPath)  # Setting the input files (ranked lists)
input_data.set_lists_file(pListFile)  # Setting the list file
input_data.set_classes_file(pClassesFile)  # Setting the classes file

# Setting parameters for precision calculation
input_data.set_param("EFFECTIVENESS_RECALLS_TO_COMPUTE", range)
input_data.set_param("EFFECTIVENESS_PRECISIONS_TO_COMPUTE", range)

# Setting output file generation
# Setting the output file to "TRUE" to enable output file generation
input_data.set_param("OUTPUT_FILE", "TRUE")  # Enable output file generation
input_data.set_output_file_format("RK")  # Set the output file format to "RK"
# Set the format of the output ranking (RK) to numeric format
input_data.set_param("OUTPUT_RK_FORMAT", "NUM")
# Set the output file path for the generated file
input_data.set_output_file_path(pOut)

# Running the UDLF with the input_data and getting the results
output = udlf.run(input_data, get_output=True)

# Printing the log from the output
output.print_log()

# Getting the log values and the rk from the output
return_values = output.get_log()
rk_out = output.get_rks()

# Displaying the first 10 elements of the first rk
print(rk_out[0][0:10])
