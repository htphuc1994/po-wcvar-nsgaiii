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
     1 |      179 |      6 |  0.000000E+00 |  2.904208E+02 |             - |             -
ACK FOUND > 1; len(fronts)=2
     2 |      358 |      8 |  0.000000E+00 |  0.000000E+00 |  0.5455658055 |         ideal
ACK FOUND > 1; len(fronts)=2
     3 |      537 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3578745760 |         ideal
ACK FOUND > 1; len(fronts)=1
     4 |      716 |     17 |  0.000000E+00 |  0.000000E+00 |  0.3346737894 |         ideal
ACK FOUND > 1; len(fronts)=1
     5 |      895 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2822291471 |         ideal
ACK FOUND > 1; len(fronts)=1
     6 |     1074 |      2 |  0.000000E+00 |  0.000000E+00 |  7.3784715601 |         ideal
ACK FOUND > 1; len(fronts)=1
     7 |     1253 |      4 |  0.000000E+00 |  0.000000E+00 |  1.6168770436 |         ideal
ACK FOUND > 1; len(fronts)=1
     8 |     1432 |      6 |  0.000000E+00 |  0.000000E+00 |  0.6995101097 |         ideal
ACK FOUND > 1; len(fronts)=1
     9 |     1611 |      7 |  0.000000E+00 |  0.000000E+00 |  0.1035878035 |         ideal
ACK FOUND > 1; len(fronts)=1
    10 |     1790 |      3 |  0.000000E+00 |  0.000000E+00 |  2.3037590671 |         ideal
ACK FOUND > 1; len(fronts)=1
    11 |     1969 |      3 |  0.000000E+00 |  0.000000E+00 |  0.7328417530 |         ideal
ACK FOUND > 1; len(fronts)=1
    12 |     2148 |     11 |  0.000000E+00 |  0.000000E+00 |  0.4898850401 |         ideal
ACK FOUND > 1; len(fronts)=1
    13 |     2327 |      9 |  0.000000E+00 |  0.000000E+00 |  0.3382907461 |         ideal
ACK FOUND > 1; len(fronts)=1
    14 |     2506 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2247560151 |         ideal
ACK FOUND > 1; len(fronts)=1
    15 |     2685 |      6 |  0.000000E+00 |  0.000000E+00 |  0.3468213847 |         ideal
ACK FOUND > 1; len(fronts)=1
    16 |     2864 |      9 |  0.000000E+00 |  0.000000E+00 |  0.2248206601 |         ideal
ACK FOUND > 1; len(fronts)=1
    17 |     3043 |     12 |  0.000000E+00 |  0.000000E+00 |  0.4148999733 |         ideal
ACK FOUND > 1; len(fronts)=1
    18 |     3222 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2019077003 |         ideal
ACK FOUND > 1; len(fronts)=1
    19 |     3401 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2529879067 |         ideal
ACK FOUND > 1; len(fronts)=1
    20 |     3580 |     21 |  0.000000E+00 |  0.000000E+00 |  0.2019077003 |         ideal
ACK FOUND > 1; len(fronts)=1
    21 |     3759 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1565483303 |         ideal
ACK FOUND > 1; len(fronts)=1
    22 |     3938 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1512571500 |         ideal
ACK FOUND > 1; len(fronts)=1
    23 |     4117 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1800282169 |         ideal
ACK FOUND > 1; len(fronts)=1
    24 |     4296 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2261836257 |         ideal
ACK FOUND > 1; len(fronts)=1
    25 |     4475 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2162531062 |         ideal
ACK FOUND > 1; len(fronts)=1
    26 |     4654 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2178165995 |         ideal
ACK FOUND > 1; len(fronts)=1
    27 |     4833 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1604513828 |         ideal
ACK FOUND > 1; len(fronts)=1
    28 |     5012 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0406208722 |         ideal
ACK FOUND > 1; len(fronts)=1
    29 |     5191 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1076427725 |         ideal
