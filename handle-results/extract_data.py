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
The time of execution of above program is : 483384.4599723816 ms
ACK FOUND > 1; len(fronts)=5
==========================================================================================
n_gen  |  n_eval  | n_nds  |     cv_min    |     cv_avg    |      eps      |   indicator  
==========================================================================================
     1 |      179 |      7 |  0.000000E+00 |  9.411311E+03 |             - |             -
ACK FOUND > 1; len(fronts)=2
     2 |      358 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1893310916 |         ideal
ACK FOUND > 1; len(fronts)=2
     3 |      537 |     12 |  0.000000E+00 |  0.000000E+00 |  0.4799427934 |         ideal
ACK FOUND > 1; len(fronts)=1
     4 |      716 |      6 |  0.000000E+00 |  0.000000E+00 |  1.2060815933 |         ideal
ACK FOUND > 1; len(fronts)=1
     5 |      895 |     12 |  0.000000E+00 |  0.000000E+00 |  0.4625567699 |         ideal
ACK FOUND > 1; len(fronts)=1
     6 |     1074 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3856723698 |         ideal
ACK FOUND > 1; len(fronts)=1
     7 |     1253 |     11 |  0.000000E+00 |  0.000000E+00 |  0.3890213906 |         ideal
ACK FOUND > 1; len(fronts)=1
     8 |     1432 |      6 |  0.000000E+00 |  0.000000E+00 |  1.8024776610 |         ideal
ACK FOUND > 1; len(fronts)=1
     9 |     1611 |      4 |  0.000000E+00 |  0.000000E+00 |  0.7813251353 |         ideal
ACK FOUND > 1; len(fronts)=1
    10 |     1790 |      6 |  0.000000E+00 |  0.000000E+00 |  0.1886998342 |         ideal
ACK FOUND > 1; len(fronts)=1
    11 |     1969 |     10 |  0.000000E+00 |  0.000000E+00 |  0.4397263353 |         ideal
ACK FOUND > 1; len(fronts)=1
    12 |     2148 |      9 |  0.000000E+00 |  0.000000E+00 |  0.4924742999 |         ideal
ACK FOUND > 1; len(fronts)=1
    13 |     2327 |      8 |  0.000000E+00 |  0.000000E+00 |  0.1729858867 |         ideal
ACK FOUND > 1; len(fronts)=1
    14 |     2506 |      8 |  0.000000E+00 |  0.000000E+00 |  0.0412583109 |         ideal
ACK FOUND > 1; len(fronts)=1
    15 |     2685 |      6 |  0.000000E+00 |  0.000000E+00 |  0.5122053011 |         ideal
ACK FOUND > 1; len(fronts)=1
    16 |     2864 |      9 |  0.000000E+00 |  0.000000E+00 |  0.9068011175 |         ideal
ACK FOUND > 1; len(fronts)=1
    17 |     3043 |     10 |  0.000000E+00 |  0.000000E+00 |  0.6820612033 |         ideal
ACK FOUND > 1; len(fronts)=1
    18 |     3222 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2192926478 |         ideal
ACK FOUND > 1; len(fronts)=1
    19 |     3401 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1199975062 |         ideal
ACK FOUND > 1; len(fronts)=1
    20 |     3580 |      4 |  0.000000E+00 |  0.000000E+00 |  4.1922882913 |         ideal
ACK FOUND > 1; len(fronts)=1
    21 |     3759 |      8 |  0.000000E+00 |  0.000000E+00 |  0.8146608410 |         ideal
ACK FOUND > 1; len(fronts)=1
    22 |     3938 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0727765582 |         ideal
ACK FOUND > 1; len(fronts)=1
    23 |     4117 |     10 |  0.000000E+00 |  0.000000E+00 |  0.7895107666 |         ideal
ACK FOUND > 1; len(fronts)=1
    24 |     4296 |      7 |  0.000000E+00 |  0.000000E+00 |  4.2382131002 |         ideal
ACK FOUND > 1; len(fronts)=1
    25 |     4475 |     11 |  0.000000E+00 |  0.000000E+00 |  0.7791147734 |         ideal
ACK FOUND > 1; len(fronts)=1
    26 |     4654 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1851412613 |         ideal
ACK FOUND > 1; len(fronts)=1
    27 |     4833 |     11 |  0.000000E+00 |  0.000000E+00 |  0.4866900978 |         ideal
