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
Objectives = ['-0.2830699771319', '-0.0392952536645', '-0.0477328360760', '-0.0679428249811', '-0.0975882101541', '-0.1819986216728', '-0.1476092764563', '-0.1517261929893', '-0.1686496086624', '-0.1638813714003', '-0.1615015131155', '-0.1686739381549']
The time of execution of above program is : 357978.46698760986 ms
ACK FOUND > 1; len(fronts)=3
==========================================================================================
n_gen  |  n_eval  | n_nds  |     cv_min    |     cv_avg    |      eps      |   indicator  
==========================================================================================
     1 |      179 |      8 |  0.000000E+00 |  2.904208E+02 |             - |             -
ACK FOUND > 1; len(fronts)=2
     2 |      358 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2539840731 |         ideal
ACK FOUND > 1; len(fronts)=1
     3 |      537 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3269032416 |         ideal
ACK FOUND > 1; len(fronts)=1
     4 |      716 |     11 |  0.000000E+00 |  0.000000E+00 |  0.4274635239 |         ideal
ACK FOUND > 1; len(fronts)=2
     5 |      895 |      8 |  0.000000E+00 |  0.000000E+00 |  0.4813854106 |         ideal
ACK FOUND > 1; len(fronts)=1
     6 |     1074 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2273700284 |         ideal
ACK FOUND > 1; len(fronts)=1
     7 |     1253 |     17 |  0.000000E+00 |  0.000000E+00 |  0.3269396138 |         ideal
ACK FOUND > 1; len(fronts)=1
     8 |     1432 |      6 |  0.000000E+00 |  0.000000E+00 |  1.0143770166 |         ideal
ACK FOUND > 1; len(fronts)=1
     9 |     1611 |      8 |  0.000000E+00 |  0.000000E+00 |  0.4608364008 |         ideal
ACK FOUND > 1; len(fronts)=1
    10 |     1790 |      7 |  0.000000E+00 |  0.000000E+00 |  0.5034736331 |         ideal
ACK FOUND > 1; len(fronts)=1
    11 |     1969 |      5 |  0.000000E+00 |  0.000000E+00 |  0.7711414875 |         ideal
ACK FOUND > 1; len(fronts)=1
    12 |     2148 |      4 |  0.000000E+00 |  0.000000E+00 |  4.5419966134 |         ideal
ACK FOUND > 1; len(fronts)=1
    13 |     2327 |      7 |  0.000000E+00 |  0.000000E+00 |  0.7348360725 |         ideal
ACK FOUND > 1; len(fronts)=1
    14 |     2506 |      1 |  0.000000E+00 |  0.000000E+00 |  0.0177615996 |         ideal
ACK FOUND > 1; len(fronts)=1
    15 |     2685 |      4 |  0.000000E+00 |  0.000000E+00 |  1.5485531196 |         ideal
ACK FOUND > 1; len(fronts)=1
    16 |     2864 |      3 |  0.000000E+00 |  0.000000E+00 |  0.6846773419 |         ideal
ACK FOUND > 1; len(fronts)=1
    17 |     3043 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4064145251 |         ideal
ACK FOUND > 1; len(fronts)=1
    18 |     3222 |      3 |  0.000000E+00 |  0.000000E+00 |  0.9082227222 |         ideal
ACK FOUND > 1; len(fronts)=1
    19 |     3401 |      8 |  0.000000E+00 |  0.000000E+00 |  0.3990391313 |         ideal
ACK FOUND > 1; len(fronts)=1
    20 |     3580 |      9 |  0.000000E+00 |  0.000000E+00 |  0.2022960714 |         ideal
ACK FOUND > 1; len(fronts)=1
    21 |     3759 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3346244694 |         ideal
ACK FOUND > 1; len(fronts)=1
    22 |     3938 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2529499264 |         ideal
ACK FOUND > 1; len(fronts)=1
    23 |     4117 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2318185999 |         ideal
ACK FOUND > 1; len(fronts)=1
    24 |     4296 |      4 |  0.000000E+00 |  0.000000E+00 |  0.4869607961 |         ideal
ACK FOUND > 1; len(fronts)=1
    25 |     4475 |      3 |  0.000000E+00 |  0.000000E+00 |  1.1380078076 |         ideal
