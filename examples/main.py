from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType

# Setando o caminho do binário e do config (1)
udlf.setBinaryPath("/home/vbox/UDLF/bin/udlf")
udlf.setConfigPath = ("/home/vbox/UDLF/bin/minha_config.ini")

# Definindo o objeto input, com o nome de input_data (2)
input_data = inputType.InputType()

# Alterando valores do config. (2)
#parametros mais usados
#set_*param_name*(param_value)
#files_path = "./Dataset/matrices/distance/acc.txt"
classes_path = "./Dataset/flowers_classes.txt"
input_data.set_method_name("CPRR")   #(NONE|CPRR|RLRECOM|...)Selection of method to be executed
#input_data.set_input_files(files_path)   #Path of the main input file (matrix/ranked lists) for UDL tasks
input_data.set_lists_file("./Dataset/flowers_list.txt")    #Path of the lists file
input_data.set_classes_file(classes_path)   #Path of the classes file
...

#parâmetro genérico
#set_param("param_name", param_value) 
input_data.set_param("UDL_TASK", "UDL")     #(UDL|FUSION): Selection of task to be executed
input_data.set_param("PARAM_NONE_L", 1360)  #(TUint): Size of the ranked list (must be lesser than SIZE_DATASET)
...

# Executando (3)
output = udlf.run(input_data, get_output = True)

# Resultado
output.print_log()
results = output.get_log()
print(results["MAP"]["After"]) # or ["Before"] or ["Gain"]
print(results["MAP"])
print(results["Time"])