ACK FOUND > 1; len(fronts)=1
    30 |     5370 |      8 |  0.000000E+00 |  0.000000E+00 |  0.4126593673 |         ideal
ACK FOUND > 1; len(fronts)=1
    31 |     5549 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2617987630 |         ideal
ACK FOUND > 1; len(fronts)=1
    32 |     5728 |     13 |  0.000000E+00 |  0.000000E+00 |  0.5478182696 |         ideal
ACK FOUND > 1; len(fronts)=1
    33 |     5907 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1354260322 |         ideal
ACK FOUND > 1; len(fronts)=1
    34 |     6086 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1768990344 |         ideal
ACK FOUND > 1; len(fronts)=1
    35 |     6265 |     10 |  0.000000E+00 |  0.000000E+00 |  2.0831661030 |         ideal
ACK FOUND > 1; len(fronts)=1
    36 |     6444 |     15 |  0.000000E+00 |  0.000000E+00 |  0.5778577051 |         ideal
ACK FOUND > 1; len(fronts)=1
    37 |     6623 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2401464386 |         ideal
ACK FOUND > 1; len(fronts)=1
    38 |     6802 |      7 |  0.000000E+00 |  0.000000E+00 |  0.8072529882 |         ideal
ACK FOUND > 1; len(fronts)=1
    39 |     6981 |      8 |  0.000000E+00 |  0.000000E+00 |  0.8977028497 |         nadir
ACK FOUND > 1; len(fronts)=1
    40 |     7160 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2475664157 |         ideal
ACK FOUND > 1; len(fronts)=1
    41 |     7339 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0298313664 |         ideal
ACK FOUND > 1; len(fronts)=1
    42 |     7518 |     14 |  0.000000E+00 |  0.000000E+00 |  0.4820703802 |         ideal
ACK FOUND > 1; len(fronts)=1
    43 |     7697 |     15 |  0.000000E+00 |  0.000000E+00 |  0.2155101449 |         ideal
ACK FOUND > 1; len(fronts)=1
    44 |     7876 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0930051892 |         ideal
ACK FOUND > 1; len(fronts)=1
    45 |     8055 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1484008120 |         ideal
ACK FOUND > 1; len(fronts)=1
    46 |     8234 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1255122205 |         ideal
ACK FOUND > 1; len(fronts)=1
    47 |     8413 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0573003040 |         ideal
ACK FOUND > 1; len(fronts)=1
    48 |     8592 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1681238418 |         ideal
ACK FOUND > 1; len(fronts)=1
    49 |     8771 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0699739304 |         ideal
ACK FOUND > 1; len(fronts)=1
    50 |     8950 |     24 |  0.000000E+00 |  0.000000E+00 |  0.2046904476 |         ideal
ACK FOUND > 1; len(fronts)=1
    51 |     9129 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0673131370 |         ideal
ACK FOUND > 1; len(fronts)=1
    52 |     9308 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1350812373 |         ideal
ACK FOUND > 1; len(fronts)=1
    53 |     9487 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2012641050 |         ideal
ACK FOUND > 1; len(fronts)=1
    54 |     9666 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2005606002 |         ideal
ACK FOUND > 1; len(fronts)=1
    55 |     9845 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2508765521 |         ideal
ACK FOUND > 1; len(fronts)=1
    56 |    10024 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0507326860 |         ideal
ACK FOUND > 1; len(fronts)=1
    57 |    10203 |     15 |  0.000000E+00 |  0.000000E+00 |  0.3054860313 |         ideal
ACK FOUND > 1; len(fronts)=1
    58 |    10382 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0797901576 |         ideal
ACK FOUND > 1; len(fronts)=1
    59 |    10561 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1384765957 |         ideal
ACK FOUND > 1; len(fronts)=1
    60 |    10740 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0391096314 |         ideal
ACK FOUND > 1; len(fronts)=1
    61 |    10919 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0763980580 |         ideal
ACK FOUND > 1; len(fronts)=1
    62 |    11098 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0906044291 |         ideal
