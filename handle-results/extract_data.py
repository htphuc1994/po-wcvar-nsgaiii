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
Objectives = ['-0.2693077451180', '-0.1659529284200', '-0.1254670980393', '-0.1538921879517', '-0.1598979045081', '-0.2087403672313', '-0.2236038309798', '-0.2251050994162', '-0.2192899802956', '-0.2243583778912', '-0.2242203408825', '-0.1942640919064']
The time of execution of above program is : 707121.1400032043 ms
ACK FOUND > 1; len(fronts)=4
==========================================================================================
n_gen  |  n_eval  | n_nds  |     cv_min    |     cv_avg    |      eps      |   indicator  
==========================================================================================
     1 |      179 |      5 |  0.000000E+00 |  0.000000E+00 |             - |             -
ACK FOUND > 1; len(fronts)=3
     2 |      358 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0263224292 |         ideal
ACK FOUND > 1; len(fronts)=2
     3 |      537 |      7 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=2
     4 |      716 |      2 |  0.000000E+00 |  0.000000E+00 |  6.4714613636 |         ideal
ACK FOUND > 1; len(fronts)=2
     5 |      895 |      6 |  0.000000E+00 |  0.000000E+00 |  0.9201862775 |         ideal
ACK FOUND > 1; len(fronts)=2
     6 |     1074 |      7 |  0.000000E+00 |  0.000000E+00 |  0.4728547552 |         ideal
ACK FOUND > 1; len(fronts)=2
     7 |     1253 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0782786451 |         ideal
ACK FOUND > 1; len(fronts)=2
     8 |     1432 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0458252155 |         ideal
ACK FOUND > 1; len(fronts)=2
     9 |     1611 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0135105656 |         ideal
ACK FOUND > 1; len(fronts)=2
    10 |     1790 |      1 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
    11 |     1969 |      1 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
    12 |     2148 |      1 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
    13 |     2327 |      2 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
    14 |     2506 |      4 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
    15 |     2685 |      4 |  0.000000E+00 |  0.000000E+00 |  0.8588677043 |         ideal
ACK FOUND > 1; len(fronts)=1
    16 |     2864 |      8 |  0.000000E+00 |  0.000000E+00 |  0.5514058463 |         ideal
ACK FOUND > 1; len(fronts)=1
    17 |     3043 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0247752828 |         ideal
ACK FOUND > 1; len(fronts)=1
    18 |     3222 |      2 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
    19 |     3401 |      2 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
    20 |     3580 |      4 |  0.000000E+00 |  0.000000E+00 |  0.8998081875 |         ideal
ACK FOUND > 1; len(fronts)=1
    21 |     3759 |      5 |  0.000000E+00 |  0.000000E+00 |  0.5616643859 |         ideal
ACK FOUND > 1; len(fronts)=1
    22 |     3938 |      6 |  0.000000E+00 |  0.000000E+00 |  0.1192045348 |         ideal
ACK FOUND > 1; len(fronts)=1
    23 |     4117 |      6 |  0.000000E+00 |  0.000000E+00 |  0.3785977568 |         ideal
ACK FOUND > 1; len(fronts)=1
    24 |     4296 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2758520378 |         ideal
ACK FOUND > 1; len(fronts)=1
    25 |     4475 |      5 |  0.000000E+00 |  0.000000E+00 |  0.2605737177 |         ideal
ACK FOUND > 1; len(fronts)=1
    26 |     4654 |      6 |  0.000000E+00 |  0.000000E+00 |  0.1816222354 |         ideal
ACK FOUND > 1; len(fronts)=1
    27 |     4833 |      7 |  0.000000E+00 |  0.000000E+00 |  0.2838784128 |         ideal
ACK FOUND > 1; len(fronts)=1
    28 |     5012 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4357062949 |         ideal
ACK FOUND > 1; len(fronts)=1
    29 |     5191 |      7 |  0.000000E+00 |  0.000000E+00 |  0.4553078342 |         ideal
ACK FOUND > 1; len(fronts)=1
    30 |     5370 |      8 |  0.000000E+00 |  0.000000E+00 |  0.0759573895 |         ideal
