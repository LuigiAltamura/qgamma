# value expressed in nJ/op
energy_data = {
    'FLOAT': {
        'MULT': {
            '7nm': {'FP32': 1.31e-3, 'FP16': 0.34e-3},
            '45nm': {'FP32': 3.7e-3, 'FP16': 1.1e-3, 'FP8': 0.327027027e-3, 'FP4': 0.097224251e-3},
            '22nm': {'FP32': 2.368e-3, 'FP16': 0.704e-3, 'FP8': 0.209297297e-3, 'FP4': 0.062223521e-3}
        },
        'ADD': {
            '7nm': {'FP32': 0.38e-3, 'FP16': 0.16e-3},
            '45nm': {'FP32': 0.9e-3, 'FP16': 0.4e-3, 'FP8': 0.2e-3, 'FP4': 0.1e-3},
            '22nm': {'FP32': 0.576e-3, 'FP16': 0.256e-3, 'FP8': 0.128e-3, 'FP4': 0.064e-3}
        },
        'MAC': {
            '7nm': {},
            '45nm': {'FP32': 16.8e-3, 'FP16': 7.85e-3, 'FP8': 3.802027027e-3, 'FP4': 2.183474251e-3},
            '22nm': {'FP32': 10.752e-3, 'FP16': 5.024e-3, 'FP8': 2.433297297e-3, 'FP4': 1.397423521e-3}
        }
    },
    'INT': {
        'MULT': {
            '7nm': {'INT32': 1.48e-3, 'INT8': 0.07e-3},
            '45nm': {'INT32': 3.1e-3, 'INT16': 0.8e-3, 'INT8': 0.2e-3, 'INT4': 0.05e-3, 'INT2': 0.003225806e-3},
            '22nm': {'INT32': 1.984e-3, 'INT8': 0.128e-3}
        },
        'ADD': {
            '7nm': {'INT32': 0.03e-3, 'INT8': 0.007e-3},
            '45nm': {'INT32': 0.1e-3, 'INT16': 0.06e-3, 'INT8': 0.03e-3, 'INT4': 0.015e-3, 'INT2': 0.0075e-3},
            '22nm (ext)': {'INT32': 0.064e-3, 'INT16': 0.0384e-3, 'INT8': 0.0192e-3, 'INT4': 0.0096e-3, 'INT2': 0.0048e-3}
        },
        'MAC': {
            '7nm': {},
            '45nm': {'INT32': 3.470506757e-3, 'INT16': 2.030506757e-3, 'INT8': 1.290506757e-3, 'INT4': 0.950506757e-3,
                     'INT2': 0.66211966e-3},
            '22nm': {'INT32': 2.221124324e-3, 'INT16': 1.299524324e-3, 'INT8': 0.825924324e-3, 'INT4': 0.608324324e-3,
                     'INT2': 0.423756582e-3}
        }
    }
}

# Read and Write values expressed in nJ
sram_data = {
    512: {'Write': 2.73e-13, 'Read': 2.91e-13, 'Leakage Power (mW)': 5.81e-05},
    1024: {'Write': 3.35e-13, 'Read': 4.18e-13, 'Leakage Power (mW)': 0.000130558},
    2048: {'Write': 5.06e-13, 'Read': 5.89e-13, 'Leakage Power (mW)': 0.000300498},
    4096: {'Write': 9.51e-13, 'Read': 9.73e-13, 'Leakage Power (mW)': 0.000518707},
    8192: {'Write': 1.51e-12, 'Read': 1.53e-12, 'Leakage Power (mW)': 0.00101401},
    16384: {'Write': 2.17e-12, 'Read': 2.24e-12, 'Leakage Power (mW)': 0.00210329},
    32768: {'Write': 3.39e-12, 'Read': 3.45e-12, 'Leakage Power (mW)': 0.00400746},
    65536: {'Write': 5.19e-12, 'Read': 5.30e-12, 'Leakage Power (mW)': 0.00865728},
    131072: {'Write': 7.94e-12, 'Read': 8.06e-12, 'Leakage Power (mW)': 0.0169947},
    262144: {'Write': 1.08e-11, 'Read': 1.09e-11, 'Leakage Power (mW)': 0.0326368},
    524288: {'Write': 1.62e-11, 'Read': 1.63e-11, 'Leakage Power (mW)': 0.0642241},
    1048576: {'Write': 2.22e-11, 'Read': 2.23e-11, 'Leakage Power (mW)': 0.125151},
    2097152: {'Write': 3.33e-11, 'Read': 3.34e-11, 'Leakage Power (mW)': 0.247646},
    4194304: {'Write': 4.59e-11, 'Read': 4.60e-11, 'Leakage Power (mW)': 0.487825},
    8388608: {'Write': 9.18e-11, 'Read': 9.2e-11, 'Leakage Power (mW)': 0.97565},
    16777216: {'Write': 1.836e-10, 'Read': 1.84e-10, 'Leakage Power (mW)': 1.9513},
    33554432: {'Write': 3.672e-10, 'Read': 3.68e-10, 'Leakage Power (mW)': 3.9026},
    67108864: {'Write': 7.344e-10, 'Read': 7.36e-10, 'Leakage Power (mW)': 7.8052},
    134217728: {'Write': 1.4688e-9, 'Read': 1.472e-9, 'Leakage Power (mW)': 15.6104},
    268435456: {'Write': 2.937e-9, 'Read': 2.944e-9, 'Leakage Power (mW)': 31.2208},
    536870912: {'Write': 5.8752e-9, 'Read': 5.88e-9, 'Leakage Power (mW)': 62.4416},
    1073741824: {'Write': 1.175e-8, 'Read': 1.176e-8, 'Leakage Power (mW)': 124.8832},
    2147483648: {'Write': 2.35e-8, 'Read': 2.352e-8, 'Leakage Power (mW)': 249.7664}
}

noc_dyn_energy_per_bit = 0.1143e-12  # J/bit/hop

precision_to_bits = {
    'FP32': 32,
    'FP16': 16,
    'FP8': 8,
    'FP4': 4,
    'INT32': 32,
    'INT16': 16,
    'INT8': 8,
    'INT4': 4,
    'INT2': 2
}


def get_sram_data(size, parameter):
    try:
        return sram_data[size][parameter]
    except KeyError:
        return None


def get_energy(operation, tech='22nm', precision=None):
    try:
        datatype = 'FLOAT' if precision.startswith('FP') else 'INT'
        return energy_data[datatype][operation][tech][precision]
    except KeyError:
        return None


def calculate_noc_dyn_energy(precision, bw, hops=2):
    if precision in precision_to_bits:
        bits = precision_to_bits[precision]
        # return a value expressed in nJ as for the other values considered
        return noc_dyn_energy_per_bit * bits * float(bw) * hops * 1e9
    else:
        raise ValueError(f"Unknown precision: {precision}")