ACK FOUND > 1; len(fronts)=1
    63 |    11277 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0639136144 |         ideal
ACK FOUND > 1; len(fronts)=1
    64 |    11456 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1570584122 |         ideal
ACK FOUND > 1; len(fronts)=1
    65 |    11635 |     30 |  0.000000E+00 |  0.000000E+00 |  0.1374172137 |         ideal
ACK FOUND > 1; len(fronts)=1
    66 |    11814 |     18 |  0.000000E+00 |  0.000000E+00 |  0.1482889623 |         ideal
ACK FOUND > 1; len(fronts)=1
    67 |    11993 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0927583956 |         ideal
ACK FOUND > 1; len(fronts)=1
    68 |    12172 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1831817533 |         ideal
ACK FOUND > 1; len(fronts)=1
    69 |    12351 |      3 |  0.000000E+00 |  0.000000E+00 |  3.9814508341 |         ideal
ACK FOUND > 1; len(fronts)=1
    70 |    12530 |      6 |  0.000000E+00 |  0.000000E+00 |  0.4751314254 |         ideal
ACK FOUND > 1; len(fronts)=1
    71 |    12709 |      5 |  0.000000E+00 |  0.000000E+00 |  0.5117198267 |         ideal
ACK FOUND > 1; len(fronts)=1
    72 |    12888 |      3 |  0.000000E+00 |  0.000000E+00 |  0.8354044312 |         ideal
ACK FOUND > 1; len(fronts)=1
    73 |    13067 |      5 |  0.000000E+00 |  0.000000E+00 |  0.3863837388 |         ideal
ACK FOUND > 1; len(fronts)=1
    74 |    13246 |      5 |  0.000000E+00 |  0.000000E+00 |  0.2833845787 |         ideal
ACK FOUND > 1; len(fronts)=1
    75 |    13425 |      7 |  0.000000E+00 |  0.000000E+00 |  0.1696184254 |         ideal
ACK FOUND > 1; len(fronts)=1
    76 |    13604 |      4 |  0.000000E+00 |  0.000000E+00 |  0.6210539848 |         ideal
ACK FOUND > 1; len(fronts)=1
    77 |    13783 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2320493901 |         ideal
ACK FOUND > 1; len(fronts)=1
    78 |    13962 |     10 |  0.000000E+00 |  0.000000E+00 |  0.7414136793 |         ideal
ACK FOUND > 1; len(fronts)=1
    79 |    14141 |      9 |  0.000000E+00 |  0.000000E+00 |  0.2726406320 |         ideal
ACK FOUND > 1; len(fronts)=1
    80 |    14320 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1081803872 |         ideal
ACK FOUND > 1; len(fronts)=1
    81 |    14499 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1857125583 |         ideal
ACK FOUND > 1; len(fronts)=1
    82 |    14678 |     12 |  0.000000E+00 |  0.000000E+00 |  0.3551689423 |         ideal
ACK FOUND > 1; len(fronts)=1
    83 |    14857 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0827292242 |         ideal
ACK FOUND > 1; len(fronts)=1
    84 |    15036 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0158278585 |         ideal
ACK FOUND > 1; len(fronts)=1
    85 |    15215 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0460469905 |         ideal
ACK FOUND > 1; len(fronts)=1
    86 |    15394 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0628171822 |         ideal
ACK FOUND > 1; len(fronts)=1
    87 |    15573 |     11 |  0.000000E+00 |  0.000000E+00 |  0.0221294527 |         ideal
ACK FOUND > 1; len(fronts)=1
    88 |    15752 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2221032427 |         ideal
ACK FOUND > 1; len(fronts)=1
    89 |    15931 |      9 |  0.000000E+00 |  0.000000E+00 |  0.1496552160 |         ideal
ACK FOUND > 1; len(fronts)=1
    90 |    16110 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2996382822 |         ideal
ACK FOUND > 1; len(fronts)=1
    91 |    16289 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3217219329 |         ideal
