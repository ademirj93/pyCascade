
import heapq
from pyUDLF import run_calls as udlf
from pyUDLF.utils import inputType
from pyUDLF.utils import outputType
from pyUDLF.utils import evaluation as ev
from pyUDLF.utils import readData as rd
# Setting the paths for the binary and the configuration file.
udlf.setBinaryPath('/home/gustavo/Desktop/files/UDLF/bin/udlf')
udlf.setConfigPath('/home/gustavo/Desktop/files/UDLF/bin/config.ini')

# Method to be used
# NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC
rk_rdpac1 = '/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/output_73s.txt'
Listfile = '/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/list_pollen73s_70class.txt'
ClassFile = '/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/class_pollen73s_70class.txt'

# Path to the ranked list file
RksPath = "/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/resnet152_rk_pollen73s.txt"  # swintf_rk_newz_2k
# Path to the list file
pListFile = '/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/list_pollen73s_70class.txt'
# Path to the classes file
pClassesFile = '/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/class_pollen73s_70class.txt'
# Size dataset
pN = 2450

pOut =  "/home/gustavo/Desktop/UDLF_novo/UDLF-1.60/bin/DATASET/pollen73s/output_73s.txt"
#imagePath = "/home/gustavo/Downloads/POLLEN73S_padronizado/"

rks1 = rd.read_ranked_lists_file_numeric(RksPath)
rks2 = rd.read_ranked_lists_file_numeric(pOut)

list_test = rd.read_classes(pListFile, pClassesFile)
print(len(list_test))
print(len(rks1), len(rks2))

#print(ev.compute_map(rks1, list_test, 1000)[0])
a = ev.compute_gain(rks1, rks2, list_test, 35,
                    measure="Precision", verbose=True)

maiores_valores = heapq.nlargest(10, a, key=lambda x: x[0])

for valor in maiores_valores:
    print(valor)