ACK FOUND > 1; len(fronts)=1
    28 |     5012 |     16 |  0.000000E+00 |  0.000000E+00 |  0.2075292739 |         ideal
ACK FOUND > 1; len(fronts)=1
    29 |     5191 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2126755285 |         ideal
ACK FOUND > 1; len(fronts)=1
    30 |     5370 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1753771091 |         ideal
ACK FOUND > 1; len(fronts)=1
    31 |     5549 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0733795723 |         ideal
ACK FOUND > 1; len(fronts)=1
    32 |     5728 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1762038914 |         ideal
ACK FOUND > 1; len(fronts)=1
    33 |     5907 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2301629447 |         ideal
ACK FOUND > 1; len(fronts)=1
    34 |     6086 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1516067265 |         ideal
ACK FOUND > 1; len(fronts)=1
    35 |     6265 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2127871664 |         ideal
ACK FOUND > 1; len(fronts)=1
    36 |     6444 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0767199929 |         ideal
ACK FOUND > 1; len(fronts)=1
    37 |     6623 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0724813514 |         ideal
ACK FOUND > 1; len(fronts)=1
    38 |     6802 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1116259839 |         ideal
ACK FOUND > 1; len(fronts)=1
    39 |     6981 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0791381490 |         ideal
ACK FOUND > 1; len(fronts)=1
    40 |     7160 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0812604951 |         ideal
ACK FOUND > 1; len(fronts)=1
    41 |     7339 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0556900257 |         ideal
ACK FOUND > 1; len(fronts)=1
    42 |     7518 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0379054748 |         ideal
ACK FOUND > 1; len(fronts)=1
    43 |     7697 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0462539095 |         ideal
ACK FOUND > 1; len(fronts)=1
    44 |     7876 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1107206753 |         ideal
ACK FOUND > 1; len(fronts)=1
    45 |     8055 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1010519548 |         ideal
ACK FOUND > 1; len(fronts)=1
    46 |     8234 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2595548986 |         ideal
ACK FOUND > 1; len(fronts)=1
    47 |     8413 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0425700646 |         ideal
ACK FOUND > 1; len(fronts)=1
    48 |     8592 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1799910546 |         ideal
ACK FOUND > 1; len(fronts)=1
    49 |     8771 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1859410654 |         ideal
ACK FOUND > 1; len(fronts)=1
    50 |     8950 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1721733034 |         ideal
ACK FOUND > 1; len(fronts)=1
    51 |     9129 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0663251150 |         ideal
ACK FOUND > 1; len(fronts)=1
    52 |     9308 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0363611903 |         ideal
ACK FOUND > 1; len(fronts)=1
    53 |     9487 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0365761936 |         ideal
ACK FOUND > 1; len(fronts)=1
    54 |     9666 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0875318324 |         ideal
ACK FOUND > 1; len(fronts)=1
    55 |     9845 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0556542201 |         ideal
ACK FOUND > 1; len(fronts)=1
    56 |    10024 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0622590245 |         ideal
ACK FOUND > 1; len(fronts)=1
    57 |    10203 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1121876735 |         ideal
ACK FOUND > 1; len(fronts)=1
    58 |    10382 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0788615834 |         ideal
ACK FOUND > 1; len(fronts)=1
    59 |    10561 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0870305094 |         ideal
ACK FOUND > 1; len(fronts)=1
    60 |    10740 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0302643850 |         ideal
ACK FOUND > 1; len(fronts)=1
    61 |    10919 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1515408554 |         ideal
ACK FOUND > 1; len(fronts)=1
    62 |    11098 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0096452182 |         ideal
ACK FOUND > 1; len(fronts)=1
    63 |    11277 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0869161009 |         ideal
ACK FOUND > 1; len(fronts)=1
    64 |    11456 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0727899829 |         ideal
ACK FOUND > 1; len(fronts)=1
    65 |    11635 |     29 |  0.000000E+00 |  0.000000E+00 |  0.2810609875 |         ideal
ACK FOUND > 1; len(fronts)=1
    66 |    11814 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1202295880 |         ideal
ACK FOUND > 1; len(fronts)=1
    67 |    11993 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2461683817 |         ideal
ACK FOUND > 1; len(fronts)=1
    68 |    12172 |     32 |  0.000000E+00 |  0.000000E+00 |  0.1282380466 |         ideal
