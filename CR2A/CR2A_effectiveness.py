from multiprocessing import Pool


def compute_authority_score(ranked_lists, index, top_k):
    score = 0
    rk1 = ranked_lists[index][:top_k]
    for img1 in rk1:
        rk2 = ranked_lists[img1][:top_k]
        for img2 in rk2:
            for current_img in rk1:
                if img2 == current_img:
                    score += 1
                    break
    return (score/(top_k**2))


def compute_reciprocal_score(ranked_lists, index, top_k):
    score = 0
    rk1 = ranked_lists[index][:top_k]
    for img1 in rk1:
        rk2 = ranked_lists[img1][:top_k]
        for img2 in rk2:
            for k, current_img in enumerate(rk1):
                if img2 == current_img:
                    score += 1/(k+1)
                    break
    return (score/(top_k**2))


def compute_rk_effectiveness(effectiveness_function, ranked_lists, top_k):
    n = int(len(ranked_lists))
    total = 0
    for index in range(n):
        total += effectiveness_function(ranked_lists, index, top_k)
    return total/n


def compute_descriptors_effectiveness(parameters,
                                      effectiveness_function,
                                      ranked_lists,
                                      descriptors,
                                      top_k):
    effectiveness = {}
    print("\n Computing effectiveness estimations...")
    n_pools = parameters["multithreading_pools"]
    pool_params = [[effectiveness_function, ranked_lists[descriptor], top_k]
                   for descriptor in descriptors]
    with Pool(n_pools) as p:
        # Some print messages may not be reported while running pool map
        output_effectiveness = p.starmap(compute_rk_effectiveness, pool_params)
    for i, descriptor in enumerate(descriptors):
        effectiveness[descriptor] = output_effectiveness[i]
    print(" Done!")
    return effectiveness