ACK FOUND > 1; len(fronts)=1
    26 |     4654 |     11 |  0.000000E+00 |  0.000000E+00 |  0.4141577024 |         ideal
ACK FOUND > 1; len(fronts)=1
    27 |     4833 |     19 |  0.000000E+00 |  0.000000E+00 |  0.3503188317 |         ideal
ACK FOUND > 1; len(fronts)=1
    28 |     5012 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1079880400 |         ideal
ACK FOUND > 1; len(fronts)=1
    29 |     5191 |      6 |  0.000000E+00 |  0.000000E+00 |  0.8993597434 |         ideal
ACK FOUND > 1; len(fronts)=1
    30 |     5370 |      9 |  0.000000E+00 |  0.000000E+00 |  0.4735067943 |         ideal
ACK FOUND > 1; len(fronts)=1
    31 |     5549 |     15 |  0.000000E+00 |  0.000000E+00 |  0.4859217992 |         ideal
ACK FOUND > 1; len(fronts)=1
    32 |     5728 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3759221997 |         ideal
ACK FOUND > 1; len(fronts)=1
    33 |     5907 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0930761880 |         ideal
ACK FOUND > 1; len(fronts)=1
    34 |     6086 |     13 |  0.000000E+00 |  0.000000E+00 |  0.4000201689 |         ideal
ACK FOUND > 1; len(fronts)=1
    35 |     6265 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2490167688 |         ideal
ACK FOUND > 1; len(fronts)=1
    36 |     6444 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2026868574 |         ideal
ACK FOUND > 1; len(fronts)=1
    37 |     6623 |     10 |  0.000000E+00 |  0.000000E+00 |  0.5021850885 |         ideal
ACK FOUND > 1; len(fronts)=1
    38 |     6802 |     16 |  0.000000E+00 |  0.000000E+00 |  0.4175790030 |         ideal
ACK FOUND > 1; len(fronts)=1
    39 |     6981 |     10 |  0.000000E+00 |  0.000000E+00 |  0.5301777993 |         ideal
ACK FOUND > 1; len(fronts)=1
    40 |     7160 |      7 |  0.000000E+00 |  0.000000E+00 |  0.4634492234 |         ideal
ACK FOUND > 1; len(fronts)=1
    41 |     7339 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2961502538 |         ideal
ACK FOUND > 1; len(fronts)=1
    42 |     7518 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3196954029 |         ideal
ACK FOUND > 1; len(fronts)=1
    43 |     7697 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2422493874 |         ideal
ACK FOUND > 1; len(fronts)=1
    44 |     7876 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1158536498 |         ideal
ACK FOUND > 1; len(fronts)=1
    45 |     8055 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0846017179 |         ideal
ACK FOUND > 1; len(fronts)=1
    46 |     8234 |     13 |  0.000000E+00 |  0.000000E+00 |  0.6237706968 |         nadir
ACK FOUND > 1; len(fronts)=1
    47 |     8413 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0641734998 |         ideal
ACK FOUND > 1; len(fronts)=1
    48 |     8592 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1035966635 |         ideal
ACK FOUND > 1; len(fronts)=1
    49 |     8771 |     13 |  0.000000E+00 |  0.000000E+00 |  0.4579559838 |         ideal
ACK FOUND > 1; len(fronts)=1
    50 |     8950 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3143363560 |         ideal
ACK FOUND > 1; len(fronts)=1
    51 |     9129 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3915409147 |         ideal
ACK FOUND > 1; len(fronts)=1
    52 |     9308 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1300739913 |         ideal
ACK FOUND > 1; len(fronts)=1
    53 |     9487 |     11 |  0.000000E+00 |  0.000000E+00 |  0.4579857118 |         ideal
ACK FOUND > 1; len(fronts)=1
    54 |     9666 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3301106005 |         ideal
ACK FOUND > 1; len(fronts)=1
    55 |     9845 |     13 |  0.000000E+00 |  0.000000E+00 |  0.5869219337 |         ideal
ACK FOUND > 1; len(fronts)=1
    56 |    10024 |     23 |  0.000000E+00 |  0.000000E+00 |  0.2361098426 |         ideal
ACK FOUND > 1; len(fronts)=1
    57 |    10203 |     23 |  0.000000E+00 |  0.000000E+00 |  0.2387409603 |         ideal
