import os, random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image

current_path = os.getcwd()
# Caminho para a pasta com as imagens
caminho_pasta = f"{current_path}/dataset/oxford17flowers/jpg"

# Listar todos os arquivos na pasta
arquivos = os.listdir(caminho_pasta)

# Selecionar aleatoriamente 6 imagens
selecionadas = random.sample(arquivos, 6)

# Plotar as imagens horizontalmente
fig, axs = plt.subplots(1, 6, figsize=(15, 5))  # 1 linha, 6 colunas

for i, imagem in enumerate(selecionadas):
    caminho_imagem = os.path.join(caminho_pasta, imagem)
    img = Image.open(caminho_imagem)
    img_title = caminho_imagem.split('/')[-1]
    axs[i].imshow(img)
    axs[i].axis('off')  # Ocultar os eixos
    axs[i].set_title(img_title)  # Definir título para cada imagem

plt.tight_layout()
plt.show()