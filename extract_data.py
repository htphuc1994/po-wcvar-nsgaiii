input_file = 'output/output-06072024065058.txt'  # Replace with your input file path
output_file = 'output/experiment_.txt'  # Replace with your output file path
patterns = ['len(fronts)', '========', 'n_gen  |  n_eval', '     ']  # The pattern to look for



with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    lines = infile.readlines()
    last_two_lines = lines[-2:]
    # outfile.writelines(last_two_lines)

    lines_to_write = last_two_lines.copy()

    for line in lines:
        if any(pattern in line for pattern in patterns):
            lines_to_write.append(line)
            # outfile.write(line)
    outfile.writelines(lines_to_write)