ACK FOUND > 1; len(fronts)=1
    92 |    16468 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0568786198 |         ideal
ACK FOUND > 1; len(fronts)=1
    93 |    16647 |     12 |  0.000000E+00 |  0.000000E+00 |  0.3518709158 |         ideal
ACK FOUND > 1; len(fronts)=1
    94 |    16826 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1401606389 |         ideal
ACK FOUND > 1; len(fronts)=1
    95 |    17005 |     15 |  0.000000E+00 |  0.000000E+00 |  0.1884738137 |         ideal
ACK FOUND > 1; len(fronts)=1
    96 |    17184 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2155559765 |         ideal
ACK FOUND > 1; len(fronts)=1
    97 |    17363 |     23 |  0.000000E+00 |  0.000000E+00 |  0.3249446817 |         ideal
ACK FOUND > 1; len(fronts)=1
    98 |    17542 |     17 |  0.000000E+00 |  0.000000E+00 |  0.0740819416 |         ideal
ACK FOUND > 1; len(fronts)=1
    99 |    17721 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1706935276 |         ideal
ACK FOUND > 1; len(fronts)=1
   100 |    17900 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1228577103 |         ideal
ACK FOUND > 1; len(fronts)=1
   101 |    18079 |     26 |  0.000000E+00 |  0.000000E+00 |  0.2273959190 |         ideal
ACK FOUND > 1; len(fronts)=1
   102 |    18258 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0547526202 |         nadir
ACK FOUND > 1; len(fronts)=1
   103 |    18437 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0768544616 |         ideal
ACK FOUND > 1; len(fronts)=1
   104 |    18616 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0803003192 |         ideal
ACK FOUND > 1; len(fronts)=1
   105 |    18795 |     36 |  0.000000E+00 |  0.000000E+00 |  0.0701419123 |         ideal
ACK FOUND > 1; len(fronts)=1
   106 |    18974 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0388881397 |         ideal
ACK FOUND > 1; len(fronts)=1
   107 |    19153 |     35 |  0.000000E+00 |  0.000000E+00 |  0.0415451850 |         ideal
ACK FOUND > 1; len(fronts)=1
   108 |    19332 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0617191495 |         ideal
ACK FOUND > 1; len(fronts)=1
   109 |    19511 |     18 |  0.000000E+00 |  0.000000E+00 |  0.2822224955 |         ideal
ACK FOUND > 1; len(fronts)=1
   110 |    19690 |     16 |  0.000000E+00 |  0.000000E+00 |  0.3201624079 |         ideal
ACK FOUND > 1; len(fronts)=1
   111 |    19869 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0573105702 |         ideal
ACK FOUND > 1; len(fronts)=1
   112 |    20048 |     16 |  0.000000E+00 |  0.000000E+00 |  0.3508564250 |         ideal
ACK FOUND > 1; len(fronts)=1
   113 |    20227 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0965200696 |         ideal
ACK FOUND > 1; len(fronts)=1
   114 |    20406 |      6 |  0.000000E+00 |  0.000000E+00 |  0.3281285689 |         ideal
ACK FOUND > 1; len(fronts)=1
   115 |    20585 |      9 |  0.000000E+00 |  0.000000E+00 |  0.5065289148 |         ideal
ACK FOUND > 1; len(fronts)=1
   116 |    20764 |      8 |  0.000000E+00 |  0.000000E+00 |  0.2821565108 |         ideal
ACK FOUND > 1; len(fronts)=1
   117 |    20943 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3529883476 |         ideal
ACK FOUND > 1; len(fronts)=1
   118 |    21122 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3067936338 |         ideal
ACK FOUND > 1; len(fronts)=1
   119 |    21301 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0932403140 |         ideal
ACK FOUND > 1; len(fronts)=1
   120 |    21480 |     14 |  0.000000E+00 |  0.000000E+00 |  0.1062539063 |         ideal