ACK FOUND > 1; len(fronts)=1
    58 |    10382 |     18 |  0.000000E+00 |  0.000000E+00 |  0.4096527065 |         ideal
ACK FOUND > 1; len(fronts)=1
    59 |    10561 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0568122562 |         ideal
ACK FOUND > 1; len(fronts)=1
    60 |    10740 |     21 |  0.000000E+00 |  0.000000E+00 |  0.3701161399 |         ideal
ACK FOUND > 1; len(fronts)=1
    61 |    10919 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2310384670 |         ideal
ACK FOUND > 1; len(fronts)=1
    62 |    11098 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2423366610 |         ideal
ACK FOUND > 1; len(fronts)=1
    63 |    11277 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2135181842 |         ideal
ACK FOUND > 1; len(fronts)=1
    64 |    11456 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0753864834 |         ideal
ACK FOUND > 1; len(fronts)=1
    65 |    11635 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1103730785 |         ideal
ACK FOUND > 1; len(fronts)=1
    66 |    11814 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2961284575 |         ideal
ACK FOUND > 1; len(fronts)=1
    67 |    11993 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2467378529 |         ideal
ACK FOUND > 1; len(fronts)=1
    68 |    12172 |     13 |  0.000000E+00 |  0.000000E+00 |  0.5094731435 |         ideal
ACK FOUND > 1; len(fronts)=1
    69 |    12351 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0299185601 |         ideal
ACK FOUND > 1; len(fronts)=1
    70 |    12530 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0597574826 |         ideal
ACK FOUND > 1; len(fronts)=1
    71 |    12709 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2485594436 |         ideal
ACK FOUND > 1; len(fronts)=1
    72 |    12888 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0551281075 |         ideal
ACK FOUND > 1; len(fronts)=1
    73 |    13067 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2136717341 |         ideal
ACK FOUND > 1; len(fronts)=1
    74 |    13246 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3022272964 |         ideal
ACK FOUND > 1; len(fronts)=1
    75 |    13425 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1096639370 |         nadir
ACK FOUND > 1; len(fronts)=1
    76 |    13604 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2126564690 |         nadir
ACK FOUND > 1; len(fronts)=1
    77 |    13783 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0574944149 |         ideal
ACK FOUND > 1; len(fronts)=1
    78 |    13962 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0610016703 |         ideal
ACK FOUND > 1; len(fronts)=1
    79 |    14141 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1049715913 |         ideal
ACK FOUND > 1; len(fronts)=1
    80 |    14320 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2008500205 |         ideal
ACK FOUND > 1; len(fronts)=1
    81 |    14499 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0171084715 |         ideal
ACK FOUND > 1; len(fronts)=1
    82 |    14678 |     13 |  0.000000E+00 |  0.000000E+00 |  0.4051326252 |         ideal
ACK FOUND > 1; len(fronts)=1
    83 |    14857 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0898652221 |         ideal
ACK FOUND > 1; len(fronts)=1
    84 |    15036 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0845056291 |         ideal
ACK FOUND > 1; len(fronts)=1
    85 |    15215 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0948850659 |         ideal
ACK FOUND > 1; len(fronts)=1
    86 |    15394 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1392764588 |         ideal
ACK FOUND > 1; len(fronts)=1
    87 |    15573 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1154582449 |         ideal
ACK FOUND > 1; len(fronts)=1
    88 |    15752 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0081384428 |         ideal
ACK FOUND > 1; len(fronts)=1
    89 |    15931 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1459163858 |         ideal
ACK FOUND > 1; len(fronts)=1
    90 |    16110 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0991572763 |         ideal
ACK FOUND > 1; len(fronts)=1
    91 |    16289 |     17 |  0.000000E+00 |  0.000000E+00 |  0.3605411262 |         ideal
ACK FOUND > 1; len(fronts)=1
    92 |    16468 |     14 |  0.000000E+00 |  0.000000E+00 |  0.3662204236 |         ideal
ACK FOUND > 1; len(fronts)=1
    93 |    16647 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1260287639 |         ideal
ACK FOUND > 1; len(fronts)=1
    94 |    16826 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1312926277 |         ideal
ACK FOUND > 1; len(fronts)=1
    95 |    17005 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0936381720 |         ideal
ACK FOUND > 1; len(fronts)=1
    96 |    17184 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1028757813 |         ideal