ACK FOUND > 1; len(fronts)=1
    69 |    12351 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1151252877 |         ideal
ACK FOUND > 1; len(fronts)=1
    70 |    12530 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0920576686 |         ideal
ACK FOUND > 1; len(fronts)=1
    71 |    12709 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1364536494 |         ideal
ACK FOUND > 1; len(fronts)=1
    72 |    12888 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0272119137 |         ideal
ACK FOUND > 1; len(fronts)=1
    73 |    13067 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1064207412 |         ideal
ACK FOUND > 1; len(fronts)=1
    74 |    13246 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1061362675 |         ideal
ACK FOUND > 1; len(fronts)=1
    75 |    13425 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2998768281 |         ideal
ACK FOUND > 1; len(fronts)=1
    76 |    13604 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1921872905 |         ideal
ACK FOUND > 1; len(fronts)=1
    77 |    13783 |     26 |  0.000000E+00 |  0.000000E+00 |  0.2551175537 |         ideal
ACK FOUND > 1; len(fronts)=1
    78 |    13962 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0453000136 |         ideal
ACK FOUND > 1; len(fronts)=1
    79 |    14141 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1689356013 |         ideal
ACK FOUND > 1; len(fronts)=1
    80 |    14320 |     13 |  0.000000E+00 |  0.000000E+00 |  0.8182614317 |         ideal
ACK FOUND > 1; len(fronts)=1
    81 |    14499 |     20 |  0.000000E+00 |  0.000000E+00 |  0.4106690083 |         ideal
ACK FOUND > 1; len(fronts)=1
    82 |    14678 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1682476814 |         ideal
ACK FOUND > 1; len(fronts)=1
    83 |    14857 |     25 |  0.000000E+00 |  0.000000E+00 |  0.2722268793 |         ideal
ACK FOUND > 1; len(fronts)=1
    84 |    15036 |     23 |  0.000000E+00 |  0.000000E+00 |  0.2128694655 |         ideal
ACK FOUND > 1; len(fronts)=1
    85 |    15215 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1797926344 |         ideal
ACK FOUND > 1; len(fronts)=1
    86 |    15394 |     27 |  0.000000E+00 |  0.000000E+00 |  0.6420458523 |         ideal
ACK FOUND > 1; len(fronts)=1
    87 |    15573 |     29 |  0.000000E+00 |  0.000000E+00 |  0.3910036077 |         ideal
ACK FOUND > 1; len(fronts)=1
    88 |    15752 |     21 |  0.000000E+00 |  0.000000E+00 |  0.3451581549 |         ideal
ACK FOUND > 1; len(fronts)=1
    89 |    15931 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0684542680 |         ideal
ACK FOUND > 1; len(fronts)=1
    90 |    16110 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0506244118 |         ideal
ACK FOUND > 1; len(fronts)=1
    91 |    16289 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1786572218 |         ideal
ACK FOUND > 1; len(fronts)=1
    92 |    16468 |     29 |  0.000000E+00 |  0.000000E+00 |  0.2191258851 |         ideal
ACK FOUND > 1; len(fronts)=1
    93 |    16647 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0555663179 |         ideal
ACK FOUND > 1; len(fronts)=1
    94 |    16826 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1239004854 |         ideal
ACK FOUND > 1; len(fronts)=1
    95 |    17005 |     31 |  0.000000E+00 |  0.000000E+00 |  0.1003751513 |         ideal
ACK FOUND > 1; len(fronts)=1
    96 |    17184 |     23 |  0.000000E+00 |  0.000000E+00 |  0.4285767101 |         ideal
ACK FOUND > 1; len(fronts)=1
    97 |    17363 |     24 |  0.000000E+00 |  0.000000E+00 |  0.2960241608 |         ideal
ACK FOUND > 1; len(fronts)=1
    98 |    17542 |     13 |  0.000000E+00 |  0.000000E+00 |  1.8958044783 |         ideal
ACK FOUND > 1; len(fronts)=1
    99 |    17721 |     25 |  0.000000E+00 |  0.000000E+00 |  0.3606125270 |         ideal
ACK FOUND > 1; len(fronts)=1
   100 |    17900 |     32 |  0.000000E+00 |  0.000000E+00 |  0.2179543395 |         ideal