ACK FOUND > 1; len(fronts)=1
   121 |    21659 |     16 |  0.000000E+00 |  0.000000E+00 |  0.1298271242 |         ideal
ACK FOUND > 1; len(fronts)=1
   122 |    21838 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2122903784 |         ideal
ACK FOUND > 1; len(fronts)=1
   123 |    22017 |     12 |  0.000000E+00 |  0.000000E+00 |  0.2625512534 |         ideal
ACK FOUND > 1; len(fronts)=1
   124 |    22196 |     13 |  0.000000E+00 |  0.000000E+00 |  0.3008233717 |         ideal
ACK FOUND > 1; len(fronts)=1
   125 |    22375 |     14 |  0.000000E+00 |  0.000000E+00 |  0.2697488645 |         ideal
ACK FOUND > 1; len(fronts)=1
   126 |    22554 |     15 |  0.000000E+00 |  0.000000E+00 |  0.0772741001 |         ideal
ACK FOUND > 1; len(fronts)=1
   127 |    22733 |     12 |  0.000000E+00 |  0.000000E+00 |  0.3398180398 |         ideal
ACK FOUND > 1; len(fronts)=1
   128 |    22912 |     16 |  0.000000E+00 |  0.000000E+00 |  0.0357554940 |         ideal
ACK FOUND > 1; len(fronts)=1
   129 |    23091 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0940440999 |         ideal
ACK FOUND > 1; len(fronts)=1
   130 |    23270 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0958153019 |         ideal
ACK FOUND > 1; len(fronts)=1
   131 |    23449 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1424292522 |         ideal
ACK FOUND > 1; len(fronts)=1
   132 |    23628 |     17 |  0.000000E+00 |  0.000000E+00 |  0.2194766218 |         ideal
ACK FOUND > 1; len(fronts)=1
   133 |    23807 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1558674271 |         ideal
ACK FOUND > 1; len(fronts)=1
   134 |    23986 |     24 |  0.000000E+00 |  0.000000E+00 |  0.0412267639 |         ideal
ACK FOUND > 1; len(fronts)=1
   135 |    24165 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0590751347 |         ideal
ACK FOUND > 1; len(fronts)=1
   136 |    24344 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0567879549 |         ideal
ACK FOUND > 1; len(fronts)=1
   137 |    24523 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0026595031 |         ideal
ACK FOUND > 1; len(fronts)=1
   138 |    24702 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1357419374 |         ideal
ACK FOUND > 1; len(fronts)=1
   139 |    24881 |     22 |  0.000000E+00 |  0.000000E+00 |  0.2293963834 |         ideal
ACK FOUND > 1; len(fronts)=1
   140 |    25060 |     29 |  0.000000E+00 |  0.000000E+00 |  0.2384037459 |         ideal
ACK FOUND > 1; len(fronts)=1
   141 |    25239 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1357882109 |         ideal
ACK FOUND > 1; len(fronts)=1
   142 |    25418 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1730415693 |         ideal
ACK FOUND > 1; len(fronts)=1
   143 |    25597 |     18 |  0.000000E+00 |  0.000000E+00 |  0.0921036302 |         ideal
ACK FOUND > 1; len(fronts)=1
   144 |    25776 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0885494820 |         ideal
ACK FOUND > 1; len(fronts)=1
   145 |    25955 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1450003066 |         ideal
ACK FOUND > 1; len(fronts)=1
   146 |    26134 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1144416667 |         ideal
ACK FOUND > 1; len(fronts)=1
   147 |    26313 |     20 |  0.000000E+00 |  0.000000E+00 |  0.1365652491 |         ideal
ACK FOUND > 1; len(fronts)=1
   148 |    26492 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1439601852 |         ideal
ACK FOUND > 1; len(fronts)=1
   149 |    26671 |      5 |  0.000000E+00 |  0.000000E+00 |  1.1373186952 |         ideal
ACK FOUND > 1; len(fronts)=1
   150 |    26850 |      4 |  0.000000E+00 |  0.000000E+00 |  0.2183078706 |         ideal