ACK FOUND > 1; len(fronts)=1
    97 |    17363 |     23 |  0.000000E+00 |  0.000000E+00 |  0.4744842040 |         ideal
ACK FOUND > 1; len(fronts)=1
    98 |    17542 |     27 |  0.000000E+00 |  0.000000E+00 |  0.3415460839 |         ideal
ACK FOUND > 1; len(fronts)=1
    99 |    17721 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0803520119 |         ideal
ACK FOUND > 1; len(fronts)=1
   100 |    17900 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1331433377 |         ideal
ACK FOUND > 1; len(fronts)=1
   101 |    18079 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1153262756 |         ideal
ACK FOUND > 1; len(fronts)=1
   102 |    18258 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0626615051 |         ideal
ACK FOUND > 1; len(fronts)=1
   103 |    18437 |     27 |  0.000000E+00 |  0.000000E+00 |  0.2674224177 |         ideal
ACK FOUND > 1; len(fronts)=1
   104 |    18616 |     17 |  0.000000E+00 |  0.000000E+00 |  0.5862222076 |         ideal
ACK FOUND > 1; len(fronts)=1
   105 |    18795 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2024276162 |         ideal
ACK FOUND > 1; len(fronts)=1
   106 |    18974 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1423692829 |         ideal
ACK FOUND > 1; len(fronts)=1
   107 |    19153 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1403271863 |         ideal
ACK FOUND > 1; len(fronts)=1
   108 |    19332 |     15 |  0.000000E+00 |  0.000000E+00 |  0.4189279996 |         ideal
ACK FOUND > 1; len(fronts)=1
   109 |    19511 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1686945192 |         ideal
ACK FOUND > 1; len(fronts)=1
   110 |    19690 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0974649859 |         ideal
ACK FOUND > 1; len(fronts)=1
   111 |    19869 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1867637317 |         ideal
ACK FOUND > 1; len(fronts)=1
   112 |    20048 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1082450521 |         ideal
ACK FOUND > 1; len(fronts)=1
   113 |    20227 |     22 |  0.000000E+00 |  0.000000E+00 |  0.3615982116 |         ideal
ACK FOUND > 1; len(fronts)=1
   114 |    20406 |     25 |  0.000000E+00 |  0.000000E+00 |  0.3029704728 |         ideal
ACK FOUND > 1; len(fronts)=1
   115 |    20585 |     24 |  0.000000E+00 |  0.000000E+00 |  0.2475753310 |         ideal
ACK FOUND > 1; len(fronts)=1
   116 |    20764 |     17 |  0.000000E+00 |  0.000000E+00 |  0.3125293221 |         ideal
ACK FOUND > 1; len(fronts)=1
   117 |    20943 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1488369524 |         ideal
ACK FOUND > 1; len(fronts)=1
   118 |    21122 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1958053130 |         ideal
ACK FOUND > 1; len(fronts)=1
   119 |    21301 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0702979215 |         ideal
ACK FOUND > 1; len(fronts)=1
   120 |    21480 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1934124038 |         ideal
ACK FOUND > 1; len(fronts)=1
   121 |    21659 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2397909473 |         ideal
ACK FOUND > 1; len(fronts)=1
   122 |    21838 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0722176741 |         ideal
ACK FOUND > 1; len(fronts)=1
   123 |    22017 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0070928775 |         ideal
ACK FOUND > 1; len(fronts)=1
   124 |    22196 |      8 |  0.000000E+00 |  0.000000E+00 |  0.1953648645 |         ideal
ACK FOUND > 1; len(fronts)=1
   125 |    22375 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2677802628 |         ideal
ACK FOUND > 1; len(fronts)=1
   126 |    22554 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1639402687 |         ideal
ACK FOUND > 1; len(fronts)=1
   127 |    22733 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0601263784 |         ideal
ACK FOUND > 1; len(fronts)=1
   128 |    22912 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1324545629 |         ideal
ACK FOUND > 1; len(fronts)=1
   129 |    23091 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1169623641 |         ideal
ACK FOUND > 1; len(fronts)=1
   130 |    23270 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1909889134 |         ideal
ACK FOUND > 1; len(fronts)=1
   131 |    23449 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1860684413 |         ideal
ACK FOUND > 1; len(fronts)=1
   132 |    23628 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0514119769 |             f
