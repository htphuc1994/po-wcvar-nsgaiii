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
     1 |      179 |      8 |  0.000000E+00 |  2.904208E+02 |             - |             -
ACK FOUND > 1; len(fronts)=2
     2 |      358 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2759140546 |         ideal
ACK FOUND > 1; len(fronts)=2
     3 |      537 |      3 |  0.000000E+00 |  0.000000E+00 |  0.7708429302 |         ideal
ACK FOUND > 1; len(fronts)=2
     4 |      716 |      5 |  0.000000E+00 |  0.000000E+00 |  0.2993459157 |         ideal
ACK FOUND > 1; len(fronts)=1
     5 |      895 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3436836401 |         ideal
ACK FOUND > 1; len(fronts)=1
     6 |     1074 |      7 |  0.000000E+00 |  0.000000E+00 |  0.6068766530 |         ideal
ACK FOUND > 1; len(fronts)=1
     7 |     1253 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3551297780 |         ideal
ACK FOUND > 1; len(fronts)=1
     8 |     1432 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1517838936 |         ideal
ACK FOUND > 1; len(fronts)=1
     9 |     1611 |      7 |  0.000000E+00 |  0.000000E+00 |  0.8050211997 |         ideal
ACK FOUND > 1; len(fronts)=1
    10 |     1790 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3644439739 |         ideal
ACK FOUND > 1; len(fronts)=1
    11 |     1969 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2574241405 |         ideal
ACK FOUND > 1; len(fronts)=1
    12 |     2148 |      6 |  0.000000E+00 |  0.000000E+00 |  0.2633411864 |         ideal
ACK FOUND > 1; len(fronts)=1
    13 |     2327 |      7 |  0.000000E+00 |  0.000000E+00 |  0.3567792321 |         ideal
ACK FOUND > 1; len(fronts)=1
    14 |     2506 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1663281122 |         ideal
ACK FOUND > 1; len(fronts)=1
    15 |     2685 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1046246408 |         ideal
ACK FOUND > 1; len(fronts)=1
    16 |     2864 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2758447606 |         ideal
ACK FOUND > 1; len(fronts)=1
    17 |     3043 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2899659170 |         ideal
ACK FOUND > 1; len(fronts)=1
    18 |     3222 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2184942628 |         ideal
ACK FOUND > 1; len(fronts)=1
    19 |     3401 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1210112938 |         ideal
ACK FOUND > 1; len(fronts)=1
    20 |     3580 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1319590243 |         ideal
ACK FOUND > 1; len(fronts)=1
    21 |     3759 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1544850724 |         ideal
ACK FOUND > 1; len(fronts)=1
    22 |     3938 |      8 |  0.000000E+00 |  0.000000E+00 |  0.1475968974 |         ideal
ACK FOUND > 1; len(fronts)=1
    23 |     4117 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0996593602 |         ideal
ACK FOUND > 1; len(fronts)=1
    24 |     4296 |      3 |  0.000000E+00 |  0.000000E+00 |  3.3526189250 |         ideal
ACK FOUND > 1; len(fronts)=1
    25 |     4475 |      6 |  0.000000E+00 |  0.000000E+00 |  0.8272148904 |         ideal
ACK FOUND > 1; len(fronts)=1
    26 |     4654 |      5 |  0.000000E+00 |  0.000000E+00 |  1.7370622054 |         ideal
ACK FOUND > 1; len(fronts)=1
    27 |     4833 |     10 |  0.000000E+00 |  0.000000E+00 |  0.6769116799 |         ideal
ACK FOUND > 1; len(fronts)=1
    28 |     5012 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2221225040 |         ideal
ACK FOUND > 1; len(fronts)=1
    29 |     5191 |      5 |  0.000000E+00 |  0.000000E+00 |  1.5216311565 |         ideal
ACK FOUND > 1; len(fronts)=1
    30 |     5370 |      8 |  0.000000E+00 |  0.000000E+00 |  0.6198969174 |         ideal
