input_file = 'output/output-04072024115025.txt'  # Replace with your input file path
output_file = 'output/out-refined.txt'  # Replace with your output file path
patterns = ['len(fronts)', '========', 'n_gen  |  n_eval', '     ']  # The pattern to look for

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if any(pattern in line for pattern in patterns):
            outfile.write(line)