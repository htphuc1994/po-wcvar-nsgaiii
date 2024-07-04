import re

def extract_arrays(text):
    # Regular expressions to find the required data
    ack_pattern = re.compile(r'ACK FOUND > 1; len\(fronts\)=(\d+)')
    n_nds_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*(\d+)\s*\|', re.MULTILINE)

    # Find all matches for ACK and n_nds
    ack_matches = ack_pattern.findall(text)
    n_nds_matches = n_nds_pattern.findall(text)

    # Convert matches to integers
    ack_array = list(map(int, ack_matches))
    n_nds_array = list(map(int, n_nds_matches))

    return ack_array, n_nds_array

# Given text data
text_data = """
ACK FOUND > 1; len(fronts)=5
==========================================================================================
n_gen  |  n_eval  | n_nds  |     cv_min    |     cv_avg    |      eps      |   indicator
==========================================================================================
     1 |      339 |      4 |  0.000000E+00 |  8.637182E+03 |             - |             -
ACK FOUND > 1; len(fronts)=2
     2 |      678 |      6 |  0.000000E+00 |  0.000000E+00 |  0.7782375103 |         ideal
"""

# Extract arrays
ack_array, n_nds_array = extract_arrays(text_data)

print("ACK Array:", ack_array)
print("n_nds Array:", n_nds_array)