ACK FOUND > 1; len(fronts)=1
   151 |    27029 |      7 |  0.000000E+00 |  0.000000E+00 |  0.5547820966 |         ideal
ACK FOUND > 1; len(fronts)=1
   152 |    27208 |      8 |  0.000000E+00 |  0.000000E+00 |  0.0315457889 |         ideal
ACK FOUND > 1; len(fronts)=1
   153 |    27387 |      8 |  0.000000E+00 |  0.000000E+00 |  0.3236290831 |         ideal
ACK FOUND > 1; len(fronts)=1
   154 |    27566 |     10 |  0.000000E+00 |  0.000000E+00 |  0.2082588863 |         ideal
ACK FOUND > 1; len(fronts)=1
   155 |    27745 |     10 |  0.000000E+00 |  0.000000E+00 |  0.3217700613 |         ideal
ACK FOUND > 1; len(fronts)=1
   156 |    27924 |     13 |  0.000000E+00 |  0.000000E+00 |  0.1908430858 |         ideal
ACK FOUND > 1; len(fronts)=1
   157 |    28103 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0883562419 |         ideal
ACK FOUND > 1; len(fronts)=1
   158 |    28282 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1483091843 |         ideal
ACK FOUND > 1; len(fronts)=1
   159 |    28461 |     11 |  0.000000E+00 |  0.000000E+00 |  0.2539153669 |         ideal
ACK FOUND > 1; len(fronts)=1
   160 |    28640 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1374122437 |         ideal
ACK FOUND > 1; len(fronts)=1
   161 |    28819 |      4 |  0.000000E+00 |  0.000000E+00 |  1.9884292367 |         ideal
ACK FOUND > 1; len(fronts)=1
   162 |    28998 |     24 |  0.000000E+00 |  0.000000E+00 |  0.4192601985 |         ideal
ACK FOUND > 1; len(fronts)=1
   163 |    29177 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2955590548 |         ideal
ACK FOUND > 1; len(fronts)=1
   164 |    29356 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0830655980 |         ideal
ACK FOUND > 1; len(fronts)=1
   165 |    29535 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0905905568 |         ideal
ACK FOUND > 1; len(fronts)=1
   166 |    29714 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0678813879 |         ideal
ACK FOUND > 1; len(fronts)=1
   167 |    29893 |      9 |  0.000000E+00 |  0.000000E+00 |  0.7151582851 |         ideal
ACK FOUND > 1; len(fronts)=1
   168 |    30072 |     13 |  0.000000E+00 |  0.000000E+00 |  0.2993506485 |         ideal
ACK FOUND > 1; len(fronts)=1
   169 |    30251 |     14 |  0.000000E+00 |  0.000000E+00 |  0.0875920181 |         ideal
ACK FOUND > 1; len(fronts)=1
   170 |    30430 |      8 |  0.000000E+00 |  0.000000E+00 |  0.8485735642 |         ideal
ACK FOUND > 1; len(fronts)=1
   171 |    30609 |     18 |  0.000000E+00 |  0.000000E+00 |  0.5767336263 |         ideal
ACK FOUND > 1; len(fronts)=1
   172 |    30788 |     12 |  0.000000E+00 |  0.000000E+00 |  0.1226737723 |         ideal
ACK FOUND > 1; len(fronts)=1
   173 |    30967 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0223909250 |         ideal
ACK FOUND > 1; len(fronts)=1
   174 |    31146 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0249956815 |         ideal
ACK FOUND > 1; len(fronts)=1
   175 |    31325 |     12 |  0.000000E+00 |  0.000000E+00 |  0.0921189615 |         ideal
ACK FOUND > 1; len(fronts)=1
   176 |    31504 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0571105545 |         ideal
ACK FOUND > 1; len(fronts)=1
   177 |    31683 |     13 |  0.000000E+00 |  0.000000E+00 |  0.0974555509 |         ideal
