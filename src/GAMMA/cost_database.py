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
    512: {'Write': 2.73e-4, 'Read': 2.91e-4, 'Leakage Power (W)': 5.81e-5},
    1024: {'Write': 3.35e-4, 'Read': 4.18e-4, 'Leakage Power (W)': 1.30558e-4},
    2048: {'Write': 5.06e-4, 'Read': 5.89e-4, 'Leakage Power (W)': 3.00498e-4},
    4096: {'Write': 9.51e-4, 'Read': 9.73e-4, 'Leakage Power (W)': 5.18707e-4},
    8192: {'Write': 1.51e-3, 'Read': 1.53e-3, 'Leakage Power (W)': 1.01401e-3},
    16384: {'Write': 2.17e-3, 'Read': 2.24e-3, 'Leakage Power (W)': 2.10329e-3},
    32768: {'Write': 3.39e-3, 'Read': 3.45e-3, 'Leakage Power (W)': 4.00746e-3},
    65536: {'Write': 5.19e-3, 'Read': 5.30e-3, 'Leakage Power (W)': 8.65728e-3},
    131072: {'Write': 7.94e-3, 'Read': 8.06e-3, 'Leakage Power (W)': 1.69947e-2},
    262144: {'Write': 1.08e-2, 'Read': 1.09e-2, 'Leakage Power (W)': 3.26368e-2},
    524288: {'Write': 1.62e-2, 'Read': 1.63e-2, 'Leakage Power (W)': 6.42241e-2},
    1048576: {'Write': 2.22e-2, 'Read': 2.23e-2, 'Leakage Power (W)': 1.25151e-1},
    2097152: {'Write': 3.33e-2, 'Read': 3.34e-2, 'Leakage Power (W)': 2.47646e-1},
    4194304: {'Write': 4.59e-2, 'Read': 4.60e-2, 'Leakage Power (W)': 4.87825e-1},
    8388608: {'Write': 9.18e-2, 'Read': 9.20e-2, 'Leakage Power (W)': 9.7565e-1},
    16777216: {'Write': 1.836e-1, 'Read': 1.840e-1, 'Leakage Power (W)': 1.9513e+0},
    33554432: {'Write': 3.672e-1, 'Read': 3.680e-1, 'Leakage Power (W)': 3.9026e+0},
    67108864: {'Write': 7.344e-1, 'Read': 7.360e-1, 'Leakage Power (W)': 7.8052e+0},
    134217728: {'Write': 1.4688e+0, 'Read': 1.472e+0, 'Leakage Power (W)': 1.56104e+1},
    268435456: {'Write': 2.937e+0, 'Read': 2.944e+0, 'Leakage Power (W)': 3.12208e+1},
    536870912: {'Write': 5.8752e+0, 'Read': 5.880e+0, 'Leakage Power (W)': 6.24416e+1},
    1073741824: {'Write': 1.175e+1, 'Read': 1.176e+1, 'Leakage Power (W)': 1.248832e+2},
    2147483648: {'Write': 2.35e+1, 'Read': 2.352e+1, 'Leakage Power (W)': 2.497664e+2}
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

