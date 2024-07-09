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
ACK FOUND > 1; len(fronts)=3
==========================================================================================
n_gen  |  n_eval  | n_nds  |     cv_min    |     cv_avg    |      eps      |   indicator  
==========================================================================================
     1 |      179 |      7 |  0.000000E+00 |  2.904208E+02 |             - |             -
ACK FOUND > 1; len(fronts)=2
     2 |      358 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2319371645 |         ideal
ACK FOUND > 1; len(fronts)=1
     3 |      537 |     13 |  0.000000E+00 |  0.000000E+00 |  0.4642760326 |         ideal
ACK FOUND > 1; len(fronts)=1
     4 |      716 |     10 |  0.000000E+00 |  0.000000E+00 |  0.4245421233 |         ideal
ACK FOUND > 1; len(fronts)=1
     5 |      895 |      7 |  0.000000E+00 |  0.000000E+00 |  0.6041900461 |         ideal
ACK FOUND > 1; len(fronts)=1
     6 |     1074 |      9 |  0.000000E+00 |  0.000000E+00 |  0.4411281822 |         ideal
ACK FOUND > 1; len(fronts)=1
     7 |     1253 |     15 |  0.000000E+00 |  0.000000E+00 |  0.4071107216 |         ideal
ACK FOUND > 1; len(fronts)=1
     8 |     1432 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2422516013 |         ideal
ACK FOUND > 1; len(fronts)=1
     9 |     1611 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0956855508 |         ideal
ACK FOUND > 1; len(fronts)=1
    10 |     1790 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1015021043 |         ideal
ACK FOUND > 1; len(fronts)=1
    11 |     1969 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1779031614 |         ideal
ACK FOUND > 1; len(fronts)=1
    12 |     2148 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1857223492 |         ideal
ACK FOUND > 1; len(fronts)=1
    13 |     2327 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2544476950 |         ideal
ACK FOUND > 1; len(fronts)=1
    14 |     2506 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2331493956 |         ideal
ACK FOUND > 1; len(fronts)=1
    15 |     2685 |     10 |  0.000000E+00 |  0.000000E+00 |  0.4990158202 |         ideal
ACK FOUND > 1; len(fronts)=1
    16 |     2864 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4933796038 |         ideal
ACK FOUND > 1; len(fronts)=1
    17 |     3043 |      5 |  0.000000E+00 |  0.000000E+00 |  0.2377621119 |         ideal
ACK FOUND > 1; len(fronts)=1
    18 |     3222 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2927908832 |         ideal
ACK FOUND > 1; len(fronts)=1
    19 |     3401 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1106066412 |         ideal
ACK FOUND > 1; len(fronts)=1
    20 |     3580 |      8 |  0.000000E+00 |  0.000000E+00 |  0.4975470657 |         ideal
ACK FOUND > 1; len(fronts)=1
    21 |     3759 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2911459853 |         ideal
ACK FOUND > 1; len(fronts)=1
    22 |     3938 |     15 |  0.000000E+00 |  0.000000E+00 |  0.4573162208 |         ideal
ACK FOUND > 1; len(fronts)=1
    23 |     4117 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2643629586 |         ideal
ACK FOUND > 1; len(fronts)=1
    24 |     4296 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1748788113 |         ideal
ACK FOUND > 1; len(fronts)=1
    25 |     4475 |      8 |  0.000000E+00 |  0.000000E+00 |  0.1906946480 |         ideal
ACK FOUND > 1; len(fronts)=1
    26 |     4654 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1463199748 |         ideal
ACK FOUND > 1; len(fronts)=1
    27 |     4833 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1049411463 |         ideal
ACK FOUND > 1; len(fronts)=1
    28 |     5012 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2024833327 |         ideal
ACK FOUND > 1; len(fronts)=1
    29 |     5191 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1287075724 |         ideal
ACK FOUND > 1; len(fronts)=1
    30 |     5370 |     19 |  0.000000E+00 |  0.000000E+00 |  0.3824630952 |         ideal
ACK FOUND > 1; len(fronts)=1
    31 |     5549 |     11 |  0.000000E+00 |  0.000000E+00 |  0.5255903386 |         ideal
