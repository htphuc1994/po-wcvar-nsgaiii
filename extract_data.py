import os
import glob

# input_file = 'output/output-06072024065058.txt'  # Replace with your input file path
# output_file = 'output/experiment_.txt'  # Replace with your output file path
patterns = ['len(fronts)', '========', 'n_gen  |  n_eval', '     ']  # The pattern to look for


def extract_file_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        last_two_lines = lines[-2:]
        # outfile.writelines(last_two_lines)

        lines_to_write = last_two_lines.copy()

        for line in lines:
            if any(pattern in line for pattern in patterns):
                lines_to_write.append(line)

        outfile.writelines(lines_to_write)

# Specify the folder containing the .txt files
input_path = 'output/temp'
# Change the current working directory to the specified folder
os.chdir(input_path)
# Find all .txt files in the folder
txt_files = glob.glob('*.txt')

# Read the contents of each text file
for txt_file in txt_files:
    with open(txt_file, 'r') as file:
        output_file = 'refined-' + txt_file
        extract_file_data(txt_file, output_file)
        print('done refined ' + txt_file)