ACK FOUND > 1; len(fronts)=1
    31 |     5549 |     10 |  0.000000E+00 |  0.000000E+00 |  0.5866771653 |         ideal
ACK FOUND > 1; len(fronts)=1
    32 |     5728 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3391413967 |         ideal
ACK FOUND > 1; len(fronts)=1
    33 |     5907 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2717531990 |         ideal
ACK FOUND > 1; len(fronts)=1
    34 |     6086 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1451453902 |         ideal
ACK FOUND > 1; len(fronts)=1
    35 |     6265 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1424068388 |         ideal
ACK FOUND > 1; len(fronts)=1
    36 |     6444 |     12 |  0.000000E+00 |  0.000000E+00 |  0.4629213007 |         ideal
ACK FOUND > 1; len(fronts)=1
    37 |     6623 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2985565253 |         ideal
ACK FOUND > 1; len(fronts)=1
    38 |     6802 |      3 |  0.000000E+00 |  0.000000E+00 |  2.6720252422 |         ideal
ACK FOUND > 1; len(fronts)=1
    39 |     6981 |      3 |  0.000000E+00 |  0.000000E+00 |  1.0484453461 |         ideal
ACK FOUND > 1; len(fronts)=1
    40 |     7160 |      3 |  0.000000E+00 |  0.000000E+00 |  0.3436217414 |         ideal
ACK FOUND > 1; len(fronts)=1
    41 |     7339 |      6 |  0.000000E+00 |  0.000000E+00 |  0.5665302285 |         ideal
ACK FOUND > 1; len(fronts)=1
    42 |     7518 |      5 |  0.000000E+00 |  0.000000E+00 |  0.7306383768 |         ideal
ACK FOUND > 1; len(fronts)=1
    43 |     7697 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3466660189 |         ideal
ACK FOUND > 1; len(fronts)=1
    44 |     7876 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3732003774 |         ideal
ACK FOUND > 1; len(fronts)=1
    45 |     8055 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3331292975 |         ideal
ACK FOUND > 1; len(fronts)=1
    46 |     8234 |     11 |  0.000000E+00 |  0.000000E+00 |  0.1650220258 |         ideal
ACK FOUND > 1; len(fronts)=1
    47 |     8413 |     12 |  0.000000E+00 |  0.000000E+00 |  0.4597193438 |         ideal
ACK FOUND > 1; len(fronts)=1
    48 |     8592 |     10 |  0.000000E+00 |  0.000000E+00 |  0.4797894212 |         ideal
ACK FOUND > 1; len(fronts)=1
    49 |     8771 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2325012117 |         ideal
ACK FOUND > 1; len(fronts)=1
    50 |     8950 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1611529991 |         ideal
ACK FOUND > 1; len(fronts)=1
    51 |     9129 |      5 |  0.000000E+00 |  0.000000E+00 |  0.2575627674 |         ideal
ACK FOUND > 1; len(fronts)=1
    52 |     9308 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3541380457 |         ideal
ACK FOUND > 1; len(fronts)=1
    53 |     9487 |     16 |  0.000000E+00 |  0.000000E+00 |  0.3553902949 |         ideal
ACK FOUND > 1; len(fronts)=1
    54 |     9666 |      9 |  0.000000E+00 |  0.000000E+00 |  0.4483277254 |         ideal
ACK FOUND > 1; len(fronts)=1
    55 |     9845 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1187540324 |         ideal
ACK FOUND > 1; len(fronts)=1
    56 |    10024 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3745284602 |         ideal
ACK FOUND > 1; len(fronts)=1
    57 |    10203 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0282134126 |         ideal
ACK FOUND > 1; len(fronts)=1
    58 |    10382 |      2 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
    59 |    10561 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0125791012 |         ideal
ACK FOUND > 1; len(fronts)=1
    60 |    10740 |      4 |  0.000000E+00 |  0.000000E+00 |  0.9614540436 |         ideal
ACK FOUND > 1; len(fronts)=1
    61 |    10919 |      2 |  0.000000E+00 |  0.000000E+00 |  3.6335690340 |         ideal
