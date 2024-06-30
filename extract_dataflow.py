import os
import argparse

def extract_sections(file_name, output_folder, output_file_name=None):
    # Read the content of the original file
    with open(file_name, 'r') as f:
        content = f.read()

    # Initialize sections
    precision_section = ""
    dataflow_section = ""

    # Find the Precision section, if it exists
    precision_start_index = content.find("Precision:")
    if precision_start_index != -1:
        precision_end_index = content.find("}", precision_start_index) + 1
        precision_section = content[precision_start_index:precision_end_index]
        precision_section += '\n'

    # Find the Dataflow section
    dataflow_start_index = content.find("Dataflow {")
    if dataflow_start_index != -1:
        dataflow_end_index = content.find("}", dataflow_start_index) + 1
        dataflow_section = content[dataflow_start_index:dataflow_end_index]
        dataflow_section += '\n'

        # Indent lines in Dataflow section (excluding the first and last lines)
        dataflow_lines = dataflow_section.split('\n')
        indented_dataflow_lines = '\n'.join(dataflow_lines[0:1] + ['\t' + line for line in dataflow_lines[1:-1]] + dataflow_lines[-1:])
        dataflow_section = indented_dataflow_lines

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Determine the output file name
    if output_file_name is None:
        output_file_name = os.path.basename(file_name)
    output_file_path = os.path.join(output_folder, output_file_name)

    # Write the modified Precision and Dataflow sections to the new file
    with open(output_file_path, 'w') as f:
        if precision_section:
            f.write(precision_section)
        if dataflow_section:
            f.write(dataflow_section)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Extract Precision and Dataflow from a file and save to a new file.')

    # Add the file and output folder arguments
    parser.add_argument('--file', type=str, required=True, help='Path of the input file')
    parser.add_argument('--out', type=str, required=True, help='Path of the output folder')
    parser.add_argument('--outname', type=str, help='Optional name of the output file')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract the Precision and Dataflow parts and save them to the output folder
    extract_sections(args.file, args.out, args.outname)