ACK FOUND > 1; len(fronts)=1
    32 |     5728 |      6 |  0.000000E+00 |  0.000000E+00 |  0.3486993192 |         ideal
ACK FOUND > 1; len(fronts)=1
    33 |     5907 |      8 |  0.000000E+00 |  0.000000E+00 |  0.3201748929 |         ideal
ACK FOUND > 1; len(fronts)=1
    34 |     6086 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2773419919 |         ideal
ACK FOUND > 1; len(fronts)=1
    35 |     6265 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3429431469 |         ideal
ACK FOUND > 1; len(fronts)=1
    36 |     6444 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1874707265 |         ideal
ACK FOUND > 1; len(fronts)=1
    37 |     6623 |      9 |  0.000000E+00 |  0.000000E+00 |  0.2376183574 |         ideal
ACK FOUND > 1; len(fronts)=1
    38 |     6802 |     11 |  0.000000E+00 |  0.000000E+00 |  0.1318501670 |         ideal
ACK FOUND > 1; len(fronts)=1
    39 |     6981 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2751593673 |         ideal
ACK FOUND > 1; len(fronts)=1
    40 |     7160 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2575218208 |         ideal
ACK FOUND > 1; len(fronts)=1
    41 |     7339 |     10 |  0.000000E+00 |  0.000000E+00 |  0.7259116276 |         ideal
ACK FOUND > 1; len(fronts)=1
    42 |     7518 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2329893800 |         ideal
ACK FOUND > 1; len(fronts)=1
    43 |     7697 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2668768744 |         ideal
ACK FOUND > 1; len(fronts)=1
    44 |     7876 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1383668988 |         ideal
ACK FOUND > 1; len(fronts)=1
    45 |     8055 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2485693020 |         ideal
ACK FOUND > 1; len(fronts)=1
    46 |     8234 |     20 |  0.000000E+00 |  0.000000E+00 |  0.3610847843 |         ideal
ACK FOUND > 1; len(fronts)=1
    47 |     8413 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0733388192 |         ideal
ACK FOUND > 1; len(fronts)=1
    48 |     8592 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1010273904 |         ideal
ACK FOUND > 1; len(fronts)=1
    49 |     8771 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1609525060 |         ideal
ACK FOUND > 1; len(fronts)=1
    50 |     8950 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1426950744 |         ideal
ACK FOUND > 1; len(fronts)=1
    51 |     9129 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2802924136 |         ideal
ACK FOUND > 1; len(fronts)=1
    52 |     9308 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0915242693 |         ideal
ACK FOUND > 1; len(fronts)=1
    53 |     9487 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2572433869 |         ideal
ACK FOUND > 1; len(fronts)=1
    54 |     9666 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1706257086 |         ideal
ACK FOUND > 1; len(fronts)=1
    55 |     9845 |     17 |  0.000000E+00 |  0.000000E+00 |  0.3755356819 |         ideal
ACK FOUND > 1; len(fronts)=1
    56 |    10024 |      7 |  0.000000E+00 |  0.000000E+00 |  0.4260867993 |         ideal
ACK FOUND > 1; len(fronts)=1
    57 |    10203 |      4 |  0.000000E+00 |  0.000000E+00 |  1.7653446557 |         ideal
ACK FOUND > 1; len(fronts)=1
    58 |    10382 |      5 |  0.000000E+00 |  0.000000E+00 |  0.6538180077 |         nadir
ACK FOUND > 1; len(fronts)=1
    59 |    10561 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3777766396 |         ideal
ACK FOUND > 1; len(fronts)=1
    60 |    10740 |     10 |  0.000000E+00 |  0.000000E+00 |  0.6266642063 |         ideal
ACK FOUND > 1; len(fronts)=1
    61 |    10919 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1498500336 |         ideal
ACK FOUND > 1; len(fronts)=1
    62 |    11098 |      5 |  0.000000E+00 |  0.000000E+00 |  3.5198066994 |         ideal
ACK FOUND > 1; len(fronts)=1
    63 |    11277 |     10 |  0.000000E+00 |  0.000000E+00 |  0.7240320348 |         ideal
ACK FOUND > 1; len(fronts)=1
    64 |    11456 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3453703954 |         ideal
ACK FOUND > 1; len(fronts)=1
    65 |    11635 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0809397711 |         ideal