ACK FOUND > 1; len(fronts)=1
   101 |    18079 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0581763416 |         ideal
ACK FOUND > 1; len(fronts)=1
   102 |    18258 |     30 |  0.000000E+00 |  0.000000E+00 |  0.1915382546 |         ideal
ACK FOUND > 1; len(fronts)=1
   103 |    18437 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1512737105 |         ideal
ACK FOUND > 1; len(fronts)=1
   104 |    18616 |     29 |  0.000000E+00 |  0.000000E+00 |  0.3054804207 |         ideal
ACK FOUND > 1; len(fronts)=1
   105 |    18795 |     27 |  0.000000E+00 |  0.000000E+00 |  0.2127998576 |         ideal
ACK FOUND > 1; len(fronts)=1
   106 |    18974 |     21 |  0.000000E+00 |  0.000000E+00 |  0.3399634079 |         ideal
ACK FOUND > 1; len(fronts)=1
   107 |    19153 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0664647055 |         ideal
ACK FOUND > 1; len(fronts)=1
   108 |    19332 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0711967784 |         ideal
ACK FOUND > 1; len(fronts)=1
   109 |    19511 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0571624980 |         ideal
ACK FOUND > 1; len(fronts)=1
   110 |    19690 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0858418734 |         ideal
ACK FOUND > 1; len(fronts)=1
   111 |    19869 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0796210281 |         ideal
ACK FOUND > 1; len(fronts)=1
   112 |    20048 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0189737905 |         ideal
ACK FOUND > 1; len(fronts)=1
   113 |    20227 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1173300754 |         ideal
ACK FOUND > 1; len(fronts)=1
   114 |    20406 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1387030976 |         ideal
ACK FOUND > 1; len(fronts)=1
   115 |    20585 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2275106031 |         nadir
ACK FOUND > 1; len(fronts)=1
   116 |    20764 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0347012991 |         ideal
ACK FOUND > 1; len(fronts)=1
   117 |    20943 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0359487680 |         ideal
ACK FOUND > 1; len(fronts)=1
   118 |    21122 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1030663730 |         ideal
ACK FOUND > 1; len(fronts)=1
   119 |    21301 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1415210951 |         ideal
ACK FOUND > 1; len(fronts)=1
   120 |    21480 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1280571145 |         ideal
ACK FOUND > 1; len(fronts)=1
   121 |    21659 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1149096988 |         ideal
ACK FOUND > 1; len(fronts)=1
   122 |    21838 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1030663730 |         ideal
ACK FOUND > 1; len(fronts)=1
   123 |    22017 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1816979865 |         ideal
ACK FOUND > 1; len(fronts)=1
   124 |    22196 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1594007271 |         ideal
ACK FOUND > 1; len(fronts)=1
   125 |    22375 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0549055644 |         ideal
ACK FOUND > 1; len(fronts)=1
   126 |    22554 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1126287042 |         ideal
ACK FOUND > 1; len(fronts)=1
   127 |    22733 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1084685731 |             f
ACK FOUND > 1; len(fronts)=1
   128 |    22912 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0543649089 |         ideal
ACK FOUND > 1; len(fronts)=1
   129 |    23091 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0737592603 |         ideal
ACK FOUND > 1; len(fronts)=1
   130 |    23270 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1186897343 |         ideal
ACK FOUND > 1; len(fronts)=1
   131 |    23449 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0457075342 |         ideal
ACK FOUND > 1; len(fronts)=1
   132 |    23628 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0775073202 |         ideal
ACK FOUND > 1; len(fronts)=1
   133 |    23807 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0478967778 |         ideal
ACK FOUND > 1; len(fronts)=1
   134 |    23986 |     29 |  0.000000E+00 |  0.000000E+00 |  0.2193499658 |         ideal
ACK FOUND > 1; len(fronts)=1
   135 |    24165 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0586780816 |         ideal
ACK FOUND > 1; len(fronts)=1
   136 |    24344 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0408079641 |         ideal
ACK FOUND > 1; len(fronts)=1
   137 |    24523 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0611542449 |         ideal
ACK FOUND > 1; len(fronts)=1
   138 |    24702 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0327158952 |         ideal
ACK FOUND > 1; len(fronts)=1
   139 |    24881 |     26 |  0.000000E+00 |  0.000000E+00 |  0.2649198641 |         ideal
