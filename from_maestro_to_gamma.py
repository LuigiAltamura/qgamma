import csv
import re
import argparse

def parse_m_file(file_path):
    layers = []
    with open('../qmaestro/data/model/' + file_path, 'r') as file:
        content = file.read()
        layers_type = re.findall(r'Type: (\w+)', content, re.DOTALL)
        dimension_matches = re.findall(r'Dimensions \{.*?\}', content, re.DOTALL)
        stride_matches = re.findall(r'Stride \{.*?\}', content, re.DOTALL)

        for i, (dimensions, stride) in enumerate(zip(dimension_matches, stride_matches)):
            dim_values = re.findall(r'\b\w: \d+', dimensions)
            stride_values = re.findall(r'\b\w: \d+', stride)
            dim_dict = {d.split(': ')[0]: int(d.split(': ')[1]) for d in dim_values}
            stride_dict = {s.split(': ')[0]: int(s.split(': ')[1]) for s in stride_values}

            if layers_type[i] == 'DSCONV':
                dim_dict['T'] = 2
            else:
                dim_dict['T'] = 1

            dim_dict['SX'] = stride_dict.get('X', 1)
            dim_dict['SY'] = stride_dict.get('Y', 1)
            layers.append(dim_dict)
    return layers

def write_csv(layers, precision, output_file):
    with open('./data/model/'+ output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["K", "C", "Y", "X", "R", "S", "T", "SX", "SY", "Precision"])
        for layer in layers:
            writer.writerow([
                layer.get('K', 0),
                layer.get('C', 0),
                layer.get('Y', 0),
                layer.get('X', 0),
                layer.get('R', 0),
                layer.get('S', 0),
                layer.get('T', 1),
                layer.get('SX', 1),
                layer.get('SY', 1),
                precision
            ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a .m file and generate a CSV.')
    parser.add_argument('input_file', type=str, help='Path to the input .m file')
    parser.add_argument('precision', type=str, help='Precision value for the CSV')
    parser.add_argument('output_file', type=str, help='Path to the output CSV file')
    args = parser.parse_args()

    layers = parse_m_file(args.input_file)
    write_csv(layers, args.precision, args.output_file)