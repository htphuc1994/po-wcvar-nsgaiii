import os
import glob
import ast
import re

import constants

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

        # extract the chosen solution
        suitable_return = 0
        for line in lines:
            if line.startswith('Objectives'):
                # Extract the list part from the line
                list_str = line.split('=')[1].strip()
                # Convert the string representation of the list to an actual list
                objectives_list = ast.literal_eval(list_str)
                # Extract the first value
                suitable_return = objectives_list[0]
        begin_solution_marker = re.compile(r'Begin print with Final Cash: ([\d\.\-]+) => return: ' + re.escape(str(suitable_return[1:])))
        end_solution_marker = re.compile(r'Final Cash: ([\d\.\-]+) => return: ' + re.escape(str(suitable_return[1:])))

        capture = False
        for line in lines:
            if begin_solution_marker.search(line):
                capture = True
                lines_to_write.append(line)
            elif end_solution_marker.search(line):
                if capture:
                    lines_to_write.append(line)
                    break
            elif capture:
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