import copy
import argparse
from datetime import datetime

import glob
import os, sys
import cost_database as cdb

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


def train_model(model_defs, input_arg, chkpt_file='./chkpt', precisions=None, stride=None):
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

        layer_stride = stride[num_layer-1]

        map_cstr = map_constraints(map_cstr, opt, precision)

        env.reset_dimension(fitness=fitness, constraints=constraints, dimension=dimension, stride=layer_stride)
        env.reset_hw_parm(num_pe=get_value_for_pe(precision, opt.num_pe),
                          l1_size=opt.l1_size,
                          l2_size=opt.l2_size, pe_limit=opt.pe_limit,
                          area_pebuf_only=False, external_area_model=True, map_cstr=map_cstr,
                          slevel_max=get_value_for_precision(precision), slevel_min=get_value_for_precision(precision),
                          precision=precision)
        #tolto calcolo su l1 value da verificare se rimettere
        chkpt, pops = env.run(dimension, stage_idx=0, num_population=opt.num_pop, prev_stage_value=None,
                              num_generations=opt.epochs,
                              best_sol_1st=None, init_pop=None, bias=None, uni_base=True, use_factor=opt.use_factor,
                              use_pleteau=False)
        best_sol = chkpt["best_sol"]
        (best_runtime, best_throughput, best_energy, best_area, best_l1_size, best_l2_size, best_mac, best_power,
         best_num_pe, best_l1_read, best_l1_write, best_l2_read, best_l2_write, best_avg_pe, best_avg_bw) = \
            (env.get_indiv_info(best_sol, num_pe=None, precision=precision))
        print("Mapping:", chkpt["best_sol"])
        print(
            f"{num_layer}. Reward: {chkpt['best_reward'][0]:.3e}, Runtime: {best_runtime:.0f}(cycles), "
            f"Area: {best_area / 1e6:.3f}(mm2), Num_PE: {best_num_pe:.0f}, L1 Buffer: {best_l1_size:.0f}(elements),"
            f" L2 Buffer: {best_l2_size:.0f}(elements)")
        chkpt = {
            "reward": chkpt['best_reward'][0],
            "Best_solution": best_sol,
            "Runtime": best_runtime,
            "Throughput (MACs/Cycle)": best_throughput,
            "Activity count-based Energy (nJ)": best_energy,
            "Area": best_area,
            "PE": best_num_pe,
            "PE_area": best_num_pe * MAC_AREA_INT8,
            "L1_area": best_l1_size * best_num_pe * BUF_AREA_perbit * 8,
            "L2_area": best_l2_size * BUF_AREA_perbit * 8,
            "L1_size": best_l1_size,
            "L2_size": best_l2_size,
            "L1_read": best_l1_read,
            "L1_write": best_l1_write,
            "L2_read": best_l2_read,
            "L2_write": best_l2_write,
            "#MACs": best_mac,
            "Avg #PE utilized": best_avg_pe,
            "Avg BW": best_avg_bw
        }
        chkpt_list.append(chkpt)
        if opt.num_layer != 0:
            env.write_maestro(best_sol, m_file=opt.model, layer_id=num_layer, folder_path=os.path.dirname(chkpt_file),
                              precision=precision)
        else:
            env.write_maestro(best_sol, m_file=opt.model, layer_id=opt.singlelayer,
                              folder_path=os.path.dirname(chkpt_file), precision=precision)

        num_layer += 1

    columns = ["Runtime", "Throughput (MACs/Cycle)", "Activity count-based Energy (nJ)", "PE",
               "L1_size", "L2_size", "L1_read", "L1_write", "L2_read", "L2_write",
               "#MACs", "Avg #PE utilized", "Avg BW", "Best_solution"]
    np_array = None
    for chkpt in chkpt_list:
        if np_array is None:
            np_array = np.array([chkpt[t] for t in columns[:-1]] + [f'{chkpt["Best_solution"]}']).reshape(1, -1)
        else:
            np_array = np.vstack(
                [np_array, np.array([chkpt[t] for t in columns[:-1]] + [f'{chkpt["Best_solution"]}']).reshape(1, -1)])
    df = pd.DataFrame(np_array, columns=columns)

    if precisions is not None:
        df['L1_size(bytes)'] = df.apply(
            lambda row: convert_to_bytes(row['L1_size'], precisions[df.index.get_loc(row.name)]),
            axis=1).astype(int)
        # Add 'sram_size' to the DataFrame
        df['L1_normalized_size'] = df['L1_size(bytes)'].apply(find_sram_size)
        df['L1_read_energy'] = df.apply(lambda row: float(row['L1_read']) * cdb.get_sram_data(row['L1_normalized_size'], 'Read'),
                                        axis=1)
        df['L1_write_energy'] = df.apply(
            lambda row: float(row['L1_write']) * cdb.get_sram_data(row['L1_normalized_size'], 'Write'), axis=1)
        df['L2_size(bytes)'] = df.apply(
            lambda row: convert_to_bytes(row['L2_size'], precisions[df.index.get_loc(row.name)]), axis=1).astype(int)

        df['L2_normalized_size'] = df['L2_size(bytes)'].apply(find_sram_size)
        df['L2_read_energy'] = df.apply(lambda row: float(row['L2_read']) * cdb.get_sram_data(row['L2_normalized_size'], 'Read'),
                                        axis=1)
        df['L2_write_energy'] = df.apply(
            lambda row: float(row['L2_write']) * cdb.get_sram_data(row['L2_normalized_size'], 'Write'), axis=1)
        df['MAC_energy'] = df.apply(lambda row: cdb.get_energy(operation='MAC', precision=precisions[df.index.get_loc(row.name)]) * float(row['#MACs']), axis=1)
        df['NoC_energy'] = df.apply(lambda row: cdb.calculate_noc_dyn_energy(precision=precisions[row.name], bw=row['Avg BW']), axis=1)
        df['L1 energy'] = df['L1_read_energy'] + df['L1_write_energy']
        df['L2 energy'] = df['L2_read_energy'] + df['L2_write_energy']
        df['Activity count-based Energy (nJ)'] = df['Activity count-based Energy (nJ)'].astype(float).astype(int)
        df['Runtime'] = df['Runtime'].astype(float).astype(int)
        df['EDP'] = df['Activity count-based Energy (nJ)'] * df['Runtime']
        df['#MACs'] = df['#MACs'].astype(float).astype(int)
        df['Runtime'] = df['Runtime'].astype(float).astype(int)
        df['Activity count-based Energy (nJ)'] = df['Activity count-based Energy (nJ)'].astype('int')
        df['PE'] = df['PE'].astype(float).astype(int)
        df['L1_size'] = df['L1_size'].astype(float).astype(int)
        df['L2_size'] = df['L2_size'].astype(float).astype(int)
        df['L1_read'] = df['L1_read'].astype(float).astype(int)
        df['L1_write'] = df['L1_write'].astype(float).astype(int)
        df['L2_read'] = df['L2_read'].astype(float).astype(int)
        df['L2_write'] = df['L2_write'].astype(float).astype(int)
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
    if precision is None or precision == "FP32" or precision == "INT32":
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
    if precision == "FP4":
        return int(num_pe * 8)
    if precision == "FP2":
        return int(num_pe * 16)
    if precision == "INT32":
        return int(num_pe)
    if precision == "INT16":
        return int(num_pe * 2)
    if precision == "INT8":
        return int(num_pe * 4)
    if precision == "INT4":
        return int(num_pe * 8)
    if precision == "INT2":
        return int(num_pe * 16)


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


def convert_to_bytes(size, precision):
    if precision in cdb.precision_to_bits:
        bits = cdb.precision_to_bits[precision]
        return (int(float(size)) * bits) / 8
    else:
        raise ValueError(f"Unknown precision: {precision}")


# Function to find the appropriate SRAM size
def find_sram_size(required_bytes):
    for size in sorted(cdb.sram_data.keys()):
        if size >= required_bytes:
            return size
    raise ValueError(f"No suitable SRAM size found for {required_bytes} bytes")


