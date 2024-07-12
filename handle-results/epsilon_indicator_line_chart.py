import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# experiment 19
n_gen = list(range(1, 201))
front_num_Array = [26, 11, 7, 7, 5, 5, 5, 5, 4, 4, 4, 3, 3, 2, 2, 2, 3, 3, 4, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
n_nds_Array = [8, 6, 12, 16, 14, 16, 14, 15, 20, 20, 17, 25, 23, 25, 31, 25, 19, 18, 13, 11, 13, 12, 8, 7, 10, 8, 6, 12, 13, 10, 13, 14, 16, 10, 17, 13, 21, 20, 23, 27, 21, 35, 30, 23, 24, 32, 25, 30, 32, 33, 29, 24, 25, 16, 20, 21, 23, 17, 23, 24, 23, 27, 35, 34, 30, 18, 21, 21, 32, 28, 29, 49, 47, 45, 38, 42, 26, 35, 42, 40, 38, 37, 43, 58, 63, 56, 61, 51, 57, 59, 56, 54, 55, 56, 37, 54, 60, 50, 54, 49, 30, 37, 49, 55, 54, 57, 52, 55, 55, 56, 50, 51, 52, 55, 53, 64, 64, 63, 59, 63, 58, 49, 51, 62, 68, 67, 61, 62, 63, 68, 70, 60, 66, 70, 71, 67, 68, 72, 72, 58, 64, 68, 61, 60, 61, 60, 63, 62, 67, 69, 60, 50, 43, 63, 62, 62, 62, 56, 55, 57, 60, 58, 52, 57, 53, 53, 54, 60, 67, 66, 69, 70, 72, 72, 70, 62, 65, 62, 58, 59, 57, 62, 56, 66, 64, 67, 60, 62, 63, 67, 68, 68, 68, 68, 68, 69, 70, 68, 65, 65]
eps = [None, 0.2196678015, 0.1038036579, 0.0726244745, 0.084995645, 0.1904194786, 0.2714498339, 0.0132890392, 0.0208817308, 0.00796083, 0.0268406328, 0.0904253274, 0.0375106564, 0.0351504823, 0.2442511719, 0.0700461026, 0.0789707792, 0.0721536568, 0.0061676367, 0.1843706325, 0.3576670106, 0.0896840841, 0.1654627832, 0.0870525071, 0.0844012636, 0.1128875193, 0.1397156325, 0.1476604566, 0.0209164012, 0.0944492185, 0.164844682, 0.108995372, 0.0193384369, 0.1882400744, 0.0047089068, 0.0075375856, 0.0369338932, 0.0307847391, 0.0426488429, 0.052559604, 0.0911423635, 0.0236517892, 0.0251602739, 0.0894798167, 0.0175217366, 0.0182786183, 0.0054346238, 0.0210274078, 0.0874126886, 0.0373929148, 0.1032847369, 0.1021936346, 0.0280730938, 0.0064290184, 0.0588477162, 0.0138895257, 0.0550221411, 0.0891456578, 0.0578150372, 0.0606849458, 0.0596789657, 0.0221489836, 0.0915884082, 0.0153878838, 0.026870508, 0.2364495345, 0.0257756054, 0.0390880174, 0.0889996471, 0.0127842898, 0.0089937063, 0.0241374149, 0.0240613759, 0.0151057305, 0.0395347553, 0.0447545563, 0.0686529159, 0.0129273334, 0.0190254666, 0.0056199419, 0.0528887781, 0.087415911, 0.0042080859, 0.0134700799, 0.0087520503, 0.026609271, 0.0724008466, 0.0218914058, 0.0263579634, 0.0353932587, 0.034864127, 0.0163628203, 0.021321141, 0.0274447908, 0.0680313666, 0.0134166681, 0.0717022336, 0.0069087386, 0.0399265115, 0.0386018281, 0.0504546351, 0.0590648294, 0.0216849215, 0.0142551138, 0.0500341419, 0.0601868692, 0.0640413155, 0.0038639336, 0.0606427961, 0.0228090488, 0.0882706687, 0.0371640587, 0.0192289115, 0.0071727474, 0.0166282658, 0.0280734189, 0.027306823, 0.0310968992, 0.0492951295, 0.0301590464, 0.0072604779, 0.0809896821, 0.0301590464, 0.0468613442, 0.0371209953, 0.0140138432, 0.0238942176, 0.0102515495, 0.0068764979, 0.0070275803, 0.0054596221, 0.0063598912, 0.0243635118, 0.0089039725, 0.0109641528, 0.016545976, 0.012420507, 0.0815598216, 0.041350054, 0.0354187446, 0.0138946191, 0.1032223788, 0.0624684358, 0.0177869754, 0.0181156922, 0.0081413385, 0.0177870888, 0.0186564654, 0.0129504861, 0.0134946009, 0.059592303, 0.077888741, 0.0237353027, 0.0642082778, 0.0362682099, 0.0499474386, 0.0198983911, 0.0553178921, 0.0167665182, 0.0153161597, 0.024105691, 0.0255348301, 0.0269125639, 0.0418859892, 0.0071198285, 0.0070694949, 0.0402020851, 0.0354767035, 0.0130334794, 0.0413181479, 0.0391593641, 0.0108602899, 0.0119367928, 0.0204910816, 0.0328738622, 0.0158895645, 0.0110427668, 0.0386338095, 0.0369026686, 0.0273623743, 0.042750875, 0.0410301859, 0.0303784383, 0.0034580272, 0.021583872, 0.0120346392, 0.007972356, 0.008816883, 0.0114860906, 0.0068062744, 0.0094771139, 0.012417291, 0.0050207281, 0.0183175548, 0.0091585786, 0.0027115555, 0.0095338271, 0.017527776, 0.0070785215, 0.0051548538]
indicators = ['-', 'ideal', 'nadir', 'f', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'nadir', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'f', 'ideal', 'ideal', 'f', 'f', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'f', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'f', 'nadir', 'ideal', 'ideal', 'nadir', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'nadir', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'nadir', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'f', 'f', 'f', 'ideal', 'f', 'f', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'f', 'nadir', 'nadir', 'nadir', 'ideal', 'f', 'f', 'f', 'ideal', 'f', 'ideal', 'f', 'ideal', 'f', 'ideal']
#
# # # experiment 10
front_num_Array = [7, 5, 6, 5, 5, 4, 4, 5, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
n_nds_Array = [4, 3, 5, 8, 8, 10, 7, 8, 15, 4, 6, 11, 9, 12, 13, 15, 17, 18, 13, 18, 21, 16, 24, 24, 26, 21, 23, 25, 26, 28, 31, 31, 22, 28, 26, 25, 29, 37, 36, 40, 32, 39, 35, 22, 31, 32, 30, 34, 33, 36, 34, 38, 43, 38, 37, 37, 38, 36, 38, 34, 35, 39, 38, 38, 37, 37, 38, 41, 40, 43, 40, 41, 43, 42, 47, 47, 41, 42, 45, 47, 41, 46, 40, 44, 46, 43, 48, 48, 51, 44, 50, 46, 47, 53, 48, 50, 50, 53, 47, 42, 48, 45, 49, 51, 44, 49, 50, 52, 50, 52, 55, 51, 54, 55, 54, 48, 53, 52, 56, 54, 53, 52, 56, 48, 49, 54, 53, 53, 44, 37, 36, 36, 32, 25, 24, 23, 27, 32, 23, 25, 28, 25, 25, 28, 28, 34, 39, 17, 15, 33, 27, 25, 25, 27, 23, 32, 34, 22, 23, 20, 27, 32, 36, 30, 32, 41, 43, 31, 36, 37, 35, 30, 43, 38, 32, 34, 37, 38, 37, 37, 41, 34, 35, 37, 44, 37, 41, 44, 42, 42, 40, 42, 44, 41, 40, 41, 37, 38, 48, 40]
eps = [None, 0.9728862383, 0.8009415383, 0.3462299919, 0.2835503038, 0.2595124692, 0.0357370929, 0.333082249, 0.2696080889, 0.5461929729, 0.8068807488, 0.1893450343, 0.1971704188, 0.3014202879, 0.3272402218, 0.0486134541, 0.1088958197, 0.2385182504, 0.0449481833, 0.063985951, 0.0372656997, 0.1204948848, 0.1696714408, 0.0626205787, 0.1379274718, 0.1158372271, 0.0710381793, 0.2357055022, 0.1011091898, 0.0575919966, 0.2806764813, 0.1028833396, 0.0657243258, 0.4085373245, 0.1057682157, 0.147911529, 0.095816368, 0.0224429333, 0.0522450029, 0.027488255, 0.2056461321, 0.0471914308, 0.0106004232, 0.2153636865, 0.2748630685, 0.0551523385, 0.0473989975, 0.07362268, 0.0835475153, 0.0230287288, 0.0210748202, 0.0158356589, 0.0234915502, 0.0685539995, 0.0051341745, 0.0150201674, 0.0089704066, 0.0128963034, 0.017539878, 0.0181728068, 0.0266121761, 0.0860946773, 0.0727988463, 0.0694903134, 0.0109900238, 0.0057030321, 0.0687022982, 0.016103801, 0.0136932869, 0.0093554349, 0.0526165862, 0.0048294236, 0.0449014033, 0.0062100397, 0.045332226, 0.0243012492, 0.0573502313, 0.2563341998, 0.0348436133, 0.1926811959, 0.0079791004, 0.0345488389, 0.0401598581, 0.0102618347, 0.0103682318, 0.0102618347, 0.0498913513, 0.0475204899, 0.0498913513, 0.0475204899, 0.1708809943, 0.0170084576, 0.0297793727, 0.012522154, 0.004647452, 0.0048117655, 0.1408866362, 0.0050583546, 0.0279725615, 0.0350391391, 0.1194411339, 0.0148573243, 0.0180970641, 0.0401606118, 0.0379056885, 0.02452697, 0.009425357, 0.0090284304, 0.0078854076, 0.0078237144, 0.0145095011, 0.049923477, 0.0055995304, 0.0249385051, 0.0083763892, 0.0329195837, 0.026025765, 0.0157731279, 0.0321635447, 0.0048905446, 0.0152334698, 0.0195402796, 0.0104628451, 0.0032876598, 0.2715366222, 0.0085692846, 0.0027827927, 0.0084159847, 0.4237572253, 0.1005077812, 0.1707388002, 0.0435081523, 0.0272007962, 0.1979692062, 0.0582616259, 0.0514161013, 0.0961156268, 0.1690249231, 0.1589942687, 0.084658184, 0.0629719719, 0.0534024677, 0.0388553782, 0.0134313586, 0.0069167925, 0.0400360022, 0.0206540265, 0.0455737901, 0.1564320206, 0.1536370682, 0.0270290612, 0.1330433611, 0.0391538045, 0.0570786763, 0.0324037342, 0.0405980206, 0.0487034621, 0.0625438812, 0.1021213554, 0.0564279507, 0.1445122957, 0.0985875811, 0.1132426072, 0.0889781414, 0.0604508841, 0.0580556819, 0.0322113351, 0.0260260691, 0.0359253241, 0.0257653836, 0.0179578065, 0.0586565134, 0.0289209661, 0.0034200306, 0.0529194233, 0.0606734729, 0.0383404426, 0.0461812456, 0.0354503803, 0.0045405451, 0.0310917477, 0.0435816736, 0.0250918357, 0.0317478603, 0.0462105283, 0.0508953677, 0.072949137, 0.0543674876, 0.031852455, 0.0520029518, 0.058488819, 0.0487183742, 0.1101500824, 0.121436706, 0.1294108255, 0.0494218253, 0.0551387839, 0.0590576427, 0.0545095828, 0.0472905091]
indicators = ['-', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'f', 'ideal', 'nadir', 'ideal', 'nadir', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal']

# # experiment 13
front_num_Array = [4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
n_nds_Array = [5, 1, 7, 2, 6, 7, 1, 1, 1, 1, 1, 1, 2, 4, 4, 8, 1, 2, 2, 4, 5, 6, 6, 12, 5, 6, 7, 6, 7, 8, 10, 13, 14, 14, 13, 12, 14, 3, 3, 3, 6, 5, 7, 9, 13, 11, 12, 10, 14, 9, 5, 7, 16, 9, 10, 13, 1, 2, 1, 4, 2, 2, 2, 3, 6, 3, 6, 5, 11, 13, 21, 17, 17, 20, 15, 16, 15, 21, 6, 13, 13, 16, 17, 16, 18, 6, 5, 9, 9, 10, 12, 12, 12, 7, 7, 14, 10, 14, 11, 16, 17, 23, 21, 28, 32, 13, 7, 7, 9, 12, 12, 14, 9, 14, 13, 18, 16, 12, 11, 12, 11, 17, 13, 12, 11, 9, 9, 9, 6, 7, 1, 2, 2, 2, 3, 2, 4, 3, 2, 6, 6, 7, 1, 2, 3, 5, 3, 4, 6, 9, 10, 10, 10, 10, 4, 6, 10, 9, 6, 9, 7, 7, 10, 8, 11, 9, 9, 9, 10, 8, 8, 9, 9, 10, 10, 11, 11, 8, 12, 11, 13, 13, 11, 14, 17, 18, 18, 13, 13, 12, 14, 16, 13, 10, 14, 16, 18, 15, 15, 15]
eps = [None, 0.0263224292, 1.0, 6.4714613636, 0.9201862775, 0.4728547552, 0.0782786451, 0.0458252155, 0.0135105656, 0.0, 0.0, 0.0, 1.0, 1.0, 0.8588677043, 0.5514058463, 0.0247752828, 1.0, 0.0, 0.8998081875, 0.5616643859, 0.1192045348, 0.3785977568, 0.2758520378, 0.2605737177, 0.1816222354, 0.2838784128, 0.4357062949, 0.4553078342, 0.0759573895, 0.5866771653, 0.3391413967, 0.271753199, 0.1451453902, 0.1424068388, 0.4629213007, 0.2985565253, 2.6720252422, 1.0484453461, 0.3436217414, 0.5665302285, 0.7306383768, 0.3466660189, 0.3732003774, 0.3331292975, 0.1650220258, 0.4597193438, 0.4797894212, 0.2325012117, 0.1611529991, 0.2575627674, 0.3541380457, 0.3553902949, 0.4483277254, 0.1187540324, 0.3745284602, 0.0282134126, 1.0, 0.0125791012, 0.9614540436, 3.633569034, 1.0, 0.0, 0.9669813214, 0.416120273, 1.4257651961, 0.6646123593, 1.3085888596, 0.3997584226, 0.3245271052, 0.2039481321, 0.1015626814, 0.1189325732, 0.1077936371, 0.1104711319, 0.102707072, 0.0810258458, 0.2547537798, 0.4340596831, 0.9263278125, 0.2383056498, 0.1924449346, 0.0535472872, 0.8071942968, 0.0173264893, 0.5316309361, 0.5367215315, 0.3456699943, 0.1294029339, 0.147170121, 0.2726067855, 0.2756179058, 0.2305731345, 0.4602132963, 0.358986186, 0.851849547, 1.6843674379, 0.8377322237, 0.1897231529, 0.2435762337, 0.2482083121, 0.1472769282, 0.1521108166, 0.1210488174, 0.1529712097, 0.1345319862, 0.3906333852, 0.1267653441, 0.4183964983, 0.0780085717, 0.0147867978, 0.1486748306, 0.0544518312, 0.1190577377, 0.0399686734, 0.2000249634, 0.0694043061, 0.1596346297, 0.1616195734, 0.2711117853, 0.2363842976, 0.1536961339, 0.1886079705, 0.2749351839, 0.2089056385, 0.0672727731, 0.1830666808, 0.1679653559, 0.4914667646, 0.313721204, 0.0187651785, 1.0, 0.0, 0.0, 0.9981408917, 1.0, 0.9981408917, 0.8716510268, 1.0, 0.9997409928, 0.0, 0.3003335888, 0.0176257182, 1.0, 1.0, 0.7373221775, 3.7426700158, 0.8021134185, 0.256440813, 0.1660067968, 0.1549794743, 0.073995863, 0.1462798865, 0.1801431955, 0.6899194032, 0.667546066, 0.2949845527, 0.3297576385, 0.4523254512, 0.3677041178, 0.5145324074, 0.6217483783, 0.4141322231, 0.7068697742, 0.084178548, 0.186876596, 0.0770277355, 0.0, 0.3685527328, 0.0190787583, 0.2834727833, 0.3127727523, 0.0168164234, 0.1620134976, 0.156023295, 0.0997082833, 0.2673824651, 0.2824547378, 0.0107530116, 0.0273808301, 0.1125237649, 0.1527101554, 0.0363411041, 0.1125237649, 0.1076001907, 0.1427533876, 0.1665254613, 0.1907230907, 0.0784649408, 0.0711187645, 0.0876454843, 0.1491966144, 0.0429500832, 0.2619100114, 0.2697957703, 0.0904138377, 0.2537116354, 0.3456365759, 0.2133658885, 0.1831706669]
indicators = ['-', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'f', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal']



# Convert None to NaN for plotting purposes
eps = [float('nan') if v is None else v for v in eps]

# Create a color map for the indicators
color_map = {
    '-': 'gray',
    'ideal': 'b',
    'f': 'g',
    'nadir': 'r'
}

# Assign colors based on the indicators
colors = [color_map[indicator] for indicator in indicators]

# Plotting the line through all points
plt.figure(figsize=(21, 7))
plt.plot(n_gen, eps, linestyle='-', color='gray', label='Epsilon Indicator Line')

# Plotting the epsilon values over generations with corresponding colors
marker = 'o'
for i in range(len(n_gen)):
    if indicators[i] == 'ideal':
        marker = 'o'
    elif indicators[i] == 'f':
        marker = 'p'
    else:
        marker = 'h'
    plt.plot(n_gen[i], eps[i], marker=marker, color=colors[i])

# Custom legend
custom_lines = [
    Line2D([0], [0], color=color_map['-'], marker='o', linestyle='-', label='Epsilon Indicator', markersize=16),
    Line2D([0], [0], color=color_map['ideal'], marker='o', linestyle='None', label='ideal', markersize=16),
    Line2D([0], [0], color=color_map['f'], marker='p', linestyle='None', label='f', markersize=16),
    Line2D([0], [0], color=color_map['nadir'], marker='h', linestyle='None', label='nadir', markersize=16)]

plt.legend(handles=custom_lines, loc='best', fontsize=16)

# Adding labels and title
plt.xlabel('Generation (n_gen)', fontsize=16)
plt.ylabel('Epsilon Indicator (eps)', fontsize=16)
plt.title('Epsilon Indicator Over Generations', fontsize=16)
# plt.legend(fontsize=14)
plt.tick_params(axis='y', labelsize=16)
plt.tick_params(axis='x', labelsize=16)
plt.grid(True)


# Show plot
plt.show()