ACK FOUND > 1; len(fronts)=1
    31 |     5549 |      4 |  0.000000E+00 |  0.000000E+00 |  1.5608227785 |         ideal
ACK FOUND > 1; len(fronts)=1
    32 |     5728 |      7 |  0.000000E+00 |  0.000000E+00 |  0.6094355961 |         ideal
ACK FOUND > 1; len(fronts)=1
    33 |     5907 |      7 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
    34 |     6086 |      8 |  0.000000E+00 |  0.000000E+00 |  0.5543190116 |         ideal
ACK FOUND > 1; len(fronts)=1
    35 |     6265 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3475357738 |         ideal
ACK FOUND > 1; len(fronts)=1
    36 |     6444 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2510400833 |         ideal
ACK FOUND > 1; len(fronts)=1
    37 |     6623 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2575547466 |         ideal
ACK FOUND > 1; len(fronts)=1
    38 |     6802 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2048059914 |         ideal
ACK FOUND > 1; len(fronts)=1
    39 |     6981 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1610875216 |         ideal
ACK FOUND > 1; len(fronts)=1
    40 |     7160 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2167734294 |         ideal
ACK FOUND > 1; len(fronts)=1
    41 |     7339 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2207747322 |         ideal
ACK FOUND > 1; len(fronts)=1
    42 |     7518 |     27 |  0.000000E+00 |  0.000000E+00 |  0.5497799505 |         ideal
ACK FOUND > 1; len(fronts)=1
    43 |     7697 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1246762749 |         ideal
ACK FOUND > 1; len(fronts)=1
    44 |     7876 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0189164469 |         ideal
ACK FOUND > 1; len(fronts)=1
    45 |     8055 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1503695165 |         ideal
ACK FOUND > 1; len(fronts)=1
    46 |     8234 |     16 |  0.000000E+00 |  0.000000E+00 |  0.3787661615 |         ideal
ACK FOUND > 1; len(fronts)=1
    47 |     8413 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1295437997 |         ideal
ACK FOUND > 1; len(fronts)=1
    48 |     8592 |      4 |  0.000000E+00 |  0.000000E+00 |  0.8318560236 |         ideal
ACK FOUND > 1; len(fronts)=1
    49 |     8771 |      7 |  0.000000E+00 |  0.000000E+00 |  0.5999150100 |         ideal
ACK FOUND > 1; len(fronts)=1
    50 |     8950 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0558325832 |         ideal
ACK FOUND > 1; len(fronts)=1
    51 |     9129 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3184331360 |         ideal
ACK FOUND > 1; len(fronts)=1
    52 |     9308 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1647354015 |         ideal
ACK FOUND > 1; len(fronts)=1
    53 |     9487 |     17 |  0.000000E+00 |  0.000000E+00 |  0.3057550109 |         ideal
ACK FOUND > 1; len(fronts)=1
    54 |     9666 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1149309176 |         ideal
ACK FOUND > 1; len(fronts)=1
    55 |     9845 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0881491227 |         ideal
ACK FOUND > 1; len(fronts)=1
    56 |    10024 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1692735565 |         ideal
ACK FOUND > 1; len(fronts)=1
    57 |    10203 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1698442900 |         ideal
ACK FOUND > 1; len(fronts)=1
    58 |    10382 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1534312755 |         ideal
ACK FOUND > 1; len(fronts)=1
    59 |    10561 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2021382859 |         ideal
ACK FOUND > 1; len(fronts)=1
    60 |    10740 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1039425965 |         ideal
ACK FOUND > 1; len(fronts)=1
    61 |    10919 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1951505969 |         ideal
ACK FOUND > 1; len(fronts)=1
    62 |    11098 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3034599393 |         ideal
ACK FOUND > 1; len(fronts)=1
    63 |    11277 |     11 |  0.000000E+00 |  0.000000E+00 |  0.3684307523 |         ideal