ACK FOUND > 1; len(fronts)=1
    62 |    11098 |      2 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
    63 |    11277 |      2 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
    64 |    11456 |      3 |  0.000000E+00 |  0.000000E+00 |  0.9669813214 |         ideal
ACK FOUND > 1; len(fronts)=1
    65 |    11635 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4161202730 |         ideal
ACK FOUND > 1; len(fronts)=1
    66 |    11814 |      3 |  0.000000E+00 |  0.000000E+00 |  1.4257651961 |         ideal
ACK FOUND > 1; len(fronts)=1
    67 |    11993 |      6 |  0.000000E+00 |  0.000000E+00 |  0.6646123593 |         ideal
ACK FOUND > 1; len(fronts)=1
    68 |    12172 |      5 |  0.000000E+00 |  0.000000E+00 |  1.3085888596 |         ideal
ACK FOUND > 1; len(fronts)=1
    69 |    12351 |     11 |  0.000000E+00 |  0.000000E+00 |  0.3997584226 |         ideal
ACK FOUND > 1; len(fronts)=1
    70 |    12530 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3245271052 |         ideal
ACK FOUND > 1; len(fronts)=1
    71 |    12709 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2039481321 |         ideal
ACK FOUND > 1; len(fronts)=1
    72 |    12888 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1015626814 |         ideal
ACK FOUND > 1; len(fronts)=1
    73 |    13067 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1189325732 |         ideal
ACK FOUND > 1; len(fronts)=1
    74 |    13246 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1077936371 |         ideal
ACK FOUND > 1; len(fronts)=1
    75 |    13425 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1104711319 |         ideal
ACK FOUND > 1; len(fronts)=1
    76 |    13604 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1027070720 |         ideal
ACK FOUND > 1; len(fronts)=1
    77 |    13783 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0810258458 |         ideal
ACK FOUND > 1; len(fronts)=1
    78 |    13962 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2547537798 |         ideal
ACK FOUND > 1; len(fronts)=1
    79 |    14141 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4340596831 |         ideal
ACK FOUND > 1; len(fronts)=1
    80 |    14320 |     13 |  0.000000E+00 |  0.000000E+00 |  0.9263278125 |         ideal
ACK FOUND > 1; len(fronts)=1
    81 |    14499 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2383056498 |         ideal
ACK FOUND > 1; len(fronts)=1
    82 |    14678 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1924449346 |         ideal
ACK FOUND > 1; len(fronts)=1
    83 |    14857 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0535472872 |         ideal
ACK FOUND > 1; len(fronts)=1
    84 |    15036 |     16 |  0.000000E+00 |  0.000000E+00 |  0.8071942968 |         ideal
ACK FOUND > 1; len(fronts)=1
    85 |    15215 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0173264893 |         ideal
ACK FOUND > 1; len(fronts)=1
    86 |    15394 |      6 |  0.000000E+00 |  0.000000E+00 |  0.5316309361 |         ideal
ACK FOUND > 1; len(fronts)=1
    87 |    15573 |      5 |  0.000000E+00 |  0.000000E+00 |  0.5367215315 |         ideal
ACK FOUND > 1; len(fronts)=1
    88 |    15752 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3456699943 |         ideal
ACK FOUND > 1; len(fronts)=1
    89 |    15931 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1294029339 |         ideal
ACK FOUND > 1; len(fronts)=1
    90 |    16110 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1471701210 |         ideal
ACK FOUND > 1; len(fronts)=1
    91 |    16289 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2726067855 |         ideal
ACK FOUND > 1; len(fronts)=1
    92 |    16468 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2756179058 |         ideal
ACK FOUND > 1; len(fronts)=1
    93 |    16647 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2305731345 |         ideal
ACK FOUND > 1; len(fronts)=1
    94 |    16826 |      7 |  0.000000E+00 |  0.000000E+00 |  0.4602132963 |         ideal
ACK FOUND > 1; len(fronts)=1
    95 |    17005 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3589861860 |         ideal
ACK FOUND > 1; len(fronts)=1
    96 |    17184 |     14 |  0.000000E+00 |  0.000000E+00 |  0.8518495470 |         ideal