ACK FOUND > 1; len(fronts)=1
    66 |    11814 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1061236685 |         ideal
ACK FOUND > 1; len(fronts)=1
    67 |    11993 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0511859687 |         ideal
ACK FOUND > 1; len(fronts)=1
    68 |    12172 |     19 |  0.000000E+00 |  0.000000E+00 |  0.5487090445 |         ideal
ACK FOUND > 1; len(fronts)=1
    69 |    12351 |     11 |  0.000000E+00 |  0.000000E+00 |  0.1058388291 |         ideal
ACK FOUND > 1; len(fronts)=1
    70 |    12530 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0640351365 |         ideal
ACK FOUND > 1; len(fronts)=1
    71 |    12709 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2976428813 |         ideal
ACK FOUND > 1; len(fronts)=1
    72 |    12888 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1341638201 |         ideal
ACK FOUND > 1; len(fronts)=1
    73 |    13067 |     19 |  0.000000E+00 |  0.000000E+00 |  0.3582973041 |         ideal
ACK FOUND > 1; len(fronts)=1
    74 |    13246 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2031962220 |         ideal
ACK FOUND > 1; len(fronts)=1
    75 |    13425 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1943659813 |         ideal
ACK FOUND > 1; len(fronts)=1
    76 |    13604 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1280962739 |         ideal
ACK FOUND > 1; len(fronts)=1
    77 |    13783 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2663044032 |         ideal
ACK FOUND > 1; len(fronts)=1
    78 |    13962 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2649219332 |         nadir
ACK FOUND > 1; len(fronts)=1
    79 |    14141 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1864480770 |         ideal
ACK FOUND > 1; len(fronts)=1
    80 |    14320 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1239862278 |         ideal
ACK FOUND > 1; len(fronts)=1
    81 |    14499 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1585135513 |         ideal
ACK FOUND > 1; len(fronts)=1
    82 |    14678 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1700824715 |         ideal
ACK FOUND > 1; len(fronts)=1
    83 |    14857 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1155273439 |         ideal
ACK FOUND > 1; len(fronts)=1
    84 |    15036 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1714999297 |         ideal
ACK FOUND > 1; len(fronts)=1
    85 |    15215 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2491538094 |         ideal
ACK FOUND > 1; len(fronts)=1
    86 |    15394 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2902535857 |         ideal
ACK FOUND > 1; len(fronts)=1
    87 |    15573 |     26 |  0.000000E+00 |  0.000000E+00 |  0.2941974545 |         ideal
ACK FOUND > 1; len(fronts)=1
    88 |    15752 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2091904128 |         ideal
ACK FOUND > 1; len(fronts)=1
    89 |    15931 |      9 |  0.000000E+00 |  0.000000E+00 |  0.4340242022 |         ideal
ACK FOUND > 1; len(fronts)=1
    90 |    16110 |     10 |  0.000000E+00 |  0.000000E+00 |  0.7668600033 |         ideal
ACK FOUND > 1; len(fronts)=1
    91 |    16289 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1184246302 |         ideal
ACK FOUND > 1; len(fronts)=1
    92 |    16468 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1620787922 |         ideal
ACK FOUND > 1; len(fronts)=1
    93 |    16647 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2066019529 |         ideal
ACK FOUND > 1; len(fronts)=1
    94 |    16826 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1683287088 |         ideal
ACK FOUND > 1; len(fronts)=1
    95 |    17005 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0302812243 |         ideal
ACK FOUND > 1; len(fronts)=1
    96 |    17184 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1559716776 |         ideal
ACK FOUND > 1; len(fronts)=1
    97 |    17363 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1688346497 |         ideal
ACK FOUND > 1; len(fronts)=1
    98 |    17542 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0352906275 |         ideal
ACK FOUND > 1; len(fronts)=1
    99 |    17721 |      8 |  0.000000E+00 |  0.000000E+00 |  0.8101367402 |         ideal
ACK FOUND > 1; len(fronts)=1
   100 |    17900 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1311127303 |             f
ACK FOUND > 1; len(fronts)=1
   101 |    18079 |      9 |  0.000000E+00 |  0.000000E+00 |  0.2974566190 |         ideal
ACK FOUND > 1; len(fronts)=1
   102 |    18258 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3936658310 |         ideal
