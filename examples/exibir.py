# -----------------
# Runs the Correlation Graph algorithm with varying end thresholds and collects the MAP values for each threshold.
# ATTENTION: Please check and modify the paths according to the file locations on your system.
# -----------------

from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
from pyUDLF.utils import outputType

# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath('/home/gustavo/Desktop/files/UDLF/bin/udlf')
udlf.setConfigPath('/home/gustavo/Desktop/files/UDLF/bin/config.ini')

# Method to be used
# NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC
method = "RDPAC"

# Path to the ranked list file
RksPath = "/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/swintf_rk_pollen73s.txt"
# Path to the list file
pListFile = "/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/list_pollen73s_70class.txt"
# Path to the classes file
pClassesFile = "/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/class_pollen73s_70class.txt"
# Size dataset
pN = 2450
pOut = "/home/gustavo/Desktop/files/UDLF/bin/output_apagar"
imagePath = "/home/gustavo/Downloads/POLLEN73S_padronizado/"

# Creating an instance of InputType
input_data = inputType.InputType()

# Setting parameters for input_data
input_data.set_param("SIZE_DATASET", pN)  # Setting the size of the dataset
input_data.set_ranked_lists_size(pN)  # Setting the size of the ranked lists
input_data.set_method_name(method)  # Setting the method name
input_data.set_input_files(RksPath)  # Setting the input files (ranked lists)
input_data.set_lists_file(pListFile)  # Setting the list file
input_data.set_classes_file(pClassesFile)  # Setting the classes file
# Setting the size of the dataset
input_data.set_param("INPUT_IMAGES_PATH", imagePath)
input_data.set_param("PARAM_NONE_L", pN)
input_data.set_param("PARAM_RFE_L", pN)
input_data.set_param("PARAM_RDPAC_L", 1000)
input_data.set_param("PARAM_LHRR_L", pN)
input_data.set_param("PARAM_CPRR_L", pN)


# Setting output file generation
# Setting the output file to "TRUE" to enable output file generation
input_data.set_param("OUTPUT_FILE", "TRUE")  # Enable output file generation
input_data.set_output_file_format('RK')  # Set the output file format to "RK"
# Set the format of the output ranking (RK) to numeric format
input_data.set_param('OUTPUT_RK_FORMAT', 'NUM')
# Set the output file path for the generated file
input_data.set_output_file_path(pOut)

# Running the UDLF with the input_data and getting the results
output = udlf.run(input_data, get_output=True, compute_individual_gain=False)
output.list_path = pListFile
output.classes_path = pClassesFile
# print(output.rk_path)
output.images_path = imagePath
output.save_rk_img(1378, 10, (0, 0), "/home/gustavo/Desktop/files/UDLF/bin/RDPAC_1378.jpg", 0)
output.show_rk(1378, 10, (0, 0), 0)  # 1378

# output.print_log()
