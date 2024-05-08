import copy
import argparse
from datetime import datetime

import glob
import os, sys

script_dir = os.path.dirname(__file__)
module_path = os.path.abspath(os.path.join(script_dir, '../'))
project_path = os.path.abspath(os.path.join(script_dir, '../../'))
if module_path not in sys.path:
    sys.path.insert(0, module_path)
if project_path not in sys.path:
    sys.path.insert(0, project_path)
from utils import *
import gamma as gamma
import importlib

fitness_list = None
fitness = None
stage_idx = 0
prev_stage_value = []
tune_iter = 1
opt = None
MAC_AREA_MAESTRO = 4470
MAC_AREA_INT8 = 282
BUF_AREA_perbit = 0.086
L2BUF_AREA_MAESTRO = 4161.536
L1BUF_AREA_MAESTRO = 4505.1889
L2BUF_UNIT = 32768
L1BUF_UNIT = 64

# bias = {"par": {1: "K", 2:"C"}, "order":{1:["K", "C"]}, "tiles": {1:{"K":0.1, "C":0.2}, 2:{"K":0.3}}}
bias = {"par": {1: "K", 2: "C"}, "order": {1: ["K", "C", "Y", "X"], 2: ["K", "C", "Y", "X"]}}


# bias = {"par": {1: "K", 2:"C"}}
# bias = {"par": {1: "Y"}}


def get_pe_usage(env, sol, num_pe):
    util_num_pe = num_pe
    baseline = env.get_indiv_info(sol, num_pe=num_pe)
    best_runtime, best_throughput, best_energy, best_area, best_l1_size, best_l2_size, best_mac, best_power, best_num_pe = baseline
    baseline = np.array(baseline)[:-2]
    for i in range(num_pe - 1):
        util_num_pe -= 1
        cur = env.get_indiv_info(sol, num_pe=util_num_pe)
        best_runtime, best_throughput, best_energy, best_area, best_l1_size, best_l2_size, best_mac, best_power, best_num_pe = cur
        cur = np.array(cur)[:-2]
        if sum(baseline != cur) > 1:
            util_num_pe += 1
            break
    return util_num_pe


def train_model(model_defs, input_arg, chkpt_file='./chkpt', precisions=None):
    global opt
    opt = input_arg
    fitness = [opt.fitness1, opt.fitness2]
    dimension = model_defs[0]
    map_cstr = None
    env = gamma.GAMMA(dimension=dimension, num_pe=opt.num_pe, fitness=fitness, par_RS=opt.parRS,
                      l1_size=opt.l1_size,
                      l2_size=opt.l2_size, NocBW=opt.NocBW, offchipBW=opt.offchipBW, slevel_min=opt.slevel_min,
                      slevel_max=opt.slevel_max,
                      fixedCluster=opt.fixedCluster, log_level=opt.log_level, map_cstr=map_cstr)
    constraints = {"area": opt.area_budget * 1e6}
    chkpt_list = []
    num_layer = 1

    for dimension in model_defs:

        # ridefinire i valori di PE e l1 in base al tipo di quantizzazione
        if len(precisions):
            precision = precisions[num_layer - 1]
        else:
            precision = None

        map_cstr = map_constraints(map_cstr, opt, precision)

        env.reset_dimension(fitness=fitness, constraints=constraints, dimension=dimension)
        env.reset_hw_parm(num_pe=get_value_for_pe(precision, opt.num_pe),
                          l1_size=opt.l1_size,
                          l2_size=opt.l2_size, pe_limit=opt.pe_limit,
                          area_pebuf_only=False, external_area_model=True, map_cstr=map_cstr,
                          slevel_max=get_value_for_precision(precision), slevel_min=get_value_for_precision(precision))
        #tolto calcolo su l1 value da verificare se rimettere
        chkpt, pops = env.run(dimension, stage_idx=0, num_population=opt.num_pop, prev_stage_value=None,
                              num_generations=opt.epochs,
                              best_sol_1st=None, init_pop=None, bias=None, uni_base=True, use_factor=opt.use_factor,
                              use_pleteau=False, precision=precision)
        best_sol = chkpt["best_sol"]
        best_runtime, best_throughput, best_energy, best_area, best_l1_size, best_l2_size, best_mac, best_power, best_num_pe = env.get_indiv_info(
            best_sol, num_pe=None, precision=precision)
        print("Mapping:", chkpt["best_sol"])
        print(
            f"Reward: {chkpt['best_reward'][0]:.3e}, Runtime: {best_runtime:.0f}(cycles), Area: {best_area / 1e6:.3f}(mm2), PE Area_ratio: {best_num_pe * MAC_AREA_INT8 / best_area * 100:.1f}%, Num_PE: {best_num_pe:.0f}, L1 Buffer: {best_l1_size:.0f}(elements), L2 Buffer: {best_l2_size:.0f}(elements)")
        chkpt = {
            "reward": chkpt['best_reward'][0],
            "Best_solution": best_sol,
            "Runtime": best_runtime,
            "Throughput (MACs/Cycle)": best_throughput,
            "Activity count-based Energy (nJ)": best_energy,
            "Area": best_area,
            "PE_Area_Ratio": best_num_pe * MAC_AREA_INT8 / best_area,
            "PE": best_num_pe,
            "PE_area": best_num_pe * MAC_AREA_INT8,
            "L1_area": best_l1_size * best_num_pe * BUF_AREA_perbit * 8,
            "L2_area": best_l2_size * BUF_AREA_perbit * 8,
            "L1_size": best_l1_size,
            "L2_size": best_l2_size
        }
        chkpt_list.append(chkpt)
        if opt.num_layer != 0:
            env.write_maestro(best_sol, m_file=opt.model, layer_id=num_layer, folder_path=os.path.dirname(chkpt_file),
                              precision=precision)
        else:
            env.write_maestro(best_sol, m_file=opt.model, layer_id=opt.singlelayer,
                              folder_path=os.path.dirname(chkpt_file), precision=precision)

        num_layer += 1

    columns = ["Runtime", "Throughput (MACs/Cycle)", "Activity count-based Energy (nJ)", "Area", "PE_Area_Ratio", "PE", "L1_size", "L2_size", "PE_area", "L1_area", "L2_area",
               "Best_solution"]
    np_array = None
    for chkpt in chkpt_list:
        if np_array is None:
            np_array = np.array([chkpt[t] for t in columns[:-1]] + [f'{chkpt["Best_solution"]}']).reshape(1, -1)
        else:
            np_array = np.vstack(
                [np_array, np.array([chkpt[t] for t in columns[:-1]] + [f'{chkpt["Best_solution"]}']).reshape(1, -1)])
    df = pd.DataFrame(np_array, columns=columns)
    df.to_csv(chkpt_file[:-4] + ".csv", index_label="Layer")

    with open(chkpt_file, "wb") as fd:
        pickle.dump(chkpt_list, fd)


