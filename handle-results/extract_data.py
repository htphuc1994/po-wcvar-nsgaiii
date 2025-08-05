import re

def extract_arrays(text):
    # Regular expressions to find the required data
    ack_pattern = re.compile(r'ACK FOUND > 1; len\(fronts\)=(\d+)')
    n_nds_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*(\d+)\s*\|', re.MULTILINE)
    # eps_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s+[0-9.E+-]+\s+\|\s+[0-9.E+-]+\s+\|\s+([0-9.]+|-)\s+\|', re.MULTILINE)
    # eps_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s+[0-9.E+-]+\s+\|\s+[0-9.E+-]+\s+\|\s+([0-9.E+-]+|-)\s+\|', re.MULTILINE)
    # indicator_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s+[0-9.E+-]+\s+\|\s+[0-9.E+-]+\s+\|\s+[0-9.]+|-\s+\|\s+([a-zA-Z-]+)\s*\n', re.MULTILINE)
    # indicator_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s+[0-9.E+-]+\s+\|\s+[0-9.E+-]+\s+\|\s+[0-9.E+-]+|-\s+\|\s+([a-zA-Z-]+)\s*$', re.MULTILINE)
    # indicator_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s+[0-9.E+-]+\s+\|\s+[0-9.E+-]+\s+\|\s+([0-9.E+-]+|-)\s+\|\s+([a-zA-Z-]+)\s*$', re.MULTILINE)

    line_pattern = re.compile(r'^\s*\d+\s*\|\s*\d+\s*\|\s*\d+\s*\|\s+([0-9.E+-]+)\s+\|\s+([0-9.E+-]+)\s+\|\s+([0-9.E+-]+|-)\s+\|\s+([a-zA-Z-]+)\s*$', re.MULTILINE)

    # Find all matches for ACK and n_nds
    ack_matches = ack_pattern.findall(text)
    n_nds_matches = n_nds_pattern.findall(text)
    # eps_matches = eps_pattern.findall(text)
    # indicator_matches = indicator_pattern.findall(text)
    # indicator_matches = indicator_pattern.finditer(text)
    line_matches = line_pattern.finditer(text)

    # Convert matches to integers
    ack_array = list(map(int, ack_matches))
    n_nds_array = list(map(int, n_nds_matches))
    # eps_array = [float('NaN') if v == '-' else float(v) for v in eps_matches]
    # indicator_array = list(map(str, indicator_matches))
    cv_min_array = []
    cv_avg_array = []
    eps_array = []
    indicator_array = []
    # for match in indicator_matches:
    #     indicator_array.append(match.group(2).strip())
    # indicator_array = [match.group(1) for match in indicator_pattern.finditer(text) if match.group(1)]
    for match in line_matches:
        cv_min_array.append(float(match.group(1)))
        cv_avg_array.append(float(match.group(2)))
        eps_array.append(float(match.group(3)) if match.group(3) != '-' else float('nan'))
        indicator_array.append(match.group(4).strip())

    return ack_array, n_nds_array, eps_array, indicator_array