ACK FOUND > 1; len(fronts)=1
    97 |    17363 |     10 |  0.000000E+00 |  0.000000E+00 |  1.6843674379 |         ideal
ACK FOUND > 1; len(fronts)=1
    98 |    17542 |     14 |  0.000000E+00 |  0.000000E+00 |  0.8377322237 |         ideal
ACK FOUND > 1; len(fronts)=1
    99 |    17721 |     11 |  0.000000E+00 |  0.000000E+00 |  0.1897231529 |         ideal
ACK FOUND > 1; len(fronts)=1
   100 |    17900 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2435762337 |         ideal
ACK FOUND > 1; len(fronts)=1
   101 |    18079 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2482083121 |         ideal
ACK FOUND > 1; len(fronts)=1
   102 |    18258 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1472769282 |         ideal
ACK FOUND > 1; len(fronts)=1
   103 |    18437 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1521108166 |         ideal
ACK FOUND > 1; len(fronts)=1
   104 |    18616 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1210488174 |         ideal
ACK FOUND > 1; len(fronts)=1
   105 |    18795 |     32 |  0.000000E+00 |  0.000000E+00 |  0.1529712097 |         ideal
ACK FOUND > 1; len(fronts)=1
   106 |    18974 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1345319862 |         ideal
ACK FOUND > 1; len(fronts)=1
   107 |    19153 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3906333852 |         ideal
ACK FOUND > 1; len(fronts)=1
   108 |    19332 |      7 |  0.000000E+00 |  0.000000E+00 |  0.1267653441 |         ideal
ACK FOUND > 1; len(fronts)=1
   109 |    19511 |      9 |  0.000000E+00 |  0.000000E+00 |  0.4183964983 |         ideal
ACK FOUND > 1; len(fronts)=1
   110 |    19690 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0780085717 |         ideal
ACK FOUND > 1; len(fronts)=1
   111 |    19869 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0147867978 |         ideal
ACK FOUND > 1; len(fronts)=1
   112 |    20048 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1486748306 |         ideal
ACK FOUND > 1; len(fronts)=1
   113 |    20227 |      9 |  0.000000E+00 |  0.000000E+00 |  0.0544518312 |         ideal
ACK FOUND > 1; len(fronts)=1
   114 |    20406 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1190577377 |         ideal
ACK FOUND > 1; len(fronts)=1
   115 |    20585 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0399686734 |         ideal
ACK FOUND > 1; len(fronts)=1
   116 |    20764 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2000249634 |         ideal
ACK FOUND > 1; len(fronts)=1
   117 |    20943 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0694043061 |         ideal
ACK FOUND > 1; len(fronts)=1
   118 |    21122 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1596346297 |         ideal
ACK FOUND > 1; len(fronts)=1
   119 |    21301 |     11 |  0.000000E+00 |  0.000000E+00 |  0.1616195734 |         ideal
ACK FOUND > 1; len(fronts)=1
   120 |    21480 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2711117853 |         ideal
ACK FOUND > 1; len(fronts)=1
   121 |    21659 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2363842976 |         ideal
ACK FOUND > 1; len(fronts)=1
   122 |    21838 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1536961339 |         ideal
ACK FOUND > 1; len(fronts)=1
   123 |    22017 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1886079705 |         ideal
ACK FOUND > 1; len(fronts)=1
   124 |    22196 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2749351839 |         ideal
ACK FOUND > 1; len(fronts)=1
   125 |    22375 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2089056385 |         ideal
ACK FOUND > 1; len(fronts)=1
   126 |    22554 |      9 |  0.000000E+00 |  0.000000E+00 |  0.0672727731 |         ideal
ACK FOUND > 1; len(fronts)=1
   127 |    22733 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1830666808 |         ideal
ACK FOUND > 1; len(fronts)=1
   128 |    22912 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1679653559 |         ideal
ACK FOUND > 1; len(fronts)=1
   129 |    23091 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4914667646 |         ideal
ACK FOUND > 1; len(fronts)=1
   130 |    23270 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3137212040 |         ideal
ACK FOUND > 1; len(fronts)=1
   131 |    23449 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0187651785 |         ideal