ACK FOUND > 1; len(fronts)=1
   140 |    25060 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0519701063 |         ideal
ACK FOUND > 1; len(fronts)=1
   141 |    25239 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0288325341 |         ideal
ACK FOUND > 1; len(fronts)=1
   142 |    25418 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0390403695 |         ideal
ACK FOUND > 1; len(fronts)=1
   143 |    25597 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0166802910 |         ideal
ACK FOUND > 1; len(fronts)=1
   144 |    25776 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0120612210 |         ideal
ACK FOUND > 1; len(fronts)=1
   145 |    25955 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0183955114 |         ideal
ACK FOUND > 1; len(fronts)=1
   146 |    26134 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0147461323 |         ideal
ACK FOUND > 1; len(fronts)=1
   147 |    26313 |     30 |  0.000000E+00 |  0.000000E+00 |  0.1954697409 |         ideal
ACK FOUND > 1; len(fronts)=1
   148 |    26492 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0522332877 |         ideal
ACK FOUND > 1; len(fronts)=1
   149 |    26671 |     34 |  0.000000E+00 |  0.000000E+00 |  0.1251083053 |         ideal
ACK FOUND > 1; len(fronts)=1
   150 |    26850 |     34 |  0.000000E+00 |  0.000000E+00 |  0.3318858223 |         nadir
ACK FOUND > 1; len(fronts)=1
   151 |    27029 |     31 |  0.000000E+00 |  0.000000E+00 |  0.1075886525 |         ideal
ACK FOUND > 1; len(fronts)=1
   152 |    27208 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0956525291 |         ideal
ACK FOUND > 1; len(fronts)=1
   153 |    27387 |     37 |  0.000000E+00 |  0.000000E+00 |  0.0866495512 |         ideal
ACK FOUND > 1; len(fronts)=1
   154 |    27566 |     37 |  0.000000E+00 |  0.000000E+00 |  0.0053551373 |         ideal
ACK FOUND > 1; len(fronts)=1
   155 |    27745 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0266355540 |         ideal
ACK FOUND > 1; len(fronts)=1
   156 |    27924 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0189535569 |         ideal
ACK FOUND > 1; len(fronts)=1
   157 |    28103 |     28 |  0.000000E+00 |  0.000000E+00 |  0.0468093872 |         ideal
ACK FOUND > 1; len(fronts)=1
   158 |    28282 |     35 |  0.000000E+00 |  0.000000E+00 |  0.0234502102 |         ideal
ACK FOUND > 1; len(fronts)=1
   159 |    28461 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0403909186 |         ideal
ACK FOUND > 1; len(fronts)=1
   160 |    28640 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0545606097 |         ideal
ACK FOUND > 1; len(fronts)=1
   161 |    28819 |     29 |  0.000000E+00 |  0.000000E+00 |  0.0363948834 |         ideal
ACK FOUND > 1; len(fronts)=1
   162 |    28998 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0813144036 |         ideal
ACK FOUND > 1; len(fronts)=1
   163 |    29177 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0885116779 |         ideal
ACK FOUND > 1; len(fronts)=1
   164 |    29356 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0813144036 |         ideal
ACK FOUND > 1; len(fronts)=1
   165 |    29535 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0512924826 |         ideal
ACK FOUND > 1; len(fronts)=1
   166 |    29714 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0325720513 |         ideal
ACK FOUND > 1; len(fronts)=1
   167 |    29893 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0176154640 |         ideal
ACK FOUND > 1; len(fronts)=1
   168 |    30072 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0032845276 |         ideal
ACK FOUND > 1; len(fronts)=1
   169 |    30251 |     31 |  0.000000E+00 |  0.000000E+00 |  0.0935703656 |         ideal
ACK FOUND > 1; len(fronts)=1
   170 |    30430 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0855641014 |         ideal
ACK FOUND > 1; len(fronts)=1
   171 |    30609 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0935703656 |         ideal
ACK FOUND > 1; len(fronts)=1
   172 |    30788 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0226519041 |         ideal
ACK FOUND > 1; len(fronts)=1
   173 |    30967 |     36 |  0.000000E+00 |  0.000000E+00 |  0.0873874331 |         ideal
ACK FOUND > 1; len(fronts)=1
   174 |    31146 |     35 |  0.000000E+00 |  0.000000E+00 |  0.0245449247 |         ideal
