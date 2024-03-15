import tkinter as tk
from tkinter import ttk


# Função para ser chamada quando uma opção é selecionada no ComboBox
def choose_dataset_name():

    match combo_dataset.get():
        case "Corel5k":
            dataset_name = "corel5k"
        case "Flowers 17":
            dataset_name = "oxford17flowers"
        



# Cria a janela principal
window = tk.Tk()
window.title("PyCascade Aggregation Multi-nível Methode")

# Cria um rótulo
label = tk.Label(window, text="Selecione o dataset a ser utilizado:")
label.pack(pady=10)

# Cria um ComboBox
datasets = ["corel5k", "oxford17flowers"]
combo_dataset = ttk.Combobox(window, values=datasets)
combo_dataset.pack()

# Configura a função a ser chamada quando uma opção é selecionada
combo_dataset.bind("<<ComboboxSelected>>", lambda event: choose_dataset_name())

# Cria um rótulo para exibir a opção selecionada
dataset_choose = tk.Label(window, text="")
dataset_choose.pack(pady=10)

# Inicia o loop principal da aplicação
window.mainloop()