ACK FOUND > 1; len(fronts)=1
    64 |    11456 |      6 |  0.000000E+00 |  0.000000E+00 |  0.3650715552 |         ideal
ACK FOUND > 1; len(fronts)=1
    65 |    11635 |     11 |  0.000000E+00 |  0.000000E+00 |  0.7226467256 |         ideal
ACK FOUND > 1; len(fronts)=1
    66 |    11814 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2057534794 |         ideal
ACK FOUND > 1; len(fronts)=1
    67 |    11993 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1879793464 |         ideal
ACK FOUND > 1; len(fronts)=1
    68 |    12172 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0830704298 |         ideal
ACK FOUND > 1; len(fronts)=1
    69 |    12351 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1735005392 |         ideal
ACK FOUND > 1; len(fronts)=1
    70 |    12530 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0739277229 |         ideal
ACK FOUND > 1; len(fronts)=1
    71 |    12709 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3017934415 |         ideal
ACK FOUND > 1; len(fronts)=1
    72 |    12888 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1248916714 |         ideal
ACK FOUND > 1; len(fronts)=1
    73 |    13067 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2116618505 |         ideal
ACK FOUND > 1; len(fronts)=1
    74 |    13246 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2254520038 |         ideal
ACK FOUND > 1; len(fronts)=1
    75 |    13425 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1793012131 |         ideal
ACK FOUND > 1; len(fronts)=1
    76 |    13604 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2184738371 |         ideal
ACK FOUND > 1; len(fronts)=1
    77 |    13783 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0044809647 |         ideal
ACK FOUND > 1; len(fronts)=1
    78 |    13962 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0944562316 |         ideal
ACK FOUND > 1; len(fronts)=1
    79 |    14141 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1162874912 |         ideal
ACK FOUND > 1; len(fronts)=1
    80 |    14320 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0426802709 |         ideal
ACK FOUND > 1; len(fronts)=1
    81 |    14499 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0396381885 |         nadir
ACK FOUND > 1; len(fronts)=1
    82 |    14678 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0378721384 |         ideal
ACK FOUND > 1; len(fronts)=1
    83 |    14857 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1411963358 |         ideal
ACK FOUND > 1; len(fronts)=1
    84 |    15036 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0574443192 |         ideal
ACK FOUND > 1; len(fronts)=1
    85 |    15215 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0171550219 |         ideal
ACK FOUND > 1; len(fronts)=1
    86 |    15394 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0433058366 |         ideal
ACK FOUND > 1; len(fronts)=1
    87 |    15573 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0707487160 |         ideal
ACK FOUND > 1; len(fronts)=1
    88 |    15752 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2654102152 |         ideal
ACK FOUND > 1; len(fronts)=1
    89 |    15931 |      9 |  0.000000E+00 |  0.000000E+00 |  0.8592361522 |         ideal
ACK FOUND > 1; len(fronts)=1
    90 |    16110 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1604615137 |         ideal
ACK FOUND > 1; len(fronts)=1
    91 |    16289 |      8 |  0.000000E+00 |  0.000000E+00 |  0.000000E+00 |             f
ACK FOUND > 1; len(fronts)=1
    92 |    16468 |     10 |  0.000000E+00 |  0.000000E+00 |  0.1053530642 |         ideal
ACK FOUND > 1; len(fronts)=1
    93 |    16647 |      8 |  0.000000E+00 |  0.000000E+00 |  0.1172605507 |         ideal
ACK FOUND > 1; len(fronts)=1
    94 |    16826 |     10 |  0.000000E+00 |  0.000000E+00 |  0.0508337957 |         ideal
ACK FOUND > 1; len(fronts)=1
    95 |    17005 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0242051121 |         nadir
ACK FOUND > 1; len(fronts)=1
    96 |    17184 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1036009076 |         ideal
ACK FOUND > 1; len(fronts)=1
    97 |    17363 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2962836750 |         ideal
ACK FOUND > 1; len(fronts)=1
    98 |    17542 |      8 |  0.000000E+00 |  0.000000E+00 |  0.4210271448 |         ideal