ACK FOUND > 1; len(fronts)=1
   103 |    18437 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0782098618 |         ideal
ACK FOUND > 1; len(fronts)=1
   104 |    18616 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0340683525 |         ideal
ACK FOUND > 1; len(fronts)=1
   105 |    18795 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1578683980 |         ideal
ACK FOUND > 1; len(fronts)=1
   106 |    18974 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1199100431 |         ideal
ACK FOUND > 1; len(fronts)=1
   107 |    19153 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0727802307 |         ideal
ACK FOUND > 1; len(fronts)=1
   108 |    19332 |     19 |  0.000000E+00 |  0.000000E+00 |  0.3520247411 |         ideal
ACK FOUND > 1; len(fronts)=1
   109 |    19511 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0945366762 |         ideal
ACK FOUND > 1; len(fronts)=1
   110 |    19690 |     10 |  0.000000E+00 |  0.000000E+00 |  1.3948068323 |         ideal
ACK FOUND > 1; len(fronts)=1
   111 |    19869 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1916313611 |         ideal
ACK FOUND > 1; len(fronts)=1
   112 |    20048 |     12 |  0.000000E+00 |  0.000000E+00 |  0.4019484961 |         ideal
ACK FOUND > 1; len(fronts)=1
   113 |    20227 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3076038444 |         ideal
ACK FOUND > 1; len(fronts)=1
   114 |    20406 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0311463676 |         ideal
ACK FOUND > 1; len(fronts)=1
   115 |    20585 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2999230826 |         ideal
ACK FOUND > 1; len(fronts)=1
   116 |    20764 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0730754907 |         ideal
ACK FOUND > 1; len(fronts)=1
   117 |    20943 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1596977693 |         ideal
ACK FOUND > 1; len(fronts)=1
   118 |    21122 |     19 |  0.000000E+00 |  0.000000E+00 |  0.3162777465 |         ideal
ACK FOUND > 1; len(fronts)=1
   119 |    21301 |     18 |  0.000000E+00 |  0.000000E+00 |  0.3601439484 |         ideal
ACK FOUND > 1; len(fronts)=1
   120 |    21480 |      8 |  0.000000E+00 |  0.000000E+00 |  0.1291110428 |         ideal
ACK FOUND > 1; len(fronts)=1
   121 |    21659 |      8 |  0.000000E+00 |  0.000000E+00 |  0.1171105295 |         ideal
ACK FOUND > 1; len(fronts)=1
   122 |    21838 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0677345203 |         ideal
ACK FOUND > 1; len(fronts)=1
   123 |    22017 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2469452360 |         ideal
ACK FOUND > 1; len(fronts)=1
   124 |    22196 |     14 |  0.000000E+00 |  0.000000E+00 |  0.3593911823 |         nadir
ACK FOUND > 1; len(fronts)=1
   125 |    22375 |     17 |  0.000000E+00 |  0.000000E+00 |  0.8650123978 |         ideal
ACK FOUND > 1; len(fronts)=1
   126 |    22554 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0573756898 |         ideal
ACK FOUND > 1; len(fronts)=1
   127 |    22733 |     19 |  0.000000E+00 |  0.000000E+00 |  0.4243772569 |         ideal
ACK FOUND > 1; len(fronts)=1
   128 |    22912 |     20 |  0.000000E+00 |  0.000000E+00 |  0.8895838384 |         ideal
ACK FOUND > 1; len(fronts)=1
   129 |    23091 |     16 |  0.000000E+00 |  0.000000E+00 |  0.5526597520 |         ideal
ACK FOUND > 1; len(fronts)=1
   130 |    23270 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1874303660 |         ideal
ACK FOUND > 1; len(fronts)=1
   131 |    23449 |     14 |  0.000000E+00 |  0.000000E+00 |  0.4368586347 |         nadir
ACK FOUND > 1; len(fronts)=1
   132 |    23628 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0068633702 |         ideal
ACK FOUND > 1; len(fronts)=1
   133 |    23807 |     11 |  0.000000E+00 |  0.000000E+00 |  0.1869906957 |         ideal
ACK FOUND > 1; len(fronts)=1
   134 |    23986 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2345615267 |         ideal
