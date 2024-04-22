import os
import argparse

def extract_dataflow(file_name, output_folder):
    # Read the content of the original file
    with open(file_name, 'r') as f:
        content = f.read()

    # Find the starting and ending indices of the Dataflow section
    start_index = content.find("Dataflow {")
    end_index = content.find("}", start_index) + 1

    # Extract the Dataflow section
    dataflow_section = content[start_index:end_index]

    # Add a new line after the closing parenthesis
    dataflow_section += '\n'

    # Add a tab of shift to each line inside the Dataflow section, excluding the first and last lines
    lines = dataflow_section.split('\n')
    indented_lines = '\n'.join(lines[0:1] + ['\t' + line for line in lines[1:-2]] + lines[-2:])

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the output file path without the "_dataflow" suffix
    output_file_name = os.path.splitext(os.path.basename(file_name))[0].replace('_dataflow', '')
    output_file_path = os.path.join(output_folder, output_file_name + '.m')

    # Write the modified Dataflow content to the new file
    with open(output_file_path, 'w') as f:
        # Write the modified Dataflow section
        f.write(indented_lines)

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Extract Dataflow from a file and save to a new file.')

    # Add the file and output folder arguments
    parser.add_argument('--file', type=str, help='Path of the input file')
    parser.add_argument('--out', type=str, help='Path of the output folder')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if both --file and --out arguments are provided
    if args.file and args.out:
        # Extract the Dataflow part and save it to the output folder
        extract_dataflow(args.file, args.out)
    else:
        print("Both --file and --out arguments are required.")