ACK FOUND > 1; len(fronts)=1
    99 |    17721 |     12 |  0.000000E+00 |  0.000000E+00 |  0.3787495423 |         ideal
ACK FOUND > 1; len(fronts)=1
   100 |    17900 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2052750583 |         ideal
ACK FOUND > 1; len(fronts)=1
   101 |    18079 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0507081212 |         ideal
ACK FOUND > 1; len(fronts)=1
   102 |    18258 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0795413423 |         ideal
ACK FOUND > 1; len(fronts)=1
   103 |    18437 |     20 |  0.000000E+00 |  0.000000E+00 |  0.2176097382 |         ideal
ACK FOUND > 1; len(fronts)=1
   104 |    18616 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0782072967 |         ideal
ACK FOUND > 1; len(fronts)=1
   105 |    18795 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1657790130 |         ideal
ACK FOUND > 1; len(fronts)=1
   106 |    18974 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0765522081 |         ideal
ACK FOUND > 1; len(fronts)=1
   107 |    19153 |     14 |  0.000000E+00 |  0.000000E+00 |  0.3863482490 |         ideal
ACK FOUND > 1; len(fronts)=1
   108 |    19332 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2771812108 |         ideal
ACK FOUND > 1; len(fronts)=1
   109 |    19511 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0418086326 |         ideal
ACK FOUND > 1; len(fronts)=1
   110 |    19690 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0436328630 |         ideal
ACK FOUND > 1; len(fronts)=1
   111 |    19869 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1541058202 |         ideal
ACK FOUND > 1; len(fronts)=1
   112 |    20048 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0824155009 |         ideal
ACK FOUND > 1; len(fronts)=1
   113 |    20227 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1913881920 |         ideal
ACK FOUND > 1; len(fronts)=1
   114 |    20406 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1670052148 |         nadir
ACK FOUND > 1; len(fronts)=1
   115 |    20585 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1236802542 |         ideal
ACK FOUND > 1; len(fronts)=1
   116 |    20764 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2192544108 |         ideal
ACK FOUND > 1; len(fronts)=1
   117 |    20943 |      8 |  0.000000E+00 |  0.000000E+00 |  0.3032423565 |         ideal
ACK FOUND > 1; len(fronts)=1
   118 |    21122 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1236802542 |         ideal
ACK FOUND > 1; len(fronts)=1
   119 |    21301 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0770611690 |         ideal
ACK FOUND > 1; len(fronts)=1
   120 |    21480 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0797938732 |         ideal
ACK FOUND > 1; len(fronts)=1
   121 |    21659 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0260226458 |         ideal
ACK FOUND > 1; len(fronts)=1
   122 |    21838 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1599705274 |         ideal
ACK FOUND > 1; len(fronts)=1
   123 |    22017 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0283075945 |         ideal
ACK FOUND > 1; len(fronts)=1
   124 |    22196 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1902942937 |         ideal
ACK FOUND > 1; len(fronts)=1
   125 |    22375 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0694005373 |         ideal
ACK FOUND > 1; len(fronts)=1
   126 |    22554 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0089594654 |         ideal
ACK FOUND > 1; len(fronts)=1
   127 |    22733 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2350166143 |         ideal
ACK FOUND > 1; len(fronts)=1
   128 |    22912 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1902942937 |         ideal
ACK FOUND > 1; len(fronts)=1
   129 |    23091 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1739078876 |         nadir
ACK FOUND > 1; len(fronts)=1
   130 |    23270 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0257398166 |         ideal
ACK FOUND > 1; len(fronts)=1
   131 |    23449 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2350166143 |         ideal
ACK FOUND > 1; len(fronts)=1
   132 |    23628 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1770998912 |         ideal
ACK FOUND > 1; len(fronts)=1
   133 |    23807 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0382665014 |         ideal
ACK FOUND > 1; len(fronts)=1
   134 |    23986 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0665628275 |         ideal
