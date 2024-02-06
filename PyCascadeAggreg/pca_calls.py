import os
from itertools import zip_longest
import PyCascadeAggreg.pca_utils as utils
import PyCascadeAggreg.pca_effectiveness as effectiv
import PyCascadeAggreg.pca_savefiles as savefile
import PyCascadeAggreg.pca_aggregate as aggregate
import PyCascadeAggreg.pca_rk_compute as rkc

def cascade_execute(dataset_name: str,top_k: int, top_m: int, agg_method_layer_one: str, agg_method_layer_two: str, outlayer: str, number_combinations: int, evall_mode: str):
    
    # Valida o valor minimo do top M, calcula o tamanho da saida da cascata e valida o modo de estimativa de eficácia
    # cascade_size: int -> Número de elementos resultante da combinações da cascata
    # evall_mode: str
    cascade_size, evall_mode = utils.validate_data(top_m, number_combinations, evall_mode)
    
    # rootDir: str -> Pasta raiz do código
    rootDir = os.getcwd()

    # dataset-path: Str -> Caminho para pasta do dataset
    dataset_path = f"{rootDir}/dataset/{dataset_name}"

    # Cria as pastas caso necessário e armazena os caminhos nas varíaveis 
    output_dataset_path, output_rk_fusion_path, output_rankedlists = utils.paths_creations(
        dataset_name, top_k, top_m, outlayer, evall_mode, agg_method_layer_one.upper(), agg_method_layer_two.upper())
    
    if len(os.listdir(output_rankedlists)) != len(os.listdir(f"{rootDir}/dataset/{dataset_name}/features")):
        print("Calculando listas ranqueadas dos descritores isolados")
        rkc.compute_rklists_from_feat(dataset_name)

    print("\nCalculando valores do MAP, Precision e Recall...")

    utils.get_all_eval(dataset_path, output_dataset_path, outlayer)

    authority, reciprocal = effectiv.call_compute_descriptors_effectiveness(top_k, f"{dataset_path}/ranked_lists", outlayer) 

    print("\nSalvando os dados das estimativas authority e reciprocal dos descritores isolados...")

    savefile.save_effectiveness_scores(dataset_name, authority, reciprocal, output_dataset_path)

    utils.get_borda_ranked_lists(dataset_name, output_dataset_path)

    aggregate.first_layer_fusion(agg_method_layer_one, dataset_path, evall_mode, top_m, output_dataset_path, output_rk_fusion_path)

    authority, reciprocal = effectiv.call_compute_descriptors_effectiveness(top_k, output_rk_fusion_path, outlayer)

    print("\nSalvando os dados das estimativas authority e reciprocal dos pares combinados...")

    savefile.save_effectiveness_scores(f"{dataset_name}_cascade", authority, reciprocal, output_dataset_path)

    utils.get_borda_ranked_lists(f"{dataset_name}_cascade", output_dataset_path)

    aggregate.second_layer_fusion(agg_method_layer_two, dataset_path, evall_mode, cascade_size, output_dataset_path, output_rk_fusion_path)
    return