ACK FOUND > 1; len(fronts)=1
   132 |    23628 |      2 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
   133 |    23807 |      2 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
   134 |    23986 |      2 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
   135 |    24165 |      3 |  0.000000E+00 |  0.000000E+00 |  0.9981408917 |         ideal
ACK FOUND > 1; len(fronts)=1
   136 |    24344 |      2 |  0.000000E+00 |  0.000000E+00 |  5.368923E+02 |         ideal
ACK FOUND > 1; len(fronts)=1
   137 |    24523 |      4 |  0.000000E+00 |  0.000000E+00 |  0.9981408917 |         ideal
ACK FOUND > 1; len(fronts)=1
   138 |    24702 |      3 |  0.000000E+00 |  0.000000E+00 |  0.8716510268 |         ideal
ACK FOUND > 1; len(fronts)=1
   139 |    24881 |      2 |  0.000000E+00 |  0.000000E+00 |  5.368923E+02 |         ideal
ACK FOUND > 1; len(fronts)=1
   140 |    25060 |      6 |  0.000000E+00 |  0.000000E+00 |  0.9997409928 |         ideal
ACK FOUND > 1; len(fronts)=1
   141 |    25239 |      6 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
   142 |    25418 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3003335888 |         ideal
ACK FOUND > 1; len(fronts)=2
   143 |    25597 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0176257182 |         ideal
ACK FOUND > 1; len(fronts)=1
   144 |    25776 |      2 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
   145 |    25955 |      3 |  0.000000E+00 |  0.000000E+00 |  1.0000000000 |         ideal
ACK FOUND > 1; len(fronts)=1
   146 |    26134 |      5 |  0.000000E+00 |  0.000000E+00 |  0.7373221775 |         ideal
ACK FOUND > 1; len(fronts)=1
   147 |    26313 |      3 |  0.000000E+00 |  0.000000E+00 |  3.7426700158 |         ideal
ACK FOUND > 1; len(fronts)=1
   148 |    26492 |      4 |  0.000000E+00 |  0.000000E+00 |  0.8021134185 |         ideal
ACK FOUND > 1; len(fronts)=1
   149 |    26671 |      6 |  0.000000E+00 |  0.000000E+00 |  0.2564408130 |         ideal
ACK FOUND > 1; len(fronts)=1
   150 |    26850 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1660067968 |         ideal
ACK FOUND > 1; len(fronts)=1
   151 |    27029 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1549794743 |         ideal
ACK FOUND > 1; len(fronts)=1
   152 |    27208 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0739958630 |         ideal
ACK FOUND > 1; len(fronts)=1
   153 |    27387 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1462798865 |         ideal
ACK FOUND > 1; len(fronts)=1
   154 |    27566 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1801431955 |         ideal
ACK FOUND > 1; len(fronts)=1
   155 |    27745 |      4 |  0.000000E+00 |  0.000000E+00 |  0.6899194032 |         ideal
ACK FOUND > 1; len(fronts)=1
   156 |    27924 |      6 |  0.000000E+00 |  0.000000E+00 |  0.6675460660 |         ideal
ACK FOUND > 1; len(fronts)=1
   157 |    28103 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2949845527 |         ideal
ACK FOUND > 1; len(fronts)=1
   158 |    28282 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3297576385 |         ideal
ACK FOUND > 1; len(fronts)=1
   159 |    28461 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4523254512 |         ideal
ACK FOUND > 1; len(fronts)=1
   160 |    28640 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3677041178 |         ideal
ACK FOUND > 1; len(fronts)=1
   161 |    28819 |      7 |  0.000000E+00 |  0.000000E+00 |  0.5145324074 |         ideal
ACK FOUND > 1; len(fronts)=1
   162 |    28998 |      7 |  0.000000E+00 |  0.000000E+00 |  0.6217483783 |         ideal
ACK FOUND > 1; len(fronts)=1
   163 |    29177 |     10 |  0.000000E+00 |  0.000000E+00 |  0.4141322231 |         ideal
ACK FOUND > 1; len(fronts)=1
   164 |    29356 |      8 |  0.000000E+00 |  0.000000E+00 |  0.7068697742 |         ideal
