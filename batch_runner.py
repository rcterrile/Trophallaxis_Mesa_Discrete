from mesa.model import Model
from bee_troph.model import TrophallaxisABM
import numpy as np

def _get_model_parameters(n: int=110, frac_fed: int=10, attr_rad: float=2.5, th: int=180,
                          aboost: int=1, epsboost: int=8, endboost: int=1):
    model_params = {
        "N": n,
        "fraction_of_fed_bees": frac_fed,
        "attraction_radius": attr_rad,
        "theta": th,
        "solid_bounds": True,
        "attraction_bias": True,
        "always_random_walk": True,
        "data_out": True,
        "food_out": True,
        "session_id": 0,
        "batch_id": 0,
        "run_id": 0,
        "a_boost": aboost,
        "eps_boost": epsboost,
        "end_boost": endboost,
        "width": 32,
        "height": 32,
    }
    return model_params
# _get_model_parameters()

def batch_run(session_num: int = 0, batch_num: int = 0, repetitions: int = 10,
                max_steps: int = 1000, display_progress: bool = True,
                atb: int = 1, epb: int=8, enb: int=1, attr_rad: float = 2.5,
                n: int = 110, frac_fed: int = 10, th: int = 180):
    ## Start terminal printout:
    if display_progress:
        print("BATCH: " + str(batch_num))

    ## Get parameters:
    params = _get_model_parameters(n, frac_fed, attr_rad, th, atb, epb, enb)
    params["session_id"] = session_num
    params["batch_id"] = batch_num

    ## Run model and repeat 'repetitions' times:
    id_counter = 0                #  ---- change if not starting at run 0 ----
    for i in range(repetitions):
        params["run_id"] = i + id_counter
        _run_model(TrophallaxisABM, params, max_steps)
        if display_progress:
            if i == 0 or i%2 == 0:
                # print("- " + str(i+1) + " of " + str(repetitions))
                print(str(int((i+1)/repetitions*100))+"%")
    if display_progress:
        print("Batch Finished")
# batch_run()

def _run_model(model_cls: type[Model], model_params, max_steps: int): #, iter: int, rep: int, max_reps: int):
    model = model_cls(**model_params)
    while model.running and model.schedule.steps <= max_steps:
        model.step()
    if model.running:
        print("oops")
# _run_model()

# # batch_run(sess, batch, reps, max_s, display, atb, epb, enb, attr_rad, n, frac, th, )
# #

#####  Previously run batches ####

# batch_run(4, 2, 40, 1000, True, 10, 8, 8, 2)
# batch_run(4, 4, 40, 1000, True, 10, 8, 8, 3)
# batch_run(4, 7, 40, 1000, True, 10, 8, 8, 10)

# atr = [0,1,2.5,4,8]
# cnt = 0
# for a in atr:
#     batch_run(4, cnt, 40, 1000, True, 10, 8, 8, a)
#     cnt += 1

# [0,1,2,2.5,3,4,8,10]
# [0,1,2, 3, 4,5,6, 7]

# ###
# # eps: 8
# end = [8,8.5,9,9.5]
# ab = [5,10]
# cnt = 0
# for a in ab:
#     for e in end:
#         batch_run(1, cnt, 30, 1000, True, a, 8, e, 2.5)
#         cnt += 1
# ###

# eps = [8,7,6]
# end = [9,10,11]
# cnt = 0
# for ep in eps:
#     for en in end:
#         batch_run(3, cnt, 30, 1000, True, 10,  ep, en, 2.5)
#         cnt += 1

# eps = [8,7,6,5,4]
# end = [1,3,6,10]
# cnt = 0
# for ep in eps:
#     for en in end:
#         batch_run(2, cnt, 30, 1000, True, 10,  ep, en, 2.5)
#         cnt += 1
# #         s  b   r    ms   dis  at ep en rd  n  fr  th
# # batch_run(2, 0, 30, 1000, True, 10,  8, 1, 2.5)


# batch_run(0, 0, 30, 1000, True, 1, 8, 1, 0)
# batch_run(0, 1, 30, 1000, True, 5, 8, 1, 0)
# batch_run(0, 2, 30, 1000, True, 10,8, 1, 0)
# batch_run(0, 3, 30, 1000, True, 10, 8, 3, 0)
# batch_run(0, 4, 30, 1000, True, 10, 7, 6, 0)
# batch_run(0, 5, 30, 1000, True, 10, 7, 10, 0)
# batch_run(0, 6, 30, 1000, True, 10, 6, 3, 0)
# batch_run(0, 7, 30, 1000, True, 10, 5, 3, 0)
# batch_run(0, 8, 30, 1000, True, 10, 4, 3, 0)