ACK FOUND > 1; len(fronts)=1
   135 |    24165 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0624087262 |         ideal
ACK FOUND > 1; len(fronts)=1
   136 |    24344 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0632144093 |         ideal
ACK FOUND > 1; len(fronts)=1
   137 |    24523 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0751378022 |         ideal
ACK FOUND > 1; len(fronts)=1
   138 |    24702 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0733824094 |             f
ACK FOUND > 1; len(fronts)=1
   139 |    24881 |     33 |  0.000000E+00 |  0.000000E+00 |  0.1983031657 |         ideal
ACK FOUND > 1; len(fronts)=1
   140 |    25060 |     31 |  0.000000E+00 |  0.000000E+00 |  0.2473543080 |         ideal
ACK FOUND > 1; len(fronts)=1
   141 |    25239 |     30 |  0.000000E+00 |  0.000000E+00 |  0.1139711865 |         ideal
ACK FOUND > 1; len(fronts)=1
   142 |    25418 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1983031657 |         ideal
ACK FOUND > 1; len(fronts)=1
   143 |    25597 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0413139146 |         ideal
ACK FOUND > 1; len(fronts)=1
   144 |    25776 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0430943092 |         ideal
ACK FOUND > 1; len(fronts)=1
   145 |    25955 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1868006987 |         ideal
ACK FOUND > 1; len(fronts)=1
   146 |    26134 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1765893981 |         ideal
ACK FOUND > 1; len(fronts)=1
   147 |    26313 |     28 |  0.000000E+00 |  0.000000E+00 |  0.2144609236 |         ideal
ACK FOUND > 1; len(fronts)=1
   148 |    26492 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0691628947 |         ideal
ACK FOUND > 1; len(fronts)=1
   149 |    26671 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0478012824 |         ideal
ACK FOUND > 1; len(fronts)=1
   150 |    26850 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1370056544 |         ideal
ACK FOUND > 1; len(fronts)=1
   151 |    27029 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0148366777 |         ideal
ACK FOUND > 1; len(fronts)=1
   152 |    27208 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0066561136 |         ideal
ACK FOUND > 1; len(fronts)=1
   153 |    27387 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1668900559 |         ideal
ACK FOUND > 1; len(fronts)=1
   154 |    27566 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0176062737 |         ideal
ACK FOUND > 1; len(fronts)=1
   155 |    27745 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0434043755 |         ideal
ACK FOUND > 1; len(fronts)=1
   156 |    27924 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0798282271 |         ideal
ACK FOUND > 1; len(fronts)=1
   157 |    28103 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0451038059 |         ideal
ACK FOUND > 1; len(fronts)=1
   158 |    28282 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0494671490 |         ideal
ACK FOUND > 1; len(fronts)=1
   159 |    28461 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0085854609 |         ideal
ACK FOUND > 1; len(fronts)=1
   160 |    28640 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0201142950 |         ideal
ACK FOUND > 1; len(fronts)=1
   161 |    28819 |     30 |  0.000000E+00 |  0.000000E+00 |  0.1727643296 |         ideal
ACK FOUND > 1; len(fronts)=1
   162 |    28998 |     31 |  0.000000E+00 |  0.000000E+00 |  0.1860912107 |         ideal
ACK FOUND > 1; len(fronts)=1
   163 |    29177 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0087374748 |             f
ACK FOUND > 1; len(fronts)=1
   164 |    29356 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0121933420 |         ideal
ACK FOUND > 1; len(fronts)=1
   165 |    29535 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0129894738 |         ideal
ACK FOUND > 1; len(fronts)=1
   166 |    29714 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0131604208 |         ideal
ACK FOUND > 1; len(fronts)=1
   167 |    29893 |     32 |  0.000000E+00 |  0.000000E+00 |  0.1284600870 |         ideal
ACK FOUND > 1; len(fronts)=1
   168 |    30072 |     28 |  0.000000E+00 |  0.000000E+00 |  0.1903259031 |         ideal