ACK FOUND > 1; len(fronts)=1
   165 |    29535 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0841785480 |         ideal
ACK FOUND > 1; len(fronts)=1
   166 |    29714 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1868765960 |         ideal
ACK FOUND > 1; len(fronts)=1
   167 |    29893 |      9 |  0.000000E+00 |  0.000000E+00 |  0.0770277355 |         ideal
ACK FOUND > 1; len(fronts)=1
   168 |    30072 |      9 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
   169 |    30251 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3685527328 |         ideal
ACK FOUND > 1; len(fronts)=1
   170 |    30430 |      8 |  0.000000E+00 |  0.000000E+00 |  0.0190787583 |         ideal
ACK FOUND > 1; len(fronts)=1
   171 |    30609 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2834727833 |         ideal
ACK FOUND > 1; len(fronts)=1
   172 |    30788 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3127727523 |         ideal
ACK FOUND > 1; len(fronts)=1
   173 |    30967 |      9 |  0.000000E+00 |  0.000000E+00 |  0.0168164234 |         ideal
ACK FOUND > 1; len(fronts)=1
   174 |    31146 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1620134976 |         ideal
ACK FOUND > 1; len(fronts)=1
   175 |    31325 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1560232950 |         nadir
ACK FOUND > 1; len(fronts)=1
   176 |    31504 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0997082833 |         ideal
ACK FOUND > 1; len(fronts)=1
   177 |    31683 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2673824651 |         ideal
ACK FOUND > 1; len(fronts)=1
   178 |    31862 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2824547378 |         ideal
ACK FOUND > 1; len(fronts)=1
   179 |    32041 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0107530116 |         ideal
ACK FOUND > 1; len(fronts)=1
   180 |    32220 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0273808301 |         ideal
ACK FOUND > 1; len(fronts)=1
   181 |    32399 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1125237649 |         ideal
ACK FOUND > 1; len(fronts)=1
   182 |    32578 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1527101554 |         ideal
ACK FOUND > 1; len(fronts)=1
   183 |    32757 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0363411041 |         ideal
ACK FOUND > 1; len(fronts)=1
   184 |    32936 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1125237649 |         ideal
ACK FOUND > 1; len(fronts)=1
   185 |    33115 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1076001907 |         ideal
ACK FOUND > 1; len(fronts)=1
   186 |    33294 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1427533876 |         ideal
ACK FOUND > 1; len(fronts)=1
   187 |    33473 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1665254613 |         ideal
ACK FOUND > 1; len(fronts)=1
   188 |    33652 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1907230907 |         ideal
ACK FOUND > 1; len(fronts)=1
   189 |    33831 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0784649408 |         ideal
ACK FOUND > 1; len(fronts)=1
   190 |    34010 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0711187645 |         ideal
ACK FOUND > 1; len(fronts)=1
   191 |    34189 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0876454843 |         ideal
ACK FOUND > 1; len(fronts)=1
   192 |    34368 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1491966144 |         ideal
ACK FOUND > 1; len(fronts)=1
   193 |    34547 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0429500832 |         ideal
ACK FOUND > 1; len(fronts)=1
   194 |    34726 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2619100114 |         ideal
ACK FOUND > 1; len(fronts)=1
   195 |    34905 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2697957703 |         ideal
ACK FOUND > 1; len(fronts)=1
   196 |    35084 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0904138377 |         ideal
ACK FOUND > 1; len(fronts)=1
   197 |    35263 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2537116354 |         ideal
ACK FOUND > 1; len(fronts)=1
   198 |    35442 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3456365759 |         ideal
ACK FOUND > 1; len(fronts)=1
   199 |    35621 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2133658885 |         ideal
ACK FOUND > 1; len(fronts)=1
   200 |    35800 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1831706669 |         ideal
Begin print with Final Cash: 126930.7745117953891 => return: 0.2693077451180
Month 1:
"""

# Extract arrays
ack_array, n_nds_array, eps_array, indicator_array = extract_arrays(text_data)

print("front_num_Array =", ack_array)
print("n_nds_Array =", n_nds_array)
print("eps_Array =", eps_array)
print("indicator_Array =", indicator_array)
