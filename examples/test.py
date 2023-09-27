# --------------
# Performs a second execution of the UDLF method using the generated ranking file
# ATTENTION: Please check and modify the paths according to the file locations on your system.
# --------------

from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType

# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath('UDLF/bin/udlf')
udlf.setConfigPath('UDLF/bin/config.ini')

# Method to be used
method = "RLSIM"  # Options: NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE

# Path to the ranked list file
RksPath = "Dataset/arai/rk_palinomorfos_genero_imagenet_vit16.txt"
# Path to the list file
pListFile = "Dataset/arai/lists_generos.txt"
# Path to the classes file
pClassesFile = "Dataset/arai/classes_generos.txt"
# Size dataset
K = 1147
# Output Path / do not add the extension -> .txt, .html, and others
pOut = "output"
# Interval to compute precision and recall
range = '1,2,5,10,15'

# Creating an instance of InputType
input_data = inputType.InputType()

# Setting parameters for precision calculation
input_data.set_param("EFFECTIVENESS_RECALLS_TO_COMPUTE", '10,50')
input_data.set_param("EFFECTIVENESS_PRECISIONS_TO_COMPUTE", range)

# Setting output file generation
# Setting the output file to "TRUE" to enable output file generation
input_data.set_param("OUTPUT_FILE", "TRUE")  # Enable output file generation
input_data.set_output_file_format('RK')  # Set the output file format to "RK"
# Set the format of the output ranking (RK) to numeric format
input_data.set_param('OUTPUT_RK_FORMAT', 'NUM')
# Set the output file path for the generated file
input_data.set_output_file_path(pOut)

input_data.set_method_name(method)
input_data.set_param("UDL_TASK", "UDL")
input_data.set_param('INPUT_FILE_FORMAT', 'RK')
input_data.set_param('INPUT_RK_FORMAT', 'NUM')
input_data.set_param("INPUT_FILE", RksPath)
input_data.set_lists_file(pListFile)
input_data.set_classes_file(pClassesFile)
input_data.set_ranked_lists_size(K)
input_data.set_dataset_size(K)

input_data.set_param("OUTPUT_FILE", "TRUE")
input_data.set_param("OUTPUT_FILE_FORMAT", "RK")
input_data.set_param("OUTPUT_RK_FORMAT", "NUM")
input_data.set_param("EFFECTIVENESS_COMPUTE_RECALL", "TRUE")


input_data.write_config('config_teste.ini')


# Running the UDLF with the input_data and getting the results
output = udlf.run(input_data, get_output=True)
output.print_log()