ACK FOUND > 1; len(fronts)=1
   135 |    24165 |     13 |  0.000000E+00 |  0.000000E+00 |  0.4825239081 |         ideal
ACK FOUND > 1; len(fronts)=1
   136 |    24344 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3254746217 |         ideal
ACK FOUND > 1; len(fronts)=1
   137 |    24523 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2538162419 |         ideal
ACK FOUND > 1; len(fronts)=1
   138 |    24702 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1018505444 |         ideal
ACK FOUND > 1; len(fronts)=1
   139 |    24881 |     12 |  0.000000E+00 |  0.000000E+00 |  2.3747353466 |         ideal
ACK FOUND > 1; len(fronts)=1
   140 |    25060 |     11 |  0.000000E+00 |  0.000000E+00 |  0.3893992789 |         ideal
ACK FOUND > 1; len(fronts)=1
   141 |    25239 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0753471900 |         ideal
ACK FOUND > 1; len(fronts)=1
   142 |    25418 |     18 |  0.000000E+00 |  0.000000E+00 |  0.5673198520 |         ideal
ACK FOUND > 1; len(fronts)=1
   143 |    25597 |     15 |  0.000000E+00 |  0.000000E+00 |  0.4153230082 |         ideal
ACK FOUND > 1; len(fronts)=1
   144 |    25776 |     17 |  0.000000E+00 |  0.000000E+00 |  0.6813051102 |         ideal
ACK FOUND > 1; len(fronts)=1
   145 |    25955 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2565724242 |         ideal
ACK FOUND > 1; len(fronts)=1
   146 |    26134 |     16 |  0.000000E+00 |  0.000000E+00 |  1.8861324080 |         ideal
ACK FOUND > 1; len(fronts)=1
   147 |    26313 |     17 |  0.000000E+00 |  0.000000E+00 |  0.6535155500 |         ideal
ACK FOUND > 1; len(fronts)=1
   148 |    26492 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0404760644 |         ideal
ACK FOUND > 1; len(fronts)=1
   149 |    26671 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0480503386 |         ideal
ACK FOUND > 1; len(fronts)=1
   150 |    26850 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0441139846 |         ideal
ACK FOUND > 1; len(fronts)=1
   151 |    27029 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1028435656 |         ideal
ACK FOUND > 1; len(fronts)=1
   152 |    27208 |     18 |  0.000000E+00 |  0.000000E+00 |  0.3662465262 |         ideal
ACK FOUND > 1; len(fronts)=1
   153 |    27387 |     18 |  0.000000E+00 |  0.000000E+00 |  0.3097809233 |         ideal
ACK FOUND > 1; len(fronts)=1
   154 |    27566 |     17 |  0.000000E+00 |  0.000000E+00 |  0.4338102806 |         ideal
ACK FOUND > 1; len(fronts)=1
   155 |    27745 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2889944599 |         nadir
ACK FOUND > 1; len(fronts)=1
   156 |    27924 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1509532841 |         ideal
ACK FOUND > 1; len(fronts)=1
   157 |    28103 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0882968158 |         ideal
ACK FOUND > 1; len(fronts)=1
   158 |    28282 |     20 |  0.000000E+00 |  0.000000E+00 |  0.3400637920 |         nadir
ACK FOUND > 1; len(fronts)=1
   159 |    28461 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0236286190 |         ideal
ACK FOUND > 1; len(fronts)=1
   160 |    28640 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0653808586 |         ideal
ACK FOUND > 1; len(fronts)=1
   161 |    28819 |      8 |  0.000000E+00 |  0.000000E+00 |  0.3197901978 |         ideal
ACK FOUND > 1; len(fronts)=1
   162 |    28998 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2543014348 |         ideal
ACK FOUND > 1; len(fronts)=1
   163 |    29177 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1852897396 |         ideal
ACK FOUND > 1; len(fronts)=1
   164 |    29356 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2985639276 |         nadir
ACK FOUND > 1; len(fronts)=1
   165 |    29535 |      9 |  0.000000E+00 |  0.000000E+00 |  0.5352731954 |         ideal
ACK FOUND > 1; len(fronts)=1
   166 |    29714 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2192190640 |         ideal
ACK FOUND > 1; len(fronts)=1
   167 |    29893 |      8 |  0.000000E+00 |  0.000000E+00 |  0.0396978612 |         ideal
