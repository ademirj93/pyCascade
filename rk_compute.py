import numpy as np
from sklearn.neighbors import BallTree
import os, re

rootDir = os.getcwd()
dataset_name = "corel5k"
way_features = f'{rootDir}/dataset/{dataset_name}/features/'

if not os.path.exists(f'{rootDir}/rk_lists/{dataset_name}/'):
    os.makedirs(f'{rootDir}/rk_lists/{dataset_name}/')

for feature in os.listdir(way_features):
    
    #feature = "FOH.npz"
    #feature = "features_swintf_corel5k.npy"
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


    rk_save = f'{rootDir}/rk_lists/{dataset_name}/{feat_name}.txt'

    #Tamanho que quer calcular do RK
    size = len(features)
    print(f"Calculando ranking das features {feat_name}")

    #Calculando RK
    tree = BallTree(features) #indexing
    _, rks = tree.query(features, k=size) #Fazendo as querys


    #Salvando o rk
    f = open(rk_save, "w+")
    for rk in rks:
        for i in rk:
            print(i, file=f, end=" ")
        print(file=f)
    f.close()