import pandas as pd
import os

dataset_name = "flowers17"

rootDir = os.getcwd()
last_dataset = "empty"

# Lê o arquivo CSV para um DataFrame usando pandas, pulando as primeiras linhas
df = pd.read_csv(f'{rootDir}/index.csv', delimiter=';')

print(df.columns)

for index, row in df.iterrows():
    index_value = row['Index']
    dataset_value = row['DataSet']
    layer_one_value = row['Layer One']
    layer_two_value = row['Layer Two']
    outlayer_value = row['Outlayer']
    top_k_value = row['Top K']
    top_m_value = row['Top M']
    alpha_value = row['Alpha']
    effectiveness_value = row['Effectiveness']
    l_size_value = row['L Size']
    map_value = row['MAP']
    data_folder_value = row['Data Folder']

    # Crie o caminho completo para o arquivo
    file = f"tabular_latex_isolated_results_{dataset_value}.txt"
    file_path = os.path.join(rootDir, file)

    # Verifique se o arquivo já existe
    if not os.path.exists(file_path):
        # Abra o arquivo para escrita
        with open(file, 'w') as file:
            write_header = f"Execução {index_value} do dataset {dataset_value} com parâmetros L = {l_size_value}, K = {top_k_value}, m = {top_m_value} e alpha = {alpha_value} {layer_one_value}x{layer_two_value} \n \n"
            # Escreva o cabeçalho no arquivo
            file.write(write_header)
    else:
         # Abra o arquivo para escrita
        with open(file, 'a') as file:
            write_header = f"Execução {index_value} do dataset {dataset_value} com parâmetros L = {l_size_value}, K = {top_k_value}, m = {top_m_value} e alpha = {alpha_value} {layer_one_value}x{layer_two_value} \n \n"
            # Escreva o cabeçalho no arquivo
            file.write(write_header)

    # Defina o cabeçalho em formato LaTeX
    header = "\\\\textbf{Descritor} & \\\\textit{\\\\textbf{MAP}} & \\\\textit{\\\\textbf{Authority Score}} & \\\\textit{\\\\textbf{Reciprocal Score}} \\\\ \\hline \n"


    combined_files = f"{data_folder_value}/{dataset_value}_cascade.csv"

    if last_dataset != dataset_value:
        
        isolated_file = f"{data_folder_value}/{dataset_value}.csv"

        write_line_isolated_rk = "\n \\\\textbf{Descritor} & \\\\textbf{MAP}  & \\\\textit{\\\\textbf{Authority Score}} & \\\\textit{\\\\textbf{Reciprocal Score}} \\\\ \\hline \n"

        with open(file, 'a') as file:
            file.write(write_line_isolated_rk)

        df_isolated = pd.read_csv(isolated_file, delimiter=';')
        
        for index_isolated, row_isolated in df_isolated.iterrows():
            collum_descriptor = row_isolated['descriptor']
            collum_map = row_isolated['MAP']
            collum_authorithy = row_isolated['authority']
            collum_reciprocal = row_isolated['reciprocal']

            write_line_isolated_rk = f"{collum_descriptor} & {collum_map}  & {collum_authorithy} & {collum_reciprocal} \\\\ \\hline \n"

            with open(file, 'a') as file:
                file.write(write_line_isolated_rk)

    write_line_combined_rk = "\n \\\\textbf{Descritor} & \\\\textbf{MAP}  & \\\\textit{\\\\textbf{Authority Score}} & \\\\textit{\\\\textbf{Reciprocal Score}} \\\\ \\hline \n"

    with open(file, 'a') as file:
        file.write(write_line_combined_rk)            

    df_combined = pd.read_csv(isolated_file, delimiter=';')

    for index_combined, row_combined in df_isolated.iterrows():
        collum_descriptor = row_combined['descriptor']
        collum_map = row_combined['MAP']
        collum_authorithy = row_combined['authority']
        collum_reciprocal = row_combined['reciprocal']

        write_line_isolated_rk = f"{collum_descriptor} & {collum_map}  & {collum_authorithy} & {collum_reciprocal} \\\\ \\hline \n"


    last_dataset = dataset_value