def get_cstr_name(mapping_cstr):
    if mapping_cstr:
        cstr_name = mapping_cstr
    else:
        cstr_name = "free"
    return cstr_name


def get_value_for_precision(precision):
    if precision is None or precision == "FP32":
        return 2
    else:
        return 3


def get_value_for_pe(precision, num_pe):
    if precision is None or precision == "FP32":
        return num_pe
    if precision == "FP16":
        return int(num_pe * 2)
    if precision == "FP8":
        return int(num_pe * 4)
    if precision == "INT32":
        return int(num_pe)
    if precision == "INT16":
        return int(num_pe * 2)
    if precision == "INT8":
        return int(num_pe * 4)


def get_value_for_l1(precision, l1_size):
    if precision is None or precision == "FP32":
        return l1_size
    if precision == "FP16":
        return int(l1_size / 2)
    if precision == "FP8":
        return int(l1_size / 4)
    if precision == "INT32":
        return l1_size
    if precision == "INT16":
        return int(l1_size / 2)
    if precision == "INT8":
        return int(l1_size / 4)


def map_constraints(map_cstr, opt, precision):
    if opt.accel_cstr:
        accel_file = importlib.import_module(f'data.mapping_cstr.advanced_cstr.accel_cstr.{opt.accel_cstr}')
        accelator_cstr = accel_file.accel_cstr
        map_cstr = Constraint(num_pe=get_value_for_pe(precision, opt.num_pe))
        translate_to_actual_cstr(accelator_cstr, map_cstr)

    if opt.mapping_cstr:
        mapping_file = importlib.import_module(f'data.mapping_cstr.{opt.mapping_cstr}')
        mapping_cstr = mapping_file.mapping_cstr
        map_cstr = Constraint(num_pe=get_value_for_pe(precision, opt.num_pe)) if not map_cstr else map_cstr
        put_into_actual_cstr(mapping_cstr, map_cstr)

    if opt.costmodel_cstr:
        mapping_file = importlib.import_module(
            f'data.mapping_cstr.advanced_cstr.costmodel_cstr.{opt.costmodel_cstr}')
        costmodel_cstr = mapping_file.mapping_cstr
        map_cstr = Constraint(num_pe=get_value_for_pe(precision, opt.num_pe)) if not map_cstr else map_cstr
        put_into_actual_cstr(costmodel_cstr, map_cstr)

    return map_cstr