ACK FOUND > 1; len(fronts)=1
   175 |    31325 |     41 |  0.000000E+00 |  0.000000E+00 |  0.1105772828 |         ideal
ACK FOUND > 1; len(fronts)=1
   176 |    31504 |     40 |  0.000000E+00 |  0.000000E+00 |  0.0304830733 |         ideal
ACK FOUND > 1; len(fronts)=1
   177 |    31683 |     42 |  0.000000E+00 |  0.000000E+00 |  0.0137028876 |         ideal
ACK FOUND > 1; len(fronts)=1
   178 |    31862 |     44 |  0.000000E+00 |  0.000000E+00 |  0.0958811448 |         ideal
ACK FOUND > 1; len(fronts)=1
   179 |    32041 |     44 |  0.000000E+00 |  0.000000E+00 |  0.0357294104 |             f
ACK FOUND > 1; len(fronts)=1
   180 |    32220 |     34 |  0.000000E+00 |  0.000000E+00 |  0.1072576285 |         ideal
ACK FOUND > 1; len(fronts)=1
   181 |    32399 |     33 |  0.000000E+00 |  0.000000E+00 |  0.1027179444 |         ideal
ACK FOUND > 1; len(fronts)=1
   182 |    32578 |     36 |  0.000000E+00 |  0.000000E+00 |  0.1479725442 |         ideal
ACK FOUND > 1; len(fronts)=1
   183 |    32757 |     31 |  0.000000E+00 |  0.000000E+00 |  0.1012485632 |         ideal
ACK FOUND > 1; len(fronts)=1
   184 |    32936 |     35 |  0.000000E+00 |  0.000000E+00 |  0.2089878690 |         ideal
ACK FOUND > 1; len(fronts)=1
   185 |    33115 |     34 |  0.000000E+00 |  0.000000E+00 |  0.2548027354 |         ideal
ACK FOUND > 1; len(fronts)=1
   186 |    33294 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0862316546 |         ideal
ACK FOUND > 1; len(fronts)=1
   187 |    33473 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0058708881 |         ideal
ACK FOUND > 1; len(fronts)=1
   188 |    33652 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0173562701 |             f
ACK FOUND > 1; len(fronts)=1
   189 |    33831 |     31 |  0.000000E+00 |  0.000000E+00 |  0.2156076452 |         ideal
ACK FOUND > 1; len(fronts)=1
   190 |    34010 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0257673851 |         ideal
ACK FOUND > 1; len(fronts)=1
   191 |    34189 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0471510158 |         ideal
ACK FOUND > 1; len(fronts)=1
   192 |    34368 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0152152789 |         ideal
ACK FOUND > 1; len(fronts)=1
   193 |    34547 |     36 |  0.000000E+00 |  0.000000E+00 |  0.0049169774 |         ideal
ACK FOUND > 1; len(fronts)=1
   194 |    34726 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0273255082 |         ideal
ACK FOUND > 1; len(fronts)=1
   195 |    34905 |     34 |  0.000000E+00 |  0.000000E+00 |  0.0068956402 |         ideal
ACK FOUND > 1; len(fronts)=1
   196 |    35084 |     32 |  0.000000E+00 |  0.000000E+00 |  0.0280931683 |         ideal
ACK FOUND > 1; len(fronts)=1
   197 |    35263 |     35 |  0.000000E+00 |  0.000000E+00 |  0.0273255082 |         ideal
ACK FOUND > 1; len(fronts)=1
   198 |    35442 |     38 |  0.000000E+00 |  0.000000E+00 |  0.0568803006 |         ideal
ACK FOUND > 1; len(fronts)=1
   199 |    35621 |     33 |  0.000000E+00 |  0.000000E+00 |  0.0601763255 |         ideal
ACK FOUND > 1; len(fronts)=1
   200 |    35800 |     37 |  0.000000E+00 |  0.000000E+00 |  0.0576323938 |             f
Begin print with Final Cash: 12319966.6470943763852 => return: 0.2319966647094
"""

# Extract arrays
ack_array, n_nds_array, eps_array, indicator_array = extract_arrays(text_data)

print("front_num_Array =", ack_array)
print("n_nds_Array =", n_nds_array)
print("eps_Array =", eps_array)
print("indicator_Array =", indicator_array)
