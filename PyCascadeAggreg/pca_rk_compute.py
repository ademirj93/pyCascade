import numpy as np
from sklearn.neighbors import BallTree
import os, re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox



#way_features = f'{rootDir}/dataset/{dataset_name}/features/'
def compute_rklists_from_feat(dataset_name: str, l_size: int):
    # Função para abrir a janela de seleção de arquivo
    rootDir = os.getcwd()
    
    #def set_path():
        # Abre a janela para seleção de arquivo
        #way_file = filedialog.askdirectory(title=f"{dataset_name} selecione o caminho das features!")
        
        #if not way_file:
            #window.destroy()
            #exit()
        # Atualiza o conteúdo da variável com o caminho selecionado
        #way_features.set(way_file)
        #return way_file
    # Cria uma janela tkinter
    #window = tk.Tk()

    # Define as dimensões da janela
    #window.geometry("1x1")
    #window.withdraw()

    #way_features = tk.StringVar()
    way_features = f"{rootDir}/dataset/{dataset_name}/features" 

    #messagebox.showinfo("Seleção do diretório das features", "Selecine o diretório onde as features a serem ranqueadas estão salvas.")
    #way_file = set_path()
    way_file = f"{rootDir}/dataset/{dataset_name}/features" 
    #if len(way_features.get()) == len(way_file):
            
        #way_features = way_features.get()
        #window.destroy()

    # Inicia o loop principal da janela tkinter
    #window.mainloop()

    #way_features = way_features.get()

    if not any(feature.endswith(('.npy', '.npz')) for feature in os.listdir(way_features)):
        messagebox.showwarning(message="Nenhum arquivo válido foi encontrado no diretório informado!")
        exit()

    for feature in os.listdir(way_features):
        
        features_path = f'{rootDir}/dataset/{dataset_name}/features/{feature}'

        if feature.endswith(".npy"):
            #Load features
            features = np.load(features_path)
        elif feature.endswith(".npz"):
            #Load features
            features = np.load(features_path)["features"]

        pattern = r'([a-zA-Z]+)(\d+)([a-zA-Z]+)'
        dataset_name_clean = re.findall(pattern, dataset_name)

        feat_name = feature.split('.')[0]
        feat_name = re.sub("features_","", feat_name)
        feat_name = re.sub("-last_linear","", feat_name)
        feat_name = re.sub(f"_{dataset_name}","", feat_name)
        feat_name = re.sub(f"{dataset_name}_","", feat_name)
        for name in dataset_name_clean[0]:
            if name in feat_name:
                feat_name.replace(f"_{name}", "")
                feat_name.replace(f"{name}_", "")

        #Caminho com o nome para salvar o rk


        rk_save = f'{rootDir}/dataset/{dataset_name}/ranked_lists/{feat_name}.txt'
            
        print(f"Calculando ranking das features {feat_name}")

        #Calculando RK
        tree = BallTree(features) #indexing
        _, rks = tree.query(features, k=l_size) #Fazendo as querys


        #Salvando o rk
        f = open(rk_save, "w+")
        for rk in rks:
            for i in rk:
                print(i, file=f, end=" ")
            print(file=f)
        f.close()
    return