# Given text data
text_data = """
Objectives = ['-0.2035273731406', '0.0034615528590', '0.2985444958479', '0.0350776723685', '0.1040432445387', '0.1382970650287', '0.1457005384351', '0.0882995626138', '0.1478373373461', '0.4690795680723', '0.4905515803680', '0.4170157196841']
The time of execution of above program is : 247362.65802383423 ms
ACK FOUND > 1; len(fronts)=4
==========================================================================================
n_gen  |  n_eval  | n_nds  |     cv_min    |     cv_avg    |      eps      |   indicator  
==========================================================================================
     1 |      179 |      7 |  0.000000E+00 |  1.009005E+04 |             - |             -
ACK FOUND > 1; len(fronts)=1
     2 |      358 |     10 |  0.000000E+00 |  0.000000E+00 |  0.6590569256 |         ideal
ACK FOUND > 1; len(fronts)=1
     3 |      537 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2148645665 |         ideal
ACK FOUND > 1; len(fronts)=1
     4 |      716 |     11 |  0.000000E+00 |  0.000000E+00 |  0.3137574132 |         ideal
ACK FOUND > 1; len(fronts)=1
     5 |      895 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2178343222 |         ideal
ACK FOUND > 1; len(fronts)=1
     6 |     1074 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2769711122 |         ideal
ACK FOUND > 1; len(fronts)=1
     7 |     1253 |     14 |  0.000000E+00 |  0.000000E+00 |  0.4239672002 |         ideal
ACK FOUND > 1; len(fronts)=1
     8 |     1432 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2524353288 |         ideal
ACK FOUND > 1; len(fronts)=1
     9 |     1611 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0990371535 |         ideal
ACK FOUND > 1; len(fronts)=1
    10 |     1790 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1354515488 |         ideal
ACK FOUND > 1; len(fronts)=1
    11 |     1969 |     14 |  0.000000E+00 |  0.000000E+00 |  0.4006249668 |         ideal
ACK FOUND > 1; len(fronts)=1
    12 |     2148 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1320667105 |         ideal
ACK FOUND > 1; len(fronts)=1
    13 |     2327 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2083400707 |         ideal
ACK FOUND > 1; len(fronts)=1
    14 |     2506 |     12 |  0.000000E+00 |  0.000000E+00 |  0.3440603714 |         ideal
ACK FOUND > 1; len(fronts)=1
    15 |     2685 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2373453396 |         ideal
ACK FOUND > 1; len(fronts)=1
    16 |     2864 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1898810283 |         ideal
ACK FOUND > 1; len(fronts)=1
    17 |     3043 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1689151619 |         ideal
ACK FOUND > 1; len(fronts)=1
    18 |     3222 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1708523040 |         ideal
ACK FOUND > 1; len(fronts)=1
    19 |     3401 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1547411499 |         ideal
ACK FOUND > 1; len(fronts)=1
    20 |     3580 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0090838702 |         ideal
ACK FOUND > 1; len(fronts)=1
    21 |     3759 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2085518021 |         ideal
ACK FOUND > 1; len(fronts)=1
    22 |     3938 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1643375627 |         ideal
ACK FOUND > 1; len(fronts)=1
    23 |     4117 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1415959776 |         ideal
ACK FOUND > 1; len(fronts)=1
    24 |     4296 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1026190312 |         ideal
ACK FOUND > 1; len(fronts)=1
    25 |     4475 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2502927476 |         ideal
ACK FOUND > 1; len(fronts)=1
    26 |     4654 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0154920417 |         ideal
ACK FOUND > 1; len(fronts)=1
    27 |     4833 |     11 |  0.000000E+00 |  0.000000E+00 |  0.5757755944 |         ideal
ACK FOUND > 1; len(fronts)=1
    28 |     5012 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2073151799 |         ideal
ACK FOUND > 1; len(fronts)=1
    29 |     5191 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1684520534 |         ideal
ACK FOUND > 1; len(fronts)=1
    30 |     5370 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0632833592 |         ideal
ACK FOUND > 1; len(fronts)=1
    31 |     5549 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1369204355 |         ideal
ACK FOUND > 1; len(fronts)=1
    32 |     5728 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2525652634 |         ideal
ACK FOUND > 1; len(fronts)=1
    33 |     5907 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0861360960 |         ideal
ACK FOUND > 1; len(fronts)=1
    34 |     6086 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0611123235 |         ideal
ACK FOUND > 1; len(fronts)=1
    35 |     6265 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0434934099 |         ideal
ACK FOUND > 1; len(fronts)=1
    36 |     6444 |     25 |  0.000000E+00 |  0.000000E+00 |  0.2323786475 |         ideal
ACK FOUND > 1; len(fronts)=1
    37 |     6623 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0735622703 |         ideal
ACK FOUND > 1; len(fronts)=1
    38 |     6802 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1017653496 |         ideal
ACK FOUND > 1; len(fronts)=1
    39 |     6981 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0171362391 |         ideal
ACK FOUND > 1; len(fronts)=1
    40 |     7160 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1315091511 |         ideal
ACK FOUND > 1; len(fronts)=1
    41 |     7339 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2074449011 |         ideal
ACK FOUND > 1; len(fronts)=1
    42 |     7518 |      7 |  0.000000E+00 |  0.000000E+00 |  1.0388315729 |         ideal
ACK FOUND > 1; len(fronts)=1
    43 |     7697 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3609692708 |         ideal
ACK FOUND > 1; len(fronts)=1
    44 |     7876 |      8 |  0.000000E+00 |  0.000000E+00 |  0.5652678957 |         ideal
ACK FOUND > 1; len(fronts)=1
    45 |     8055 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2483588856 |         ideal
ACK FOUND > 1; len(fronts)=1
    46 |     8234 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0818835010 |         ideal
ACK FOUND > 1; len(fronts)=1
    47 |     8413 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0341929209 |         ideal
ACK FOUND > 1; len(fronts)=1
    48 |     8592 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0273479190 |         ideal
ACK FOUND > 1; len(fronts)=1
    49 |     8771 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0394926922 |         ideal
ACK FOUND > 1; len(fronts)=1
    50 |     8950 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0737266722 |         ideal
ACK FOUND > 1; len(fronts)=1
    51 |     9129 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0916400873 |         ideal
ACK FOUND > 1; len(fronts)=1
    52 |     9308 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2067145101 |         ideal
ACK FOUND > 1; len(fronts)=1
    53 |     9487 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0766630655 |         ideal
ACK FOUND > 1; len(fronts)=1
    54 |     9666 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1735743456 |         ideal
ACK FOUND > 1; len(fronts)=1
    55 |     9845 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0059887456 |         ideal
ACK FOUND > 1; len(fronts)=1
    56 |    10024 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0894326276 |         ideal
ACK FOUND > 1; len(fronts)=1
    57 |    10203 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1112785415 |         ideal
ACK FOUND > 1; len(fronts)=1
    58 |    10382 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2359287572 |         ideal
ACK FOUND > 1; len(fronts)=1
    59 |    10561 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0334045213 |         ideal
ACK FOUND > 1; len(fronts)=1
    60 |    10740 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1069611022 |         ideal
ACK FOUND > 1; len(fronts)=1
    61 |    10919 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0092050860 |         ideal
ACK FOUND > 1; len(fronts)=1
    62 |    11098 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1225993628 |         ideal
ACK FOUND > 1; len(fronts)=1
    63 |    11277 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0857069957 |         ideal
ACK FOUND > 1; len(fronts)=1
    64 |    11456 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1166290031 |         ideal
ACK FOUND > 1; len(fronts)=1
    65 |    11635 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1320272043 |         ideal
ACK FOUND > 1; len(fronts)=1
    66 |    11814 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1103455640 |         ideal
ACK FOUND > 1; len(fronts)=1
    67 |    11993 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1553319788 |         ideal
ACK FOUND > 1; len(fronts)=1
    68 |    12172 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1752054280 |         ideal
ACK FOUND > 1; len(fronts)=1
    69 |    12351 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0813744570 |         ideal
ACK FOUND > 1; len(fronts)=1
    70 |    12530 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0711321330 |         ideal
ACK FOUND > 1; len(fronts)=1
    71 |    12709 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1718220835 |         ideal
ACK FOUND > 1; len(fronts)=1
    72 |    12888 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1228363428 |         ideal
ACK FOUND > 1; len(fronts)=1
    73 |    13067 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0160175340 |         ideal
ACK FOUND > 1; len(fronts)=1
    74 |    13246 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1758951010 |         ideal
ACK FOUND > 1; len(fronts)=1
    75 |    13425 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1495840070 |         ideal
ACK FOUND > 1; len(fronts)=1
    76 |    13604 |     34 |  0.000000E+00 |  0.000000E+00 |  0.1613482132 |         ideal
ACK FOUND > 1; len(fronts)=1
    77 |    13783 |     32 |  0.000000E+00 |  0.000000E+00 |  0.1378709211 |         ideal
ACK FOUND > 1; len(fronts)=1
    78 |    13962 |     31 |  0.000000E+00 |  0.000000E+00 |  0.1030810052 |         ideal
ACK FOUND > 1; len(fronts)=1
    79 |    14141 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0223643672 |         nadir
ACK FOUND > 1; len(fronts)=1
    80 |    14320 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0698317872 |             f
ACK FOUND > 1; len(fronts)=1
    81 |    14499 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0173785165 |         ideal
ACK FOUND > 1; len(fronts)=1
    82 |    14678 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0294889275 |         ideal
ACK FOUND > 1; len(fronts)=1
    83 |    14857 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0193359665 |         ideal
ACK FOUND > 1; len(fronts)=1
    84 |    15036 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0384829448 |         ideal
ACK FOUND > 1; len(fronts)=1
    85 |    15215 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0197840994 |         ideal
ACK FOUND > 1; len(fronts)=1
    86 |    15394 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1161303975 |         nadir
ACK FOUND > 1; len(fronts)=1
    87 |    15573 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0413346689 |         ideal
ACK FOUND > 1; len(fronts)=1
    88 |    15752 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0568518068 |         ideal
ACK FOUND > 1; len(fronts)=1
    89 |    15931 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0088014979 |         ideal
ACK FOUND > 1; len(fronts)=1
    90 |    16110 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0808371981 |         ideal
ACK FOUND > 1; len(fronts)=1
    91 |    16289 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0879465509 |         ideal
ACK FOUND > 1; len(fronts)=1
    92 |    16468 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1402333657 |         ideal
ACK FOUND > 1; len(fronts)=1
    93 |    16647 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0236664697 |         nadir
ACK FOUND > 1; len(fronts)=1
    94 |    16826 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1061693520 |         ideal
ACK FOUND > 1; len(fronts)=1
    95 |    17005 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0492606799 |         ideal
ACK FOUND > 1; len(fronts)=1
    96 |    17184 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1790613457 |         ideal
ACK FOUND > 1; len(fronts)=1
    97 |    17363 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0167388542 |         ideal
ACK FOUND > 1; len(fronts)=1
    98 |    17542 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0783892404 |         ideal
ACK FOUND > 1; len(fronts)=1
    99 |    17721 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0797283107 |         ideal
ACK FOUND > 1; len(fronts)=1
   100 |    17900 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0873420242 |         ideal
ACK FOUND > 1; len(fronts)=1
   101 |    18079 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0509063236 |         ideal
ACK FOUND > 1; len(fronts)=1
   102 |    18258 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0589608405 |         ideal
ACK FOUND > 1; len(fronts)=1
   103 |    18437 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0526967721 |         ideal
ACK FOUND > 1; len(fronts)=1
   104 |    18616 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0322681485 |         ideal
ACK FOUND > 1; len(fronts)=1
   105 |    18795 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0891043477 |         ideal
ACK FOUND > 1; len(fronts)=1
   106 |    18974 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0434748721 |         ideal
ACK FOUND > 1; len(fronts)=1
   107 |    19153 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0454508417 |         ideal
ACK FOUND > 1; len(fronts)=1
   108 |    19332 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0333441009 |         ideal
ACK FOUND > 1; len(fronts)=1
   109 |    19511 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0982716270 |         ideal
ACK FOUND > 1; len(fronts)=1
   110 |    19690 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0098479345 |         ideal
ACK FOUND > 1; len(fronts)=1
   111 |    19869 |     29 |  0.000000E+00 |  0.000000E+00 |  0.3417009885 |         nadir
ACK FOUND > 1; len(fronts)=1
   112 |    20048 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0110155950 |         ideal
ACK FOUND > 1; len(fronts)=1
   113 |    20227 |     31 |  0.000000E+00 |  0.000000E+00 |  0.1103203173 |         ideal
ACK FOUND > 1; len(fronts)=1
   114 |    20406 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0495747639 |         ideal
ACK FOUND > 1; len(fronts)=1
   115 |    20585 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0088480675 |         ideal
ACK FOUND > 1; len(fronts)=1
   116 |    20764 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0063123878 |         ideal
ACK FOUND > 1; len(fronts)=1
   117 |    20943 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0171537159 |         ideal
ACK FOUND > 1; len(fronts)=1
   118 |    21122 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0168644283 |         ideal
ACK FOUND > 1; len(fronts)=1
   119 |    21301 |     30 |  0.000000E+00 |  0.000000E+00 |  0.2637964252 |         nadir
ACK FOUND > 1; len(fronts)=1
   120 |    21480 |     26 |  0.000000E+00 |  0.000000E+00 |  2.2462929202 |         nadir
ACK FOUND > 1; len(fronts)=1
   121 |    21659 |     25 |  0.000000E+00 |  0.000000E+00 |  0.6919563254 |         nadir
ACK FOUND > 1; len(fronts)=1
   122 |    21838 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0771505536 |         ideal
ACK FOUND > 1; len(fronts)=1
   123 |    22017 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0149925871 |         ideal
ACK FOUND > 1; len(fronts)=1
   124 |    22196 |     24 |  0.000000E+00 |  0.000000E+00 |  0.6289181915 |         nadir
ACK FOUND > 1; len(fronts)=1
   125 |    22375 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0988543539 |         ideal
ACK FOUND > 1; len(fronts)=1
   126 |    22554 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0766518815 |         ideal
ACK FOUND > 1; len(fronts)=1
   127 |    22733 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0435148335 |         ideal
ACK FOUND > 1; len(fronts)=1
   128 |    22912 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0314658387 |         ideal
ACK FOUND > 1; len(fronts)=1
   129 |    23091 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0166607863 |         ideal
ACK FOUND > 1; len(fronts)=1
   130 |    23270 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0825995475 |         ideal
ACK FOUND > 1; len(fronts)=1
   131 |    23449 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0050880401 |         ideal
ACK FOUND > 1; len(fronts)=1
   132 |    23628 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0284872500 |         ideal
ACK FOUND > 1; len(fronts)=1
   133 |    23807 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0067781249 |         ideal
ACK FOUND > 1; len(fronts)=1
   134 |    23986 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0511295925 |         ideal
ACK FOUND > 1; len(fronts)=1
   135 |    24165 |     40 |  0.000000E+00 |  0.000000E+00 |  0.0086074652 |         ideal
ACK FOUND > 1; len(fronts)=1
   136 |    24344 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0583865287 |         ideal
ACK FOUND > 1; len(fronts)=1
   137 |    24523 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0271840555 |         ideal
ACK FOUND > 1; len(fronts)=1
   138 |    24702 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0536177358 |         ideal
ACK FOUND > 1; len(fronts)=1
   139 |    24881 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0279611938 |         ideal
ACK FOUND > 1; len(fronts)=1
   140 |    25060 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0404993841 |         ideal
ACK FOUND > 1; len(fronts)=1
   141 |    25239 |     35 |  0.000000E+00 |  0.000000E+00 |  0.0157459176 |         ideal
ACK FOUND > 1; len(fronts)=1
   142 |    25418 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0047435562 |         ideal
ACK FOUND > 1; len(fronts)=1
   143 |    25597 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1010207773 |         ideal
ACK FOUND > 1; len(fronts)=1
   144 |    25776 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0810087290 |         ideal
ACK FOUND > 1; len(fronts)=1
   145 |    25955 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0340026637 |         ideal
ACK FOUND > 1; len(fronts)=1
   146 |    26134 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0408841548 |         ideal
ACK FOUND > 1; len(fronts)=1
   147 |    26313 |     35 |  0.000000E+00 |  0.000000E+00 |  0.0537963394 |         ideal
ACK FOUND > 1; len(fronts)=1
   148 |    26492 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0267575038 |         ideal
ACK FOUND > 1; len(fronts)=1
   149 |    26671 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0128057830 |         ideal
ACK FOUND > 1; len(fronts)=1
   150 |    26850 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0233407065 |         ideal
ACK FOUND > 1; len(fronts)=1
   151 |    27029 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0029341095 |         nadir
ACK FOUND > 1; len(fronts)=1
   152 |    27208 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1792457247 |         nadir
ACK FOUND > 1; len(fronts)=1
   153 |    27387 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0088893040 |         ideal
ACK FOUND > 1; len(fronts)=1
   154 |    27566 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0759980085 |         ideal
ACK FOUND > 1; len(fronts)=1
   155 |    27745 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0204940983 |         ideal
ACK FOUND > 1; len(fronts)=1
   156 |    27924 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0121638918 |         ideal
ACK FOUND > 1; len(fronts)=1
   157 |    28103 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0041302252 |         ideal
ACK FOUND > 1; len(fronts)=1
   158 |    28282 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0209228942 |         ideal
ACK FOUND > 1; len(fronts)=1
   159 |    28461 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0335559765 |         ideal
ACK FOUND > 1; len(fronts)=1
   160 |    28640 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0183001226 |         ideal
ACK FOUND > 1; len(fronts)=1
   161 |    28819 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0126648363 |         ideal
ACK FOUND > 1; len(fronts)=1
   162 |    28998 |     31 |  0.000000E+00 |  0.000000E+00 |  0.3747526674 |         nadir
ACK FOUND > 1; len(fronts)=1
   163 |    29177 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0487064041 |         ideal
ACK FOUND > 1; len(fronts)=1
   164 |    29356 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0246185632 |         ideal
ACK FOUND > 1; len(fronts)=1
   165 |    29535 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0648569679 |         nadir
ACK FOUND > 1; len(fronts)=1
   166 |    29714 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0609067413 |         nadir
ACK FOUND > 1; len(fronts)=1
   167 |    29893 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0648569679 |         nadir
ACK FOUND > 1; len(fronts)=1
   168 |    30072 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0529551605 |         ideal
ACK FOUND > 1; len(fronts)=1
   169 |    30251 |     36 |  0.000000E+00 |  0.000000E+00 |  0.0287070732 |         ideal
ACK FOUND > 1; len(fronts)=1
   170 |    30430 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0742002194 |         ideal
ACK FOUND > 1; len(fronts)=1
   171 |    30609 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0690748504 |         ideal
ACK FOUND > 1; len(fronts)=1
   172 |    30788 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0931189372 |         ideal
ACK FOUND > 1; len(fronts)=1
   173 |    30967 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0451494120 |         ideal
ACK FOUND > 1; len(fronts)=1
   174 |    31146 |     36 |  0.000000E+00 |  0.000000E+00 |  0.0358564935 |         ideal
ACK FOUND > 1; len(fronts)=1
   175 |    31325 |     37 |  0.000000E+00 |  0.000000E+00 |  0.0571925573 |         ideal
ACK FOUND > 1; len(fronts)=1
   176 |    31504 |     40 |  0.000000E+00 |  0.000000E+00 |  0.6028061260 |         nadir
ACK FOUND > 1; len(fronts)=1
   177 |    31683 |     36 |  0.000000E+00 |  0.000000E+00 |  0.0710071239 |         ideal
ACK FOUND > 1; len(fronts)=1
   178 |    31862 |     37 |  0.000000E+00 |  0.000000E+00 |  0.0764345192 |         ideal
ACK FOUND > 1; len(fronts)=1
   179 |    32041 |     38 |  0.000000E+00 |  0.000000E+00 |  0.0642057386 |         ideal
ACK FOUND > 1; len(fronts)=1
   180 |    32220 |     40 |  0.000000E+00 |  0.000000E+00 |  0.0723368913 |         ideal
ACK FOUND > 1; len(fronts)=1
   181 |    32399 |     38 |  0.000000E+00 |  0.000000E+00 |  0.0779775444 |         ideal
ACK FOUND > 1; len(fronts)=1
   182 |    32578 |     39 |  0.000000E+00 |  0.000000E+00 |  0.0723368913 |         ideal
ACK FOUND > 1; len(fronts)=1
   183 |    32757 |     41 |  0.000000E+00 |  0.000000E+00 |  0.6595302965 |         nadir
ACK FOUND > 1; len(fronts)=1
   184 |    32936 |     38 |  0.000000E+00 |  0.000000E+00 |  0.1037476815 |         ideal
ACK FOUND > 1; len(fronts)=1
   185 |    33115 |     43 |  0.000000E+00 |  0.000000E+00 |  0.0082628239 |         ideal
ACK FOUND > 1; len(fronts)=1
   186 |    33294 |     40 |  0.000000E+00 |  0.000000E+00 |  0.0779775444 |         ideal
ACK FOUND > 1; len(fronts)=1
   187 |    33473 |     46 |  0.000000E+00 |  0.000000E+00 |  0.0722496233 |         ideal
ACK FOUND > 1; len(fronts)=1
   188 |    33652 |     47 |  0.000000E+00 |  0.000000E+00 |  0.0493948947 |         ideal
ACK FOUND > 1; len(fronts)=1
   189 |    33831 |     46 |  0.000000E+00 |  0.000000E+00 |  0.0548529252 |         ideal
ACK FOUND > 1; len(fronts)=1
   190 |    34010 |     47 |  0.000000E+00 |  0.000000E+00 |  0.0072606266 |         nadir
ACK FOUND > 1; len(fronts)=1
   191 |    34189 |     41 |  0.000000E+00 |  0.000000E+00 |  0.0768219762 |         ideal
ACK FOUND > 1; len(fronts)=1
   192 |    34368 |     38 |  0.000000E+00 |  0.000000E+00 |  0.0606220142 |         ideal
ACK FOUND > 1; len(fronts)=1
   193 |    34547 |     39 |  0.000000E+00 |  0.000000E+00 |  0.0571570393 |         ideal
ACK FOUND > 1; len(fronts)=1
   194 |    34726 |     41 |  0.000000E+00 |  0.000000E+00 |  0.0406150301 |         ideal
ACK FOUND > 1; len(fronts)=1
   195 |    34905 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0264242131 |         ideal
ACK FOUND > 1; len(fronts)=1
   196 |    35084 |     42 |  0.000000E+00 |  0.000000E+00 |  0.0143591454 |         ideal
ACK FOUND > 1; len(fronts)=1
   197 |    35263 |     41 |  0.000000E+00 |  0.000000E+00 |  0.0605287255 |         ideal
ACK FOUND > 1; len(fronts)=1
   198 |    35442 |     41 |  0.000000E+00 |  0.000000E+00 |  0.0598353396 |         ideal
ACK FOUND > 1; len(fronts)=1
   199 |    35621 |     47 |  0.000000E+00 |  0.000000E+00 |  0.0437710770 |         ideal
ACK FOUND > 1; len(fronts)=1
   200 |    35800 |     39 |  0.000000E+00 |  0.000000E+00 |  0.0457746843 |         ideal
Begin print with Final Cash: 12035273.7314055282623 => return: 0.2035273731406
Month 1:
  Buy: Stock ABT, Amount: 411
  Buy: Stock ACB, Amount: 399
  Buy: Stock ACL, Amount: 356
  Buy: Stock AGF, Amount: 212
  Buy: Stock ALT, Amount: 245
  Buy: Stock ANV, Amount: 77
  Buy: Stock ASP, Amount: 23
  Buy: Stock B82, Amount: 976
  Buy: Stock BBC, Amount: 69
  Buy: Stock BBS, Amount: 877
  Buy: Stock BCC, Amount: 70
  Buy: Stock BMI, Amount: 1
  Buy: Stock BST, Amount: 19
  Buy: Stock BTS, Amount: 1
  Buy: Stock CLC, Amount: 1
  Bank Deposit: 9947604.32
Month 2:
  Buy: Stock ACL, Amount: 1437
  Buy: Stock ALT, Amount: 243
  Buy: Stock B82, Amount: 1
  Buy: Stock BBC, Amount: 5
  Buy: Stock BCC, Amount: 15
  Buy: Stock BVS, Amount: 1
  Buy: Stock CAP, Amount: 127934
  Buy: Stock CDC, Amount: 2
  Buy: Stock DRC, Amount: 601
  Buy: Stock DST, Amount: 594
  Buy: Stock FMC, Amount: 352
  Buy: Stock HT1, Amount: 7
  Buy: Stock HTV, Amount: 106
  Buy: Stock KKC, Amount: 22
  Sell: Stock ABT, Amount: 375.0
  Sell: Stock ACL, Amount: 541.0
  Sell: Stock AGF, Amount: 212.0
  Sell: Stock ANV, Amount: 77.0
  Sell: Stock ASP, Amount: 23.0
  Sell: Stock B82, Amount: 66.0
  Sell: Stock BBS, Amount: 869.0
  Sell: Stock BMI, Amount: 1.0
  Sell: Stock BST, Amount: 19.0
  Sell: Stock BTS, Amount: 1.0
  Sell: Stock CAP, Amount: 726.0
  Dividends: 1.50
  Bank Deposit: 161511.29
Month 3:
  Buy: Stock ABT, Amount: 1066
  Buy: Stock ACB, Amount: 71
  Buy: Stock ACL, Amount: 262
  Buy: Stock AGF, Amount: 34
  Buy: Stock ALT, Amount: 372
  Buy: Stock ANV, Amount: 16
  Buy: Stock B82, Amount: 7
  Buy: Stock BMP, Amount: 663
  Buy: Stock BVS, Amount: 1053
  Buy: Stock CII, Amount: 3
  Buy: Stock DTT, Amount: 1
  Buy: Stock HBC, Amount: 20
  Buy: Stock IMP, Amount: 1
  Sell: Stock BBS, Amount: 8.0
  Sell: Stock BCC, Amount: 85.0
  Sell: Stock CAP, Amount: 112957.0
  Sell: Stock CDC, Amount: 2.0
  Sell: Stock CLC, Amount: 1.0
  Sell: Stock DRC, Amount: 601.0
  Sell: Stock DST, Amount: 594.0
  Sell: Stock FMC, Amount: 83.0
  Dividends: 948.40
  Bank Deposit: 140111.88
Month 4:
  Buy: Stock AGF, Amount: 282
  Buy: Stock ALT, Amount: 163
  Buy: Stock ASP, Amount: 141
  Buy: Stock B82, Amount: 75699
  Buy: Stock BMC, Amount: 9637
  Buy: Stock BMI, Amount: 46220
  Buy: Stock BMP, Amount: 10373
  Buy: Stock BPC, Amount: 13151
  Buy: Stock BTS, Amount: 170
  Buy: Stock BVS, Amount: 15
  Buy: Stock CAN, Amount: 11250
  Sell: Stock AGF, Amount: 19.0
  Sell: Stock ALT, Amount: 158.0
  Sell: Stock ASP, Amount: 71.0
  Sell: Stock B82, Amount: 57591.0
  Sell: Stock BMI, Amount: 39552.0
  Sell: Stock BPC, Amount: 490.0
  Sell: Stock CAN, Amount: 165.0
  Sell: Stock CAP, Amount: 3208.0
  Bank Deposit: 6930950.51
Month 5:
  Buy: Stock ABT, Amount: 544
  Buy: Stock ACB, Amount: 4897
  Buy: Stock ACL, Amount: 1264
  Buy: Stock AGF, Amount: 28192
  Buy: Stock ALT, Amount: 379
  Buy: Stock ANV, Amount: 22205
  Buy: Stock ASP, Amount: 1449
  Buy: Stock B82, Amount: 4310
  Buy: Stock BBC, Amount: 1689
  Sell: Stock ACB, Amount: 1668.0
  Sell: Stock ACL, Amount: 394.0
  Sell: Stock AGF, Amount: 479.0
  Sell: Stock ANV, Amount: 20733.0
  Sell: Stock ASP, Amount: 351.0
  Sell: Stock BBC, Amount: 1.0
  Bank Deposit: 7185987.18
Month 6:
  Buy: Stock ABT, Amount: 7856
  Buy: Stock ACB, Amount: 11615
  Buy: Stock ACL, Amount: 8366
  Buy: Stock AGF, Amount: 29321
  Buy: Stock ALT, Amount: 19
  Buy: Stock ANV, Amount: 612
  Buy: Stock ASP, Amount: 205
  Buy: Stock B82, Amount: 3
  Buy: Stock BBC, Amount: 1
  Sell: Stock ABT, Amount: 74.0
  Sell: Stock AGF, Amount: 57331.0
  Sell: Stock ALT, Amount: 706.0
  Sell: Stock ASP, Amount: 59.0
  Sell: Stock B82, Amount: 2101.0
  Sell: Stock BBC, Amount: 37.0
  Dividends: 3699.00
  Bank Deposit: 7227566.85
Month 7:
  Buy: Stock ABT, Amount: 386
  Buy: Stock ACB, Amount: 9267
  Buy: Stock ACL, Amount: 1
  Buy: Stock DC4, Amount: 127
  Sell: Stock ACB, Amount: 6958.0
  Sell: Stock ALT, Amount: 15.0
  Sell: Stock ANV, Amount: 2100.0
  Sell: Stock ASP, Amount: 1314.0
  Sell: Stock BBC, Amount: 1726.0
  Sell: Stock BMI, Amount: 6668.0
  Sell: Stock BMP, Amount: 11036.0
  Sell: Stock BPC, Amount: 6336.0
  Sell: Stock CAN, Amount: 12.0
  Sell: Stock CAP, Amount: 10135.0
  Dividends: 9428.00
  Bank Deposit: 7213912.91
Month 8:
  Buy: Stock ABT, Amount: 13429
  Buy: Stock ACB, Amount: 29222
  Buy: Stock ACL, Amount: 1326
  Buy: Stock AGF, Amount: 17780
  Buy: Stock ALT, Amount: 806
  Buy: Stock ANV, Amount: 13810
  Buy: Stock ASP, Amount: 1049
  Buy: Stock B82, Amount: 566
  Buy: Stock BBC, Amount: 846
  Buy: Stock BBS, Amount: 229
  Sell: Stock ABT, Amount: 23243.0
  Sell: Stock AGF, Amount: 14153.0
  Sell: Stock ALT, Amount: 781.0
  Sell: Stock ANV, Amount: 7294.0
  Sell: Stock CAN, Amount: 2919.0
  Bank Deposit: 7898880.41
Month 9:
  Buy: Stock ABT, Amount: 35114
  Buy: Stock ACB, Amount: 259413
  Buy: Stock ACL, Amount: 1143
  Buy: Stock AGF, Amount: 1498
  Buy: Stock B82, Amount: 46
  Sell: Stock ABT, Amount: 6239.0
  Sell: Stock ACB, Amount: 138679.0
  Sell: Stock AGF, Amount: 3013.0
  Sell: Stock B82, Amount: 4.0
  Sell: Stock BMC, Amount: 2.0
  Sell: Stock CAN, Amount: 25.57666818664478
  Dividends: 567.00
  Bank Deposit: 1939129.47
Month 10:
  Buy: Stock ABT, Amount: 7200
  Buy: Stock ACB, Amount: 4497
  Buy: Stock ACL, Amount: 20
  Buy: Stock B82, Amount: 400
  Buy: Stock BBS, Amount: 1593
  Buy: Stock BMC, Amount: 2
  Sell: Stock ALT, Amount: 567.0
  Sell: Stock ASP, Amount: 342.0
  Sell: Stock B82, Amount: 2760.0
  Sell: Stock BBC, Amount: 279.0
  Dividends: 6516.00
  Bank Deposit: 4973796.21
Month 11:
  Buy: Stock ABT, Amount: 998
  Buy: Stock ACB, Amount: 21990
  Buy: Stock ACL, Amount: 76918
  Buy: Stock AGF, Amount: 491
  Buy: Stock ALT, Amount: 690
  Buy: Stock ANV, Amount: 3125
  Buy: Stock ASP, Amount: 1109
  Buy: Stock B82, Amount: 86
  Buy: Stock BBC, Amount: 4
  Buy: Stock BBS, Amount: 5
  Sell: Stock ABT, Amount: 41.0
  Sell: Stock ACB, Amount: 66640.0
  Sell: Stock ACL, Amount: 38837.0
  Sell: Stock B82, Amount: 5515.0
  Sell: Stock BBC, Amount: 206.0
  Sell: Stock BBS, Amount: 23.0
  Bank Deposit: 3379799.32
Month 12:
  Sell: Stock ABT, Amount: 37032.0
  Sell: Stock ACB, Amount: 3126.0
  Sell: Stock AGF, Amount: 2603.0
  Sell: Stock BBS, Amount: 1804.0
  Sell: Stock BMC, Amount: 7561.0
  Sell: Stock BPC, Amount: 6325.0
  Sell: Stock BVS, Amount: 1069.0
  Sell: Stock CAN, Amount: 8128.0
  Sell: Stock CAP, Amount: 908.0
  Sell: Stock CII, Amount: 3.0
  Sell: Stock DC4, Amount: 127.0
  Sell: Stock DTT, Amount: 1.0
  Sell: Stock FMC, Amount: 269.0
  Sell: Stock HBC, Amount: 20.0
  Sell: Stock HT1, Amount: 7.0
  Sell: Stock HTV, Amount: 106.0
  Sell: Stock IMP, Amount: 1.0
  Sell: Stock KKC, Amount: 22.0
  Sell: Stock ACB, Amount: 124300.0
  Sell: Stock ACL, Amount: 51321.0
  Sell: Stock ALT, Amount: 690.0
  Sell: Stock ANV, Amount: 9641.0
  Sell: Stock ASP, Amount: 1816.0
  Sell: Stock B82, Amount: 14057.0
  Sell: Stock BBC, Amount: 365.0
  Sell: Stock BMC, Amount: 2076.0
  Sell: Stock BTS, Amount: 170.0
  Bank Deposit: 5458108.67


Final Cash: 12035273.7314055282623 => return: 0.2035273731406

"""

# Extract arrays
ack_array, n_nds_array, eps_array, indicator_array = extract_arrays(text_data)

print("front_num_Array =", ack_array)
print("n_nds_Array =", n_nds_array)
print("eps_Array =", eps_array)
print("indicator_Array =", indicator_array)