ACK FOUND > 1; len(fronts)=1
   133 |    23807 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0345380664 |         ideal
ACK FOUND > 1; len(fronts)=1
   134 |    23986 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0327620496 |         ideal
ACK FOUND > 1; len(fronts)=1
   135 |    24165 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2674053364 |         ideal
ACK FOUND > 1; len(fronts)=1
   136 |    24344 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0528841094 |         ideal
ACK FOUND > 1; len(fronts)=1
   137 |    24523 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2434317472 |         ideal
ACK FOUND > 1; len(fronts)=1
   138 |    24702 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2067574860 |         ideal
ACK FOUND > 1; len(fronts)=1
   139 |    24881 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0505199419 |         ideal
ACK FOUND > 1; len(fronts)=1
   140 |    25060 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1211206841 |         ideal
ACK FOUND > 1; len(fronts)=1
   141 |    25239 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0702652499 |         ideal
ACK FOUND > 1; len(fronts)=1
   142 |    25418 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0222542456 |         ideal
ACK FOUND > 1; len(fronts)=1
   143 |    25597 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0618426378 |         ideal
ACK FOUND > 1; len(fronts)=1
   144 |    25776 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1397129199 |         nadir
ACK FOUND > 1; len(fronts)=1
   145 |    25955 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1681024790 |         ideal
ACK FOUND > 1; len(fronts)=1
   146 |    26134 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0749072557 |         ideal
ACK FOUND > 1; len(fronts)=1
   147 |    26313 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1658642247 |         ideal
ACK FOUND > 1; len(fronts)=1
   148 |    26492 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1071973671 |         ideal
ACK FOUND > 1; len(fronts)=1
   149 |    26671 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0718202849 |         ideal
ACK FOUND > 1; len(fronts)=1
   150 |    26850 |     19 |  0.000000E+00 |  0.000000E+00 |  2.5754087441 |         nadir
ACK FOUND > 1; len(fronts)=1
   151 |    27029 |      9 |  0.000000E+00 |  0.000000E+00 |  0.5879446617 |         ideal
ACK FOUND > 1; len(fronts)=1
   152 |    27208 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0683692950 |         ideal
ACK FOUND > 1; len(fronts)=1
   153 |    27387 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3551343295 |         ideal
ACK FOUND > 1; len(fronts)=1
   154 |    27566 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2625566595 |         ideal
ACK FOUND > 1; len(fronts)=1
   155 |    27745 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2432882860 |         ideal
ACK FOUND > 1; len(fronts)=1
   156 |    27924 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1029284595 |         ideal
ACK FOUND > 1; len(fronts)=1
   157 |    28103 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0275553140 |         ideal
ACK FOUND > 1; len(fronts)=1
   158 |    28282 |      9 |  0.000000E+00 |  0.000000E+00 |  0.2638695226 |         ideal
ACK FOUND > 1; len(fronts)=1
   159 |    28461 |     10 |  0.000000E+00 |  0.000000E+00 |  0.4678668281 |         ideal
ACK FOUND > 1; len(fronts)=1
   160 |    28640 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3392505059 |         ideal
ACK FOUND > 1; len(fronts)=1
   161 |    28819 |     10 |  0.000000E+00 |  0.000000E+00 |  0.5613630374 |         ideal
ACK FOUND > 1; len(fronts)=1
   162 |    28998 |     10 |  0.000000E+00 |  0.000000E+00 |  0.4867771915 |         ideal
ACK FOUND > 1; len(fronts)=1
   163 |    29177 |      5 |  0.000000E+00 |  0.000000E+00 |  3.6338058343 |         ideal
ACK FOUND > 1; len(fronts)=1
   164 |    29356 |     10 |  0.000000E+00 |  0.000000E+00 |  0.6349084206 |         ideal
ACK FOUND > 1; len(fronts)=1
   165 |    29535 |      4 |  0.000000E+00 |  0.000000E+00 |  1.2559750751 |         ideal
ACK FOUND > 1; len(fronts)=1
   166 |    29714 |      3 |  0.000000E+00 |  0.000000E+00 |  2.3630609052 |         ideal
ACK FOUND > 1; len(fronts)=1
   167 |    29893 |      3 |  0.000000E+00 |  0.000000E+00 |  0.7026518317 |         ideal