ACK FOUND > 1; len(fronts)=1
   169 |    30251 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0137531182 |         ideal
ACK FOUND > 1; len(fronts)=1
   170 |    30430 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0293413551 |         ideal
ACK FOUND > 1; len(fronts)=1
   171 |    30609 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0660893865 |         ideal
ACK FOUND > 1; len(fronts)=1
   172 |    30788 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0232863536 |         ideal
ACK FOUND > 1; len(fronts)=1
   173 |    30967 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0097422656 |         ideal
ACK FOUND > 1; len(fronts)=1
   174 |    31146 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0346547057 |         ideal
ACK FOUND > 1; len(fronts)=1
   175 |    31325 |     34 |  0.000000E+00 |  0.000000E+00 |  0.3051402452 |         nadir
ACK FOUND > 1; len(fronts)=1
   176 |    31504 |     35 |  0.000000E+00 |  0.000000E+00 |  0.0492938451 |         ideal
ACK FOUND > 1; len(fronts)=1
   177 |    31683 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0096294995 |         ideal
ACK FOUND > 1; len(fronts)=1
   178 |    31862 |     31 |  0.000000E+00 |  0.000000E+00 |  4.1147697362 |         nadir
ACK FOUND > 1; len(fronts)=1
   179 |    32041 |     29 |  0.000000E+00 |  0.000000E+00 |  0.8044877772 |         nadir
ACK FOUND > 1; len(fronts)=1
   180 |    32220 |     32 |  0.000000E+00 |  0.000000E+00 |  0.1080723331 |         ideal
ACK FOUND > 1; len(fronts)=1
   181 |    32399 |     29 |  0.000000E+00 |  0.000000E+00 |  0.7205454856 |         nadir
ACK FOUND > 1; len(fronts)=1
   182 |    32578 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1157879702 |         ideal
ACK FOUND > 1; len(fronts)=1
   183 |    32757 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0243323157 |         ideal
ACK FOUND > 1; len(fronts)=1
   184 |    32936 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0306796607 |         ideal
ACK FOUND > 1; len(fronts)=1
   185 |    33115 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0868655708 |         ideal
ACK FOUND > 1; len(fronts)=1
   186 |    33294 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0136572947 |         ideal
ACK FOUND > 1; len(fronts)=1
   187 |    33473 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0998403612 |         ideal
ACK FOUND > 1; len(fronts)=1
   188 |    33652 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0891001153 |         ideal
ACK FOUND > 1; len(fronts)=1
   189 |    33831 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0319847922 |         ideal
ACK FOUND > 1; len(fronts)=1
   190 |    34010 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1390750974 |         ideal
ACK FOUND > 1; len(fronts)=1
   191 |    34189 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0906083532 |         nadir
ACK FOUND > 1; len(fronts)=1
   192 |    34368 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0294221391 |         nadir
ACK FOUND > 1; len(fronts)=1
   193 |    34547 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0225462221 |         ideal
ACK FOUND > 1; len(fronts)=1
   194 |    34726 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1849174509 |         nadir
ACK FOUND > 1; len(fronts)=1
   195 |    34905 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0222107930 |         ideal
ACK FOUND > 1; len(fronts)=1
   196 |    35084 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0227153183 |         ideal
ACK FOUND > 1; len(fronts)=1
   197 |    35263 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0289673699 |             f
ACK FOUND > 1; len(fronts)=1
   198 |    35442 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1227793040 |             f
ACK FOUND > 1; len(fronts)=1
   199 |    35621 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0025305788 |         ideal
ACK FOUND > 1; len(fronts)=1
   200 |    35800 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0401610577 |         ideal
"""

# Extract arrays
ack_array, n_nds_array, eps_array, indicator_array = extract_arrays(text_data)

print("front_num_Array =", ack_array)
print("n_nds_Array =", n_nds_array)
print("eps_Array =", eps_array)
print("indicator_Array =", indicator_array)