ACK FOUND > 1; len(fronts)=1
   168 |    30072 |      9 |  0.000000E+00 |  0.000000E+00 |  1.2120642237 |         nadir
ACK FOUND > 1; len(fronts)=1
   169 |    30251 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2320252799 |         ideal
ACK FOUND > 1; len(fronts)=1
   170 |    30430 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1894595169 |         ideal
ACK FOUND > 1; len(fronts)=1
   171 |    30609 |     12 |  0.000000E+00 |  0.000000E+00 |  0.3527932598 |         ideal
ACK FOUND > 1; len(fronts)=1
   172 |    30788 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0934456602 |         ideal
ACK FOUND > 1; len(fronts)=1
   173 |    30967 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1904301907 |         ideal
ACK FOUND > 1; len(fronts)=1
   174 |    31146 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0865956948 |         ideal
ACK FOUND > 1; len(fronts)=1
   175 |    31325 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0920829371 |         ideal
ACK FOUND > 1; len(fronts)=1
   176 |    31504 |      9 |  0.000000E+00 |  0.000000E+00 |  0.6773482426 |         ideal
ACK FOUND > 1; len(fronts)=1
   177 |    31683 |     17 |  0.000000E+00 |  0.000000E+00 |  0.5059796144 |         ideal
ACK FOUND > 1; len(fronts)=1
   178 |    31862 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2272045527 |         ideal
ACK FOUND > 1; len(fronts)=1
   179 |    32041 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3202129792 |         ideal
ACK FOUND > 1; len(fronts)=1
   180 |    32220 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2035058634 |         ideal
ACK FOUND > 1; len(fronts)=1
   181 |    32399 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2891435408 |         ideal
ACK FOUND > 1; len(fronts)=1
   182 |    32578 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0631559597 |         ideal
ACK FOUND > 1; len(fronts)=1
   183 |    32757 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2107121782 |         ideal
ACK FOUND > 1; len(fronts)=1
   184 |    32936 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2563675362 |         ideal
ACK FOUND > 1; len(fronts)=1
   185 |    33115 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1866699514 |         ideal
ACK FOUND > 1; len(fronts)=1
   186 |    33294 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0935472944 |         ideal
ACK FOUND > 1; len(fronts)=1
   187 |    33473 |     25 |  0.000000E+00 |  0.000000E+00 |  0.2012521275 |         ideal
ACK FOUND > 1; len(fronts)=1
   188 |    33652 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2296354243 |         ideal
ACK FOUND > 1; len(fronts)=1
   189 |    33831 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1406332727 |         ideal
ACK FOUND > 1; len(fronts)=1
   190 |    34010 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0557966109 |         ideal
ACK FOUND > 1; len(fronts)=1
   191 |    34189 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1867508204 |         ideal
ACK FOUND > 1; len(fronts)=1
   192 |    34368 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0590938473 |         ideal
ACK FOUND > 1; len(fronts)=1
   193 |    34547 |     23 |  0.000000E+00 |  0.000000E+00 |  0.2296354243 |         ideal
ACK FOUND > 1; len(fronts)=1
   194 |    34726 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0041120190 |         ideal
ACK FOUND > 1; len(fronts)=1
   195 |    34905 |     28 |  0.000000E+00 |  0.000000E+00 |  0.3252800519 |         ideal
ACK FOUND > 1; len(fronts)=1
   196 |    35084 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1022776876 |         ideal
ACK FOUND > 1; len(fronts)=1
   197 |    35263 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0987959711 |         ideal
ACK FOUND > 1; len(fronts)=1
   198 |    35442 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1676037343 |         ideal
ACK FOUND > 1; len(fronts)=1
   199 |    35621 |     24 |  0.000000E+00 |  0.000000E+00 |  0.2009507190 |         ideal
ACK FOUND > 1; len(fronts)=1
   200 |    35800 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0099725227 |         ideal
"""

# Extract arrays
ack_array, n_nds_array, eps_array, indicator_array = extract_arrays(text_data)

print("front_num_Array =", ack_array)
print("n_nds_Array =", n_nds_array)
print("eps_Array =", eps_array)
print("indicator_Array =", indicator_array)