ACK FOUND > 1; len(fronts)=1
   178 |    31862 |     17 |  0.000000E+00 |  0.000000E+00 |  0.1197873715 |         ideal
ACK FOUND > 1; len(fronts)=1
   179 |    32041 |     20 |  0.000000E+00 |  0.000000E+00 |  0.0638250878 |         ideal
ACK FOUND > 1; len(fronts)=1
   180 |    32220 |     19 |  0.000000E+00 |  0.000000E+00 |  0.0970282540 |         ideal
ACK FOUND > 1; len(fronts)=1
   181 |    32399 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1074543632 |         ideal
ACK FOUND > 1; len(fronts)=1
   182 |    32578 |     25 |  0.000000E+00 |  0.000000E+00 |  0.0556830372 |         ideal
ACK FOUND > 1; len(fronts)=1
   183 |    32757 |     29 |  0.000000E+00 |  0.000000E+00 |  0.1494513007 |         ideal
ACK FOUND > 1; len(fronts)=1
   184 |    32936 |     25 |  0.000000E+00 |  0.000000E+00 |  0.1180937175 |         ideal
ACK FOUND > 1; len(fronts)=1
   185 |    33115 |     30 |  0.000000E+00 |  0.000000E+00 |  0.0335951237 |         ideal
ACK FOUND > 1; len(fronts)=1
   186 |    33294 |     23 |  0.000000E+00 |  0.000000E+00 |  0.1835818342 |         ideal
ACK FOUND > 1; len(fronts)=1
   187 |    33473 |     23 |  0.000000E+00 |  0.000000E+00 |  0.0539642101 |         ideal
ACK FOUND > 1; len(fronts)=1
   188 |    33652 |     26 |  0.000000E+00 |  0.000000E+00 |  0.1435345647 |         ideal
ACK FOUND > 1; len(fronts)=1
   189 |    33831 |     27 |  0.000000E+00 |  0.000000E+00 |  0.1303683136 |         ideal
ACK FOUND > 1; len(fronts)=1
   190 |    34010 |     21 |  0.000000E+00 |  0.000000E+00 |  0.0859337328 |         ideal
ACK FOUND > 1; len(fronts)=1
   191 |    34189 |     26 |  0.000000E+00 |  0.000000E+00 |  0.8368183001 |         nadir
ACK FOUND > 1; len(fronts)=1
   192 |    34368 |     22 |  0.000000E+00 |  0.000000E+00 |  0.1878807833 |         ideal
ACK FOUND > 1; len(fronts)=1
   193 |    34547 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1743074652 |         ideal
ACK FOUND > 1; len(fronts)=1
   194 |    34726 |     21 |  0.000000E+00 |  0.000000E+00 |  0.1685085239 |         ideal
ACK FOUND > 1; len(fronts)=1
   195 |    34905 |     26 |  0.000000E+00 |  0.000000E+00 |  0.0320617477 |         ideal
ACK FOUND > 1; len(fronts)=1
   196 |    35084 |     27 |  0.000000E+00 |  0.000000E+00 |  0.0202102720 |         ideal
ACK FOUND > 1; len(fronts)=1
   197 |    35263 |     19 |  0.000000E+00 |  0.000000E+00 |  0.2434437965 |         ideal
ACK FOUND > 1; len(fronts)=1
   198 |    35442 |     19 |  0.000000E+00 |  0.000000E+00 |  0.1726129650 |         ideal
ACK FOUND > 1; len(fronts)=1
   199 |    35621 |     22 |  0.000000E+00 |  0.000000E+00 |  0.0894512569 |         ideal
ACK FOUND > 1; len(fronts)=1
   200 |    35800 |     24 |  0.000000E+00 |  0.000000E+00 |  0.1196011493 |         ideal
"""

# Extract arrays
ack_array, n_nds_array, eps_array, indicator_array = extract_arrays(text_data)

print("front_num_Array =", ack_array)
print("n_nds_Array =", n_nds_array)
print("eps_Array =", eps_array)
print("indicator_Array =", indicator_array)