ACK FOUND > 1; len(fronts)=1
   168 |    30072 |      4 |  0.000000E+00 |  0.000000E+00 |  0.9468376334 |         ideal
ACK FOUND > 1; len(fronts)=1
   169 |    30251 |      6 |  0.000000E+00 |  0.000000E+00 |  0.5003982007 |         ideal
ACK FOUND > 1; len(fronts)=1
   170 |    30430 |      8 |  0.000000E+00 |  0.000000E+00 |  0.4919387270 |         ideal
ACK FOUND > 1; len(fronts)=1
   171 |    30609 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3268266028 |         ideal
ACK FOUND > 1; len(fronts)=1
   172 |    30788 |      9 |  0.000000E+00 |  0.000000E+00 |  0.0456362933 |         ideal
ACK FOUND > 1; len(fronts)=1
   173 |    30967 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0768091496 |         ideal
ACK FOUND > 1; len(fronts)=1
   174 |    31146 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0396548978 |         ideal
ACK FOUND > 1; len(fronts)=1
   175 |    31325 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1178758781 |         ideal
ACK FOUND > 1; len(fronts)=1
   176 |    31504 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3257549825 |         ideal
ACK FOUND > 1; len(fronts)=1
   177 |    31683 |     14 |  0.000000E+00 |  0.000000E+00 |  0.3204804510 |         ideal
ACK FOUND > 1; len(fronts)=1
   178 |    31862 |     14 |  0.000000E+00 |  0.000000E+00 |  0.4035140381 |         ideal
ACK FOUND > 1; len(fronts)=1
   179 |    32041 |     16 |  0.000000E+00 |  0.000000E+00 |  0.7721322025 |         ideal
ACK FOUND > 1; len(fronts)=1
   180 |    32220 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2103217396 |         ideal
ACK FOUND > 1; len(fronts)=1
   181 |    32399 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1489556650 |         ideal
ACK FOUND > 1; len(fronts)=1
   182 |    32578 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2514438328 |         ideal
ACK FOUND > 1; len(fronts)=1
   183 |    32757 |     20 |  0.000000E+00 |  0.000000E+00 |  0.4129301879 |         ideal
ACK FOUND > 1; len(fronts)=1
   184 |    32936 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2462227942 |         ideal
ACK FOUND > 1; len(fronts)=1
   185 |    33115 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1953866732 |         ideal
ACK FOUND > 1; len(fronts)=1
   186 |    33294 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1804449605 |         ideal
ACK FOUND > 1; len(fronts)=1
   187 |    33473 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1528618161 |         ideal
ACK FOUND > 1; len(fronts)=1
   188 |    33652 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1429454372 |         ideal
ACK FOUND > 1; len(fronts)=1
   189 |    33831 |     11 |  0.000000E+00 |  0.000000E+00 |  0.1804449605 |         ideal
ACK FOUND > 1; len(fronts)=1
   190 |    34010 |      9 |  0.000000E+00 |  0.000000E+00 |  0.2553882793 |         ideal
ACK FOUND > 1; len(fronts)=1
   191 |    34189 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2052041783 |         ideal
ACK FOUND > 1; len(fronts)=1
   192 |    34368 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0488665914 |         ideal
ACK FOUND > 1; len(fronts)=1
   193 |    34547 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1393518373 |         ideal
ACK FOUND > 1; len(fronts)=1
   194 |    34726 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0479933048 |         ideal
ACK FOUND > 1; len(fronts)=1
   195 |    34905 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1538071632 |         ideal
ACK FOUND > 1; len(fronts)=1
   196 |    35084 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1047691143 |         ideal
ACK FOUND > 1; len(fronts)=1
   197 |    35263 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0490702057 |         ideal
ACK FOUND > 1; len(fronts)=1
   198 |    35442 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1065283303 |         ideal
ACK FOUND > 1; len(fronts)=1
   199 |    35621 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0988924806 |         ideal
ACK FOUND > 1; len(fronts)=1
   200 |    35800 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0575807827 |         ideal
Begin print with Final Cash: 1283069.9771318878047 => return: 0.2830699771319
Month 1:
"""

# Extract arrays
ack_array, n_nds_array, eps_array, indicator_array = extract_arrays(text_data)

print("front_num_Array =", ack_array)
print("n_nds_Array =", n_nds_array)
print("eps_Array =", eps_array)
print("indicator_Array =", indicator_array)
