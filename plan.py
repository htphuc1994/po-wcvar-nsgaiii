import numpy as np
import json
import random
import math
import functools

from pymoo.algorithms.moo.nsga3 import associate_to_niches, calc_niche_count, niching
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
from sklearn.preprocessing import minmax_scale
import time
import concurrent.futures
from assets_returns import *
from constants import TAIL_PROBABILITY_EPSILON

from stock_data_input_100 import STOCK_DATA_2023_INPUT_100_STOCKS
from wavelet_cvar_utils import compute_wavelet_variance, wavelet_decomposition, calculate_var_from_wavelet_variance, \
    calculate_cvar
from pymoo.util.misc import intersect, has_feasible

# SA
initialTemperature = 750.0
coolingRate = 0.95
saIterationLength = 10

objectivesHaveProportion = False
risksRelatedRatio = 0.5
returnRatio = 0.5

tau = 12
epsilon = 0.0015
initTheta = 1000000.0
alpha = 0.0045
xi = 100
cardinalityK = 20.0
POPULATION_SIZE = 100
MAX_GENERATION = 150
generationCheckedConsecutiveNumToConvergenceDecision = 79
upsilon = 0.06
stock_data = STOCK_DATA_2023_INPUT_100_STOCKS
stock_returns = np.column_stack((
    ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP, BPC, BST, BTS, BVS,
    CAN, CAP, CCM, CDC, CID, CII, CJC, CLC, CMC, COM, CTB, CTC, CTN, DAC, DAE, DBC, DC4, DCS, DHA,
    DHG, DHT, DIC, DMC, DPC, DPM, DPR, DQC, DRC, DST, DTC, DTT, DXP, DXV, EBS, FMC, FPT, GIL, GMC,
    GMD, GTA, HAG, HAP, HAS, HAX, HBC, HCC, HCT, HDC, HEV, HHC, HJS, HMC, HPG, HRC, HSG, HSI, HT1,
    HTP, HTV, HUT, ICF, IMP, ITA, KBC, KDC, KHP, KKC, KMR, KSH, L10, L18, L43, L61, L62, LAF, LBE,
    LBM, LCG, LGC, LSS, LTC))
# jsonInput2023 = '{"stocks":[{"symbol":"ACB","companyName":"Ngân hàng TMCP Á Châu","type":"VN30","year":2023,"prices":[{"month":1,"value":26.35,"matchedTradingVolume":5.499E7},{"month":2,"value":25.8,"matchedTradingVolume":6.3237E7},{"month":3,"value":25.35,"matchedTradingVolume":9.20633E7},{"month":4,"value":25.3,"matchedTradingVolume":8.14876E7},{"month":5,"value":25.4,"matchedTradingVolume":1.608784E8},{"month":6,"value":22.3,"matchedTradingVolume":1.920848E8},{"month":7,"value":22.95,"matchedTradingVolume":1.640575E8},{"month":8,"value":24.4,"matchedTradingVolume":2.570596E8},{"month":9,"value":22.95,"matchedTradingVolume":1.263825E8},{"month":10,"value":22.8,"matchedTradingVolume":1.01492E8},{"month":11,"value":23.3,"matchedTradingVolume":1.540952E8},{"month":12,"value":23.9,"matchedTradingVolume":1.309384E8}],"dividendSpitingHistories":[]},{"symbol":"BCM","companyName":"Tổng Công ty Đầu tư và Phát triển Công nghiệp – CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":85.2,"matchedTradingVolume":1681700.0},{"month":2,"value":86.0,"matchedTradingVolume":1668200.0},{"month":3,"value":84.5,"matchedTradingVolume":2201700.0},{"month":4,"value":83.5,"matchedTradingVolume":1124200.0},{"month":5,"value":78.5,"matchedTradingVolume":1003200.0},{"month":6,"value":82.1,"matchedTradingVolume":6718400.0},{"month":7,"value":81.0,"matchedTradingVolume":5792000.0},{"month":8,"value":79.0,"matchedTradingVolume":5927500.0},{"month":9,"value":72.6,"matchedTradingVolume":5679800.0},{"month":10,"value":69.5,"matchedTradingVolume":4024400.0},{"month":11,"value":62.4,"matchedTradingVolume":6680300.0},{"month":12,"value":66.0,"matchedTradingVolume":1.05481E7}],"dividendSpitingHistories":[{"month":11,"value":800.0}]},{"symbol":"BID","companyName":"Ngân hàng TMCP Đầu tư và Phát triển Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":45.95,"matchedTradingVolume":2.88095E7},{"month":2,"value":47.2,"matchedTradingVolume":2.70027E7},{"month":3,"value":48.0,"matchedTradingVolume":1.78979E7},{"month":4,"value":46.0,"matchedTradingVolume":1.53768E7},{"month":5,"value":45.1,"matchedTradingVolume":1.2405E7},{"month":6,"value":45.35,"matchedTradingVolume":2.61229E7},{"month":7,"value":47.35,"matchedTradingVolume":3.93465E7},{"month":8,"value":49.1,"matchedTradingVolume":4.26147E7},{"month":9,"value":47.5,"matchedTradingVolume":2.19276E7},{"month":10,"value":43.95,"matchedTradingVolume":2.0611E7},{"month":11,"value":44.15,"matchedTradingVolume":1.78062E7},{"month":12,"value":43.4,"matchedTradingVolume":2.24373E7}],"dividendSpitingHistories":[]},{"symbol":"BVH","companyName":"Tập đoàn Bảo Việt","type":"VN30","year":2023,"prices":[{"month":1,"value":51.0,"matchedTradingVolume":7621200.0},{"month":2,"value":51.2,"matchedTradingVolume":9028400.0},{"month":3,"value":50.0,"matchedTradingVolume":5479800.0},{"month":4,"value":49.2,"matchedTradingVolume":5394500.0},{"month":5,"value":46.0,"matchedTradingVolume":1.05267E7},{"month":6,"value":45.3,"matchedTradingVolume":2.13723E7},{"month":7,"value":48.15,"matchedTradingVolume":2.26194E7},{"month":8,"value":48.0,"matchedTradingVolume":1.95543E7},{"month":9,"value":45.8,"matchedTradingVolume":1.30652E7},{"month":10,"value":42.65,"matchedTradingVolume":6368600.0},{"month":11,"value":41.3,"matchedTradingVolume":6801500.0},{"month":12,"value":40.5,"matchedTradingVolume":6636100.0}],"dividendSpitingHistories":[{"month":11,"value":954.0}]},{"symbol":"CTG","companyName":"Ngân hàng TMCP Công Thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":31.1,"matchedTradingVolume":6.19356E7},{"month":2,"value":30.45,"matchedTradingVolume":5.62202E7},{"month":3,"value":29.5,"matchedTradingVolume":4.62949E7},{"month":4,"value":30.0,"matchedTradingVolume":4.04912E7},{"month":5,"value":28.4,"matchedTradingVolume":7.05504E7},{"month":6,"value":30.0,"matchedTradingVolume":1.20986E8},{"month":7,"value":30.3,"matchedTradingVolume":1.269248E8},{"month":8,"value":32.6,"matchedTradingVolume":1.849013E8},{"month":9,"value":33.2,"matchedTradingVolume":1.252328E8},{"month":10,"value":29.95,"matchedTradingVolume":6.47939E7},{"month":11,"value":30.25,"matchedTradingVolume":6.29258E7},{"month":12,"value":27.1,"matchedTradingVolume":7.30158E7}],"dividendSpitingHistories":[]},{"symbol":"FPT","companyName":"CTCP FPT","type":"VN30","year":2023,"prices":[{"month":1,"value":84.0,"matchedTradingVolume":1.49761E7},{"month":2,"value":82.8,"matchedTradingVolume":1.6827E7},{"month":3,"value":80.6,"matchedTradingVolume":1.51259E7},{"month":4,"value":80.9,"matchedTradingVolume":1.11001E7},{"month":5,"value":84.1,"matchedTradingVolume":1.65431E7},{"month":6,"value":87.3,"matchedTradingVolume":1.93342E7},{"month":7,"value":87.0,"matchedTradingVolume":2.72301E7},{"month":8,"value":96.7,"matchedTradingVolume":4.53975E7},{"month":9,"value":99.0,"matchedTradingVolume":5.49667E7},{"month":10,"value":97.0,"matchedTradingVolume":5.85186E7},{"month":11,"value":93.0,"matchedTradingVolume":4.69906E7},{"month":12,"value":97.2,"matchedTradingVolume":4.36497E7}],"dividendSpitingHistories":[{"month":8,"value":1000.0}]},{"symbol":"GAS","companyName":"Tổng Công ty Khí Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":108.2,"matchedTradingVolume":3892900.0},{"month":2,"value":109.0,"matchedTradingVolume":4822000.0},{"month":3,"value":108.1,"matchedTradingVolume":4192400.0},{"month":4,"value":102.5,"matchedTradingVolume":6178600.0},{"month":5,"value":94.9,"matchedTradingVolume":7790900.0},{"month":6,"value":96.6,"matchedTradingVolume":1.45087E7},{"month":7,"value":101.6,"matchedTradingVolume":1.42296E7},{"month":8,"value":103.2,"matchedTradingVolume":1.20026E7},{"month":9,"value":110.0,"matchedTradingVolume":1.18793E7},{"month":10,"value":89.3,"matchedTradingVolume":1.23912E7},{"month":11,"value":80.1,"matchedTradingVolume":1.12482E7},{"month":12,"value":79.8,"matchedTradingVolume":1.5394E7}],"dividendSpitingHistories":[{"month":8,"value":3600.0}]},{"symbol":"GVR","companyName":"Tập đoàn Công nghiệp Cao su Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":16.85,"matchedTradingVolume":4.1546E7},{"month":2,"value":15.6,"matchedTradingVolume":3.46376E7},{"month":3,"value":15.5,"matchedTradingVolume":4.22057E7},{"month":4,"value":16.35,"matchedTradingVolume":4.92206E7},{"month":5,"value":18.4,"matchedTradingVolume":7.46486E7},{"month":6,"value":19.6,"matchedTradingVolume":8.05328E7},{"month":7,"value":22.35,"matchedTradingVolume":6.63856E7},{"month":8,"value":22.7,"matchedTradingVolume":6.33971E7},{"month":9,"value":23.2,"matchedTradingVolume":7.73157E7},{"month":10,"value":21.45,"matchedTradingVolume":6.5337E7},{"month":11,"value":20.15,"matchedTradingVolume":4.46305E7},{"month":12,"value":21.2,"matchedTradingVolume":3.96708E7}],"dividendSpitingHistories":[{"month":11,"value":350.0}]},{"symbol":"HDB","companyName":"Ngân hàng TMCP Phát triển TP. HCM","type":"VN30","year":2023,"prices":[{"month":1,"value":18.65,"matchedTradingVolume":3.22759E7},{"month":2,"value":19.0,"matchedTradingVolume":4.4446E7},{"month":3,"value":19.25,"matchedTradingVolume":5.77437E7},{"month":4,"value":19.7,"matchedTradingVolume":4.51794E7},{"month":5,"value":19.6,"matchedTradingVolume":3.38232E7},{"month":6,"value":19.2,"matchedTradingVolume":5.41306E7},{"month":7,"value":18.9,"matchedTradingVolume":6.66127E7},{"month":8,"value":17.55,"matchedTradingVolume":6.28059E7},{"month":9,"value":18.0,"matchedTradingVolume":1.529976E8},{"month":10,"value":17.75,"matchedTradingVolume":1.780465E8},{"month":11,"value":18.95,"matchedTradingVolume":1.868925E8},{"month":12,"value":20.3,"matchedTradingVolume":1.556088E8}],"dividendSpitingHistories":[{"month":5,"value":1000.0}]},{"symbol":"HPG","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":22.1,"matchedTradingVolume":4.281135E8},{"month":2,"value":21.9,"matchedTradingVolume":4.94953E8},{"month":3,"value":21.3,"matchedTradingVolume":4.610696E8},{"month":4,"value":22.0,"matchedTradingVolume":3.30845E8},{"month":5,"value":22.35,"matchedTradingVolume":3.350429E8},{"month":6,"value":26.6,"matchedTradingVolume":5.626958E8},{"month":7,"value":28.4,"matchedTradingVolume":4.653832E8},{"month":8,"value":28.15,"matchedTradingVolume":6.43047E8},{"month":9,"value":29.0,"matchedTradingVolume":6.05131E8},{"month":10,"value":26.2,"matchedTradingVolume":4.011388E8},{"month":11,"value":27.2,"matchedTradingVolume":5.466178E8},{"month":12,"value":27.95,"matchedTradingVolume":5.610034E8}],"dividendSpitingHistories":[]},{"symbol":"MBB","companyName":"Ngân hàng TMCP Quân Đội","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":1.510583E8},{"month":2,"value":18.95,"matchedTradingVolume":1.687588E8},{"month":3,"value":18.3,"matchedTradingVolume":1.717558E8},{"month":4,"value":18.8,"matchedTradingVolume":1.492544E8},{"month":5,"value":18.85,"matchedTradingVolume":1.334826E8},{"month":6,"value":20.7,"matchedTradingVolume":2.836777E8},{"month":7,"value":21.2,"matchedTradingVolume":2.36432E8},{"month":8,"value":19.35,"matchedTradingVolume":2.173509E8},{"month":9,"value":19.4,"matchedTradingVolume":2.572516E8},{"month":10,"value":18.6,"matchedTradingVolume":1.466942E8},{"month":11,"value":18.55,"matchedTradingVolume":1.853708E8},{"month":12,"value":18.65,"matchedTradingVolume":1.511428E8}],"dividendSpitingHistories":[{"month":6,"value":500.0}]},{"symbol":"MSN","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":103.7,"matchedTradingVolume":8950100.0},{"month":2,"value":96.7,"matchedTradingVolume":1.24483E7},{"month":3,"value":84.7,"matchedTradingVolume":2.91468E7},{"month":4,"value":79.5,"matchedTradingVolume":2.07545E7},{"month":5,"value":74.4,"matchedTradingVolume":1.62996E7},{"month":6,"value":78.8,"matchedTradingVolume":3.0083E7},{"month":7,"value":87.3,"matchedTradingVolume":3.79388E7},{"month":8,"value":89.2,"matchedTradingVolume":5.02759E7},{"month":9,"value":82.7,"matchedTradingVolume":3.77362E7},{"month":10,"value":77.4,"matchedTradingVolume":4.0633E7},{"month":11,"value":66.0,"matchedTradingVolume":3.84334E7},{"month":12,"value":67.5,"matchedTradingVolume":5.12021E7}],"dividendSpitingHistories":[]},{"symbol":"MWG","companyName":"CTCP Đầu tư Thế giới Di động","type":"VN30","year":2023,"prices":[{"month":1,"value":46.5,"matchedTradingVolume":3.38651E7},{"month":2,"value":49.9,"matchedTradingVolume":4.56642E7},{"month":3,"value":40.8,"matchedTradingVolume":4.16636E7},{"month":4,"value":41.05,"matchedTradingVolume":5.23766E7},{"month":5,"value":39.4,"matchedTradingVolume":3.71724E7},{"month":6,"value":44.35,"matchedTradingVolume":8.65595E7},{"month":7,"value":54.5,"matchedTradingVolume":1.189389E8},{"month":8,"value":54.2,"matchedTradingVolume":1.698499E8},{"month":9,"value":57.5,"matchedTradingVolume":1.511657E8},{"month":10,"value":51.9,"matchedTradingVolume":1.695161E8},{"month":11,"value":41.9,"matchedTradingVolume":2.478952E8},{"month":12,"value":43.05,"matchedTradingVolume":1.675436E8}],"dividendSpitingHistories":[{"month":7,"value":500.0}]},{"symbol":"PLX","companyName":"Tập đoàn Xăng Dầu Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":38.1,"matchedTradingVolume":1.25733E7},{"month":2,"value":40.6,"matchedTradingVolume":1.61479E7},{"month":3,"value":39.0,"matchedTradingVolume":2.69045E7},{"month":4,"value":38.05,"matchedTradingVolume":1.50825E7},{"month":5,"value":38.05,"matchedTradingVolume":1.33605E7},{"month":6,"value":39.1,"matchedTradingVolume":1.56871E7},{"month":7,"value":41.8,"matchedTradingVolume":3.82708E7},{"month":8,"value":41.0,"matchedTradingVolume":3.29293E7},{"month":9,"value":40.4,"matchedTradingVolume":2.22712E7},{"month":10,"value":37.5,"matchedTradingVolume":2.2156E7},{"month":11,"value":35.8,"matchedTradingVolume":1.91929E7},{"month":12,"value":35.9,"matchedTradingVolume":1.31123E7}],"dividendSpitingHistories":[{"month":9,"value":700.0}]},{"symbol":"POW","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":12.4,"matchedTradingVolume":1.438163E8},{"month":2,"value":12.65,"matchedTradingVolume":1.506917E8},{"month":3,"value":13.5,"matchedTradingVolume":2.060467E8},{"month":4,"value":13.65,"matchedTradingVolume":1.477345E8},{"month":5,"value":13.65,"matchedTradingVolume":1.43022E8},{"month":6,"value":13.95,"matchedTradingVolume":1.552269E8},{"month":7,"value":13.7,"matchedTradingVolume":1.968232E8},{"month":8,"value":14.1,"matchedTradingVolume":2.620184E8},{"month":9,"value":13.0,"matchedTradingVolume":1.309333E8},{"month":10,"value":11.75,"matchedTradingVolume":1.067952E8},{"month":11,"value":11.9,"matchedTradingVolume":1.264731E8},{"month":12,"value":11.65,"matchedTradingVolume":8.40602E7}],"dividendSpitingHistories":[]},{"symbol":"SAB","companyName":"Tổng Công ty cổ phần Bia - Rượu - Nước giải khát Sài Gòn","type":"VN30","year":2023,"prices":[{"month":1,"value":193.1,"matchedTradingVolume":2013100.0},{"month":2,"value":197.2,"matchedTradingVolume":1559600.0},{"month":3,"value":192.5,"matchedTradingVolume":3412700.0},{"month":4,"value":181.0,"matchedTradingVolume":3651800.0},{"month":5,"value":166.6,"matchedTradingVolume":2221900.0},{"month":6,"value":162.0,"matchedTradingVolume":3096200.0},{"month":7,"value":161.6,"matchedTradingVolume":3568900.0},{"month":8,"value":161.6,"matchedTradingVolume":6019000.0},{"month":9,"value":168.9,"matchedTradingVolume":9361900.0},{"month":10,"value":73.0,"matchedTradingVolume":9713900.0},{"month":11,"value":66.2,"matchedTradingVolume":1.61096E7},{"month":12,"value":65.6,"matchedTradingVolume":1.22324E7}],"dividendSpitingHistories":[{"month":3,"value":1000.0},{"month":6,"value":1500.0}]},{"symbol":"SHB","companyName":"Ngân hàng TMCP Sài Gòn - Hà Nội","type":"VN30","year":2023,"prices":[{"month":1,"value":11.2,"matchedTradingVolume":2.939803E8},{"month":2,"value":10.6,"matchedTradingVolume":2.209531E8},{"month":3,"value":10.85,"matchedTradingVolume":3.662555E8},{"month":4,"value":12.2,"matchedTradingVolume":6.056328E8},{"month":5,"value":12.0,"matchedTradingVolume":4.061201E8},{"month":6,"value":12.85,"matchedTradingVolume":6.039741E8},{"month":7,"value":14.4,"matchedTradingVolume":4.546979E8},{"month":8,"value":13.45,"matchedTradingVolume":4.740001E8},{"month":9,"value":12.75,"matchedTradingVolume":4.439107E8},{"month":10,"value":11.05,"matchedTradingVolume":2.494628E8},{"month":11,"value":11.6,"matchedTradingVolume":3.637048E8},{"month":12,"value":11.15,"matchedTradingVolume":3.281995E8}],"dividendSpitingHistories":[]},{"symbol":"SSI","companyName":"CTCP Chứng khoán SSI","type":"VN30","year":2023,"prices":[{"month":1,"value":21.6,"matchedTradingVolume":2.43128E8},{"month":2,"value":20.75,"matchedTradingVolume":2.701936E8},{"month":3,"value":21.5,"matchedTradingVolume":3.972755E8},{"month":4,"value":22.6,"matchedTradingVolume":4.024856E8},{"month":5,"value":23.4,"matchedTradingVolume":3.739481E8},{"month":6,"value":26.6,"matchedTradingVolume":4.523384E8},{"month":7,"value":29.75,"matchedTradingVolume":3.768438E8},{"month":8,"value":33.5,"matchedTradingVolume":6.115069E8},{"month":9,"value":36.45,"matchedTradingVolume":5.979921E8},{"month":10,"value":34.0,"matchedTradingVolume":5.601314E8},{"month":11,"value":32.9,"matchedTradingVolume":5.212175E8},{"month":12,"value":33.6,"matchedTradingVolume":3.923282E8}],"dividendSpitingHistories":[{"month":6,"value":1000.0}]},{"symbol":"STB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":27.1,"matchedTradingVolume":2.330793E8},{"month":2,"value":26.15,"matchedTradingVolume":3.772336E8},{"month":3,"value":26.5,"matchedTradingVolume":4.59574E8},{"month":4,"value":26.9,"matchedTradingVolume":3.08058E8},{"month":5,"value":28.15,"matchedTradingVolume":3.174901E8},{"month":6,"value":30.3,"matchedTradingVolume":3.506546E8},{"month":7,"value":30.0,"matchedTradingVolume":4.686863E8},{"month":8,"value":32.9,"matchedTradingVolume":6.076624E8},{"month":9,"value":33.3,"matchedTradingVolume":4.282722E8},{"month":10,"value":31.75,"matchedTradingVolume":3.745102E8},{"month":11,"value":30.2,"matchedTradingVolume":3.661731E8},{"month":12,"value":28.55,"matchedTradingVolume":3.171983E8}],"dividendSpitingHistories":[]},{"symbol":"TCB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":29.4,"matchedTradingVolume":6.18252E7},{"month":2,"value":28.6,"matchedTradingVolume":6.10217E7},{"month":3,"value":28.35,"matchedTradingVolume":6.78293E7},{"month":4,"value":30.7,"matchedTradingVolume":9.0173E7},{"month":5,"value":30.5,"matchedTradingVolume":6.91356E7},{"month":6,"value":33.3,"matchedTradingVolume":1.050967E8},{"month":7,"value":34.3,"matchedTradingVolume":1.146862E8},{"month":8,"value":35.3,"matchedTradingVolume":1.43969E8},{"month":9,"value":35.75,"matchedTradingVolume":1.089254E8},{"month":10,"value":33.15,"matchedTradingVolume":7.11959E7},{"month":11,"value":31.8,"matchedTradingVolume":7.9431E7},{"month":12,"value":31.8,"matchedTradingVolume":5.98825E7}],"dividendSpitingHistories":[]},{"symbol":"TPB","companyName":"Ngân hàng TMCP Tiên Phong","type":"VN30","year":2023,"prices":[{"month":1,"value":25.0,"matchedTradingVolume":1.168169E8},{"month":2,"value":24.8,"matchedTradingVolume":1.293128E8},{"month":3,"value":25.3,"matchedTradingVolume":9.12826E7},{"month":4,"value":23.8,"matchedTradingVolume":8.51845E7},{"month":5,"value":25.0,"matchedTradingVolume":6.7704E7},{"month":6,"value":26.3,"matchedTradingVolume":1.226153E8},{"month":7,"value":19.0,"matchedTradingVolume":1.497795E8},{"month":8,"value":19.6,"matchedTradingVolume":1.981773E8},{"month":9,"value":19.75,"matchedTradingVolume":1.483994E8},{"month":10,"value":17.5,"matchedTradingVolume":9.66153E7},{"month":11,"value":17.7,"matchedTradingVolume":1.206297E8},{"month":12,"value":17.55,"matchedTradingVolume":1.051146E8}],"dividendSpitingHistories":[{"month":3,"value":2500.0}]},{"symbol":"VCB","companyName":"Ngân hàng TMCP Ngoại thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":93.0,"matchedTradingVolume":1.95707E7},{"month":2,"value":96.0,"matchedTradingVolume":1.77834E7},{"month":3,"value":93.2,"matchedTradingVolume":2.03676E7},{"month":4,"value":92.8,"matchedTradingVolume":1.05433E7},{"month":5,"value":95.0,"matchedTradingVolume":1.21852E7},{"month":6,"value":105.0,"matchedTradingVolume":1.97517E7},{"month":7,"value":106.5,"matchedTradingVolume":2.00989E7},{"month":8,"value":91.5,"matchedTradingVolume":3.03631E7},{"month":9,"value":90.2,"matchedTradingVolume":2.82153E7},{"month":10,"value":86.8,"matchedTradingVolume":1.90875E7},{"month":11,"value":89.5,"matchedTradingVolume":2.49941E7},{"month":12,"value":86.0,"matchedTradingVolume":2.70841E7}],"dividendSpitingHistories":[]},{"symbol":"VHM","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":53.3,"matchedTradingVolume":2.15012E7},{"month":2,"value":48.1,"matchedTradingVolume":5.98349E7},{"month":3,"value":51.5,"matchedTradingVolume":5.67558E7},{"month":4,"value":52.6,"matchedTradingVolume":3.09891E7},{"month":5,"value":55.5,"matchedTradingVolume":3.01862E7},{"month":6,"value":57.0,"matchedTradingVolume":3.66415E7},{"month":7,"value":63.0,"matchedTradingVolume":5.51829E7},{"month":8,"value":63.0,"matchedTradingVolume":1.229843E8},{"month":9,"value":55.9,"matchedTradingVolume":1.448709E8},{"month":10,"value":48.0,"matchedTradingVolume":1.006912E8},{"month":11,"value":42.9,"matchedTradingVolume":1.672199E8},{"month":12,"value":43.7,"matchedTradingVolume":1.506395E8}],"dividendSpitingHistories":[]},{"symbol":"VIB","companyName":"Ngân hàng TMCP Quốc tế Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":23.55,"matchedTradingVolume":6.51873E7},{"month":2,"value":24.3,"matchedTradingVolume":6.42993E7},{"month":3,"value":21.4,"matchedTradingVolume":8.48303E7},{"month":4,"value":22.1,"matchedTradingVolume":7.98868E7},{"month":5,"value":21.6,"matchedTradingVolume":9.82021E7},{"month":6,"value":23.6,"matchedTradingVolume":1.718345E8},{"month":7,"value":21.0,"matchedTradingVolume":9.72921E7},{"month":8,"value":21.4,"matchedTradingVolume":1.057553E8},{"month":9,"value":21.7,"matchedTradingVolume":1.414188E8},{"month":10,"value":19.65,"matchedTradingVolume":7.06346E7},{"month":11,"value":19.65,"matchedTradingVolume":6.65855E7},{"month":12,"value":19.65,"matchedTradingVolume":7.1574E7}],"dividendSpitingHistories":[{"month":2,"value":1000.0},{"month":4,"value":500.0}]},{"symbol":"VIC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":59.2,"matchedTradingVolume":2.56029E7},{"month":2,"value":56.0,"matchedTradingVolume":3.974E7},{"month":3,"value":55.0,"matchedTradingVolume":3.25647E7},{"month":4,"value":58.0,"matchedTradingVolume":4.44255E7},{"month":5,"value":54.4,"matchedTradingVolume":3.62615E7},{"month":6,"value":54.1,"matchedTradingVolume":4.21094E7},{"month":7,"value":55.1,"matchedTradingVolume":6.40446E7},{"month":8,"value":75.6,"matchedTradingVolume":3.762692E8},{"month":9,"value":62.3,"matchedTradingVolume":2.936844E8},{"month":10,"value":46.9,"matchedTradingVolume":1.483437E8},{"month":11,"value":45.4,"matchedTradingVolume":9.69235E7},{"month":12,"value":44.6,"matchedTradingVolume":6.27363E7}],"dividendSpitingHistories":[]},{"symbol":"VJC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":116.3,"matchedTradingVolume":5537500.0},{"month":2,"value":113.9,"matchedTradingVolume":5160700.0},{"month":3,"value":108.9,"matchedTradingVolume":6564900.0},{"month":4,"value":103.0,"matchedTradingVolume":3872700.0},{"month":5,"value":99.5,"matchedTradingVolume":1.26274E7},{"month":6,"value":97.7,"matchedTradingVolume":1.6206E7},{"month":7,"value":102.0,"matchedTradingVolume":1.96767E7},{"month":8,"value":103.0,"matchedTradingVolume":2.02222E7},{"month":9,"value":101.9,"matchedTradingVolume":2.19183E7},{"month":10,"value":105.2,"matchedTradingVolume":2.09001E7},{"month":11,"value":113.0,"matchedTradingVolume":2.00095E7},{"month":12,"value":108.0,"matchedTradingVolume":2.01093E7}],"dividendSpitingHistories":[]},{"symbol":"VNM","companyName":"CTCP Sữa Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":81.3,"matchedTradingVolume":2.71532E7},{"month":2,"value":77.5,"matchedTradingVolume":2.8004E7},{"month":3,"value":77.1,"matchedTradingVolume":3.09558E7},{"month":4,"value":74.7,"matchedTradingVolume":2.10868E7},{"month":5,"value":70.7,"matchedTradingVolume":3.00439E7},{"month":6,"value":71.9,"matchedTradingVolume":1.092673E8},{"month":7,"value":78.0,"matchedTradingVolume":9.18289E7},{"month":8,"value":77.9,"matchedTradingVolume":8.24544E7},{"month":9,"value":80.3,"matchedTradingVolume":5.63057E7},{"month":10,"value":75.8,"matchedTradingVolume":4.31485E7},{"month":11,"value":71.4,"matchedTradingVolume":4.87116E7},{"month":12,"value":70.0,"matchedTradingVolume":5.76954E7}],"dividendSpitingHistories":[{"month":8,"value":1500.0},{"month":8,"value":1500.0},{"month":12,"value":500.0}]},{"symbol":"VPB","companyName":"Ngân hàng TMCP Việt Nam Thịnh Vượng","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":3.624271E8},{"month":2,"value":18.5,"matchedTradingVolume":3.291333E8},{"month":3,"value":21.25,"matchedTradingVolume":4.78505E8},{"month":4,"value":21.4,"matchedTradingVolume":2.156825E8},{"month":5,"value":19.8,"matchedTradingVolume":1.600067E8},{"month":6,"value":20.25,"matchedTradingVolume":3.597209E8},{"month":7,"value":22.15,"matchedTradingVolume":4.10663E8},{"month":8,"value":22.65,"matchedTradingVolume":4.072212E8},{"month":9,"value":22.55,"matchedTradingVolume":3.543629E8},{"month":10,"value":22.7,"matchedTradingVolume":2.767039E8},{"month":11,"value":21.35,"matchedTradingVolume":2.212622E8},{"month":12,"value":19.65,"matchedTradingVolume":2.219054E8}],"dividendSpitingHistories":[{"month":11,"value":1000.0}]},{"symbol":"VRE","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":30.3,"matchedTradingVolume":2.95246E7},{"month":2,"value":29.6,"matchedTradingVolume":3.32765E7},{"month":3,"value":29.9,"matchedTradingVolume":7.12347E7},{"month":4,"value":29.6,"matchedTradingVolume":4.78106E7},{"month":5,"value":28.4,"matchedTradingVolume":5.91646E7},{"month":6,"value":27.45,"matchedTradingVolume":7.98341E7},{"month":7,"value":29.65,"matchedTradingVolume":1.388173E8},{"month":8,"value":31.5,"matchedTradingVolume":1.701563E8},{"month":9,"value":30.3,"matchedTradingVolume":9.07252E7},{"month":10,"value":27.45,"matchedTradingVolume":7.55509E7},{"month":11,"value":24.4,"matchedTradingVolume":1.089259E8},{"month":12,"value":23.65,"matchedTradingVolume":7.37884E7}],"dividendSpitingHistories":[]}]}'

printAllowed = False
EXPERIMENT_TIMES_NUMS = 30

def calVariance(M2, w):
    return np.dot(w, np.dot(M2, w))
def calSkewness(M3, w):
    return np.dot(w, np.dot(M3, np.kron(w, w)))
def calKurtosis(M4, w):
    return np.dot(w, np.dot(M4, np.kron(np.kron(w, w), w)))
def calEntropy(w):
    if np.count_nonzero(w) == 0 or np.count_nonzero(w) == 1:
        return 0
    notZeroW = [v for v in w if v != 0]
    return -np.dot(notZeroW, np.log(notZeroW))

def myPrint(content):
    if not printAllowed:
        return
    print(content)


def loadDataInput(inputString):
    data = json.loads(inputString)
    for i in data['stocks']:
        myPrint(i)

    return data


def canReleaseAllAtTheFinalMonth(j, t, tau, futureData, spendableCash, holdingAmount, price):
    for month in range(t, tau, 1):
        for priceObject in futureData[j]['prices']:
            if priceObject['month'] - 1 == month:
                holdingAmount = holdingAmount - priceObject['matchedTradingVolume']
                if holdingAmount <= 0:
                    return spendableCash
    if holdingAmount > 0:
        return spendableCash - holdingAmount * price
    return spendableCash


def genWeightVector(holdingStocksPerMonth):
    if np.count_nonzero(holdingStocksPerMonth) == 0:
        return holdingStocksPerMonth
    sum = np.sum(holdingStocksPerMonth)
    holdingStocksPerMonthLen = len(holdingStocksPerMonth)
    response = []
    for j in range(holdingStocksPerMonthLen):
        response.append(holdingStocksPerMonth[j] / sum)
    return response


def shouldSellAsManyAsFromNowAmount(t, tau, j, futureData, holdingAmount):
    for month in range(tau, t, 1):
        for priceObject in futureData[j]['prices']:
            if priceObject['month'] - 1 == month:
                holdingAmount = holdingAmount - priceObject['matchedTradingVolume']
                if holdingAmount < 0:
                    return 0
    if holdingAmount > 0:
        return holdingAmount
    return 0

def chooseFromWhichParent(hasParents):
    if hasParents == False:
        return 0
    prob = random.random()

    # if prob is less than 0.45, insert gene
    # from parent 1
    if prob < 0.45:
        return 1
    # if prob is between 0.45 and 0.90, insert
    # gene from parent 2
    elif prob < 0.90:
        return 2
    # otherwise insert random gene(mutate),
    # for maintaining diversity
    else:
        return 0


def non_zero_indices(array):
    count = 0
    for element in array:
        if element != 0:
            count += 1

    non_zero_indices = [0] * count
    index = 0
    for i in range(len(array)):
        if array[i] != 0:
            non_zero_indices[index] = i
            index += 1

    return non_zero_indices


def genInvestmentPlan(futureData, parent1, parent2, currentSaSolution, tail_probability_epsilon):
    myPrint("gen investment plan from 2 parents")
    inputLen = len(futureData)
    myPrint('len >> %d' % inputLen)

    rows, cols = (tau + 1, inputLen)
    holdingStocks = [[0 for _ in range(cols)] for _ in range(rows)]
    buyingStocks = [[0 for _ in range(cols)] for _ in range(rows)]
    sellingStocks = [[0 for _ in range(cols)] for _ in range(rows)]
    cashBeginMonth = []
    cashEndMonth = []

    hasParent = False
    if parent1 is not None:
        hasParent = True

    findNeighborModifiedMonth = random.choice(range(tau - 2))

    availableCash = initTheta
    bankingDeposit = 0
    returns = stock_returns
    cvar_values = []
    # myPrint(random.choice(range(inputLen)))
    for t in range(tau + 1):
        myPrint(t)

        # update budget
        if t <= 0:
            availableCash = initTheta
        if t > 0:
            availableCash += bankingDeposit * (1 + alpha)
            for j in range(inputLen):
                availableCash += sellingStocks[t - 1][j] * futureData[j]['prices'][t - 1]['value'] * (1 - epsilon)

        # plus dividends if eligible for it
        if t > 2:
            for j in range(inputLen):
                for object in futureData[j]['dividendSpitingHistories']:
                    if object['month'] - 1 == t - 1:
                        availableCash += holdingStocks[t - 2][j] * object['value'] / 1000  # kVND

        cashBeginMonth.append(availableCash)

        # calculate risks
        if 0 < t < tau:
            current_month_prices = []
            for stock_info in stock_data:
                # month also is the index = month + 1 in "month" field
                current_month_prices.append(stock_info["prices"][t]["value"])
            returns = np.vstack((returns, np.array(current_month_prices).reshape(1, -1)))
            portfolio_returns = np.dot(returns, holdingStocks[t-1]) + availableCash
            portfolio_returns = (portfolio_returns - initTheta)/initTheta

            wavelet_variance = compute_wavelet_variance(wavelet_decomposition(portfolio_returns))

            portfolio_var = calculate_var_from_wavelet_variance(wavelet_variance, tail_probability_epsilon,
                                                                scaling_factor=initTheta)

            portfolio_cvar = calculate_cvar(portfolio_returns, portfolio_var)
            cvar_values.append(portfolio_cvar)

        # random to see how many stocks should we buy
        shouldBuyStockNum = random.choice(range(math.floor(cardinalityK)))
        shouldBuyStockIndices = random.sample(range(inputLen), shouldBuyStockNum)

        chooseFrom = chooseFromWhichParent(hasParent)
        if chooseFrom == 1:
            # shouldBuyStockIndices = [v for v in parent1.buyingStocks[t] if v != 0]
            shouldBuyStockIndices = non_zero_indices(parent1.buyingStocks[t])
        elif chooseFrom == 2:
            # shouldBuyStockIndices = [v for v in parent2.buyingStocks[t] if v != 0]
            shouldBuyStockIndices = non_zero_indices(parent2.buyingStocks[t])

        justBoughtStocks = []
        for j in shouldBuyStockIndices:
            if np.count_nonzero(holdingStocks[t]) >= cardinalityK or t >= tau - 2:
                break
            myPrint("Buying stock index = {}; symbol = {}".format(j, futureData[j]['symbol']))
            # random buy stock amount if valid (budget, trading capability, dividend constrains
            spendableCash = availableCash
            priceObject = futureData[j]['prices'][t]
            jPrice = priceObject['value']
            if priceObject['matchedTradingVolume'] * jPrice < availableCash:
                spendableCash = priceObject['matchedTradingVolume'] * jPrice

            spendableCash = canReleaseAllAtTheFinalMonth(j, t, tau, futureData, spendableCash, holdingStocks[t][j],
                                                         jPrice)
            if spendableCash <= 0:
                continue

            spendableCashFloor = math.floor(spendableCash)
            if spendableCashFloor > 0:
                if chooseFrom == 1 and parent1.buyingStocks[t][j] * jPrice <= spendableCash:
                    buyingStocks[t][j] = parent1.buyingStocks[t][j]
                elif chooseFrom == 2 and parent2.buyingStocks[t][j] * jPrice <= spendableCash:
                    buyingStocks[t][j] = parent2.buyingStocks[t][j]
                else:
                    myPrint("math.floor(spendableCash))= %s" % spendableCashFloor)
                    buyingStocks[t][j] = math.floor(
                        math.floor(random.choice(range(spendableCashFloor)) / jPrice) / xi) * xi
                    if currentSaSolution is not None:
                        if t < findNeighborModifiedMonth:
                            buyingStocks[t][j] = currentSaSolution.buyingStocks[t][j]
                        elif t == findNeighborModifiedMonth:
                            if random.choice(range(2)) == 1:
                                buyingStocks[t][j] = currentSaSolution.buyingStocks[t][j] + random.choice(
                                    [1, 2, 3]) * xi
                            else:
                                buyingStocks[t][j] = currentSaSolution.buyingStocks[t][j] - random.choice(
                                    [1, 2, 3]) * xi
            while buyingStocks[t][j] * jPrice * (1 + epsilon) > spendableCash:  # constraint 6
                buyingStocks[t][j] -= xi

            if buyingStocks[t][j] > 0:
                justBoughtStocks.append(j)
                # decrease budget
                availableCash -= buyingStocks[t][j] * jPrice * (1 + epsilon)
            else:
                buyingStocks[t][j] = 0
            holdingStocks[t][j] = holdingStocks[t - 1][j] + buyingStocks[t][j]

        # update holding amount
        for j in range(inputLen):
            if j in justBoughtStocks:
                continue
            holdingStocks[t][j] = holdingStocks[t - 1][j] + buyingStocks[t][j]

        myPrint('About to sell....')
        # selling stocks
        for j in range(inputLen):
            if holdingStocks[t][j] <= 0 or j in justBoughtStocks or buyingStocks[t - 1][j] > 0:
                continue
            myPrint("Selling stock index = {}; symbol = {}".format(j, futureData[j]['symbol']))
            canHaveDividendNextMonth = False
            for dividendSpitingHistoriesObject in futureData[j]['dividendSpitingHistories']:
                if dividendSpitingHistoriesObject['month'] == t + 1:
                    canHaveDividendNextMonth = True
                    break
            if canHaveDividendNextMonth and t < tau - 2:
                continue

            for priceObject in futureData[j]['prices']:
                if priceObject['month'] - 1 == t:
                    canSellNum = holdingStocks[t][j]
                    if canSellNum > priceObject['matchedTradingVolume']:
                        canSellNum = priceObject['matchedTradingVolume']

                    sellingStocks[t][j] = shouldSellAsManyAsFromNowAmount(t, tau, j, futureData, holdingStocks[t][j])
                    if sellingStocks[t][j] <= 0:
                        if chooseFrom == 1 and parent1.sellingStocks[t][j] <= canSellNum:
                            sellingStocks[t][j] = parent1.sellingStocks[t][j]
                        elif chooseFrom == 2 and parent2.sellingStocks[t][j] <= canSellNum:
                            sellingStocks[t][j] = parent2.sellingStocks[t][j]
                        else:
                            sellingStocks[t][j] = random.choice(range(math.floor(canSellNum / xi))) * xi
                            if currentSaSolution is not None:
                                if t < findNeighborModifiedMonth:
                                    sellingStocks[t][j] = currentSaSolution.sellingStocks[t][j]
                                elif t == findNeighborModifiedMonth:
                                    if random.choice(range(2)) == 1:
                                        sellingStocks[t][j] = currentSaSolution.sellingStocks[t][j] + random.choice(
                                            [1, 2, 3]) * xi
                                    else:
                                        sellingStocks[t][j] = currentSaSolution.sellingStocks[t][j] - random.choice(
                                            [1, 2, 3]) * xi

                    holdingStocks[t][j] -= sellingStocks[t][j]

        # deposit to the bank the remaining budget
        if t < tau:
            cashEndMonth.append(availableCash)
            bankingDeposit = availableCash
            availableCash = 0
        # end plan

    # fitnesses = [[0 for _ in range(4)] for _ in
    #              range(tau)]  # mean(variances), mean(skewness), mean(kurtosis), mean(entropy), tau profit


    # for t in range(tau):
    #     # w = genWeightVector(holdingStocks[t])
    #     # fitnesses[t][0] = calVariance(M2, w)
    #     # fitnesses[t][1] = calSkewness(M3, w)
    #     # fitnesses[t][2] = calKurtosis(M4, w)
    #     # fitnesses[t][3] = calEntropy(w)
    #     if t == 0:
    #         continue
    #     current_month_prices = []
    #     for stock_info in stock_data:
    #         # month also is the index = month + 1 in "month" field
    #         current_month_prices.append(stock_info["prices"][t]["value"])
    #     returns = np.vstack((returns, np.array(current_month_prices).reshape(1, -1)))
    #     portfolio_returns = np.dot(returns, holdingStocks[t])
    #     portfolio_returns = (portfolio_returns - initTheta)/initTheta
    #
    #     wavelet_variance = compute_wavelet_variance(wavelet_decomposition(portfolio_returns))
    #
    #     portfolio_var = calculate_var_from_wavelet_variance(wavelet_variance, tail_probability_epsilon,
    #                                                         scaling_factor=initTheta)
    #
    #     portfolio_cvar = calculate_cvar(portfolio_returns, portfolio_var)
    #     cvar_values.append(portfolio_cvar)

    # fitnesses_norm = minmax_scale(fitnesses, feature_range=(0,1), axis=0)

    aggregatedFitness = []
    aggregatedFitness.extend(cvar_values)
    aggregatedFitness.append((availableCash - initTheta)/initTheta)
    # aggregatedFitness = np.mean(aggregatedFitness, axis=0)
    aggregatedFitness = minmax_scale(aggregatedFitness, feature_range=(0, 1), axis=0)

    # aggregatedFitness = [0 for _ in range(tau)]
    # for i in range(4):
    #     aggregatedFitness[i] = tempAggregatedFitness[i]
    # aggregatedFitness[4] = availableCash

    finalCash = availableCash
    # finalFitness = calFitnessNom(aggregatedFitness)

    frontier = -math.inf
    return cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, aggregatedFitness, frontier, cvar_values


def verifyInvestmentPlan(holdingStocks, buyingStocks, sellingStocks, futureData):
    if np.count_nonzero(sellingStocks[0]) > 0:
        return False, "at t=0, no stock j is sold out"
    # Add more validation checks as per requirement
    for t in range(tau):
        totalSecurities = 0
        for j in range(len(holdingStocks[0])):
            totalSecurities += holdingStocks[t][j]

            if t > 0 and sellingStocks[t][j] > holdingStocks[t - 1][j]:
                return False, "the number of stock j sold out cannot exceed the number of stock j is holding"

            if buyingStocks[t][j] < 0 or sellingStocks[t][j] < 0:
                return False, "Negative stock transactions are not possible."

            if buyingStocks[t][j] % xi > 0 or sellingStocks[t][j] % xi > 0:
                return False, "The quantity of stock j available for purchase or sale is subject to its lot size constraint."

            for priceObject in futureData[j]['prices']:
                if priceObject['month'] == t + 1:
                    if priceObject['matchedTradingVolume'] < buyingStocks[t][j] or priceObject['matchedTradingVolume'] < sellingStocks[t][j]:
                        return False, 'the volume of stock j that can be bought or sold is limited by its maximum trading volume.'

        if totalSecurities < 0:
            return False, "Negative securities holding is not possible."
        if np.count_nonzero(holdingStocks[t]) > cardinalityK:
            return False, 'Violate cardinality at month t=%s' % t

    if np.count_nonzero(holdingStocks[tau - 1]) > 0:
        return False, "at t=tau, sell all the holding stocks"

    return True, "Investment plan is valid."


# Usage
# holdingStocks, buyingStocks, sellingStocks, finalCash, futureData, fitnesses, aggregatedFitness = genInvestmentPlan()
# isValid, message = verifyInvestmentPlan(holdingStocks, buyingStocks, sellingStocks, futureData)
# myPrint(message)


class Individual(object):
    '''
    Class representing individual in population
    '''

    def __init__(self, cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, aggregatedFitness, frontier,
                 cvar_values):
        self.cashBeginMonth = cashBeginMonth
        self.holdingStocks = holdingStocks
        self.buyingStocks = buyingStocks
        self.sellingStocks = sellingStocks
        self.finalCash = finalCash
        self.aggregatedFitness = aggregatedFitness
        self.frontier = frontier
        self.cvar_values = cvar_values


def compare_individuals(individual1, individual2):
    if individual1.finalFitnessNom < individual2.finalFitnessNom:
        return -1
    elif individual1.finalFitnessNom > individual2.finalFitnessNom:
        return 1
    else:
        return 0

def assign_frontiers_and_crowding_distance(populations):
    myPrint("[NSGA-III] Consider calling assign_frontiers_and_crowding_distance whenever when sorting populations")
    populationsLen = len(populations)
    frontier = 0

    for i in range(populationsLen):
        # frontier += 1
        if populations[i].frontier < 0:
            populations[i].frontier = frontier
        for j in range(populationsLen):
            if i == j:
                continue
            if not is_belonged_frontier(populations[i].aggregatedFitness, populations[j].aggregatedFitness):
                populations[i].frontier = frontier + 1
                break

    currFrontier = frontier + 1
    dominatedPopulations = [p for p in populations if p.frontier == currFrontier]
    while len(dominatedPopulations) < populationsLen:
        # can have more frontiers
        for i in range(populationsLen):
            # frontier += 1
            for j in range(populationsLen):
                if i == j or populations[i].frontier < currFrontier or populations[j].frontier < currFrontier:
                    continue
                if not is_belonged_frontier(populations[i].aggregatedFitness, populations[j].aggregatedFitness):
                    populations[i].frontier = currFrontier + 1
                    break

        currFrontier += 1
        populationsLen = len(dominatedPopulations)
        dominatedPopulations = [p for p in populations if p.frontier == currFrontier]

    frontiersLen = currFrontier + 1
    for i in range(frontiersLen):
        myPrint("calculate crowding_distance")
        frontierPopulations = [p for p in populations if p.frontier == i]
        if (len(frontierPopulations) == 0):
            continue

        # variance
        frontierPopulations.sort(key=lambda x: x.aggregatedFitness[0], reverse=True)
        frontierPopulationsLen = len(frontierPopulations)
        if frontierPopulationsLen != 1:
            for j in range(frontierPopulationsLen):
                if j == 0 and j + 1 < frontierPopulationsLen:
                    frontierPopulations[j].crowdingDistances[0] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[0] - frontierPopulations[j].aggregatedFitness[0])
                elif j == frontierPopulationsLen - 1 and frontierPopulationsLen > 1:
                    frontierPopulations[j].crowdingDistances[0] = abs(
                        frontierPopulations[j - 1].aggregatedFitness[0] - frontierPopulations[j].aggregatedFitness[0])
                else:
                    frontierPopulations[j].crowdingDistances[0] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[0] - frontierPopulations[j].aggregatedFitness[
                            0]) + abs(
                        frontierPopulations[j - 1].aggregatedFitness[0] - frontierPopulations[j].aggregatedFitness[0])

            # skewness
            frontierPopulations.sort(key=lambda x: x.aggregatedFitness[1], reverse=False)
            frontierPopulationsLen = len(frontierPopulations)
            for j in range(frontierPopulationsLen):
                if j == 0 and j + 1 < frontierPopulationsLen:
                    frontierPopulations[j].crowdingDistances[1] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[1] - frontierPopulations[j].aggregatedFitness[1])
                elif j == frontierPopulationsLen - 1 and frontierPopulationsLen > 1:
                    frontierPopulations[j].crowdingDistances[1] = abs(
                        frontierPopulations[j - 1].aggregatedFitness[1] - frontierPopulations[j].aggregatedFitness[1])
                else:
                    frontierPopulations[j].crowdingDistances[1] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[1] - frontierPopulations[j].aggregatedFitness[
                            1]) + abs(
                        frontierPopulations[j - 1].aggregatedFitness[1] - frontierPopulations[j].aggregatedFitness[1])

            # kurtosis
            frontierPopulations.sort(key=lambda x: x.aggregatedFitness[2], reverse=True)
            frontierPopulationsLen = len(frontierPopulations)
            for j in range(frontierPopulationsLen):
                if j == 0 and j + 1 < frontierPopulationsLen:
                    frontierPopulations[j].crowdingDistances[2] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[2] - frontierPopulations[j].aggregatedFitness[2])
                elif j == frontierPopulationsLen - 1 and frontierPopulationsLen > 1:
                    frontierPopulations[j].crowdingDistances[2] = abs(
                        frontierPopulations[j - 1].aggregatedFitness[2] - frontierPopulations[j].aggregatedFitness[2])
                else:
                    frontierPopulations[j].crowdingDistances[2] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[2] - frontierPopulations[j].aggregatedFitness[
                            2]) + abs(
                        frontierPopulations[j - 1].aggregatedFitness[2] - frontierPopulations[j].aggregatedFitness[2])

            # entropy
            frontierPopulations.sort(key=lambda x: x.aggregatedFitness[3], reverse=True)
            frontierPopulationsLen = len(frontierPopulations)
            for j in range(frontierPopulationsLen):
                if j == 0 and j + 1 < frontierPopulationsLen:
                    frontierPopulations[j].crowdingDistances[3] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[3] - frontierPopulations[j].aggregatedFitness[3])
                elif j == frontierPopulationsLen - 1 and frontierPopulationsLen > 1:
                    frontierPopulations[j].crowdingDistances[3] = abs(
                        frontierPopulations[j - 1].aggregatedFitness[3] - frontierPopulations[j].aggregatedFitness[3])
                else:
                    frontierPopulations[j].crowdingDistances[3] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[3] - frontierPopulations[j].aggregatedFitness[
                            3]) + abs(
                        frontierPopulations[j - 1].aggregatedFitness[3] - frontierPopulations[j].aggregatedFitness[3])

            # return or mean
            frontierPopulations.sort(key=lambda x: x.aggregatedFitness[4], reverse=False)
            frontierPopulationsLen = len(frontierPopulations)
            for j in range(frontierPopulationsLen):
                if j == 0 and j + 1 < frontierPopulationsLen:
                    frontierPopulations[j].crowdingDistances[4] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[4] - frontierPopulations[j].aggregatedFitness[4])
                elif j == frontierPopulationsLen - 1 and frontierPopulationsLen > 1:
                    frontierPopulations[j].crowdingDistances[4] = abs(
                        frontierPopulations[j - 1].aggregatedFitness[4] - frontierPopulations[j].aggregatedFitness[4])
                else:
                    frontierPopulations[j].crowdingDistances[4] = abs(
                        frontierPopulations[j + 1].aggregatedFitness[4] - frontierPopulations[j].aggregatedFitness[
                            4]) + abs(
                        frontierPopulations[j - 1].aggregatedFitness[4] - frontierPopulations[j].aggregatedFitness[4])

    for p in populations:
        p.crowdingDistance = math.sqrt(
            p.crowdingDistances[0] ** 2 + p.crowdingDistances[1] ** 2 + p.crowdingDistances[2] ** 2 +
            p.crowdingDistances[3] ** 2 + p.crowdingDistances[4] ** 2)
    myPrint("OK")

def printSolution(content):
    print(content)

def prinfReSult(population, frontierNumPassed, generationNumUntilReachingLastPivot, log_dn, log_gn, log_fitnesses):
    myPrint("Printing result")
    log_dn.append(frontierNumPassed)
    log_gn.append(generationNumUntilReachingLastPivot)
    log_fitnesses.append(population.aggregatedFitness)
    printSolution(f'To gain the solution needed {generationNumUntilReachingLastPivot} generations, and went through {frontierNumPassed} frontiers')
    printSolution('final cash = ')
    printSolution(population.finalCash)
    printSolution('fitness = ')
    printSolution(population.aggregatedFitness)
    printSolution('buying = ')
    printSolution(population.buyingStocks)
    printSolution('holding = ')
    printSolution(population.holdingStocks)
    printSolution('selling = ')
    printSolution(population.sellingStocks)
    stocksLen = len(stock_data)
    for t in range(tau):
        boughtStocks = ""
        # futureData[j]['prices'][t-1]['value']
        for j in range(stocksLen):
            if population.buyingStocks[t][j] != 0:
                boughtStocks += "\n\t\t\t" + str(population.buyingStocks[t][j]) + " " + str(
                    stock_data[j]['symbol']) + " -" + str(
                    population.buyingStocks[t][j] * stock_data[j]['prices'][t]['value'] * (1 + epsilon))

        sellStocks = ""
        for j in range(stocksLen):
            if population.sellingStocks[t][j] != 0:
                sellStocks += "\n\t\t\t" + str(population.sellingStocks[t][j]) + " " + str(
                    stock_data[j]['symbol']) + " +" + str(
                    population.sellingStocks[t][j] * stock_data[j]['prices'][t]['value'] * (1 - epsilon))

        dividends = ""
        for j in range(stocksLen):
            if population.holdingStocks != 0:
                dividendsSplitingLen = len(stock_data[j]['dividendSpitingHistories'])
                if dividendsSplitingLen > 0:
                    for d in range(dividendsSplitingLen):
                        if population.holdingStocks[t - 1][j] > 0 and \
                                stock_data[j]['dividendSpitingHistories'][d]["month"] - 1 == t and t - 1 > 0:
                            dividends += "\n\t\t\t" + str(population.holdingStocks[t - 1][j]) + " " + str(
                                stock_data[j]['symbol']) + " +" + str(stock_data[j]['dividendSpitingHistories'][d]["value"] * population.holdingStocks[t - 1][j])

        printSolution("\nMonth= " + str(t) + "\n\t>>Cash=" + str(population.cashBeginMonth[
                                                               t]) + "\n\t>>Bought= " + boughtStocks + "\n\t>>Sold= " + sellStocks + "\n\t>>Dividend payout= " + dividends + "\n\t>>Bank deposit=" + str(population.cashEndMonth[t]))
    myPrint("DONE")

def is_belonged_frontier_fixed_risk(dominator, dominated_guy):

    # min(variances), max(skewness), min(kurtosis), min(entropy), max profit
    #https://www.thearmchaircritic.org/mansplainings/nsga-ii-non-dominated-sorting-genetic-algorithm-ii

    if dominator[4] < initTheta * (1 + upsilon):
        return False

    # variance is the fixed axis
    if dominated_guy[0] < dominator[0]:
        # not bad all other criteria
        if dominated_guy[2] < dominator[2] or dominated_guy[3] < dominator[3]:
            return False
        if dominated_guy[1] > dominator[1] or dominated_guy[4] > dominator[4]:
            return False

    return True
def is_belonged_frontier(dominator, dominated_guy):

    # min(variances), max(skewness), min(kurtosis), min(entropy), max profit
    #https://www.thearmchaircritic.org/mansplainings/nsga-ii-non-dominated-sorting-genetic-algorithm-ii
    if dominator[4] < initTheta * (1 + upsilon):
        return False

    # we keep the return as the fixed axis
    if dominator[4] < dominated_guy[4]:

        # Dominated if Not Bad In Any RISK Criterias
        if (dominator[0] > dominated_guy[0] or dominator[2] > dominated_guy[2] or dominator[3] > dominated_guy[3]):
            return False
        if dominator[1] < dominated_guy[1]:
            return False

    return True

def isDominated(dominator, dominated_guy):
    # min(variances), max(skewness), min(kurtosis), min(entropy), max profit
    # Dominated if Not Bad In Any Criteria
    if dominator[0] > dominated_guy[0] or dominator[2] > dominated_guy[2] or dominator[3] > dominated_guy[3]:
        return False
    if dominator[1] < dominated_guy[1] or dominator[4] < dominated_guy[4]:
        return False

    # At least one criteria is better
    if dominator[0] < dominated_guy[0] or dominator[2] < dominated_guy[2] or dominator[3] < dominated_guy[3]:
        return True
    if dominator[1] > dominated_guy[1] or dominator[4] > dominated_guy[4]:
        return True

    return False


def sa_acceptance_probability(delta_energy, temperature):
    # print(delta_energy, temperature)
    return math.exp(-delta_energy / 10000 / temperature)


def bestSASolution(currentSaSolution):
    bestSAIndividual = currentSaSolution
    temperature = initialTemperature
    for i in range(saIterationLength):
        cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses, aggregatedFitness, finalFitness, frontier, crowdingDistance, cashEndMonth = genInvestmentPlan(
            stock_data, None, None, currentSaSolution)
        if is_belonged_frontier(aggregatedFitness, bestSAIndividual.aggregatedFitness) or sa_acceptance_probability(
                bestSAIndividual.finalFitness - finalFitness, temperature) > temperature:
            bestSAIndividual = Individual(cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash,
                                          fitnesses, aggregatedFitness, finalFitness, [], 0.0, frontier,
                                          crowdingDistance, [0, 0, 0, 0, 0], cashEndMonth)
        temperature = cool_temperature(temperature, coolingRate)
    return bestSAIndividual


def cool_temperature(currentTemperature, coolingRate):
    """
    Cooling function using exponential decay.

    Parameters:
    - current_temperature: The current temperature in the annealing process.
    - cooling_rate: The rate at which the temperature should decrease.

    Returns:
    - The updated temperature.
    """
    return currentTemperature * coolingRate

def ga_cross(new_generation, populations):
    parent1 = random.choice(populations[:50])
    parent2 = random.choice(populations[:50])
    cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses, aggregatedFitness, finalFitness, frontier, crowdingDistance, cashEndMonth = genInvestmentPlan(
        stock_data, parent1, parent2, None)
    new_generation.append(
        Individual(cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses,
                   aggregatedFitness, finalFitness, [], 0.0, frontier, crowdingDistance, [0, 0, 0, 0, 0], cashEndMonth))

def cal_delta_frontiers(sorted_population, fitnesses_pivot):
    sorted_population_len = len(sorted_population)
    for i in range(sorted_population_len):
        if sorted_population[i].aggregatedFitness[0] == fitnesses_pivot[0] and sorted_population[i].aggregatedFitness[1] == fitnesses_pivot[1] and sorted_population[i].aggregatedFitness[2] == fitnesses_pivot[2] and sorted_population[i].aggregatedFitness[3] == fitnesses_pivot[3] and sorted_population[i].aggregatedFitness[4] == fitnesses_pivot[4]:
            delta = sorted_population[i].frontier - sorted_population[0].frontier
            if delta > 0:
                return delta
            else:
                return 1
    return 1


def _do(self, pop, n_survive):

    # attributes to be set after the survival
    F = [individual.aggregatedFitness for individual in pop]

    # calculate the fronts of the population
    fronts, rank = NonDominatedSorting().do(F, return_rank=True, n_stop_if_ranked=n_survive)
    print(f'ACK FOUND > 1; len(fronts)={len(fronts)}')
    # for elem in fronts:  # todo remove me
    #     if len(elem) > 1:
    #         print(f'ACK FOUND > 1; len(elem)={len(elem)}')
    non_dominated, last_front = fronts[0], fronts[-1]

    # update the hyperplane based boundary estimation
    hyp_norm = self.norm
    hyp_norm.update(F, nds=non_dominated)
    ideal, nadir = hyp_norm.ideal_point, hyp_norm.nadir_point

    #  consider only the population until we come to the splitting front
    I = np.concatenate(fronts)
    pop, rank, F = pop[I], rank[I], F[I]

    # update the front indices for the current population
    counter = 0
    for i in range(len(fronts)):
        for j in range(len(fronts[i])):
            fronts[i][j] = counter
            counter += 1
    last_front = fronts[-1]

    # associate individuals to niches
    niche_of_individuals, dist_to_niche, dist_matrix = \
        associate_to_niches(F, self.ref_dirs, ideal, nadir)

    # attributes of a population
    pop.set('rank', rank,
            'niche', niche_of_individuals,
            'dist_to_niche', dist_to_niche)

    # set the optimum, first front and closest to all reference directions
    closest = np.unique(dist_matrix[:, np.unique(niche_of_individuals)].argmin(axis=0))
    self.opt = pop[intersect(fronts[0], closest)]
    if len(self.opt) == 0:
        self.opt = pop[fronts[0]]

    # if we need to select individuals to survive
    if len(pop) > n_survive:

        # if there is only one front
        if len(fronts) == 1:
            n_remaining = n_survive
            until_last_front = np.array([], dtype=int)
            niche_count = np.zeros(len(self.ref_dirs), dtype=int)

        # if some individuals already survived
        else:
            until_last_front = np.concatenate(fronts[:-1])
            niche_count = calc_niche_count(len(self.ref_dirs), niche_of_individuals[until_last_front])
            n_remaining = n_survive - len(until_last_front)

        S = niching(pop[last_front], n_remaining, niche_count, niche_of_individuals[last_front],
                    dist_to_niche[last_front])

        survivors = np.concatenate((until_last_front, last_front[S].tolist()))
        pop = pop[survivors]

    return pop

def ga(futureData, isNSGA_III, isHybridWithSA, log_dn, log_gn, log_fitnesses, fitness_pivot):
    myPrint('planning..')

    cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, aggregatedFitness, frontier, cvar_values = genInvestmentPlan(
        futureData, None, None, None, TAIL_PROBABILITY_EPSILON)
    currentSaSolution = Individual(cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, aggregatedFitness, frontier, cvar_values)

    # current generation
    generation = 1

    convergence = False
    populations = []

    # create initial population
    for _ in range(POPULATION_SIZE):
        cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, aggregatedFitness, frontier, cvar_values = genInvestmentPlan(
            futureData, None, None, None, TAIL_PROBABILITY_EPSILON)
        populations.append(Individual(cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, aggregatedFitness, frontier, cvar_values))
    myPrint('done giving birth')

    fitnessesPivot = []
    generationCheckedConsecutiveNumWithoutImprovement = 0
    frontierNumPassed = 1
    generationNumUntilReachingLastPivot = 0

    while not convergence:
        # GA Exploitation Phase
        myPrint('generation=%s' % generation)

        assign_frontiers_and_crowding_distance(populations)
        populations.sort(key=lambda x: (x.frontier, -x.crowdingDistance, -x.aggregatedFitness[4]))
        myPrint('sorted')

        curFitnesses = populations[0].aggregatedFitness
        # print(curFitnesses)
        if fitnessesPivot == []:
            fitnessesPivot = curFitnesses
            generationNumUntilReachingLastPivot = generation
            # print("fitnessesPivot = ")
            # print(fitnessesPivot)

        if isDominated(curFitnesses, fitnessesPivot):
            fitnessesPivot = curFitnesses
            if isNSGA_III:
                frontierNumPassed += cal_delta_frontiers(populations, fitnessesPivot)
            generationNumUntilReachingLastPivot = generation

            generationCheckedConsecutiveNumWithoutImprovement = 0
        else:
            generationCheckedConsecutiveNumWithoutImprovement += 1

        if generationCheckedConsecutiveNumWithoutImprovement == generationCheckedConsecutiveNumToConvergenceDecision or generation == MAX_GENERATION:
            prinfReSult(populations[0], frontierNumPassed, generationNumUntilReachingLastPivot, log_dn, log_gn, log_fitnesses)
            fitness_pivot.append(fitnessesPivot)
            return populations[0]

        # Otherwise generate new offsprings for new generation
        new_generation = []

        # Perform Elitism, that mean 10% of fittest population
        # goes to the next generation
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(populations[:s])

        # From 50% of fittest population, Individuals
        # will mate to produce offspring
        s = int((90 * POPULATION_SIZE) / 100)

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=6)
        for _ in range(s):
            pool.submit(ga_cross, new_generation, populations)
            # ga_cross(new_generation, populations)
            # parent1 = random.choice(populations[:50])
            # parent2 = random.choice(populations[:50])
            # cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses, aggregatedFitness, finalFitness, frontier, crowdingDistance = genInvestmentPlan(
            #     futureData, parent1, parent2, None)
            # new_generation.append(
            #     Individual(cashBeginMonth, holdingStocks, buyingStocks, sellingStocks, finalCash, fitnesses,
            #                aggregatedFitness, finalFitness, [], 0.0, frontier, crowdingDistance, [0, 0, 0, 0, 0]))

        pool.shutdown(wait=True)
        populations = new_generation

        if isHybridWithSA:
            # SA Exploration Phase
            currentSaSolution = bestSASolution(currentSaSolution)
            populations[POPULATION_SIZE - 1] = currentSaSolution
        generation += 1


# Running point.
### debug point
# M2 = np.load("data/calculate2023/vn30_3years_before/M2.dat", allow_pickle=True)
# M3 = np.load("data/calculate2023/vn30_3years_before/M3.dat", allow_pickle=True)
# M4 = np.load("data/calculate2023/vn30_3years_before/M4.dat", allow_pickle=True)
# cardinalityK = 2
# jsonInput2023 = '{"stocks":[{"symbol":"ACB","companyName":"Ngân hàng TMCP Á Châu","type":"VN30","year":2023,"prices":[{"month":1,"value":26.35,"matchedTradingVolume":5.499E7},{"month":2,"value":25.8,"matchedTradingVolume":6.3237E7},{"month":3,"value":25.35,"matchedTradingVolume":9.20633E7},{"month":4,"value":25.3,"matchedTradingVolume":8.14876E7},{"month":5,"value":25.4,"matchedTradingVolume":1.608784E8},{"month":6,"value":22.3,"matchedTradingVolume":1.920848E8},{"month":7,"value":22.95,"matchedTradingVolume":1.640575E8},{"month":8,"value":24.4,"matchedTradingVolume":2.570596E8},{"month":9,"value":22.95,"matchedTradingVolume":1.263825E8},{"month":10,"value":22.8,"matchedTradingVolume":1.01492E8},{"month":11,"value":23.3,"matchedTradingVolume":1.540952E8},{"month":12,"value":23.9,"matchedTradingVolume":1.309384E8}],"dividendSpitingHistories":[]},{"symbol":"BCM","companyName":"Tổng Công ty Đầu tư và Phát triển Công nghiệp – CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":85.2,"matchedTradingVolume":1681700.0},{"month":2,"value":86.0,"matchedTradingVolume":1668200.0},{"month":3,"value":84.5,"matchedTradingVolume":2201700.0},{"month":4,"value":83.5,"matchedTradingVolume":1124200.0},{"month":5,"value":78.5,"matchedTradingVolume":1003200.0},{"month":6,"value":82.1,"matchedTradingVolume":6718400.0},{"month":7,"value":81.0,"matchedTradingVolume":5792000.0},{"month":8,"value":79.0,"matchedTradingVolume":5927500.0},{"month":9,"value":72.6,"matchedTradingVolume":5679800.0},{"month":10,"value":69.5,"matchedTradingVolume":4024400.0},{"month":11,"value":62.4,"matchedTradingVolume":6680300.0},{"month":12,"value":66.0,"matchedTradingVolume":1.05481E7}],"dividendSpitingHistories":[{"month":11,"value":800.0}]},{"symbol":"BID","companyName":"Ngân hàng TMCP Đầu tư và Phát triển Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":45.95,"matchedTradingVolume":2.88095E7},{"month":2,"value":47.2,"matchedTradingVolume":2.70027E7},{"month":3,"value":48.0,"matchedTradingVolume":1.78979E7},{"month":4,"value":46.0,"matchedTradingVolume":1.53768E7},{"month":5,"value":45.1,"matchedTradingVolume":1.2405E7},{"month":6,"value":45.35,"matchedTradingVolume":2.61229E7},{"month":7,"value":47.35,"matchedTradingVolume":3.93465E7},{"month":8,"value":49.1,"matchedTradingVolume":4.26147E7},{"month":9,"value":47.5,"matchedTradingVolume":2.19276E7},{"month":10,"value":43.95,"matchedTradingVolume":2.0611E7},{"month":11,"value":44.15,"matchedTradingVolume":1.78062E7},{"month":12,"value":43.4,"matchedTradingVolume":2.24373E7}],"dividendSpitingHistories":[]},{"symbol":"BVH","companyName":"Tập đoàn Bảo Việt","type":"VN30","year":2023,"prices":[{"month":1,"value":51.0,"matchedTradingVolume":7621200.0},{"month":2,"value":51.2,"matchedTradingVolume":9028400.0},{"month":3,"value":50.0,"matchedTradingVolume":5479800.0},{"month":4,"value":49.2,"matchedTradingVolume":5394500.0},{"month":5,"value":46.0,"matchedTradingVolume":1.05267E7},{"month":6,"value":45.3,"matchedTradingVolume":2.13723E7},{"month":7,"value":48.15,"matchedTradingVolume":2.26194E7},{"month":8,"value":48.0,"matchedTradingVolume":1.95543E7},{"month":9,"value":45.8,"matchedTradingVolume":1.30652E7},{"month":10,"value":42.65,"matchedTradingVolume":6368600.0},{"month":11,"value":41.3,"matchedTradingVolume":6801500.0},{"month":12,"value":40.5,"matchedTradingVolume":6636100.0}],"dividendSpitingHistories":[{"month":11,"value":954.0}]},{"symbol":"CTG","companyName":"Ngân hàng TMCP Công Thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":31.1,"matchedTradingVolume":6.19356E7},{"month":2,"value":30.45,"matchedTradingVolume":5.62202E7},{"month":3,"value":29.5,"matchedTradingVolume":4.62949E7},{"month":4,"value":30.0,"matchedTradingVolume":4.04912E7},{"month":5,"value":28.4,"matchedTradingVolume":7.05504E7},{"month":6,"value":30.0,"matchedTradingVolume":1.20986E8},{"month":7,"value":30.3,"matchedTradingVolume":1.269248E8},{"month":8,"value":32.6,"matchedTradingVolume":1.849013E8},{"month":9,"value":33.2,"matchedTradingVolume":1.252328E8},{"month":10,"value":29.95,"matchedTradingVolume":6.47939E7},{"month":11,"value":30.25,"matchedTradingVolume":6.29258E7},{"month":12,"value":27.1,"matchedTradingVolume":7.30158E7}],"dividendSpitingHistories":[]},{"symbol":"FPT","companyName":"CTCP FPT","type":"VN30","year":2023,"prices":[{"month":1,"value":84.0,"matchedTradingVolume":1.49761E7},{"month":2,"value":82.8,"matchedTradingVolume":1.6827E7},{"month":3,"value":80.6,"matchedTradingVolume":1.51259E7},{"month":4,"value":80.9,"matchedTradingVolume":1.11001E7},{"month":5,"value":84.1,"matchedTradingVolume":1.65431E7},{"month":6,"value":87.3,"matchedTradingVolume":1.93342E7},{"month":7,"value":87.0,"matchedTradingVolume":2.72301E7},{"month":8,"value":96.7,"matchedTradingVolume":4.53975E7},{"month":9,"value":99.0,"matchedTradingVolume":5.49667E7},{"month":10,"value":97.0,"matchedTradingVolume":5.85186E7},{"month":11,"value":93.0,"matchedTradingVolume":4.69906E7},{"month":12,"value":97.2,"matchedTradingVolume":4.36497E7}],"dividendSpitingHistories":[{"month":8,"value":1000.0}]},{"symbol":"GAS","companyName":"Tổng Công ty Khí Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":108.2,"matchedTradingVolume":3892900.0},{"month":2,"value":109.0,"matchedTradingVolume":4822000.0},{"month":3,"value":108.1,"matchedTradingVolume":4192400.0},{"month":4,"value":102.5,"matchedTradingVolume":6178600.0},{"month":5,"value":94.9,"matchedTradingVolume":7790900.0},{"month":6,"value":96.6,"matchedTradingVolume":1.45087E7},{"month":7,"value":101.6,"matchedTradingVolume":1.42296E7},{"month":8,"value":103.2,"matchedTradingVolume":1.20026E7},{"month":9,"value":110.0,"matchedTradingVolume":1.18793E7},{"month":10,"value":89.3,"matchedTradingVolume":1.23912E7},{"month":11,"value":80.1,"matchedTradingVolume":1.12482E7},{"month":12,"value":79.8,"matchedTradingVolume":1.5394E7}],"dividendSpitingHistories":[{"month":8,"value":3600.0}]},{"symbol":"GVR","companyName":"Tập đoàn Công nghiệp Cao su Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":16.85,"matchedTradingVolume":4.1546E7},{"month":2,"value":15.6,"matchedTradingVolume":3.46376E7},{"month":3,"value":15.5,"matchedTradingVolume":4.22057E7},{"month":4,"value":16.35,"matchedTradingVolume":4.92206E7},{"month":5,"value":18.4,"matchedTradingVolume":7.46486E7},{"month":6,"value":19.6,"matchedTradingVolume":8.05328E7},{"month":7,"value":22.35,"matchedTradingVolume":6.63856E7},{"month":8,"value":22.7,"matchedTradingVolume":6.33971E7},{"month":9,"value":23.2,"matchedTradingVolume":7.73157E7},{"month":10,"value":21.45,"matchedTradingVolume":6.5337E7},{"month":11,"value":20.15,"matchedTradingVolume":4.46305E7},{"month":12,"value":21.2,"matchedTradingVolume":3.96708E7}],"dividendSpitingHistories":[{"month":11,"value":350.0}]},{"symbol":"HDB","companyName":"Ngân hàng TMCP Phát triển TP. HCM","type":"VN30","year":2023,"prices":[{"month":1,"value":18.65,"matchedTradingVolume":3.22759E7},{"month":2,"value":19.0,"matchedTradingVolume":4.4446E7},{"month":3,"value":19.25,"matchedTradingVolume":5.77437E7},{"month":4,"value":19.7,"matchedTradingVolume":4.51794E7},{"month":5,"value":19.6,"matchedTradingVolume":3.38232E7},{"month":6,"value":19.2,"matchedTradingVolume":5.41306E7},{"month":7,"value":18.9,"matchedTradingVolume":6.66127E7},{"month":8,"value":17.55,"matchedTradingVolume":6.28059E7},{"month":9,"value":18.0,"matchedTradingVolume":1.529976E8},{"month":10,"value":17.75,"matchedTradingVolume":1.780465E8},{"month":11,"value":18.95,"matchedTradingVolume":1.868925E8},{"month":12,"value":20.3,"matchedTradingVolume":1.556088E8}],"dividendSpitingHistories":[{"month":5,"value":1000.0}]},{"symbol":"HPG","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":22.1,"matchedTradingVolume":4.281135E8},{"month":2,"value":21.9,"matchedTradingVolume":4.94953E8},{"month":3,"value":21.3,"matchedTradingVolume":4.610696E8},{"month":4,"value":22.0,"matchedTradingVolume":3.30845E8},{"month":5,"value":22.35,"matchedTradingVolume":3.350429E8},{"month":6,"value":26.6,"matchedTradingVolume":5.626958E8},{"month":7,"value":28.4,"matchedTradingVolume":4.653832E8},{"month":8,"value":28.15,"matchedTradingVolume":6.43047E8},{"month":9,"value":29.0,"matchedTradingVolume":6.05131E8},{"month":10,"value":26.2,"matchedTradingVolume":4.011388E8},{"month":11,"value":27.2,"matchedTradingVolume":5.466178E8},{"month":12,"value":27.95,"matchedTradingVolume":5.610034E8}],"dividendSpitingHistories":[]},{"symbol":"MBB","companyName":"Ngân hàng TMCP Quân Đội","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":1.510583E8},{"month":2,"value":18.95,"matchedTradingVolume":1.687588E8},{"month":3,"value":18.3,"matchedTradingVolume":1.717558E8},{"month":4,"value":18.8,"matchedTradingVolume":1.492544E8},{"month":5,"value":18.85,"matchedTradingVolume":1.334826E8},{"month":6,"value":20.7,"matchedTradingVolume":2.836777E8},{"month":7,"value":21.2,"matchedTradingVolume":2.36432E8},{"month":8,"value":19.35,"matchedTradingVolume":2.173509E8},{"month":9,"value":19.4,"matchedTradingVolume":2.572516E8},{"month":10,"value":18.6,"matchedTradingVolume":1.466942E8},{"month":11,"value":18.55,"matchedTradingVolume":1.853708E8},{"month":12,"value":18.65,"matchedTradingVolume":1.511428E8}],"dividendSpitingHistories":[{"month":6,"value":500.0}]},{"symbol":"MSN","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":103.7,"matchedTradingVolume":8950100.0},{"month":2,"value":96.7,"matchedTradingVolume":1.24483E7},{"month":3,"value":84.7,"matchedTradingVolume":2.91468E7},{"month":4,"value":79.5,"matchedTradingVolume":2.07545E7},{"month":5,"value":74.4,"matchedTradingVolume":1.62996E7},{"month":6,"value":78.8,"matchedTradingVolume":3.0083E7},{"month":7,"value":87.3,"matchedTradingVolume":3.79388E7},{"month":8,"value":89.2,"matchedTradingVolume":5.02759E7},{"month":9,"value":82.7,"matchedTradingVolume":3.77362E7},{"month":10,"value":77.4,"matchedTradingVolume":4.0633E7},{"month":11,"value":66.0,"matchedTradingVolume":3.84334E7},{"month":12,"value":67.5,"matchedTradingVolume":5.12021E7}],"dividendSpitingHistories":[]},{"symbol":"MWG","companyName":"CTCP Đầu tư Thế giới Di động","type":"VN30","year":2023,"prices":[{"month":1,"value":46.5,"matchedTradingVolume":3.38651E7},{"month":2,"value":49.9,"matchedTradingVolume":4.56642E7},{"month":3,"value":40.8,"matchedTradingVolume":4.16636E7},{"month":4,"value":41.05,"matchedTradingVolume":5.23766E7},{"month":5,"value":39.4,"matchedTradingVolume":3.71724E7},{"month":6,"value":44.35,"matchedTradingVolume":8.65595E7},{"month":7,"value":54.5,"matchedTradingVolume":1.189389E8},{"month":8,"value":54.2,"matchedTradingVolume":1.698499E8},{"month":9,"value":57.5,"matchedTradingVolume":1.511657E8},{"month":10,"value":51.9,"matchedTradingVolume":1.695161E8},{"month":11,"value":41.9,"matchedTradingVolume":2.478952E8},{"month":12,"value":43.05,"matchedTradingVolume":1.675436E8}],"dividendSpitingHistories":[{"month":7,"value":500.0}]},{"symbol":"PLX","companyName":"Tập đoàn Xăng Dầu Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":38.1,"matchedTradingVolume":1.25733E7},{"month":2,"value":40.6,"matchedTradingVolume":1.61479E7},{"month":3,"value":39.0,"matchedTradingVolume":2.69045E7},{"month":4,"value":38.05,"matchedTradingVolume":1.50825E7},{"month":5,"value":38.05,"matchedTradingVolume":1.33605E7},{"month":6,"value":39.1,"matchedTradingVolume":1.56871E7},{"month":7,"value":41.8,"matchedTradingVolume":3.82708E7},{"month":8,"value":41.0,"matchedTradingVolume":3.29293E7},{"month":9,"value":40.4,"matchedTradingVolume":2.22712E7},{"month":10,"value":37.5,"matchedTradingVolume":2.2156E7},{"month":11,"value":35.8,"matchedTradingVolume":1.91929E7},{"month":12,"value":35.9,"matchedTradingVolume":1.31123E7}],"dividendSpitingHistories":[{"month":9,"value":700.0}]},{"symbol":"POW","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":12.4,"matchedTradingVolume":1.438163E8},{"month":2,"value":12.65,"matchedTradingVolume":1.506917E8},{"month":3,"value":13.5,"matchedTradingVolume":2.060467E8},{"month":4,"value":13.65,"matchedTradingVolume":1.477345E8},{"month":5,"value":13.65,"matchedTradingVolume":1.43022E8},{"month":6,"value":13.95,"matchedTradingVolume":1.552269E8},{"month":7,"value":13.7,"matchedTradingVolume":1.968232E8},{"month":8,"value":14.1,"matchedTradingVolume":2.620184E8},{"month":9,"value":13.0,"matchedTradingVolume":1.309333E8},{"month":10,"value":11.75,"matchedTradingVolume":1.067952E8},{"month":11,"value":11.9,"matchedTradingVolume":1.264731E8},{"month":12,"value":11.65,"matchedTradingVolume":8.40602E7}],"dividendSpitingHistories":[]},{"symbol":"SAB","companyName":"Tổng Công ty cổ phần Bia - Rượu - Nước giải khát Sài Gòn","type":"VN30","year":2023,"prices":[{"month":1,"value":193.1,"matchedTradingVolume":2013100.0},{"month":2,"value":197.2,"matchedTradingVolume":1559600.0},{"month":3,"value":192.5,"matchedTradingVolume":3412700.0},{"month":4,"value":181.0,"matchedTradingVolume":3651800.0},{"month":5,"value":166.6,"matchedTradingVolume":2221900.0},{"month":6,"value":162.0,"matchedTradingVolume":3096200.0},{"month":7,"value":161.6,"matchedTradingVolume":3568900.0},{"month":8,"value":161.6,"matchedTradingVolume":6019000.0},{"month":9,"value":168.9,"matchedTradingVolume":9361900.0},{"month":10,"value":73.0,"matchedTradingVolume":9713900.0},{"month":11,"value":66.2,"matchedTradingVolume":1.61096E7},{"month":12,"value":65.6,"matchedTradingVolume":1.22324E7}],"dividendSpitingHistories":[{"month":3,"value":1000.0},{"month":6,"value":1500.0}]},{"symbol":"SHB","companyName":"Ngân hàng TMCP Sài Gòn - Hà Nội","type":"VN30","year":2023,"prices":[{"month":1,"value":11.2,"matchedTradingVolume":2.939803E8},{"month":2,"value":10.6,"matchedTradingVolume":2.209531E8},{"month":3,"value":10.85,"matchedTradingVolume":3.662555E8},{"month":4,"value":12.2,"matchedTradingVolume":6.056328E8},{"month":5,"value":12.0,"matchedTradingVolume":4.061201E8},{"month":6,"value":12.85,"matchedTradingVolume":6.039741E8},{"month":7,"value":14.4,"matchedTradingVolume":4.546979E8},{"month":8,"value":13.45,"matchedTradingVolume":4.740001E8},{"month":9,"value":12.75,"matchedTradingVolume":4.439107E8},{"month":10,"value":11.05,"matchedTradingVolume":2.494628E8},{"month":11,"value":11.6,"matchedTradingVolume":3.637048E8},{"month":12,"value":11.15,"matchedTradingVolume":3.281995E8}],"dividendSpitingHistories":[]},{"symbol":"SSI","companyName":"CTCP Chứng khoán SSI","type":"VN30","year":2023,"prices":[{"month":1,"value":21.6,"matchedTradingVolume":2.43128E8},{"month":2,"value":20.75,"matchedTradingVolume":2.701936E8},{"month":3,"value":21.5,"matchedTradingVolume":3.972755E8},{"month":4,"value":22.6,"matchedTradingVolume":4.024856E8},{"month":5,"value":23.4,"matchedTradingVolume":3.739481E8},{"month":6,"value":26.6,"matchedTradingVolume":4.523384E8},{"month":7,"value":29.75,"matchedTradingVolume":3.768438E8},{"month":8,"value":33.5,"matchedTradingVolume":6.115069E8},{"month":9,"value":36.45,"matchedTradingVolume":5.979921E8},{"month":10,"value":34.0,"matchedTradingVolume":5.601314E8},{"month":11,"value":32.9,"matchedTradingVolume":5.212175E8},{"month":12,"value":33.6,"matchedTradingVolume":3.923282E8}],"dividendSpitingHistories":[{"month":6,"value":1000.0}]},{"symbol":"STB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":27.1,"matchedTradingVolume":2.330793E8},{"month":2,"value":26.15,"matchedTradingVolume":3.772336E8},{"month":3,"value":26.5,"matchedTradingVolume":4.59574E8},{"month":4,"value":26.9,"matchedTradingVolume":3.08058E8},{"month":5,"value":28.15,"matchedTradingVolume":3.174901E8},{"month":6,"value":30.3,"matchedTradingVolume":3.506546E8},{"month":7,"value":30.0,"matchedTradingVolume":4.686863E8},{"month":8,"value":32.9,"matchedTradingVolume":6.076624E8},{"month":9,"value":33.3,"matchedTradingVolume":4.282722E8},{"month":10,"value":31.75,"matchedTradingVolume":3.745102E8},{"month":11,"value":30.2,"matchedTradingVolume":3.661731E8},{"month":12,"value":28.55,"matchedTradingVolume":3.171983E8}],"dividendSpitingHistories":[]},{"symbol":"TCB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":29.4,"matchedTradingVolume":6.18252E7},{"month":2,"value":28.6,"matchedTradingVolume":6.10217E7},{"month":3,"value":28.35,"matchedTradingVolume":6.78293E7},{"month":4,"value":30.7,"matchedTradingVolume":9.0173E7},{"month":5,"value":30.5,"matchedTradingVolume":6.91356E7},{"month":6,"value":33.3,"matchedTradingVolume":1.050967E8},{"month":7,"value":34.3,"matchedTradingVolume":1.146862E8},{"month":8,"value":35.3,"matchedTradingVolume":1.43969E8},{"month":9,"value":35.75,"matchedTradingVolume":1.089254E8},{"month":10,"value":33.15,"matchedTradingVolume":7.11959E7},{"month":11,"value":31.8,"matchedTradingVolume":7.9431E7},{"month":12,"value":31.8,"matchedTradingVolume":5.98825E7}],"dividendSpitingHistories":[]},{"symbol":"TPB","companyName":"Ngân hàng TMCP Tiên Phong","type":"VN30","year":2023,"prices":[{"month":1,"value":25.0,"matchedTradingVolume":1.168169E8},{"month":2,"value":24.8,"matchedTradingVolume":1.293128E8},{"month":3,"value":25.3,"matchedTradingVolume":9.12826E7},{"month":4,"value":23.8,"matchedTradingVolume":8.51845E7},{"month":5,"value":25.0,"matchedTradingVolume":6.7704E7},{"month":6,"value":26.3,"matchedTradingVolume":1.226153E8},{"month":7,"value":19.0,"matchedTradingVolume":1.497795E8},{"month":8,"value":19.6,"matchedTradingVolume":1.981773E8},{"month":9,"value":19.75,"matchedTradingVolume":1.483994E8},{"month":10,"value":17.5,"matchedTradingVolume":9.66153E7},{"month":11,"value":17.7,"matchedTradingVolume":1.206297E8},{"month":12,"value":17.55,"matchedTradingVolume":1.051146E8}],"dividendSpitingHistories":[{"month":3,"value":2500.0}]},{"symbol":"VCB","companyName":"Ngân hàng TMCP Ngoại thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":93.0,"matchedTradingVolume":1.95707E7},{"month":2,"value":96.0,"matchedTradingVolume":1.77834E7},{"month":3,"value":93.2,"matchedTradingVolume":2.03676E7},{"month":4,"value":92.8,"matchedTradingVolume":1.05433E7},{"month":5,"value":95.0,"matchedTradingVolume":1.21852E7},{"month":6,"value":105.0,"matchedTradingVolume":1.97517E7},{"month":7,"value":106.5,"matchedTradingVolume":2.00989E7},{"month":8,"value":91.5,"matchedTradingVolume":3.03631E7},{"month":9,"value":90.2,"matchedTradingVolume":2.82153E7},{"month":10,"value":86.8,"matchedTradingVolume":1.90875E7},{"month":11,"value":89.5,"matchedTradingVolume":2.49941E7},{"month":12,"value":86.0,"matchedTradingVolume":2.70841E7}],"dividendSpitingHistories":[]},{"symbol":"VHM","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":53.3,"matchedTradingVolume":2.15012E7},{"month":2,"value":48.1,"matchedTradingVolume":5.98349E7},{"month":3,"value":51.5,"matchedTradingVolume":5.67558E7},{"month":4,"value":52.6,"matchedTradingVolume":3.09891E7},{"month":5,"value":55.5,"matchedTradingVolume":3.01862E7},{"month":6,"value":57.0,"matchedTradingVolume":3.66415E7},{"month":7,"value":63.0,"matchedTradingVolume":5.51829E7},{"month":8,"value":63.0,"matchedTradingVolume":1.229843E8},{"month":9,"value":55.9,"matchedTradingVolume":1.448709E8},{"month":10,"value":48.0,"matchedTradingVolume":1.006912E8},{"month":11,"value":42.9,"matchedTradingVolume":1.672199E8},{"month":12,"value":43.7,"matchedTradingVolume":1.506395E8}],"dividendSpitingHistories":[]},{"symbol":"VIB","companyName":"Ngân hàng TMCP Quốc tế Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":23.55,"matchedTradingVolume":6.51873E7},{"month":2,"value":24.3,"matchedTradingVolume":6.42993E7},{"month":3,"value":21.4,"matchedTradingVolume":8.48303E7},{"month":4,"value":22.1,"matchedTradingVolume":7.98868E7},{"month":5,"value":21.6,"matchedTradingVolume":9.82021E7},{"month":6,"value":23.6,"matchedTradingVolume":1.718345E8},{"month":7,"value":21.0,"matchedTradingVolume":9.72921E7},{"month":8,"value":21.4,"matchedTradingVolume":1.057553E8},{"month":9,"value":21.7,"matchedTradingVolume":1.414188E8},{"month":10,"value":19.65,"matchedTradingVolume":7.06346E7},{"month":11,"value":19.65,"matchedTradingVolume":6.65855E7},{"month":12,"value":19.65,"matchedTradingVolume":7.1574E7}],"dividendSpitingHistories":[{"month":2,"value":1000.0},{"month":4,"value":500.0}]},{"symbol":"VIC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":59.2,"matchedTradingVolume":2.56029E7},{"month":2,"value":56.0,"matchedTradingVolume":3.974E7},{"month":3,"value":55.0,"matchedTradingVolume":3.25647E7},{"month":4,"value":58.0,"matchedTradingVolume":4.44255E7},{"month":5,"value":54.4,"matchedTradingVolume":3.62615E7},{"month":6,"value":54.1,"matchedTradingVolume":4.21094E7},{"month":7,"value":55.1,"matchedTradingVolume":6.40446E7},{"month":8,"value":75.6,"matchedTradingVolume":3.762692E8},{"month":9,"value":62.3,"matchedTradingVolume":2.936844E8},{"month":10,"value":46.9,"matchedTradingVolume":1.483437E8},{"month":11,"value":45.4,"matchedTradingVolume":9.69235E7},{"month":12,"value":44.6,"matchedTradingVolume":6.27363E7}],"dividendSpitingHistories":[]},{"symbol":"VJC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":116.3,"matchedTradingVolume":5537500.0},{"month":2,"value":113.9,"matchedTradingVolume":5160700.0},{"month":3,"value":108.9,"matchedTradingVolume":6564900.0},{"month":4,"value":103.0,"matchedTradingVolume":3872700.0},{"month":5,"value":99.5,"matchedTradingVolume":1.26274E7},{"month":6,"value":97.7,"matchedTradingVolume":1.6206E7},{"month":7,"value":102.0,"matchedTradingVolume":1.96767E7},{"month":8,"value":103.0,"matchedTradingVolume":2.02222E7},{"month":9,"value":101.9,"matchedTradingVolume":2.19183E7},{"month":10,"value":105.2,"matchedTradingVolume":2.09001E7},{"month":11,"value":113.0,"matchedTradingVolume":2.00095E7},{"month":12,"value":108.0,"matchedTradingVolume":2.01093E7}],"dividendSpitingHistories":[]},{"symbol":"VNM","companyName":"CTCP Sữa Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":81.3,"matchedTradingVolume":2.71532E7},{"month":2,"value":77.5,"matchedTradingVolume":2.8004E7},{"month":3,"value":77.1,"matchedTradingVolume":3.09558E7},{"month":4,"value":74.7,"matchedTradingVolume":2.10868E7},{"month":5,"value":70.7,"matchedTradingVolume":3.00439E7},{"month":6,"value":71.9,"matchedTradingVolume":1.092673E8},{"month":7,"value":78.0,"matchedTradingVolume":9.18289E7},{"month":8,"value":77.9,"matchedTradingVolume":8.24544E7},{"month":9,"value":80.3,"matchedTradingVolume":5.63057E7},{"month":10,"value":75.8,"matchedTradingVolume":4.31485E7},{"month":11,"value":71.4,"matchedTradingVolume":4.87116E7},{"month":12,"value":70.0,"matchedTradingVolume":5.76954E7}],"dividendSpitingHistories":[{"month":8,"value":1500.0},{"month":8,"value":1500.0},{"month":12,"value":500.0}]},{"symbol":"VPB","companyName":"Ngân hàng TMCP Việt Nam Thịnh Vượng","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":3.624271E8},{"month":2,"value":18.5,"matchedTradingVolume":3.291333E8},{"month":3,"value":21.25,"matchedTradingVolume":4.78505E8},{"month":4,"value":21.4,"matchedTradingVolume":2.156825E8},{"month":5,"value":19.8,"matchedTradingVolume":1.600067E8},{"month":6,"value":20.25,"matchedTradingVolume":3.597209E8},{"month":7,"value":22.15,"matchedTradingVolume":4.10663E8},{"month":8,"value":22.65,"matchedTradingVolume":4.072212E8},{"month":9,"value":22.55,"matchedTradingVolume":3.543629E8},{"month":10,"value":22.7,"matchedTradingVolume":2.767039E8},{"month":11,"value":21.35,"matchedTradingVolume":2.212622E8},{"month":12,"value":19.65,"matchedTradingVolume":2.219054E8}],"dividendSpitingHistories":[{"month":11,"value":1000.0}]},{"symbol":"VRE","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":30.3,"matchedTradingVolume":2.95246E7},{"month":2,"value":29.6,"matchedTradingVolume":3.32765E7},{"month":3,"value":29.9,"matchedTradingVolume":7.12347E7},{"month":4,"value":29.6,"matchedTradingVolume":4.78106E7},{"month":5,"value":28.4,"matchedTradingVolume":5.91646E7},{"month":6,"value":27.45,"matchedTradingVolume":7.98341E7},{"month":7,"value":29.65,"matchedTradingVolume":1.388173E8},{"month":8,"value":31.5,"matchedTradingVolume":1.701563E8},{"month":9,"value":30.3,"matchedTradingVolume":9.07252E7},{"month":10,"value":27.45,"matchedTradingVolume":7.55509E7},{"month":11,"value":24.4,"matchedTradingVolume":1.089259E8},{"month":12,"value":23.65,"matchedTradingVolume":7.37884E7}],"dividendSpitingHistories":[]}]}'
# futureData = loadDataInput(jsonInput2023)
# log_times = []
# log_dn = []
# log_gn = []
# log_fitnesses = []
# fitness_pivot = []
# ga(futureData, True, True, log_dn, log_gn, log_fitnesses, fitness_pivot)
# myPrint('DONE')
### end debug point


def experiment(futureData, isNSGA_III, isHybrid, log_times, log_dn, log_gn, log_fitnesses, fitness_pivot):
    start_time = time.time()
    ga(futureData, isNSGA_III, isHybrid, log_dn, log_gn, log_fitnesses, fitness_pivot)
    delta_time = time.time() - start_time
    printSolution("--- %s seconds ---" % (delta_time))
    log_times.append(delta_time)


def exe_experiments(futureData):
    # experimentPool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    # log_times = []
    # log_dn = []
    # log_gn = []
    # log_fitnesses = []
    # fitness_pivot = []
    # for _ in range(EXPERIMENT_TIMES_NUMS):
    #     experimentPool.submit(experiment, futureData, False, False, log_times, log_dn, log_gn, log_fitnesses, fitness_pivot)
    #
    # experimentPool.shutdown(wait=True)
    # print(log_times)
    # print(log_dn)
    # print(log_gn)
    # print(log_fitnesses)
    # print(fitness_pivot)
    # printSolution('DONE GA!!')

    experimentPool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    log_times = []
    log_dn = []
    log_gn = []
    log_fitnesses = []
    fitness_pivot = []
    for _ in range(EXPERIMENT_TIMES_NUMS):
        experimentPool.submit(experiment, futureData, True, False, log_times, log_dn, log_gn, log_fitnesses, fitness_pivot)

    experimentPool.shutdown(wait=True)
    print(log_times)
    print(log_dn)
    print(log_gn)
    print(log_fitnesses)
    print(fitness_pivot)
    printSolution('DONE NSGA-III!!')

    # experimentPool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    # log_times = []
    # log_dn = []
    # log_gn = []
    # log_fitnesses = []
    # fitness_pivot = []
    # for _ in range(EXPERIMENT_TIMES_NUMS):
    #     experimentPool.submit(experiment, futureData, True, True, log_times, log_dn, log_gn, log_fitnesses, fitness_pivot)
    #
    # experimentPool.shutdown(wait=True)
    # print(log_times)
    # print(log_dn)
    # print(log_gn)
    # print(log_fitnesses)
    # print(fitness_pivot)
    # printSolution('DONE HYBRID SA-GA!!')

# M2 = np.load("data/calculate2023/vn30_3years_before/M2.dat", allow_pickle=True)
# M3 = np.load("data/calculate2023/vn30_3years_before/M3.dat", allow_pickle=True)
# M4 = np.load("data/calculate2023/vn30_3years_before/M4.dat", allow_pickle=True)
# jsonInput2023 = '{"stocks":[{"symbol":"ACB","companyName":"Ngân hàng TMCP Á Châu","type":"VN30","year":2023,"prices":[{"month":1,"value":26.35,"matchedTradingVolume":5.499E7},{"month":2,"value":25.8,"matchedTradingVolume":6.3237E7},{"month":3,"value":25.35,"matchedTradingVolume":9.20633E7},{"month":4,"value":25.3,"matchedTradingVolume":8.14876E7},{"month":5,"value":25.4,"matchedTradingVolume":1.608784E8},{"month":6,"value":22.3,"matchedTradingVolume":1.920848E8},{"month":7,"value":22.95,"matchedTradingVolume":1.640575E8},{"month":8,"value":24.4,"matchedTradingVolume":2.570596E8},{"month":9,"value":22.95,"matchedTradingVolume":1.263825E8},{"month":10,"value":22.8,"matchedTradingVolume":1.01492E8},{"month":11,"value":23.3,"matchedTradingVolume":1.540952E8},{"month":12,"value":23.9,"matchedTradingVolume":1.309384E8}],"dividendSpitingHistories":[]},{"symbol":"BCM","companyName":"Tổng Công ty Đầu tư và Phát triển Công nghiệp – CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":85.2,"matchedTradingVolume":1681700.0},{"month":2,"value":86.0,"matchedTradingVolume":1668200.0},{"month":3,"value":84.5,"matchedTradingVolume":2201700.0},{"month":4,"value":83.5,"matchedTradingVolume":1124200.0},{"month":5,"value":78.5,"matchedTradingVolume":1003200.0},{"month":6,"value":82.1,"matchedTradingVolume":6718400.0},{"month":7,"value":81.0,"matchedTradingVolume":5792000.0},{"month":8,"value":79.0,"matchedTradingVolume":5927500.0},{"month":9,"value":72.6,"matchedTradingVolume":5679800.0},{"month":10,"value":69.5,"matchedTradingVolume":4024400.0},{"month":11,"value":62.4,"matchedTradingVolume":6680300.0},{"month":12,"value":66.0,"matchedTradingVolume":1.05481E7}],"dividendSpitingHistories":[{"month":11,"value":800.0}]},{"symbol":"BID","companyName":"Ngân hàng TMCP Đầu tư và Phát triển Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":45.95,"matchedTradingVolume":2.88095E7},{"month":2,"value":47.2,"matchedTradingVolume":2.70027E7},{"month":3,"value":48.0,"matchedTradingVolume":1.78979E7},{"month":4,"value":46.0,"matchedTradingVolume":1.53768E7},{"month":5,"value":45.1,"matchedTradingVolume":1.2405E7},{"month":6,"value":45.35,"matchedTradingVolume":2.61229E7},{"month":7,"value":47.35,"matchedTradingVolume":3.93465E7},{"month":8,"value":49.1,"matchedTradingVolume":4.26147E7},{"month":9,"value":47.5,"matchedTradingVolume":2.19276E7},{"month":10,"value":43.95,"matchedTradingVolume":2.0611E7},{"month":11,"value":44.15,"matchedTradingVolume":1.78062E7},{"month":12,"value":43.4,"matchedTradingVolume":2.24373E7}],"dividendSpitingHistories":[]},{"symbol":"BVH","companyName":"Tập đoàn Bảo Việt","type":"VN30","year":2023,"prices":[{"month":1,"value":51.0,"matchedTradingVolume":7621200.0},{"month":2,"value":51.2,"matchedTradingVolume":9028400.0},{"month":3,"value":50.0,"matchedTradingVolume":5479800.0},{"month":4,"value":49.2,"matchedTradingVolume":5394500.0},{"month":5,"value":46.0,"matchedTradingVolume":1.05267E7},{"month":6,"value":45.3,"matchedTradingVolume":2.13723E7},{"month":7,"value":48.15,"matchedTradingVolume":2.26194E7},{"month":8,"value":48.0,"matchedTradingVolume":1.95543E7},{"month":9,"value":45.8,"matchedTradingVolume":1.30652E7},{"month":10,"value":42.65,"matchedTradingVolume":6368600.0},{"month":11,"value":41.3,"matchedTradingVolume":6801500.0},{"month":12,"value":40.5,"matchedTradingVolume":6636100.0}],"dividendSpitingHistories":[{"month":11,"value":954.0}]},{"symbol":"CTG","companyName":"Ngân hàng TMCP Công Thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":31.1,"matchedTradingVolume":6.19356E7},{"month":2,"value":30.45,"matchedTradingVolume":5.62202E7},{"month":3,"value":29.5,"matchedTradingVolume":4.62949E7},{"month":4,"value":30.0,"matchedTradingVolume":4.04912E7},{"month":5,"value":28.4,"matchedTradingVolume":7.05504E7},{"month":6,"value":30.0,"matchedTradingVolume":1.20986E8},{"month":7,"value":30.3,"matchedTradingVolume":1.269248E8},{"month":8,"value":32.6,"matchedTradingVolume":1.849013E8},{"month":9,"value":33.2,"matchedTradingVolume":1.252328E8},{"month":10,"value":29.95,"matchedTradingVolume":6.47939E7},{"month":11,"value":30.25,"matchedTradingVolume":6.29258E7},{"month":12,"value":27.1,"matchedTradingVolume":7.30158E7}],"dividendSpitingHistories":[]},{"symbol":"FPT","companyName":"CTCP FPT","type":"VN30","year":2023,"prices":[{"month":1,"value":84.0,"matchedTradingVolume":1.49761E7},{"month":2,"value":82.8,"matchedTradingVolume":1.6827E7},{"month":3,"value":80.6,"matchedTradingVolume":1.51259E7},{"month":4,"value":80.9,"matchedTradingVolume":1.11001E7},{"month":5,"value":84.1,"matchedTradingVolume":1.65431E7},{"month":6,"value":87.3,"matchedTradingVolume":1.93342E7},{"month":7,"value":87.0,"matchedTradingVolume":2.72301E7},{"month":8,"value":96.7,"matchedTradingVolume":4.53975E7},{"month":9,"value":99.0,"matchedTradingVolume":5.49667E7},{"month":10,"value":97.0,"matchedTradingVolume":5.85186E7},{"month":11,"value":93.0,"matchedTradingVolume":4.69906E7},{"month":12,"value":97.2,"matchedTradingVolume":4.36497E7}],"dividendSpitingHistories":[{"month":8,"value":1000.0}]},{"symbol":"GAS","companyName":"Tổng Công ty Khí Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":108.2,"matchedTradingVolume":3892900.0},{"month":2,"value":109.0,"matchedTradingVolume":4822000.0},{"month":3,"value":108.1,"matchedTradingVolume":4192400.0},{"month":4,"value":102.5,"matchedTradingVolume":6178600.0},{"month":5,"value":94.9,"matchedTradingVolume":7790900.0},{"month":6,"value":96.6,"matchedTradingVolume":1.45087E7},{"month":7,"value":101.6,"matchedTradingVolume":1.42296E7},{"month":8,"value":103.2,"matchedTradingVolume":1.20026E7},{"month":9,"value":110.0,"matchedTradingVolume":1.18793E7},{"month":10,"value":89.3,"matchedTradingVolume":1.23912E7},{"month":11,"value":80.1,"matchedTradingVolume":1.12482E7},{"month":12,"value":79.8,"matchedTradingVolume":1.5394E7}],"dividendSpitingHistories":[{"month":8,"value":3600.0}]},{"symbol":"GVR","companyName":"Tập đoàn Công nghiệp Cao su Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":16.85,"matchedTradingVolume":4.1546E7},{"month":2,"value":15.6,"matchedTradingVolume":3.46376E7},{"month":3,"value":15.5,"matchedTradingVolume":4.22057E7},{"month":4,"value":16.35,"matchedTradingVolume":4.92206E7},{"month":5,"value":18.4,"matchedTradingVolume":7.46486E7},{"month":6,"value":19.6,"matchedTradingVolume":8.05328E7},{"month":7,"value":22.35,"matchedTradingVolume":6.63856E7},{"month":8,"value":22.7,"matchedTradingVolume":6.33971E7},{"month":9,"value":23.2,"matchedTradingVolume":7.73157E7},{"month":10,"value":21.45,"matchedTradingVolume":6.5337E7},{"month":11,"value":20.15,"matchedTradingVolume":4.46305E7},{"month":12,"value":21.2,"matchedTradingVolume":3.96708E7}],"dividendSpitingHistories":[{"month":11,"value":350.0}]},{"symbol":"HDB","companyName":"Ngân hàng TMCP Phát triển TP. HCM","type":"VN30","year":2023,"prices":[{"month":1,"value":18.65,"matchedTradingVolume":3.22759E7},{"month":2,"value":19.0,"matchedTradingVolume":4.4446E7},{"month":3,"value":19.25,"matchedTradingVolume":5.77437E7},{"month":4,"value":19.7,"matchedTradingVolume":4.51794E7},{"month":5,"value":19.6,"matchedTradingVolume":3.38232E7},{"month":6,"value":19.2,"matchedTradingVolume":5.41306E7},{"month":7,"value":18.9,"matchedTradingVolume":6.66127E7},{"month":8,"value":17.55,"matchedTradingVolume":6.28059E7},{"month":9,"value":18.0,"matchedTradingVolume":1.529976E8},{"month":10,"value":17.75,"matchedTradingVolume":1.780465E8},{"month":11,"value":18.95,"matchedTradingVolume":1.868925E8},{"month":12,"value":20.3,"matchedTradingVolume":1.556088E8}],"dividendSpitingHistories":[{"month":5,"value":1000.0}]},{"symbol":"HPG","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":22.1,"matchedTradingVolume":4.281135E8},{"month":2,"value":21.9,"matchedTradingVolume":4.94953E8},{"month":3,"value":21.3,"matchedTradingVolume":4.610696E8},{"month":4,"value":22.0,"matchedTradingVolume":3.30845E8},{"month":5,"value":22.35,"matchedTradingVolume":3.350429E8},{"month":6,"value":26.6,"matchedTradingVolume":5.626958E8},{"month":7,"value":28.4,"matchedTradingVolume":4.653832E8},{"month":8,"value":28.15,"matchedTradingVolume":6.43047E8},{"month":9,"value":29.0,"matchedTradingVolume":6.05131E8},{"month":10,"value":26.2,"matchedTradingVolume":4.011388E8},{"month":11,"value":27.2,"matchedTradingVolume":5.466178E8},{"month":12,"value":27.95,"matchedTradingVolume":5.610034E8}],"dividendSpitingHistories":[]},{"symbol":"MBB","companyName":"Ngân hàng TMCP Quân Đội","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":1.510583E8},{"month":2,"value":18.95,"matchedTradingVolume":1.687588E8},{"month":3,"value":18.3,"matchedTradingVolume":1.717558E8},{"month":4,"value":18.8,"matchedTradingVolume":1.492544E8},{"month":5,"value":18.85,"matchedTradingVolume":1.334826E8},{"month":6,"value":20.7,"matchedTradingVolume":2.836777E8},{"month":7,"value":21.2,"matchedTradingVolume":2.36432E8},{"month":8,"value":19.35,"matchedTradingVolume":2.173509E8},{"month":9,"value":19.4,"matchedTradingVolume":2.572516E8},{"month":10,"value":18.6,"matchedTradingVolume":1.466942E8},{"month":11,"value":18.55,"matchedTradingVolume":1.853708E8},{"month":12,"value":18.65,"matchedTradingVolume":1.511428E8}],"dividendSpitingHistories":[{"month":6,"value":500.0}]},{"symbol":"MSN","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":103.7,"matchedTradingVolume":8950100.0},{"month":2,"value":96.7,"matchedTradingVolume":1.24483E7},{"month":3,"value":84.7,"matchedTradingVolume":2.91468E7},{"month":4,"value":79.5,"matchedTradingVolume":2.07545E7},{"month":5,"value":74.4,"matchedTradingVolume":1.62996E7},{"month":6,"value":78.8,"matchedTradingVolume":3.0083E7},{"month":7,"value":87.3,"matchedTradingVolume":3.79388E7},{"month":8,"value":89.2,"matchedTradingVolume":5.02759E7},{"month":9,"value":82.7,"matchedTradingVolume":3.77362E7},{"month":10,"value":77.4,"matchedTradingVolume":4.0633E7},{"month":11,"value":66.0,"matchedTradingVolume":3.84334E7},{"month":12,"value":67.5,"matchedTradingVolume":5.12021E7}],"dividendSpitingHistories":[]},{"symbol":"MWG","companyName":"CTCP Đầu tư Thế giới Di động","type":"VN30","year":2023,"prices":[{"month":1,"value":46.5,"matchedTradingVolume":3.38651E7},{"month":2,"value":49.9,"matchedTradingVolume":4.56642E7},{"month":3,"value":40.8,"matchedTradingVolume":4.16636E7},{"month":4,"value":41.05,"matchedTradingVolume":5.23766E7},{"month":5,"value":39.4,"matchedTradingVolume":3.71724E7},{"month":6,"value":44.35,"matchedTradingVolume":8.65595E7},{"month":7,"value":54.5,"matchedTradingVolume":1.189389E8},{"month":8,"value":54.2,"matchedTradingVolume":1.698499E8},{"month":9,"value":57.5,"matchedTradingVolume":1.511657E8},{"month":10,"value":51.9,"matchedTradingVolume":1.695161E8},{"month":11,"value":41.9,"matchedTradingVolume":2.478952E8},{"month":12,"value":43.05,"matchedTradingVolume":1.675436E8}],"dividendSpitingHistories":[{"month":7,"value":500.0}]},{"symbol":"PLX","companyName":"Tập đoàn Xăng Dầu Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":38.1,"matchedTradingVolume":1.25733E7},{"month":2,"value":40.6,"matchedTradingVolume":1.61479E7},{"month":3,"value":39.0,"matchedTradingVolume":2.69045E7},{"month":4,"value":38.05,"matchedTradingVolume":1.50825E7},{"month":5,"value":38.05,"matchedTradingVolume":1.33605E7},{"month":6,"value":39.1,"matchedTradingVolume":1.56871E7},{"month":7,"value":41.8,"matchedTradingVolume":3.82708E7},{"month":8,"value":41.0,"matchedTradingVolume":3.29293E7},{"month":9,"value":40.4,"matchedTradingVolume":2.22712E7},{"month":10,"value":37.5,"matchedTradingVolume":2.2156E7},{"month":11,"value":35.8,"matchedTradingVolume":1.91929E7},{"month":12,"value":35.9,"matchedTradingVolume":1.31123E7}],"dividendSpitingHistories":[{"month":9,"value":700.0}]},{"symbol":"POW","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":12.4,"matchedTradingVolume":1.438163E8},{"month":2,"value":12.65,"matchedTradingVolume":1.506917E8},{"month":3,"value":13.5,"matchedTradingVolume":2.060467E8},{"month":4,"value":13.65,"matchedTradingVolume":1.477345E8},{"month":5,"value":13.65,"matchedTradingVolume":1.43022E8},{"month":6,"value":13.95,"matchedTradingVolume":1.552269E8},{"month":7,"value":13.7,"matchedTradingVolume":1.968232E8},{"month":8,"value":14.1,"matchedTradingVolume":2.620184E8},{"month":9,"value":13.0,"matchedTradingVolume":1.309333E8},{"month":10,"value":11.75,"matchedTradingVolume":1.067952E8},{"month":11,"value":11.9,"matchedTradingVolume":1.264731E8},{"month":12,"value":11.65,"matchedTradingVolume":8.40602E7}],"dividendSpitingHistories":[]},{"symbol":"SAB","companyName":"Tổng Công ty cổ phần Bia - Rượu - Nước giải khát Sài Gòn","type":"VN30","year":2023,"prices":[{"month":1,"value":193.1,"matchedTradingVolume":2013100.0},{"month":2,"value":197.2,"matchedTradingVolume":1559600.0},{"month":3,"value":192.5,"matchedTradingVolume":3412700.0},{"month":4,"value":181.0,"matchedTradingVolume":3651800.0},{"month":5,"value":166.6,"matchedTradingVolume":2221900.0},{"month":6,"value":162.0,"matchedTradingVolume":3096200.0},{"month":7,"value":161.6,"matchedTradingVolume":3568900.0},{"month":8,"value":161.6,"matchedTradingVolume":6019000.0},{"month":9,"value":168.9,"matchedTradingVolume":9361900.0},{"month":10,"value":73.0,"matchedTradingVolume":9713900.0},{"month":11,"value":66.2,"matchedTradingVolume":1.61096E7},{"month":12,"value":65.6,"matchedTradingVolume":1.22324E7}],"dividendSpitingHistories":[{"month":3,"value":1000.0},{"month":6,"value":1500.0}]},{"symbol":"SHB","companyName":"Ngân hàng TMCP Sài Gòn - Hà Nội","type":"VN30","year":2023,"prices":[{"month":1,"value":11.2,"matchedTradingVolume":2.939803E8},{"month":2,"value":10.6,"matchedTradingVolume":2.209531E8},{"month":3,"value":10.85,"matchedTradingVolume":3.662555E8},{"month":4,"value":12.2,"matchedTradingVolume":6.056328E8},{"month":5,"value":12.0,"matchedTradingVolume":4.061201E8},{"month":6,"value":12.85,"matchedTradingVolume":6.039741E8},{"month":7,"value":14.4,"matchedTradingVolume":4.546979E8},{"month":8,"value":13.45,"matchedTradingVolume":4.740001E8},{"month":9,"value":12.75,"matchedTradingVolume":4.439107E8},{"month":10,"value":11.05,"matchedTradingVolume":2.494628E8},{"month":11,"value":11.6,"matchedTradingVolume":3.637048E8},{"month":12,"value":11.15,"matchedTradingVolume":3.281995E8}],"dividendSpitingHistories":[]},{"symbol":"SSI","companyName":"CTCP Chứng khoán SSI","type":"VN30","year":2023,"prices":[{"month":1,"value":21.6,"matchedTradingVolume":2.43128E8},{"month":2,"value":20.75,"matchedTradingVolume":2.701936E8},{"month":3,"value":21.5,"matchedTradingVolume":3.972755E8},{"month":4,"value":22.6,"matchedTradingVolume":4.024856E8},{"month":5,"value":23.4,"matchedTradingVolume":3.739481E8},{"month":6,"value":26.6,"matchedTradingVolume":4.523384E8},{"month":7,"value":29.75,"matchedTradingVolume":3.768438E8},{"month":8,"value":33.5,"matchedTradingVolume":6.115069E8},{"month":9,"value":36.45,"matchedTradingVolume":5.979921E8},{"month":10,"value":34.0,"matchedTradingVolume":5.601314E8},{"month":11,"value":32.9,"matchedTradingVolume":5.212175E8},{"month":12,"value":33.6,"matchedTradingVolume":3.923282E8}],"dividendSpitingHistories":[{"month":6,"value":1000.0}]},{"symbol":"STB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":27.1,"matchedTradingVolume":2.330793E8},{"month":2,"value":26.15,"matchedTradingVolume":3.772336E8},{"month":3,"value":26.5,"matchedTradingVolume":4.59574E8},{"month":4,"value":26.9,"matchedTradingVolume":3.08058E8},{"month":5,"value":28.15,"matchedTradingVolume":3.174901E8},{"month":6,"value":30.3,"matchedTradingVolume":3.506546E8},{"month":7,"value":30.0,"matchedTradingVolume":4.686863E8},{"month":8,"value":32.9,"matchedTradingVolume":6.076624E8},{"month":9,"value":33.3,"matchedTradingVolume":4.282722E8},{"month":10,"value":31.75,"matchedTradingVolume":3.745102E8},{"month":11,"value":30.2,"matchedTradingVolume":3.661731E8},{"month":12,"value":28.55,"matchedTradingVolume":3.171983E8}],"dividendSpitingHistories":[]},{"symbol":"TCB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":29.4,"matchedTradingVolume":6.18252E7},{"month":2,"value":28.6,"matchedTradingVolume":6.10217E7},{"month":3,"value":28.35,"matchedTradingVolume":6.78293E7},{"month":4,"value":30.7,"matchedTradingVolume":9.0173E7},{"month":5,"value":30.5,"matchedTradingVolume":6.91356E7},{"month":6,"value":33.3,"matchedTradingVolume":1.050967E8},{"month":7,"value":34.3,"matchedTradingVolume":1.146862E8},{"month":8,"value":35.3,"matchedTradingVolume":1.43969E8},{"month":9,"value":35.75,"matchedTradingVolume":1.089254E8},{"month":10,"value":33.15,"matchedTradingVolume":7.11959E7},{"month":11,"value":31.8,"matchedTradingVolume":7.9431E7},{"month":12,"value":31.8,"matchedTradingVolume":5.98825E7}],"dividendSpitingHistories":[]},{"symbol":"TPB","companyName":"Ngân hàng TMCP Tiên Phong","type":"VN30","year":2023,"prices":[{"month":1,"value":25.0,"matchedTradingVolume":1.168169E8},{"month":2,"value":24.8,"matchedTradingVolume":1.293128E8},{"month":3,"value":25.3,"matchedTradingVolume":9.12826E7},{"month":4,"value":23.8,"matchedTradingVolume":8.51845E7},{"month":5,"value":25.0,"matchedTradingVolume":6.7704E7},{"month":6,"value":26.3,"matchedTradingVolume":1.226153E8},{"month":7,"value":19.0,"matchedTradingVolume":1.497795E8},{"month":8,"value":19.6,"matchedTradingVolume":1.981773E8},{"month":9,"value":19.75,"matchedTradingVolume":1.483994E8},{"month":10,"value":17.5,"matchedTradingVolume":9.66153E7},{"month":11,"value":17.7,"matchedTradingVolume":1.206297E8},{"month":12,"value":17.55,"matchedTradingVolume":1.051146E8}],"dividendSpitingHistories":[{"month":3,"value":2500.0}]},{"symbol":"VCB","companyName":"Ngân hàng TMCP Ngoại thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":93.0,"matchedTradingVolume":1.95707E7},{"month":2,"value":96.0,"matchedTradingVolume":1.77834E7},{"month":3,"value":93.2,"matchedTradingVolume":2.03676E7},{"month":4,"value":92.8,"matchedTradingVolume":1.05433E7},{"month":5,"value":95.0,"matchedTradingVolume":1.21852E7},{"month":6,"value":105.0,"matchedTradingVolume":1.97517E7},{"month":7,"value":106.5,"matchedTradingVolume":2.00989E7},{"month":8,"value":91.5,"matchedTradingVolume":3.03631E7},{"month":9,"value":90.2,"matchedTradingVolume":2.82153E7},{"month":10,"value":86.8,"matchedTradingVolume":1.90875E7},{"month":11,"value":89.5,"matchedTradingVolume":2.49941E7},{"month":12,"value":86.0,"matchedTradingVolume":2.70841E7}],"dividendSpitingHistories":[]},{"symbol":"VHM","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":53.3,"matchedTradingVolume":2.15012E7},{"month":2,"value":48.1,"matchedTradingVolume":5.98349E7},{"month":3,"value":51.5,"matchedTradingVolume":5.67558E7},{"month":4,"value":52.6,"matchedTradingVolume":3.09891E7},{"month":5,"value":55.5,"matchedTradingVolume":3.01862E7},{"month":6,"value":57.0,"matchedTradingVolume":3.66415E7},{"month":7,"value":63.0,"matchedTradingVolume":5.51829E7},{"month":8,"value":63.0,"matchedTradingVolume":1.229843E8},{"month":9,"value":55.9,"matchedTradingVolume":1.448709E8},{"month":10,"value":48.0,"matchedTradingVolume":1.006912E8},{"month":11,"value":42.9,"matchedTradingVolume":1.672199E8},{"month":12,"value":43.7,"matchedTradingVolume":1.506395E8}],"dividendSpitingHistories":[]},{"symbol":"VIB","companyName":"Ngân hàng TMCP Quốc tế Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":23.55,"matchedTradingVolume":6.51873E7},{"month":2,"value":24.3,"matchedTradingVolume":6.42993E7},{"month":3,"value":21.4,"matchedTradingVolume":8.48303E7},{"month":4,"value":22.1,"matchedTradingVolume":7.98868E7},{"month":5,"value":21.6,"matchedTradingVolume":9.82021E7},{"month":6,"value":23.6,"matchedTradingVolume":1.718345E8},{"month":7,"value":21.0,"matchedTradingVolume":9.72921E7},{"month":8,"value":21.4,"matchedTradingVolume":1.057553E8},{"month":9,"value":21.7,"matchedTradingVolume":1.414188E8},{"month":10,"value":19.65,"matchedTradingVolume":7.06346E7},{"month":11,"value":19.65,"matchedTradingVolume":6.65855E7},{"month":12,"value":19.65,"matchedTradingVolume":7.1574E7}],"dividendSpitingHistories":[{"month":2,"value":1000.0},{"month":4,"value":500.0}]},{"symbol":"VIC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":59.2,"matchedTradingVolume":2.56029E7},{"month":2,"value":56.0,"matchedTradingVolume":3.974E7},{"month":3,"value":55.0,"matchedTradingVolume":3.25647E7},{"month":4,"value":58.0,"matchedTradingVolume":4.44255E7},{"month":5,"value":54.4,"matchedTradingVolume":3.62615E7},{"month":6,"value":54.1,"matchedTradingVolume":4.21094E7},{"month":7,"value":55.1,"matchedTradingVolume":6.40446E7},{"month":8,"value":75.6,"matchedTradingVolume":3.762692E8},{"month":9,"value":62.3,"matchedTradingVolume":2.936844E8},{"month":10,"value":46.9,"matchedTradingVolume":1.483437E8},{"month":11,"value":45.4,"matchedTradingVolume":9.69235E7},{"month":12,"value":44.6,"matchedTradingVolume":6.27363E7}],"dividendSpitingHistories":[]},{"symbol":"VJC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":116.3,"matchedTradingVolume":5537500.0},{"month":2,"value":113.9,"matchedTradingVolume":5160700.0},{"month":3,"value":108.9,"matchedTradingVolume":6564900.0},{"month":4,"value":103.0,"matchedTradingVolume":3872700.0},{"month":5,"value":99.5,"matchedTradingVolume":1.26274E7},{"month":6,"value":97.7,"matchedTradingVolume":1.6206E7},{"month":7,"value":102.0,"matchedTradingVolume":1.96767E7},{"month":8,"value":103.0,"matchedTradingVolume":2.02222E7},{"month":9,"value":101.9,"matchedTradingVolume":2.19183E7},{"month":10,"value":105.2,"matchedTradingVolume":2.09001E7},{"month":11,"value":113.0,"matchedTradingVolume":2.00095E7},{"month":12,"value":108.0,"matchedTradingVolume":2.01093E7}],"dividendSpitingHistories":[]},{"symbol":"VNM","companyName":"CTCP Sữa Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":81.3,"matchedTradingVolume":2.71532E7},{"month":2,"value":77.5,"matchedTradingVolume":2.8004E7},{"month":3,"value":77.1,"matchedTradingVolume":3.09558E7},{"month":4,"value":74.7,"matchedTradingVolume":2.10868E7},{"month":5,"value":70.7,"matchedTradingVolume":3.00439E7},{"month":6,"value":71.9,"matchedTradingVolume":1.092673E8},{"month":7,"value":78.0,"matchedTradingVolume":9.18289E7},{"month":8,"value":77.9,"matchedTradingVolume":8.24544E7},{"month":9,"value":80.3,"matchedTradingVolume":5.63057E7},{"month":10,"value":75.8,"matchedTradingVolume":4.31485E7},{"month":11,"value":71.4,"matchedTradingVolume":4.87116E7},{"month":12,"value":70.0,"matchedTradingVolume":5.76954E7}],"dividendSpitingHistories":[{"month":8,"value":1500.0},{"month":8,"value":1500.0},{"month":12,"value":500.0}]},{"symbol":"VPB","companyName":"Ngân hàng TMCP Việt Nam Thịnh Vượng","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":3.624271E8},{"month":2,"value":18.5,"matchedTradingVolume":3.291333E8},{"month":3,"value":21.25,"matchedTradingVolume":4.78505E8},{"month":4,"value":21.4,"matchedTradingVolume":2.156825E8},{"month":5,"value":19.8,"matchedTradingVolume":1.600067E8},{"month":6,"value":20.25,"matchedTradingVolume":3.597209E8},{"month":7,"value":22.15,"matchedTradingVolume":4.10663E8},{"month":8,"value":22.65,"matchedTradingVolume":4.072212E8},{"month":9,"value":22.55,"matchedTradingVolume":3.543629E8},{"month":10,"value":22.7,"matchedTradingVolume":2.767039E8},{"month":11,"value":21.35,"matchedTradingVolume":2.212622E8},{"month":12,"value":19.65,"matchedTradingVolume":2.219054E8}],"dividendSpitingHistories":[{"month":11,"value":1000.0}]},{"symbol":"VRE","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":30.3,"matchedTradingVolume":2.95246E7},{"month":2,"value":29.6,"matchedTradingVolume":3.32765E7},{"month":3,"value":29.9,"matchedTradingVolume":7.12347E7},{"month":4,"value":29.6,"matchedTradingVolume":4.78106E7},{"month":5,"value":28.4,"matchedTradingVolume":5.91646E7},{"month":6,"value":27.45,"matchedTradingVolume":7.98341E7},{"month":7,"value":29.65,"matchedTradingVolume":1.388173E8},{"month":8,"value":31.5,"matchedTradingVolume":1.701563E8},{"month":9,"value":30.3,"matchedTradingVolume":9.07252E7},{"month":10,"value":27.45,"matchedTradingVolume":7.55509E7},{"month":11,"value":24.4,"matchedTradingVolume":1.089259E8},{"month":12,"value":23.65,"matchedTradingVolume":7.37884E7}],"dividendSpitingHistories":[]}]}'
# futureData = loadDataInput(jsonInput2023)
exe_experiments(stock_data)
# printSolution('DONE vn30_3years_before')


# M2 = np.load("data/calculate2023/hnx30_3years_before/M2.npy", allow_pickle=True)
# M3 = np.load("data/calculate2023/hnx30_3years_before/M3.npy", allow_pickle=True)
# M4 = np.load("data/calculate2023/hnx30_3years_before/M4.npy", allow_pickle=True)
# jsonInput2023 = '{"stocks":[{"symbol":"BCC","companyName":"CTCP Xi măng Bỉm Sơn","type":"HNX30","year":2023,"prices":[{"month":1,"value":11.6,"matchedTradingVolume":1.6898285E7},{"month":2,"value":12.7,"matchedTradingVolume":2.6045742E7},{"month":3,"value":12.4,"matchedTradingVolume":2.0300759E7},{"month":4,"value":12.4,"matchedTradingVolume":1.3811487E7},{"month":5,"value":13.3,"matchedTradingVolume":2.0730116E7},{"month":6,"value":14.5,"matchedTradingVolume":2.4793471E7},{"month":7,"value":14.6,"matchedTradingVolume":2.2653644E7},{"month":8,"value":14.6,"matchedTradingVolume":2.1295205E7},{"month":9,"value":13.0,"matchedTradingVolume":9862493.0},{"month":10,"value":12.2,"matchedTradingVolume":6465571.0},{"month":11,"value":9.8,"matchedTradingVolume":5608050.0},{"month":12,"value":9.6,"matchedTradingVolume":3821733.0}],"dividendSpitingHistories":[{"month":8,"value":500.0}]},{"symbol":"BVS","companyName":"CTCP Chứng khoán Bảo Việt","type":"HNX30","year":2023,"prices":[{"month":1,"value":21.0,"matchedTradingVolume":1438111.0},{"month":2,"value":19.0,"matchedTradingVolume":1854612.0},{"month":3,"value":19.1,"matchedTradingVolume":3134602.0},{"month":4,"value":20.2,"matchedTradingVolume":3958340.0},{"month":5,"value":23.8,"matchedTradingVolume":9386680.0},{"month":6,"value":25.3,"matchedTradingVolume":1.4453718E7},{"month":7,"value":27.0,"matchedTradingVolume":1.3688213E7},{"month":8,"value":28.8,"matchedTradingVolume":1.3880792E7},{"month":9,"value":30.7,"matchedTradingVolume":9906439.0},{"month":10,"value":26.9,"matchedTradingVolume":6689071.0},{"month":11,"value":26.0,"matchedTradingVolume":3668846.0},{"month":12,"value":26.1,"matchedTradingVolume":3959357.0}],"dividendSpitingHistories":[{"month":10,"value":1000.0}]},{"symbol":"CAP","companyName":"CTCP Lâm Nông sản Thực phẩm Yên Bái","type":"HNX30","year":2023,"prices":[{"month":1,"value":73.2,"matchedTradingVolume":113106.0},{"month":2,"value":76.3,"matchedTradingVolume":135358.0},{"month":3,"value":83.9,"matchedTradingVolume":136556.0},{"month":4,"value":91.5,"matchedTradingVolume":342827.0},{"month":5,"value":91.7,"matchedTradingVolume":400862.0},{"month":6,"value":70.3,"matchedTradingVolume":319155.0},{"month":7,"value":76.8,"matchedTradingVolume":848052.0},{"month":8,"value":74.4,"matchedTradingVolume":808393.0},{"month":9,"value":79.0,"matchedTradingVolume":720323.0},{"month":10,"value":84.3,"matchedTradingVolume":897248.0},{"month":11,"value":76.2,"matchedTradingVolume":420061.0},{"month":12,"value":78.4,"matchedTradingVolume":593973.0}],"dividendSpitingHistories":[]},{"symbol":"CEO","companyName":"CTCP Tập đoàn C.E.O","type":"HNX30","year":2023,"prices":[{"month":1,"value":24.6,"matchedTradingVolume":1.27064933E8},{"month":2,"value":23.4,"matchedTradingVolume":1.75287235E8},{"month":3,"value":22.2,"matchedTradingVolume":1.36584726E8},{"month":4,"value":25.5,"matchedTradingVolume":1.86700486E8},{"month":5,"value":27.2,"matchedTradingVolume":1.60517931E8},{"month":6,"value":27.6,"matchedTradingVolume":1.65627114E8},{"month":7,"value":23.9,"matchedTradingVolume":2.0278093E8},{"month":8,"value":26.2,"matchedTradingVolume":3.2929596E8},{"month":9,"value":28.4,"matchedTradingVolume":1.79469034E8},{"month":10,"value":21.6,"matchedTradingVolume":2.0827932E8},{"month":11,"value":24.1,"matchedTradingVolume":4.01348366E8},{"month":12,"value":23.9,"matchedTradingVolume":2.56520459E8}],"dividendSpitingHistories":[]},{"symbol":"DTD","companyName":"CTCP Đầu tư Phát triển Thành Đạt","type":"HNX30","year":2023,"prices":[{"month":1,"value":14.4,"matchedTradingVolume":5950842.0},{"month":2,"value":13.7,"matchedTradingVolume":6378838.0},{"month":3,"value":16.6,"matchedTradingVolume":7311940.0},{"month":4,"value":18.1,"matchedTradingVolume":1.0294297E7},{"month":5,"value":31.9,"matchedTradingVolume":2.2655048E7},{"month":6,"value":32.5,"matchedTradingVolume":1.8129994E7},{"month":7,"value":36.7,"matchedTradingVolume":1.5735536E7},{"month":8,"value":32.5,"matchedTradingVolume":1.6086212E7},{"month":9,"value":30.9,"matchedTradingVolume":1.1056539E7},{"month":10,"value":30.5,"matchedTradingVolume":1.8741944E7},{"month":11,"value":24.0,"matchedTradingVolume":1.831541E7},{"month":12,"value":26.3,"matchedTradingVolume":2.4949081E7}],"dividendSpitingHistories":[]},{"symbol":"DXP","companyName":"CTCP Cảng Đoạn Xá","type":"HNX30","year":2023,"prices":[{"month":1,"value":10.4,"matchedTradingVolume":912739.0},{"month":2,"value":10.3,"matchedTradingVolume":917376.0},{"month":3,"value":9.8,"matchedTradingVolume":787279.0},{"month":4,"value":9.9,"matchedTradingVolume":885375.0},{"month":5,"value":12.8,"matchedTradingVolume":1782047.0},{"month":6,"value":13.5,"matchedTradingVolume":3439863.0},{"month":7,"value":14.0,"matchedTradingVolume":1994362.0},{"month":8,"value":13.8,"matchedTradingVolume":2432178.0},{"month":9,"value":14.1,"matchedTradingVolume":4273324.0},{"month":10,"value":14.8,"matchedTradingVolume":9033438.0},{"month":11,"value":13.3,"matchedTradingVolume":1.0391949E7},{"month":12,"value":13.4,"matchedTradingVolume":6974255.0}],"dividendSpitingHistories":[]},{"symbol":"HLD","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":29.8,"matchedTradingVolume":231503.0},{"month":2,"value":28.2,"matchedTradingVolume":226901.0},{"month":3,"value":27.4,"matchedTradingVolume":140330.0},{"month":4,"value":35.6,"matchedTradingVolume":496224.0},{"month":5,"value":37.2,"matchedTradingVolume":307238.0},{"month":6,"value":36.6,"matchedTradingVolume":339320.0},{"month":7,"value":33.0,"matchedTradingVolume":620471.0},{"month":8,"value":32.6,"matchedTradingVolume":589525.0},{"month":9,"value":31.5,"matchedTradingVolume":674240.0},{"month":10,"value":27.6,"matchedTradingVolume":250531.0},{"month":11,"value":26.4,"matchedTradingVolume":395171.0},{"month":12,"value":26.5,"matchedTradingVolume":307473.0}],"dividendSpitingHistories":[]},{"symbol":"HUT","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":16.8,"matchedTradingVolume":2.6232682E7},{"month":2,"value":15.4,"matchedTradingVolume":3.1806604E7},{"month":3,"value":16.1,"matchedTradingVolume":4.0121809E7},{"month":4,"value":17.2,"matchedTradingVolume":3.9834208E7},{"month":5,"value":18.5,"matchedTradingVolume":5.0768478E7},{"month":6,"value":20.1,"matchedTradingVolume":7.7486457E7},{"month":7,"value":21.1,"matchedTradingVolume":6.905587E7},{"month":8,"value":27.4,"matchedTradingVolume":1.21918856E8},{"month":9,"value":28.5,"matchedTradingVolume":1.24166119E8},{"month":10,"value":24.2,"matchedTradingVolume":1.05483677E8},{"month":11,"value":21.1,"matchedTradingVolume":1.2679697E8},{"month":12,"value":21.3,"matchedTradingVolume":1.20443764E8}],"dividendSpitingHistories":[]},{"symbol":"IDC","companyName":"Tổng Công ty IDICO – CTCP","type":"HNX30","year":2023,"prices":[{"month":1,"value":40.4,"matchedTradingVolume":4.2236657E7},{"month":2,"value":42.5,"matchedTradingVolume":7.1829678E7},{"month":3,"value":41.0,"matchedTradingVolume":5.5623409E7},{"month":4,"value":41.9,"matchedTradingVolume":4.1157756E7},{"month":5,"value":41.9,"matchedTradingVolume":5.167149E7},{"month":6,"value":44.2,"matchedTradingVolume":7.3655552E7},{"month":7,"value":45.7,"matchedTradingVolume":6.2733165E7},{"month":8,"value":49.3,"matchedTradingVolume":8.3958141E7},{"month":9,"value":50.4,"matchedTradingVolume":6.1038327E7},{"month":10,"value":52.5,"matchedTradingVolume":9.3609479E7},{"month":11,"value":50.5,"matchedTradingVolume":5.7923673E7},{"month":12,"value":52.2,"matchedTradingVolume":5.3508845E7}],"dividendSpitingHistories":[{"month":4,"value":2000.0},{"month":9,"value":2000.0}]},{"symbol":"L14","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":58.9,"matchedTradingVolume":7741503.0},{"month":2,"value":53.5,"matchedTradingVolume":7944098.0},{"month":3,"value":45.9,"matchedTradingVolume":5681449.0},{"month":4,"value":54.2,"matchedTradingVolume":1.0662182E7},{"month":5,"value":52.2,"matchedTradingVolume":1.278968E7},{"month":6,"value":48.0,"matchedTradingVolume":1.3094389E7},{"month":7,"value":48.0,"matchedTradingVolume":1.0732735E7},{"month":8,"value":62.0,"matchedTradingVolume":2.2437095E7},{"month":9,"value":59.9,"matchedTradingVolume":1.1478379E7},{"month":10,"value":44.5,"matchedTradingVolume":6285716.0},{"month":11,"value":46.6,"matchedTradingVolume":1.0706426E7},{"month":12,"value":48.8,"matchedTradingVolume":7059836.0}],"dividendSpitingHistories":[]},{"symbol":"L18","companyName":"CTCP Đầu tư và Xây dựng Số 18","type":"HNX30","year":2023,"prices":[{"month":1,"value":22.5,"matchedTradingVolume":762349.0},{"month":2,"value":22.8,"matchedTradingVolume":948665.0},{"month":3,"value":25.4,"matchedTradingVolume":880699.0},{"month":4,"value":29.5,"matchedTradingVolume":972819.0},{"month":5,"value":39.5,"matchedTradingVolume":1285782.0},{"month":6,"value":37.0,"matchedTradingVolume":890512.0},{"month":7,"value":39.0,"matchedTradingVolume":1114914.0},{"month":8,"value":42.0,"matchedTradingVolume":1684345.0},{"month":9,"value":41.6,"matchedTradingVolume":1101101.0},{"month":10,"value":35.0,"matchedTradingVolume":536762.0},{"month":11,"value":36.0,"matchedTradingVolume":676349.0},{"month":12,"value":42.0,"matchedTradingVolume":1204132.0}],"dividendSpitingHistories":[{"month":1,"value":800.0},{"month":3,"value":700.0}]},{"symbol":"LAS","companyName":"CTCP Supe Phốt phát và Hóa chất Lâm Thao","type":"HNX30","year":2023,"prices":[{"month":1,"value":9.0,"matchedTradingVolume":3578318.0},{"month":2,"value":8.8,"matchedTradingVolume":4052633.0},{"month":3,"value":8.6,"matchedTradingVolume":3805041.0},{"month":4,"value":9.3,"matchedTradingVolume":8152270.0},{"month":5,"value":10.6,"matchedTradingVolume":1.5071426E7},{"month":6,"value":11.6,"matchedTradingVolume":1.6968799E7},{"month":7,"value":13.4,"matchedTradingVolume":1.3925595E7},{"month":8,"value":13.5,"matchedTradingVolume":1.0302924E7},{"month":9,"value":14.7,"matchedTradingVolume":1.2641782E7},{"month":10,"value":14.2,"matchedTradingVolume":1.1448746E7},{"month":11,"value":14.0,"matchedTradingVolume":1.3527785E7},{"month":12,"value":15.0,"matchedTradingVolume":1.7700348E7}],"dividendSpitingHistories":[{"month":8,"value":600.0}]},{"symbol":"LHC","companyName":"CTCP Đầu tư và Xây dựng Thủy lợi Lâm Đồng","type":"HNX30","year":2023,"prices":[{"month":1,"value":52.0,"matchedTradingVolume":360814.0},{"month":2,"value":51.0,"matchedTradingVolume":158300.0},{"month":3,"value":51.8,"matchedTradingVolume":534500.0},{"month":4,"value":52.0,"matchedTradingVolume":203612.0},{"month":5,"value":49.8,"matchedTradingVolume":130386.0},{"month":6,"value":50.2,"matchedTradingVolume":388275.0},{"month":7,"value":57.0,"matchedTradingVolume":891568.0},{"month":8,"value":57.5,"matchedTradingVolume":283634.0},{"month":9,"value":60.7,"matchedTradingVolume":272250.0},{"month":10,"value":57.9,"matchedTradingVolume":95227.0},{"month":11,"value":53.9,"matchedTradingVolume":397727.0},{"month":12,"value":52.9,"matchedTradingVolume":177928.0}],"dividendSpitingHistories":[{"month":3,"value":500.0},{"month":8,"value":1500.0}]},{"symbol":"MBS","companyName":"CTCP Chứng khoán MB","type":"HNX30","year":2023,"prices":[{"month":1,"value":15.3,"matchedTradingVolume":3.8321764E7},{"month":2,"value":14.8,"matchedTradingVolume":3.8730351E7},{"month":3,"value":15.8,"matchedTradingVolume":5.5555374E7},{"month":4,"value":17.6,"matchedTradingVolume":8.1238888E7},{"month":5,"value":18.5,"matchedTradingVolume":6.6965434E7},{"month":6,"value":19.5,"matchedTradingVolume":7.4072721E7},{"month":7,"value":21.2,"matchedTradingVolume":7.4782537E7},{"month":8,"value":21.2,"matchedTradingVolume":7.9872284E7},{"month":9,"value":24.5,"matchedTradingVolume":8.6962514E7},{"month":10,"value":23.5,"matchedTradingVolume":1.09345483E8},{"month":11,"value":22.0,"matchedTradingVolume":1.07702558E8},{"month":12,"value":23.4,"matchedTradingVolume":8.3679495E7}],"dividendSpitingHistories":[]},{"symbol":"NBC","companyName":"CTCP Than Núi Béo - Vinacomin","type":"HNX30","year":2023,"prices":[{"month":1,"value":11.8,"matchedTradingVolume":3613717.0},{"month":2,"value":12.1,"matchedTradingVolume":7089386.0},{"month":3,"value":11.5,"matchedTradingVolume":3494563.0},{"month":4,"value":12.7,"matchedTradingVolume":6028485.0},{"month":5,"value":12.7,"matchedTradingVolume":6823417.0},{"month":6,"value":13.3,"matchedTradingVolume":5858620.0},{"month":7,"value":13.6,"matchedTradingVolume":7106972.0},{"month":8,"value":13.4,"matchedTradingVolume":6584419.0},{"month":9,"value":12.6,"matchedTradingVolume":4992643.0},{"month":10,"value":11.7,"matchedTradingVolume":2871754.0},{"month":11,"value":11.2,"matchedTradingVolume":2702813.0},{"month":12,"value":12.2,"matchedTradingVolume":3338675.0}],"dividendSpitingHistories":[{"month":6,"value":300.0}]},{"symbol":"PLC","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":28.0,"matchedTradingVolume":8019236.0},{"month":2,"value":32.8,"matchedTradingVolume":1.6214208E7},{"month":3,"value":35.0,"matchedTradingVolume":1.7856342E7},{"month":4,"value":34.4,"matchedTradingVolume":1.3343638E7},{"month":5,"value":37.6,"matchedTradingVolume":1.1009234E7},{"month":6,"value":39.0,"matchedTradingVolume":9749548.0},{"month":7,"value":40.4,"matchedTradingVolume":8317441.0},{"month":8,"value":39.5,"matchedTradingVolume":6508016.0},{"month":9,"value":37.7,"matchedTradingVolume":4813765.0},{"month":10,"value":34.7,"matchedTradingVolume":3137853.0},{"month":11,"value":30.7,"matchedTradingVolume":3341603.0},{"month":12,"value":33.2,"matchedTradingVolume":2711591.0}],"dividendSpitingHistories":[]},{"symbol":"PSI","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":6.1,"matchedTradingVolume":563172.0},{"month":2,"value":6.0,"matchedTradingVolume":563212.0},{"month":3,"value":5.6,"matchedTradingVolume":698563.0},{"month":4,"value":7.0,"matchedTradingVolume":2494209.0},{"month":5,"value":7.9,"matchedTradingVolume":2745850.0},{"month":6,"value":9.0,"matchedTradingVolume":3780471.0},{"month":7,"value":9.0,"matchedTradingVolume":2673914.0},{"month":8,"value":9.8,"matchedTradingVolume":5783383.0},{"month":9,"value":12.2,"matchedTradingVolume":1.1061288E7},{"month":10,"value":9.9,"matchedTradingVolume":4885496.0},{"month":11,"value":9.2,"matchedTradingVolume":4076293.0},{"month":12,"value":9.5,"matchedTradingVolume":2586015.0}],"dividendSpitingHistories":[]},{"symbol":"PVC","companyName":"Tổng Công ty Hóa chất và Dịch vụ Dầu khí - CTCP","type":"HNX30","year":2023,"prices":[{"month":1,"value":15.6,"matchedTradingVolume":3.5163557E7},{"month":2,"value":15.6,"matchedTradingVolume":3.82605E7},{"month":3,"value":16.5,"matchedTradingVolume":3.9275747E7},{"month":4,"value":16.4,"matchedTradingVolume":3.8379409E7},{"month":5,"value":18.5,"matchedTradingVolume":4.7079449E7},{"month":6,"value":18.6,"matchedTradingVolume":3.9167582E7},{"month":7,"value":19.4,"matchedTradingVolume":3.1585006E7},{"month":8,"value":19.8,"matchedTradingVolume":3.2294619E7},{"month":9,"value":20.0,"matchedTradingVolume":3.0883423E7},{"month":10,"value":18.9,"matchedTradingVolume":3.0460937E7},{"month":11,"value":15.2,"matchedTradingVolume":3.6621345E7},{"month":12,"value":16.1,"matchedTradingVolume":2.7428238E7}],"dividendSpitingHistories":[{"month":11,"value":180.0}]},{"symbol":"PVG","companyName":"CTCP Kinh doanh LPG Việt Nam","type":"HNX30","year":2023,"prices":[{"month":1,"value":8.0,"matchedTradingVolume":1164214.0},{"month":2,"value":8.5,"matchedTradingVolume":1859515.0},{"month":3,"value":8.1,"matchedTradingVolume":1124560.0},{"month":4,"value":8.1,"matchedTradingVolume":1783152.0},{"month":5,"value":9.2,"matchedTradingVolume":3510578.0},{"month":6,"value":10.7,"matchedTradingVolume":6292684.0},{"month":7,"value":10.5,"matchedTradingVolume":4906952.0},{"month":8,"value":10.9,"matchedTradingVolume":6233546.0},{"month":9,"value":10.4,"matchedTradingVolume":3017782.0},{"month":10,"value":10.0,"matchedTradingVolume":1405768.0},{"month":11,"value":9.3,"matchedTradingVolume":662121.0},{"month":12,"value":9.2,"matchedTradingVolume":656764.0}],"dividendSpitingHistories":[{"month":6,"value":300.0}]},{"symbol":"PVS","companyName":"Tổng Công ty cổ phần Dịch vụ Kỹ thuật Dầu khí Việt Nam","type":"HNX30","year":2023,"prices":[{"month":1,"value":25.6,"matchedTradingVolume":8.6042635E7},{"month":2,"value":26.8,"matchedTradingVolume":1.31385208E8},{"month":3,"value":27.5,"matchedTradingVolume":1.16136499E8},{"month":4,"value":26.4,"matchedTradingVolume":8.0120016E7},{"month":5,"value":31.0,"matchedTradingVolume":1.40267109E8},{"month":6,"value":33.1,"matchedTradingVolume":1.59161373E8},{"month":7,"value":35.0,"matchedTradingVolume":1.08046493E8},{"month":8,"value":36.0,"matchedTradingVolume":1.52167647E8},{"month":9,"value":39.5,"matchedTradingVolume":1.29903345E8},{"month":10,"value":40.7,"matchedTradingVolume":1.57780759E8},{"month":11,"value":39.0,"matchedTradingVolume":1.24880714E8},{"month":12,"value":40.2,"matchedTradingVolume":8.5316604E7}],"dividendSpitingHistories":[{"month":10,"value":700.0}]},{"symbol":"SHS","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":10.0,"matchedTradingVolume":2.53793966E8},{"month":2,"value":9.3,"matchedTradingVolume":2.51382589E8},{"month":3,"value":9.2,"matchedTradingVolume":3.14457024E8},{"month":4,"value":10.6,"matchedTradingVolume":4.86724587E8},{"month":5,"value":11.8,"matchedTradingVolume":4.03628131E8},{"month":6,"value":14.0,"matchedTradingVolume":5.12915603E8},{"month":7,"value":15.6,"matchedTradingVolume":3.51958733E8},{"month":8,"value":18.6,"matchedTradingVolume":5.05353394E8},{"month":9,"value":20.5,"matchedTradingVolume":4.23334614E8},{"month":10,"value":18.2,"matchedTradingVolume":5.72161445E8},{"month":11,"value":18.4,"matchedTradingVolume":6.88673172E8},{"month":12,"value":19.7,"matchedTradingVolume":4.23218842E8}],"dividendSpitingHistories":[]},{"symbol":"SLS","companyName":"CTCP Mía Đường Sơn La","type":"HNX30","year":2023,"prices":[{"month":1,"value":141.5,"matchedTradingVolume":105965.0},{"month":2,"value":153.0,"matchedTradingVolume":371779.0},{"month":3,"value":151.0,"matchedTradingVolume":107135.0},{"month":4,"value":175.0,"matchedTradingVolume":243202.0},{"month":5,"value":172.5,"matchedTradingVolume":214329.0},{"month":6,"value":174.3,"matchedTradingVolume":161085.0},{"month":7,"value":217.5,"matchedTradingVolume":317260.0},{"month":8,"value":218.4,"matchedTradingVolume":460531.0},{"month":9,"value":207.9,"matchedTradingVolume":338896.0},{"month":10,"value":215.0,"matchedTradingVolume":570007.0},{"month":11,"value":158.0,"matchedTradingVolume":344405.0},{"month":12,"value":151.3,"matchedTradingVolume":273898.0}],"dividendSpitingHistories":[{"month":10,"value":15000.0}]},{"symbol":"TDN","companyName":"CTCP Than Đèo Nai - Vinacomin","type":"HNX30","year":2023,"prices":[{"month":1,"value":10.5,"matchedTradingVolume":830221.0},{"month":2,"value":10.9,"matchedTradingVolume":2139323.0},{"month":3,"value":10.6,"matchedTradingVolume":872061.0},{"month":4,"value":12.1,"matchedTradingVolume":2504970.0},{"month":5,"value":11.8,"matchedTradingVolume":2689719.0},{"month":6,"value":11.3,"matchedTradingVolume":2294625.0},{"month":7,"value":11.4,"matchedTradingVolume":2683671.0},{"month":8,"value":11.2,"matchedTradingVolume":2355125.0},{"month":9,"value":10.6,"matchedTradingVolume":824593.0},{"month":10,"value":10.0,"matchedTradingVolume":663198.0},{"month":11,"value":9.4,"matchedTradingVolume":317910.0},{"month":12,"value":10.3,"matchedTradingVolume":470014.0}],"dividendSpitingHistories":[{"month":5,"value":800.0}]},{"symbol":"TIG","companyName":"CTCP Tập đoàn Đầu tư Thăng Long","type":"HNX30","year":2023,"prices":[{"month":1,"value":9.4,"matchedTradingVolume":1.4718354E7},{"month":2,"value":9.2,"matchedTradingVolume":1.9183104E7},{"month":3,"value":8.5,"matchedTradingVolume":1.2889752E7},{"month":4,"value":8.6,"matchedTradingVolume":1.8732883E7},{"month":5,"value":11.5,"matchedTradingVolume":3.367642E7},{"month":6,"value":11.9,"matchedTradingVolume":2.8614289E7},{"month":7,"value":12.6,"matchedTradingVolume":2.6129853E7},{"month":8,"value":12.8,"matchedTradingVolume":3.2215207E7},{"month":9,"value":12.1,"matchedTradingVolume":1.5110764E7},{"month":10,"value":11.2,"matchedTradingVolume":1.6428527E7},{"month":11,"value":12.2,"matchedTradingVolume":3.6912427E7},{"month":12,"value":13.1,"matchedTradingVolume":6.5307842E7}],"dividendSpitingHistories":[]},{"symbol":"TNG","companyName":"CTCP Đầu tư và Thương mại TNG","type":"HNX30","year":2023,"prices":[{"month":1,"value":15.9,"matchedTradingVolume":2.2788741E7},{"month":2,"value":18.8,"matchedTradingVolume":5.383754E7},{"month":3,"value":18.5,"matchedTradingVolume":4.7327191E7},{"month":4,"value":20.0,"matchedTradingVolume":4.8994383E7},{"month":5,"value":20.1,"matchedTradingVolume":4.066419E7},{"month":6,"value":20.5,"matchedTradingVolume":3.733616E7},{"month":7,"value":21.3,"matchedTradingVolume":3.6046131E7},{"month":8,"value":21.3,"matchedTradingVolume":3.9840949E7},{"month":9,"value":22.6,"matchedTradingVolume":5.6823464E7},{"month":10,"value":21.6,"matchedTradingVolume":5.7013818E7},{"month":11,"value":19.5,"matchedTradingVolume":3.3075049E7},{"month":12,"value":20.4,"matchedTradingVolume":4.1724689E7}],"dividendSpitingHistories":[{"month":1,"value":400.0},{"month":10,"value":400.0}]},{"symbol":"TVD","companyName":"CTCP Than Vàng Danh - Vinacomin","type":"HNX30","year":2023,"prices":[{"month":1,"value":13.6,"matchedTradingVolume":4460374.0},{"month":2,"value":16.1,"matchedTradingVolume":1.2369639E7},{"month":3,"value":15.2,"matchedTradingVolume":5436677.0},{"month":4,"value":16.0,"matchedTradingVolume":7688533.0},{"month":5,"value":16.3,"matchedTradingVolume":1.0313929E7},{"month":6,"value":18.0,"matchedTradingVolume":1.0095238E7},{"month":7,"value":16.6,"matchedTradingVolume":9646606.0},{"month":8,"value":16.4,"matchedTradingVolume":6320529.0},{"month":9,"value":14.9,"matchedTradingVolume":2552604.0},{"month":10,"value":13.8,"matchedTradingVolume":1537320.0},{"month":11,"value":12.9,"matchedTradingVolume":1610533.0},{"month":12,"value":14.4,"matchedTradingVolume":1243333.0}],"dividendSpitingHistories":[{"month":6,"value":900.0}]},{"symbol":"VC3","companyName":"CTCP Tập đoàn Nam Mê Kông","type":"HNX30","year":2023,"prices":[{"month":1,"value":31.9,"matchedTradingVolume":3708499.0},{"month":2,"value":31.0,"matchedTradingVolume":6255386.0},{"month":3,"value":29.8,"matchedTradingVolume":6890555.0},{"month":4,"value":29.2,"matchedTradingVolume":4813528.0},{"month":5,"value":32.0,"matchedTradingVolume":1.0960064E7},{"month":6,"value":29.8,"matchedTradingVolume":1.4275123E7},{"month":7,"value":25.7,"matchedTradingVolume":9058122.0},{"month":8,"value":27.5,"matchedTradingVolume":1.2952619E7},{"month":9,"value":26.0,"matchedTradingVolume":7353372.0},{"month":10,"value":24.3,"matchedTradingVolume":8545141.0},{"month":11,"value":24.4,"matchedTradingVolume":1.1344333E7},{"month":12,"value":25.0,"matchedTradingVolume":1.3213301E7}],"dividendSpitingHistories":[]},{"symbol":"VCS","companyName":"CTCP Vicostone","type":"HNX30","year":2023,"prices":[{"month":1,"value":57.8,"matchedTradingVolume":1602832.0},{"month":2,"value":55.0,"matchedTradingVolume":1419547.0},{"month":3,"value":52.4,"matchedTradingVolume":733426.0},{"month":4,"value":52.2,"matchedTradingVolume":1070085.0},{"month":5,"value":56.9,"matchedTradingVolume":2587508.0},{"month":6,"value":61.7,"matchedTradingVolume":3409753.0},{"month":7,"value":64.3,"matchedTradingVolume":3504930.0},{"month":8,"value":67.5,"matchedTradingVolume":4021339.0},{"month":9,"value":69.0,"matchedTradingVolume":2404724.0},{"month":10,"value":63.8,"matchedTradingVolume":2062699.0},{"month":11,"value":57.9,"matchedTradingVolume":1492424.0},{"month":12,"value":57.3,"matchedTradingVolume":859008.0}],"dividendSpitingHistories":[{"month":6,"value":2000.0},{"month":12,"value":2000.0}]},{"symbol":"VIG","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":6.1,"matchedTradingVolume":3000777.0},{"month":2,"value":6.1,"matchedTradingVolume":2827039.0},{"month":3,"value":5.8,"matchedTradingVolume":6426854.0},{"month":4,"value":6.5,"matchedTradingVolume":1.2815084E7},{"month":5,"value":7.7,"matchedTradingVolume":1.3108227E7},{"month":6,"value":8.7,"matchedTradingVolume":1.5290969E7},{"month":7,"value":8.6,"matchedTradingVolume":1.6843152E7},{"month":8,"value":8.9,"matchedTradingVolume":2.145496E7},{"month":9,"value":10.8,"matchedTradingVolume":2.6101975E7},{"month":10,"value":8.6,"matchedTradingVolume":1.3054237E7},{"month":11,"value":7.9,"matchedTradingVolume":1.2156118E7},{"month":12,"value":8.1,"matchedTradingVolume":7288746.0}],"dividendSpitingHistories":[]}]}'
# futureData = loadDataInput(jsonInput2023)
# exe_experiments(futureData)
# printSolution('DONE hnx30_3years_before')



# M2 = np.load("data/calculate2023/vn30_5years_before/M2.npy", allow_pickle=True)
# M3 = np.load("data/calculate2023/vn30_5years_before/M3.npy", allow_pickle=True)
# M4 = np.load("data/calculate2023/vn30_5years_before/M4.npy", allow_pickle=True)
# jsonInput2023='{"stocks":[{"symbol":"ACB","companyName":"Ngân hàng TMCP Á Châu","type":"VN30","year":2023,"prices":[{"month":1,"value":26.35,"matchedTradingVolume":5.499E7},{"month":2,"value":25.8,"matchedTradingVolume":6.3237E7},{"month":3,"value":25.35,"matchedTradingVolume":9.20633E7},{"month":4,"value":25.3,"matchedTradingVolume":8.14876E7},{"month":5,"value":25.4,"matchedTradingVolume":1.608784E8},{"month":6,"value":22.3,"matchedTradingVolume":1.920848E8},{"month":7,"value":22.95,"matchedTradingVolume":1.640575E8},{"month":8,"value":24.4,"matchedTradingVolume":2.570596E8},{"month":9,"value":22.95,"matchedTradingVolume":1.263825E8},{"month":10,"value":22.8,"matchedTradingVolume":1.01492E8},{"month":11,"value":23.3,"matchedTradingVolume":1.540952E8},{"month":12,"value":23.9,"matchedTradingVolume":1.309384E8}],"dividendSpitingHistories":[]},{"symbol":"BID","companyName":"Ngân hàng TMCP Đầu tư và Phát triển Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":45.95,"matchedTradingVolume":2.88095E7},{"month":2,"value":47.2,"matchedTradingVolume":2.70027E7},{"month":3,"value":48.0,"matchedTradingVolume":1.78979E7},{"month":4,"value":46.0,"matchedTradingVolume":1.53768E7},{"month":5,"value":45.1,"matchedTradingVolume":1.2405E7},{"month":6,"value":45.35,"matchedTradingVolume":2.61229E7},{"month":7,"value":47.35,"matchedTradingVolume":3.93465E7},{"month":8,"value":49.1,"matchedTradingVolume":4.26147E7},{"month":9,"value":47.5,"matchedTradingVolume":2.19276E7},{"month":10,"value":43.95,"matchedTradingVolume":2.0611E7},{"month":11,"value":44.15,"matchedTradingVolume":1.78062E7},{"month":12,"value":43.4,"matchedTradingVolume":2.24373E7}],"dividendSpitingHistories":[]},{"symbol":"BVH","companyName":"Tập đoàn Bảo Việt","type":"VN30","year":2023,"prices":[{"month":1,"value":51.0,"matchedTradingVolume":7621200.0},{"month":2,"value":51.2,"matchedTradingVolume":9028400.0},{"month":3,"value":50.0,"matchedTradingVolume":5479800.0},{"month":4,"value":49.2,"matchedTradingVolume":5394500.0},{"month":5,"value":46.0,"matchedTradingVolume":1.05267E7},{"month":6,"value":45.3,"matchedTradingVolume":2.13723E7},{"month":7,"value":48.15,"matchedTradingVolume":2.26194E7},{"month":8,"value":48.0,"matchedTradingVolume":1.95543E7},{"month":9,"value":45.8,"matchedTradingVolume":1.30652E7},{"month":10,"value":42.65,"matchedTradingVolume":6368600.0},{"month":11,"value":41.3,"matchedTradingVolume":6801500.0},{"month":12,"value":40.5,"matchedTradingVolume":6636100.0}],"dividendSpitingHistories":[{"month":11,"value":954.0}]},{"symbol":"CTG","companyName":"Ngân hàng TMCP Công Thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":31.1,"matchedTradingVolume":6.19356E7},{"month":2,"value":30.45,"matchedTradingVolume":5.62202E7},{"month":3,"value":29.5,"matchedTradingVolume":4.62949E7},{"month":4,"value":30.0,"matchedTradingVolume":4.04912E7},{"month":5,"value":28.4,"matchedTradingVolume":7.05504E7},{"month":6,"value":30.0,"matchedTradingVolume":1.20986E8},{"month":7,"value":30.3,"matchedTradingVolume":1.269248E8},{"month":8,"value":32.6,"matchedTradingVolume":1.849013E8},{"month":9,"value":33.2,"matchedTradingVolume":1.252328E8},{"month":10,"value":29.95,"matchedTradingVolume":6.47939E7},{"month":11,"value":30.25,"matchedTradingVolume":6.29258E7},{"month":12,"value":27.1,"matchedTradingVolume":7.30158E7}],"dividendSpitingHistories":[]},{"symbol":"FPT","companyName":"CTCP FPT","type":"VN30","year":2023,"prices":[{"month":1,"value":84.0,"matchedTradingVolume":1.49761E7},{"month":2,"value":82.8,"matchedTradingVolume":1.6827E7},{"month":3,"value":80.6,"matchedTradingVolume":1.51259E7},{"month":4,"value":80.9,"matchedTradingVolume":1.11001E7},{"month":5,"value":84.1,"matchedTradingVolume":1.65431E7},{"month":6,"value":87.3,"matchedTradingVolume":1.93342E7},{"month":7,"value":87.0,"matchedTradingVolume":2.72301E7},{"month":8,"value":96.7,"matchedTradingVolume":4.53975E7},{"month":9,"value":99.0,"matchedTradingVolume":5.49667E7},{"month":10,"value":97.0,"matchedTradingVolume":5.85186E7},{"month":11,"value":93.0,"matchedTradingVolume":4.69906E7},{"month":12,"value":97.2,"matchedTradingVolume":4.36497E7}],"dividendSpitingHistories":[{"month":8,"value":1000.0}]},{"symbol":"GAS","companyName":"Tổng Công ty Khí Việt Nam - CTCP","type":"VN30","year":2023,"prices":[{"month":1,"value":108.2,"matchedTradingVolume":3892900.0},{"month":2,"value":109.0,"matchedTradingVolume":4822000.0},{"month":3,"value":108.1,"matchedTradingVolume":4192400.0},{"month":4,"value":102.5,"matchedTradingVolume":6178600.0},{"month":5,"value":94.9,"matchedTradingVolume":7790900.0},{"month":6,"value":96.6,"matchedTradingVolume":1.45087E7},{"month":7,"value":101.6,"matchedTradingVolume":1.42296E7},{"month":8,"value":103.2,"matchedTradingVolume":1.20026E7},{"month":9,"value":110.0,"matchedTradingVolume":1.18793E7},{"month":10,"value":89.3,"matchedTradingVolume":1.23912E7},{"month":11,"value":80.1,"matchedTradingVolume":1.12482E7},{"month":12,"value":79.8,"matchedTradingVolume":1.5394E7}],"dividendSpitingHistories":[{"month":8,"value":3600.0}]},{"symbol":"HDB","companyName":"Ngân hàng TMCP Phát triển TP. HCM","type":"VN30","year":2023,"prices":[{"month":1,"value":18.65,"matchedTradingVolume":3.22759E7},{"month":2,"value":19.0,"matchedTradingVolume":4.4446E7},{"month":3,"value":19.25,"matchedTradingVolume":5.77437E7},{"month":4,"value":19.7,"matchedTradingVolume":4.51794E7},{"month":5,"value":19.6,"matchedTradingVolume":3.38232E7},{"month":6,"value":19.2,"matchedTradingVolume":5.41306E7},{"month":7,"value":18.9,"matchedTradingVolume":6.66127E7},{"month":8,"value":17.55,"matchedTradingVolume":6.28059E7},{"month":9,"value":18.0,"matchedTradingVolume":1.529976E8},{"month":10,"value":17.75,"matchedTradingVolume":1.780465E8},{"month":11,"value":18.95,"matchedTradingVolume":1.868925E8},{"month":12,"value":20.3,"matchedTradingVolume":1.556088E8}],"dividendSpitingHistories":[{"month":5,"value":1000.0}]},{"symbol":"HPG","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":22.1,"matchedTradingVolume":4.281135E8},{"month":2,"value":21.9,"matchedTradingVolume":4.94953E8},{"month":3,"value":21.3,"matchedTradingVolume":4.610696E8},{"month":4,"value":22.0,"matchedTradingVolume":3.30845E8},{"month":5,"value":22.35,"matchedTradingVolume":3.350429E8},{"month":6,"value":26.6,"matchedTradingVolume":5.626958E8},{"month":7,"value":28.4,"matchedTradingVolume":4.653832E8},{"month":8,"value":28.15,"matchedTradingVolume":6.43047E8},{"month":9,"value":29.0,"matchedTradingVolume":6.05131E8},{"month":10,"value":26.2,"matchedTradingVolume":4.011388E8},{"month":11,"value":27.2,"matchedTradingVolume":5.466178E8},{"month":12,"value":27.95,"matchedTradingVolume":5.610034E8}],"dividendSpitingHistories":[]},{"symbol":"MBB","companyName":"Ngân hàng TMCP Quân Đội","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":1.510583E8},{"month":2,"value":18.95,"matchedTradingVolume":1.687588E8},{"month":3,"value":18.3,"matchedTradingVolume":1.717558E8},{"month":4,"value":18.8,"matchedTradingVolume":1.492544E8},{"month":5,"value":18.85,"matchedTradingVolume":1.334826E8},{"month":6,"value":20.7,"matchedTradingVolume":2.836777E8},{"month":7,"value":21.2,"matchedTradingVolume":2.36432E8},{"month":8,"value":19.35,"matchedTradingVolume":2.173509E8},{"month":9,"value":19.4,"matchedTradingVolume":2.572516E8},{"month":10,"value":18.6,"matchedTradingVolume":1.466942E8},{"month":11,"value":18.55,"matchedTradingVolume":1.853708E8},{"month":12,"value":18.65,"matchedTradingVolume":1.511428E8}],"dividendSpitingHistories":[{"month":6,"value":500.0}]},{"symbol":"MSN","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":103.7,"matchedTradingVolume":8950100.0},{"month":2,"value":96.7,"matchedTradingVolume":1.24483E7},{"month":3,"value":84.7,"matchedTradingVolume":2.91468E7},{"month":4,"value":79.5,"matchedTradingVolume":2.07545E7},{"month":5,"value":74.4,"matchedTradingVolume":1.62996E7},{"month":6,"value":78.8,"matchedTradingVolume":3.0083E7},{"month":7,"value":87.3,"matchedTradingVolume":3.79388E7},{"month":8,"value":89.2,"matchedTradingVolume":5.02759E7},{"month":9,"value":82.7,"matchedTradingVolume":3.77362E7},{"month":10,"value":77.4,"matchedTradingVolume":4.0633E7},{"month":11,"value":66.0,"matchedTradingVolume":3.84334E7},{"month":12,"value":67.5,"matchedTradingVolume":5.12021E7}],"dividendSpitingHistories":[]},{"symbol":"MWG","companyName":"CTCP Đầu tư Thế giới Di động","type":"VN30","year":2023,"prices":[{"month":1,"value":46.5,"matchedTradingVolume":3.38651E7},{"month":2,"value":49.9,"matchedTradingVolume":4.56642E7},{"month":3,"value":40.8,"matchedTradingVolume":4.16636E7},{"month":4,"value":41.05,"matchedTradingVolume":5.23766E7},{"month":5,"value":39.4,"matchedTradingVolume":3.71724E7},{"month":6,"value":44.35,"matchedTradingVolume":8.65595E7},{"month":7,"value":54.5,"matchedTradingVolume":1.189389E8},{"month":8,"value":54.2,"matchedTradingVolume":1.698499E8},{"month":9,"value":57.5,"matchedTradingVolume":1.511657E8},{"month":10,"value":51.9,"matchedTradingVolume":1.695161E8},{"month":11,"value":41.9,"matchedTradingVolume":2.478952E8},{"month":12,"value":43.05,"matchedTradingVolume":1.675436E8}],"dividendSpitingHistories":[{"month":7,"value":500.0}]},{"symbol":"PLX","companyName":"Tập đoàn Xăng Dầu Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":38.1,"matchedTradingVolume":1.25733E7},{"month":2,"value":40.6,"matchedTradingVolume":1.61479E7},{"month":3,"value":39.0,"matchedTradingVolume":2.69045E7},{"month":4,"value":38.05,"matchedTradingVolume":1.50825E7},{"month":5,"value":38.05,"matchedTradingVolume":1.33605E7},{"month":6,"value":39.1,"matchedTradingVolume":1.56871E7},{"month":7,"value":41.8,"matchedTradingVolume":3.82708E7},{"month":8,"value":41.0,"matchedTradingVolume":3.29293E7},{"month":9,"value":40.4,"matchedTradingVolume":2.22712E7},{"month":10,"value":37.5,"matchedTradingVolume":2.2156E7},{"month":11,"value":35.8,"matchedTradingVolume":1.91929E7},{"month":12,"value":35.9,"matchedTradingVolume":1.31123E7}],"dividendSpitingHistories":[{"month":9,"value":700.0}]},{"symbol":"SAB","companyName":"Tổng Công ty cổ phần Bia - Rượu - Nước giải khát Sài Gòn","type":"VN30","year":2023,"prices":[{"month":1,"value":193.1,"matchedTradingVolume":2013100.0},{"month":2,"value":197.2,"matchedTradingVolume":1559600.0},{"month":3,"value":192.5,"matchedTradingVolume":3412700.0},{"month":4,"value":181.0,"matchedTradingVolume":3651800.0},{"month":5,"value":166.6,"matchedTradingVolume":2221900.0},{"month":6,"value":162.0,"matchedTradingVolume":3096200.0},{"month":7,"value":161.6,"matchedTradingVolume":3568900.0},{"month":8,"value":161.6,"matchedTradingVolume":6019000.0},{"month":9,"value":168.9,"matchedTradingVolume":9361900.0},{"month":10,"value":73.0,"matchedTradingVolume":9713900.0},{"month":11,"value":66.2,"matchedTradingVolume":1.61096E7},{"month":12,"value":65.6,"matchedTradingVolume":1.22324E7}],"dividendSpitingHistories":[{"month":3,"value":1000.0},{"month":6,"value":1500.0}]},{"symbol":"SHB","companyName":"Ngân hàng TMCP Sài Gòn - Hà Nội","type":"VN30","year":2023,"prices":[{"month":1,"value":11.2,"matchedTradingVolume":2.939803E8},{"month":2,"value":10.6,"matchedTradingVolume":2.209531E8},{"month":3,"value":10.85,"matchedTradingVolume":3.662555E8},{"month":4,"value":12.2,"matchedTradingVolume":6.056328E8},{"month":5,"value":12.0,"matchedTradingVolume":4.061201E8},{"month":6,"value":12.85,"matchedTradingVolume":6.039741E8},{"month":7,"value":14.4,"matchedTradingVolume":4.546979E8},{"month":8,"value":13.45,"matchedTradingVolume":4.740001E8},{"month":9,"value":12.75,"matchedTradingVolume":4.439107E8},{"month":10,"value":11.05,"matchedTradingVolume":2.494628E8},{"month":11,"value":11.6,"matchedTradingVolume":3.637048E8},{"month":12,"value":11.15,"matchedTradingVolume":3.281995E8}],"dividendSpitingHistories":[]},{"symbol":"SSI","companyName":"CTCP Chứng khoán SSI","type":"VN30","year":2023,"prices":[{"month":1,"value":21.6,"matchedTradingVolume":2.43128E8},{"month":2,"value":20.75,"matchedTradingVolume":2.701936E8},{"month":3,"value":21.5,"matchedTradingVolume":3.972755E8},{"month":4,"value":22.6,"matchedTradingVolume":4.024856E8},{"month":5,"value":23.4,"matchedTradingVolume":3.739481E8},{"month":6,"value":26.6,"matchedTradingVolume":4.523384E8},{"month":7,"value":29.75,"matchedTradingVolume":3.768438E8},{"month":8,"value":33.5,"matchedTradingVolume":6.115069E8},{"month":9,"value":36.45,"matchedTradingVolume":5.979921E8},{"month":10,"value":34.0,"matchedTradingVolume":5.601314E8},{"month":11,"value":32.9,"matchedTradingVolume":5.212175E8},{"month":12,"value":33.6,"matchedTradingVolume":3.923282E8}],"dividendSpitingHistories":[{"month":6,"value":1000.0}]},{"symbol":"STB","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":27.1,"matchedTradingVolume":2.330793E8},{"month":2,"value":26.15,"matchedTradingVolume":3.772336E8},{"month":3,"value":26.5,"matchedTradingVolume":4.59574E8},{"month":4,"value":26.9,"matchedTradingVolume":3.08058E8},{"month":5,"value":28.15,"matchedTradingVolume":3.174901E8},{"month":6,"value":30.3,"matchedTradingVolume":3.506546E8},{"month":7,"value":30.0,"matchedTradingVolume":4.686863E8},{"month":8,"value":32.9,"matchedTradingVolume":6.076624E8},{"month":9,"value":33.3,"matchedTradingVolume":4.282722E8},{"month":10,"value":31.75,"matchedTradingVolume":3.745102E8},{"month":11,"value":30.2,"matchedTradingVolume":3.661731E8},{"month":12,"value":28.55,"matchedTradingVolume":3.171983E8}],"dividendSpitingHistories":[]},{"symbol":"VCB","companyName":"Ngân hàng TMCP Ngoại thương Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":93.0,"matchedTradingVolume":1.95707E7},{"month":2,"value":96.0,"matchedTradingVolume":1.77834E7},{"month":3,"value":93.2,"matchedTradingVolume":2.03676E7},{"month":4,"value":92.8,"matchedTradingVolume":1.05433E7},{"month":5,"value":95.0,"matchedTradingVolume":1.21852E7},{"month":6,"value":105.0,"matchedTradingVolume":1.97517E7},{"month":7,"value":106.5,"matchedTradingVolume":2.00989E7},{"month":8,"value":91.5,"matchedTradingVolume":3.03631E7},{"month":9,"value":90.2,"matchedTradingVolume":2.82153E7},{"month":10,"value":86.8,"matchedTradingVolume":1.90875E7},{"month":11,"value":89.5,"matchedTradingVolume":2.49941E7},{"month":12,"value":86.0,"matchedTradingVolume":2.70841E7}],"dividendSpitingHistories":[]},{"symbol":"VIB","companyName":"Ngân hàng TMCP Quốc tế Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":23.55,"matchedTradingVolume":6.51873E7},{"month":2,"value":24.3,"matchedTradingVolume":6.42993E7},{"month":3,"value":21.4,"matchedTradingVolume":8.48303E7},{"month":4,"value":22.1,"matchedTradingVolume":7.98868E7},{"month":5,"value":21.6,"matchedTradingVolume":9.82021E7},{"month":6,"value":23.6,"matchedTradingVolume":1.718345E8},{"month":7,"value":21.0,"matchedTradingVolume":9.72921E7},{"month":8,"value":21.4,"matchedTradingVolume":1.057553E8},{"month":9,"value":21.7,"matchedTradingVolume":1.414188E8},{"month":10,"value":19.65,"matchedTradingVolume":7.06346E7},{"month":11,"value":19.65,"matchedTradingVolume":6.65855E7},{"month":12,"value":19.65,"matchedTradingVolume":7.1574E7}],"dividendSpitingHistories":[{"month":2,"value":1000.0},{"month":4,"value":500.0}]},{"symbol":"VIC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":59.2,"matchedTradingVolume":2.56029E7},{"month":2,"value":56.0,"matchedTradingVolume":3.974E7},{"month":3,"value":55.0,"matchedTradingVolume":3.25647E7},{"month":4,"value":58.0,"matchedTradingVolume":4.44255E7},{"month":5,"value":54.4,"matchedTradingVolume":3.62615E7},{"month":6,"value":54.1,"matchedTradingVolume":4.21094E7},{"month":7,"value":55.1,"matchedTradingVolume":6.40446E7},{"month":8,"value":75.6,"matchedTradingVolume":3.762692E8},{"month":9,"value":62.3,"matchedTradingVolume":2.936844E8},{"month":10,"value":46.9,"matchedTradingVolume":1.483437E8},{"month":11,"value":45.4,"matchedTradingVolume":9.69235E7},{"month":12,"value":44.6,"matchedTradingVolume":6.27363E7}],"dividendSpitingHistories":[]},{"symbol":"VJC","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":116.3,"matchedTradingVolume":5537500.0},{"month":2,"value":113.9,"matchedTradingVolume":5160700.0},{"month":3,"value":108.9,"matchedTradingVolume":6564900.0},{"month":4,"value":103.0,"matchedTradingVolume":3872700.0},{"month":5,"value":99.5,"matchedTradingVolume":1.26274E7},{"month":6,"value":97.7,"matchedTradingVolume":1.6206E7},{"month":7,"value":102.0,"matchedTradingVolume":1.96767E7},{"month":8,"value":103.0,"matchedTradingVolume":2.02222E7},{"month":9,"value":101.9,"matchedTradingVolume":2.19183E7},{"month":10,"value":105.2,"matchedTradingVolume":2.09001E7},{"month":11,"value":113.0,"matchedTradingVolume":2.00095E7},{"month":12,"value":108.0,"matchedTradingVolume":2.01093E7}],"dividendSpitingHistories":[]},{"symbol":"VNM","companyName":"CTCP Sữa Việt Nam","type":"VN30","year":2023,"prices":[{"month":1,"value":81.3,"matchedTradingVolume":2.71532E7},{"month":2,"value":77.5,"matchedTradingVolume":2.8004E7},{"month":3,"value":77.1,"matchedTradingVolume":3.09558E7},{"month":4,"value":74.7,"matchedTradingVolume":2.10868E7},{"month":5,"value":70.7,"matchedTradingVolume":3.00439E7},{"month":6,"value":71.9,"matchedTradingVolume":1.092673E8},{"month":7,"value":78.0,"matchedTradingVolume":9.18289E7},{"month":8,"value":77.9,"matchedTradingVolume":8.24544E7},{"month":9,"value":80.3,"matchedTradingVolume":5.63057E7},{"month":10,"value":75.8,"matchedTradingVolume":4.31485E7},{"month":11,"value":71.4,"matchedTradingVolume":4.87116E7},{"month":12,"value":70.0,"matchedTradingVolume":5.76954E7}],"dividendSpitingHistories":[{"month":8,"value":1500.0},{"month":8,"value":1500.0},{"month":12,"value":500.0}]},{"symbol":"VPB","companyName":"Ngân hàng TMCP Việt Nam Thịnh Vượng","type":"VN30","year":2023,"prices":[{"month":1,"value":19.7,"matchedTradingVolume":3.624271E8},{"month":2,"value":18.5,"matchedTradingVolume":3.291333E8},{"month":3,"value":21.25,"matchedTradingVolume":4.78505E8},{"month":4,"value":21.4,"matchedTradingVolume":2.156825E8},{"month":5,"value":19.8,"matchedTradingVolume":1.600067E8},{"month":6,"value":20.25,"matchedTradingVolume":3.597209E8},{"month":7,"value":22.15,"matchedTradingVolume":4.10663E8},{"month":8,"value":22.65,"matchedTradingVolume":4.072212E8},{"month":9,"value":22.55,"matchedTradingVolume":3.543629E8},{"month":10,"value":22.7,"matchedTradingVolume":2.767039E8},{"month":11,"value":21.35,"matchedTradingVolume":2.212622E8},{"month":12,"value":19.65,"matchedTradingVolume":2.219054E8}],"dividendSpitingHistories":[{"month":11,"value":1000.0}]},{"symbol":"VRE","companyName":null,"type":"VN30","year":2023,"prices":[{"month":1,"value":30.3,"matchedTradingVolume":2.95246E7},{"month":2,"value":29.6,"matchedTradingVolume":3.32765E7},{"month":3,"value":29.9,"matchedTradingVolume":7.12347E7},{"month":4,"value":29.6,"matchedTradingVolume":4.78106E7},{"month":5,"value":28.4,"matchedTradingVolume":5.91646E7},{"month":6,"value":27.45,"matchedTradingVolume":7.98341E7},{"month":7,"value":29.65,"matchedTradingVolume":1.388173E8},{"month":8,"value":31.5,"matchedTradingVolume":1.701563E8},{"month":9,"value":30.3,"matchedTradingVolume":9.07252E7},{"month":10,"value":27.45,"matchedTradingVolume":7.55509E7},{"month":11,"value":24.4,"matchedTradingVolume":1.089259E8},{"month":12,"value":23.65,"matchedTradingVolume":7.37884E7}],"dividendSpitingHistories":[]}]}'
# futureData = loadDataInput(jsonInput2023)
# exe_experiments(futureData)
# printSolution('DONE vn30_5years_before')
#
# M2 = np.load("data/calculate2023/hnx30_5years_before/M2.npy", allow_pickle=True)
# M3 = np.load("data/calculate2023/hnx30_5years_before/M3.npy", allow_pickle=True)
# M4 = np.load("data/calculate2023/hnx30_5years_before/M4.npy", allow_pickle=True)
# jsonInput2023='{"stocks":[{"symbol":"BCC","companyName":"CTCP Xi măng Bỉm Sơn","type":"HNX30","year":2023,"prices":[{"month":1,"value":11.6,"matchedTradingVolume":1.6898285E7},{"month":2,"value":12.7,"matchedTradingVolume":2.6045742E7},{"month":3,"value":12.4,"matchedTradingVolume":2.0300759E7},{"month":4,"value":12.4,"matchedTradingVolume":1.3811487E7},{"month":5,"value":13.3,"matchedTradingVolume":2.0730116E7},{"month":6,"value":14.5,"matchedTradingVolume":2.4793471E7},{"month":7,"value":14.6,"matchedTradingVolume":2.2653644E7},{"month":8,"value":14.6,"matchedTradingVolume":2.1295205E7},{"month":9,"value":13.0,"matchedTradingVolume":9862493.0},{"month":10,"value":12.2,"matchedTradingVolume":6465571.0},{"month":11,"value":9.8,"matchedTradingVolume":5608050.0},{"month":12,"value":9.6,"matchedTradingVolume":3821733.0}],"dividendSpitingHistories":[{"month":8,"value":500.0}]},{"symbol":"BVS","companyName":"CTCP Chứng khoán Bảo Việt","type":"HNX30","year":2023,"prices":[{"month":1,"value":21.0,"matchedTradingVolume":1438111.0},{"month":2,"value":19.0,"matchedTradingVolume":1854612.0},{"month":3,"value":19.1,"matchedTradingVolume":3134602.0},{"month":4,"value":20.2,"matchedTradingVolume":3958340.0},{"month":5,"value":23.8,"matchedTradingVolume":9386680.0},{"month":6,"value":25.3,"matchedTradingVolume":1.4453718E7},{"month":7,"value":27.0,"matchedTradingVolume":1.3688213E7},{"month":8,"value":28.8,"matchedTradingVolume":1.3880792E7},{"month":9,"value":30.7,"matchedTradingVolume":9906439.0},{"month":10,"value":26.9,"matchedTradingVolume":6689071.0},{"month":11,"value":26.0,"matchedTradingVolume":3668846.0},{"month":12,"value":26.1,"matchedTradingVolume":3959357.0}],"dividendSpitingHistories":[{"month":10,"value":1000.0}]},{"symbol":"CAP","companyName":"CTCP Lâm Nông sản Thực phẩm Yên Bái","type":"HNX30","year":2023,"prices":[{"month":1,"value":73.2,"matchedTradingVolume":113106.0},{"month":2,"value":76.3,"matchedTradingVolume":135358.0},{"month":3,"value":83.9,"matchedTradingVolume":136556.0},{"month":4,"value":91.5,"matchedTradingVolume":342827.0},{"month":5,"value":91.7,"matchedTradingVolume":400862.0},{"month":6,"value":70.3,"matchedTradingVolume":319155.0},{"month":7,"value":76.8,"matchedTradingVolume":848052.0},{"month":8,"value":74.4,"matchedTradingVolume":808393.0},{"month":9,"value":79.0,"matchedTradingVolume":720323.0},{"month":10,"value":84.3,"matchedTradingVolume":897248.0},{"month":11,"value":76.2,"matchedTradingVolume":420061.0},{"month":12,"value":78.4,"matchedTradingVolume":593973.0}],"dividendSpitingHistories":[]},{"symbol":"CEO","companyName":"CTCP Tập đoàn C.E.O","type":"HNX30","year":2023,"prices":[{"month":1,"value":24.6,"matchedTradingVolume":1.27064933E8},{"month":2,"value":23.4,"matchedTradingVolume":1.75287235E8},{"month":3,"value":22.2,"matchedTradingVolume":1.36584726E8},{"month":4,"value":25.5,"matchedTradingVolume":1.86700486E8},{"month":5,"value":27.2,"matchedTradingVolume":1.60517931E8},{"month":6,"value":27.6,"matchedTradingVolume":1.65627114E8},{"month":7,"value":23.9,"matchedTradingVolume":2.0278093E8},{"month":8,"value":26.2,"matchedTradingVolume":3.2929596E8},{"month":9,"value":28.4,"matchedTradingVolume":1.79469034E8},{"month":10,"value":21.6,"matchedTradingVolume":2.0827932E8},{"month":11,"value":24.1,"matchedTradingVolume":4.01348366E8},{"month":12,"value":23.9,"matchedTradingVolume":2.56520459E8}],"dividendSpitingHistories":[]},{"symbol":"DTD","companyName":"CTCP Đầu tư Phát triển Thành Đạt","type":"HNX30","year":2023,"prices":[{"month":1,"value":14.4,"matchedTradingVolume":5950842.0},{"month":2,"value":13.7,"matchedTradingVolume":6378838.0},{"month":3,"value":16.6,"matchedTradingVolume":7311940.0},{"month":4,"value":18.1,"matchedTradingVolume":1.0294297E7},{"month":5,"value":31.9,"matchedTradingVolume":2.2655048E7},{"month":6,"value":32.5,"matchedTradingVolume":1.8129994E7},{"month":7,"value":36.7,"matchedTradingVolume":1.5735536E7},{"month":8,"value":32.5,"matchedTradingVolume":1.6086212E7},{"month":9,"value":30.9,"matchedTradingVolume":1.1056539E7},{"month":10,"value":30.5,"matchedTradingVolume":1.8741944E7},{"month":11,"value":24.0,"matchedTradingVolume":1.831541E7},{"month":12,"value":26.3,"matchedTradingVolume":2.4949081E7}],"dividendSpitingHistories":[]},{"symbol":"DXP","companyName":"CTCP Cảng Đoạn Xá","type":"HNX30","year":2023,"prices":[{"month":1,"value":10.4,"matchedTradingVolume":912739.0},{"month":2,"value":10.3,"matchedTradingVolume":917376.0},{"month":3,"value":9.8,"matchedTradingVolume":787279.0},{"month":4,"value":9.9,"matchedTradingVolume":885375.0},{"month":5,"value":12.8,"matchedTradingVolume":1782047.0},{"month":6,"value":13.5,"matchedTradingVolume":3439863.0},{"month":7,"value":14.0,"matchedTradingVolume":1994362.0},{"month":8,"value":13.8,"matchedTradingVolume":2432178.0},{"month":9,"value":14.1,"matchedTradingVolume":4273324.0},{"month":10,"value":14.8,"matchedTradingVolume":9033438.0},{"month":11,"value":13.3,"matchedTradingVolume":1.0391949E7},{"month":12,"value":13.4,"matchedTradingVolume":6974255.0}],"dividendSpitingHistories":[]},{"symbol":"HLD","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":29.8,"matchedTradingVolume":231503.0},{"month":2,"value":28.2,"matchedTradingVolume":226901.0},{"month":3,"value":27.4,"matchedTradingVolume":140330.0},{"month":4,"value":35.6,"matchedTradingVolume":496224.0},{"month":5,"value":37.2,"matchedTradingVolume":307238.0},{"month":6,"value":36.6,"matchedTradingVolume":339320.0},{"month":7,"value":33.0,"matchedTradingVolume":620471.0},{"month":8,"value":32.6,"matchedTradingVolume":589525.0},{"month":9,"value":31.5,"matchedTradingVolume":674240.0},{"month":10,"value":27.6,"matchedTradingVolume":250531.0},{"month":11,"value":26.4,"matchedTradingVolume":395171.0},{"month":12,"value":26.5,"matchedTradingVolume":307473.0}],"dividendSpitingHistories":[]},{"symbol":"HUT","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":16.8,"matchedTradingVolume":2.6232682E7},{"month":2,"value":15.4,"matchedTradingVolume":3.1806604E7},{"month":3,"value":16.1,"matchedTradingVolume":4.0121809E7},{"month":4,"value":17.2,"matchedTradingVolume":3.9834208E7},{"month":5,"value":18.5,"matchedTradingVolume":5.0768478E7},{"month":6,"value":20.1,"matchedTradingVolume":7.7486457E7},{"month":7,"value":21.1,"matchedTradingVolume":6.905587E7},{"month":8,"value":27.4,"matchedTradingVolume":1.21918856E8},{"month":9,"value":28.5,"matchedTradingVolume":1.24166119E8},{"month":10,"value":24.2,"matchedTradingVolume":1.05483677E8},{"month":11,"value":21.1,"matchedTradingVolume":1.2679697E8},{"month":12,"value":21.3,"matchedTradingVolume":1.20443764E8}],"dividendSpitingHistories":[]},{"symbol":"IDC","companyName":"Tổng Công ty IDICO – CTCP","type":"HNX30","year":2023,"prices":[{"month":1,"value":40.4,"matchedTradingVolume":4.2236657E7},{"month":2,"value":42.5,"matchedTradingVolume":7.1829678E7},{"month":3,"value":41.0,"matchedTradingVolume":5.5623409E7},{"month":4,"value":41.9,"matchedTradingVolume":4.1157756E7},{"month":5,"value":41.9,"matchedTradingVolume":5.167149E7},{"month":6,"value":44.2,"matchedTradingVolume":7.3655552E7},{"month":7,"value":45.7,"matchedTradingVolume":6.2733165E7},{"month":8,"value":49.3,"matchedTradingVolume":8.3958141E7},{"month":9,"value":50.4,"matchedTradingVolume":6.1038327E7},{"month":10,"value":52.5,"matchedTradingVolume":9.3609479E7},{"month":11,"value":50.5,"matchedTradingVolume":5.7923673E7},{"month":12,"value":52.2,"matchedTradingVolume":5.3508845E7}],"dividendSpitingHistories":[{"month":4,"value":2000.0},{"month":9,"value":2000.0}]},{"symbol":"L14","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":58.9,"matchedTradingVolume":7741503.0},{"month":2,"value":53.5,"matchedTradingVolume":7944098.0},{"month":3,"value":45.9,"matchedTradingVolume":5681449.0},{"month":4,"value":54.2,"matchedTradingVolume":1.0662182E7},{"month":5,"value":52.2,"matchedTradingVolume":1.278968E7},{"month":6,"value":48.0,"matchedTradingVolume":1.3094389E7},{"month":7,"value":48.0,"matchedTradingVolume":1.0732735E7},{"month":8,"value":62.0,"matchedTradingVolume":2.2437095E7},{"month":9,"value":59.9,"matchedTradingVolume":1.1478379E7},{"month":10,"value":44.5,"matchedTradingVolume":6285716.0},{"month":11,"value":46.6,"matchedTradingVolume":1.0706426E7},{"month":12,"value":48.8,"matchedTradingVolume":7059836.0}],"dividendSpitingHistories":[]},{"symbol":"L18","companyName":"CTCP Đầu tư và Xây dựng Số 18","type":"HNX30","year":2023,"prices":[{"month":1,"value":22.5,"matchedTradingVolume":762349.0},{"month":2,"value":22.8,"matchedTradingVolume":948665.0},{"month":3,"value":25.4,"matchedTradingVolume":880699.0},{"month":4,"value":29.5,"matchedTradingVolume":972819.0},{"month":5,"value":39.5,"matchedTradingVolume":1285782.0},{"month":6,"value":37.0,"matchedTradingVolume":890512.0},{"month":7,"value":39.0,"matchedTradingVolume":1114914.0},{"month":8,"value":42.0,"matchedTradingVolume":1684345.0},{"month":9,"value":41.6,"matchedTradingVolume":1101101.0},{"month":10,"value":35.0,"matchedTradingVolume":536762.0},{"month":11,"value":36.0,"matchedTradingVolume":676349.0},{"month":12,"value":42.0,"matchedTradingVolume":1204132.0}],"dividendSpitingHistories":[{"month":1,"value":800.0},{"month":3,"value":700.0}]},{"symbol":"LAS","companyName":"CTCP Supe Phốt phát và Hóa chất Lâm Thao","type":"HNX30","year":2023,"prices":[{"month":1,"value":9.0,"matchedTradingVolume":3578318.0},{"month":2,"value":8.8,"matchedTradingVolume":4052633.0},{"month":3,"value":8.6,"matchedTradingVolume":3805041.0},{"month":4,"value":9.3,"matchedTradingVolume":8152270.0},{"month":5,"value":10.6,"matchedTradingVolume":1.5071426E7},{"month":6,"value":11.6,"matchedTradingVolume":1.6968799E7},{"month":7,"value":13.4,"matchedTradingVolume":1.3925595E7},{"month":8,"value":13.5,"matchedTradingVolume":1.0302924E7},{"month":9,"value":14.7,"matchedTradingVolume":1.2641782E7},{"month":10,"value":14.2,"matchedTradingVolume":1.1448746E7},{"month":11,"value":14.0,"matchedTradingVolume":1.3527785E7},{"month":12,"value":15.0,"matchedTradingVolume":1.7700348E7}],"dividendSpitingHistories":[{"month":8,"value":600.0}]},{"symbol":"LHC","companyName":"CTCP Đầu tư và Xây dựng Thủy lợi Lâm Đồng","type":"HNX30","year":2023,"prices":[{"month":1,"value":52.0,"matchedTradingVolume":360814.0},{"month":2,"value":51.0,"matchedTradingVolume":158300.0},{"month":3,"value":51.8,"matchedTradingVolume":534500.0},{"month":4,"value":52.0,"matchedTradingVolume":203612.0},{"month":5,"value":49.8,"matchedTradingVolume":130386.0},{"month":6,"value":50.2,"matchedTradingVolume":388275.0},{"month":7,"value":57.0,"matchedTradingVolume":891568.0},{"month":8,"value":57.5,"matchedTradingVolume":283634.0},{"month":9,"value":60.7,"matchedTradingVolume":272250.0},{"month":10,"value":57.9,"matchedTradingVolume":95227.0},{"month":11,"value":53.9,"matchedTradingVolume":397727.0},{"month":12,"value":52.9,"matchedTradingVolume":177928.0}],"dividendSpitingHistories":[{"month":3,"value":500.0},{"month":8,"value":1500.0}]},{"symbol":"MBS","companyName":"CTCP Chứng khoán MB","type":"HNX30","year":2023,"prices":[{"month":1,"value":15.3,"matchedTradingVolume":3.8321764E7},{"month":2,"value":14.8,"matchedTradingVolume":3.8730351E7},{"month":3,"value":15.8,"matchedTradingVolume":5.5555374E7},{"month":4,"value":17.6,"matchedTradingVolume":8.1238888E7},{"month":5,"value":18.5,"matchedTradingVolume":6.6965434E7},{"month":6,"value":19.5,"matchedTradingVolume":7.4072721E7},{"month":7,"value":21.2,"matchedTradingVolume":7.4782537E7},{"month":8,"value":21.2,"matchedTradingVolume":7.9872284E7},{"month":9,"value":24.5,"matchedTradingVolume":8.6962514E7},{"month":10,"value":23.5,"matchedTradingVolume":1.09345483E8},{"month":11,"value":22.0,"matchedTradingVolume":1.07702558E8},{"month":12,"value":23.4,"matchedTradingVolume":8.3679495E7}],"dividendSpitingHistories":[]},{"symbol":"NBC","companyName":"CTCP Than Núi Béo - Vinacomin","type":"HNX30","year":2023,"prices":[{"month":1,"value":11.8,"matchedTradingVolume":3613717.0},{"month":2,"value":12.1,"matchedTradingVolume":7089386.0},{"month":3,"value":11.5,"matchedTradingVolume":3494563.0},{"month":4,"value":12.7,"matchedTradingVolume":6028485.0},{"month":5,"value":12.7,"matchedTradingVolume":6823417.0},{"month":6,"value":13.3,"matchedTradingVolume":5858620.0},{"month":7,"value":13.6,"matchedTradingVolume":7106972.0},{"month":8,"value":13.4,"matchedTradingVolume":6584419.0},{"month":9,"value":12.6,"matchedTradingVolume":4992643.0},{"month":10,"value":11.7,"matchedTradingVolume":2871754.0},{"month":11,"value":11.2,"matchedTradingVolume":2702813.0},{"month":12,"value":12.2,"matchedTradingVolume":3338675.0}],"dividendSpitingHistories":[{"month":6,"value":300.0}]},{"symbol":"PLC","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":28.0,"matchedTradingVolume":8019236.0},{"month":2,"value":32.8,"matchedTradingVolume":1.6214208E7},{"month":3,"value":35.0,"matchedTradingVolume":1.7856342E7},{"month":4,"value":34.4,"matchedTradingVolume":1.3343638E7},{"month":5,"value":37.6,"matchedTradingVolume":1.1009234E7},{"month":6,"value":39.0,"matchedTradingVolume":9749548.0},{"month":7,"value":40.4,"matchedTradingVolume":8317441.0},{"month":8,"value":39.5,"matchedTradingVolume":6508016.0},{"month":9,"value":37.7,"matchedTradingVolume":4813765.0},{"month":10,"value":34.7,"matchedTradingVolume":3137853.0},{"month":11,"value":30.7,"matchedTradingVolume":3341603.0},{"month":12,"value":33.2,"matchedTradingVolume":2711591.0}],"dividendSpitingHistories":[]},{"symbol":"PSI","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":6.1,"matchedTradingVolume":563172.0},{"month":2,"value":6.0,"matchedTradingVolume":563212.0},{"month":3,"value":5.6,"matchedTradingVolume":698563.0},{"month":4,"value":7.0,"matchedTradingVolume":2494209.0},{"month":5,"value":7.9,"matchedTradingVolume":2745850.0},{"month":6,"value":9.0,"matchedTradingVolume":3780471.0},{"month":7,"value":9.0,"matchedTradingVolume":2673914.0},{"month":8,"value":9.8,"matchedTradingVolume":5783383.0},{"month":9,"value":12.2,"matchedTradingVolume":1.1061288E7},{"month":10,"value":9.9,"matchedTradingVolume":4885496.0},{"month":11,"value":9.2,"matchedTradingVolume":4076293.0},{"month":12,"value":9.5,"matchedTradingVolume":2586015.0}],"dividendSpitingHistories":[]},{"symbol":"PVC","companyName":"Tổng Công ty Hóa chất và Dịch vụ Dầu khí - CTCP","type":"HNX30","year":2023,"prices":[{"month":1,"value":15.6,"matchedTradingVolume":3.5163557E7},{"month":2,"value":15.6,"matchedTradingVolume":3.82605E7},{"month":3,"value":16.5,"matchedTradingVolume":3.9275747E7},{"month":4,"value":16.4,"matchedTradingVolume":3.8379409E7},{"month":5,"value":18.5,"matchedTradingVolume":4.7079449E7},{"month":6,"value":18.6,"matchedTradingVolume":3.9167582E7},{"month":7,"value":19.4,"matchedTradingVolume":3.1585006E7},{"month":8,"value":19.8,"matchedTradingVolume":3.2294619E7},{"month":9,"value":20.0,"matchedTradingVolume":3.0883423E7},{"month":10,"value":18.9,"matchedTradingVolume":3.0460937E7},{"month":11,"value":15.2,"matchedTradingVolume":3.6621345E7},{"month":12,"value":16.1,"matchedTradingVolume":2.7428238E7}],"dividendSpitingHistories":[{"month":11,"value":180.0}]},{"symbol":"PVG","companyName":"CTCP Kinh doanh LPG Việt Nam","type":"HNX30","year":2023,"prices":[{"month":1,"value":8.0,"matchedTradingVolume":1164214.0},{"month":2,"value":8.5,"matchedTradingVolume":1859515.0},{"month":3,"value":8.1,"matchedTradingVolume":1124560.0},{"month":4,"value":8.1,"matchedTradingVolume":1783152.0},{"month":5,"value":9.2,"matchedTradingVolume":3510578.0},{"month":6,"value":10.7,"matchedTradingVolume":6292684.0},{"month":7,"value":10.5,"matchedTradingVolume":4906952.0},{"month":8,"value":10.9,"matchedTradingVolume":6233546.0},{"month":9,"value":10.4,"matchedTradingVolume":3017782.0},{"month":10,"value":10.0,"matchedTradingVolume":1405768.0},{"month":11,"value":9.3,"matchedTradingVolume":662121.0},{"month":12,"value":9.2,"matchedTradingVolume":656764.0}],"dividendSpitingHistories":[{"month":6,"value":300.0}]},{"symbol":"PVS","companyName":"Tổng Công ty cổ phần Dịch vụ Kỹ thuật Dầu khí Việt Nam","type":"HNX30","year":2023,"prices":[{"month":1,"value":25.6,"matchedTradingVolume":8.6042635E7},{"month":2,"value":26.8,"matchedTradingVolume":1.31385208E8},{"month":3,"value":27.5,"matchedTradingVolume":1.16136499E8},{"month":4,"value":26.4,"matchedTradingVolume":8.0120016E7},{"month":5,"value":31.0,"matchedTradingVolume":1.40267109E8},{"month":6,"value":33.1,"matchedTradingVolume":1.59161373E8},{"month":7,"value":35.0,"matchedTradingVolume":1.08046493E8},{"month":8,"value":36.0,"matchedTradingVolume":1.52167647E8},{"month":9,"value":39.5,"matchedTradingVolume":1.29903345E8},{"month":10,"value":40.7,"matchedTradingVolume":1.57780759E8},{"month":11,"value":39.0,"matchedTradingVolume":1.24880714E8},{"month":12,"value":40.2,"matchedTradingVolume":8.5316604E7}],"dividendSpitingHistories":[{"month":10,"value":700.0}]},{"symbol":"SHS","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":10.0,"matchedTradingVolume":2.53793966E8},{"month":2,"value":9.3,"matchedTradingVolume":2.51382589E8},{"month":3,"value":9.2,"matchedTradingVolume":3.14457024E8},{"month":4,"value":10.6,"matchedTradingVolume":4.86724587E8},{"month":5,"value":11.8,"matchedTradingVolume":4.03628131E8},{"month":6,"value":14.0,"matchedTradingVolume":5.12915603E8},{"month":7,"value":15.6,"matchedTradingVolume":3.51958733E8},{"month":8,"value":18.6,"matchedTradingVolume":5.05353394E8},{"month":9,"value":20.5,"matchedTradingVolume":4.23334614E8},{"month":10,"value":18.2,"matchedTradingVolume":5.72161445E8},{"month":11,"value":18.4,"matchedTradingVolume":6.88673172E8},{"month":12,"value":19.7,"matchedTradingVolume":4.23218842E8}],"dividendSpitingHistories":[]},{"symbol":"SLS","companyName":"CTCP Mía Đường Sơn La","type":"HNX30","year":2023,"prices":[{"month":1,"value":141.5,"matchedTradingVolume":105965.0},{"month":2,"value":153.0,"matchedTradingVolume":371779.0},{"month":3,"value":151.0,"matchedTradingVolume":107135.0},{"month":4,"value":175.0,"matchedTradingVolume":243202.0},{"month":5,"value":172.5,"matchedTradingVolume":214329.0},{"month":6,"value":174.3,"matchedTradingVolume":161085.0},{"month":7,"value":217.5,"matchedTradingVolume":317260.0},{"month":8,"value":218.4,"matchedTradingVolume":460531.0},{"month":9,"value":207.9,"matchedTradingVolume":338896.0},{"month":10,"value":215.0,"matchedTradingVolume":570007.0},{"month":11,"value":158.0,"matchedTradingVolume":344405.0},{"month":12,"value":151.3,"matchedTradingVolume":273898.0}],"dividendSpitingHistories":[{"month":10,"value":15000.0}]},{"symbol":"TDN","companyName":"CTCP Than Đèo Nai - Vinacomin","type":"HNX30","year":2023,"prices":[{"month":1,"value":10.5,"matchedTradingVolume":830221.0},{"month":2,"value":10.9,"matchedTradingVolume":2139323.0},{"month":3,"value":10.6,"matchedTradingVolume":872061.0},{"month":4,"value":12.1,"matchedTradingVolume":2504970.0},{"month":5,"value":11.8,"matchedTradingVolume":2689719.0},{"month":6,"value":11.3,"matchedTradingVolume":2294625.0},{"month":7,"value":11.4,"matchedTradingVolume":2683671.0},{"month":8,"value":11.2,"matchedTradingVolume":2355125.0},{"month":9,"value":10.6,"matchedTradingVolume":824593.0},{"month":10,"value":10.0,"matchedTradingVolume":663198.0},{"month":11,"value":9.4,"matchedTradingVolume":317910.0},{"month":12,"value":10.3,"matchedTradingVolume":470014.0}],"dividendSpitingHistories":[{"month":5,"value":800.0}]},{"symbol":"TIG","companyName":"CTCP Tập đoàn Đầu tư Thăng Long","type":"HNX30","year":2023,"prices":[{"month":1,"value":9.4,"matchedTradingVolume":1.4718354E7},{"month":2,"value":9.2,"matchedTradingVolume":1.9183104E7},{"month":3,"value":8.5,"matchedTradingVolume":1.2889752E7},{"month":4,"value":8.6,"matchedTradingVolume":1.8732883E7},{"month":5,"value":11.5,"matchedTradingVolume":3.367642E7},{"month":6,"value":11.9,"matchedTradingVolume":2.8614289E7},{"month":7,"value":12.6,"matchedTradingVolume":2.6129853E7},{"month":8,"value":12.8,"matchedTradingVolume":3.2215207E7},{"month":9,"value":12.1,"matchedTradingVolume":1.5110764E7},{"month":10,"value":11.2,"matchedTradingVolume":1.6428527E7},{"month":11,"value":12.2,"matchedTradingVolume":3.6912427E7},{"month":12,"value":13.1,"matchedTradingVolume":6.5307842E7}],"dividendSpitingHistories":[]},{"symbol":"TNG","companyName":"CTCP Đầu tư và Thương mại TNG","type":"HNX30","year":2023,"prices":[{"month":1,"value":15.9,"matchedTradingVolume":2.2788741E7},{"month":2,"value":18.8,"matchedTradingVolume":5.383754E7},{"month":3,"value":18.5,"matchedTradingVolume":4.7327191E7},{"month":4,"value":20.0,"matchedTradingVolume":4.8994383E7},{"month":5,"value":20.1,"matchedTradingVolume":4.066419E7},{"month":6,"value":20.5,"matchedTradingVolume":3.733616E7},{"month":7,"value":21.3,"matchedTradingVolume":3.6046131E7},{"month":8,"value":21.3,"matchedTradingVolume":3.9840949E7},{"month":9,"value":22.6,"matchedTradingVolume":5.6823464E7},{"month":10,"value":21.6,"matchedTradingVolume":5.7013818E7},{"month":11,"value":19.5,"matchedTradingVolume":3.3075049E7},{"month":12,"value":20.4,"matchedTradingVolume":4.1724689E7}],"dividendSpitingHistories":[{"month":1,"value":400.0},{"month":10,"value":400.0}]},{"symbol":"TVD","companyName":"CTCP Than Vàng Danh - Vinacomin","type":"HNX30","year":2023,"prices":[{"month":1,"value":13.6,"matchedTradingVolume":4460374.0},{"month":2,"value":16.1,"matchedTradingVolume":1.2369639E7},{"month":3,"value":15.2,"matchedTradingVolume":5436677.0},{"month":4,"value":16.0,"matchedTradingVolume":7688533.0},{"month":5,"value":16.3,"matchedTradingVolume":1.0313929E7},{"month":6,"value":18.0,"matchedTradingVolume":1.0095238E7},{"month":7,"value":16.6,"matchedTradingVolume":9646606.0},{"month":8,"value":16.4,"matchedTradingVolume":6320529.0},{"month":9,"value":14.9,"matchedTradingVolume":2552604.0},{"month":10,"value":13.8,"matchedTradingVolume":1537320.0},{"month":11,"value":12.9,"matchedTradingVolume":1610533.0},{"month":12,"value":14.4,"matchedTradingVolume":1243333.0}],"dividendSpitingHistories":[{"month":6,"value":900.0}]},{"symbol":"VC3","companyName":"CTCP Tập đoàn Nam Mê Kông","type":"HNX30","year":2023,"prices":[{"month":1,"value":31.9,"matchedTradingVolume":3708499.0},{"month":2,"value":31.0,"matchedTradingVolume":6255386.0},{"month":3,"value":29.8,"matchedTradingVolume":6890555.0},{"month":4,"value":29.2,"matchedTradingVolume":4813528.0},{"month":5,"value":32.0,"matchedTradingVolume":1.0960064E7},{"month":6,"value":29.8,"matchedTradingVolume":1.4275123E7},{"month":7,"value":25.7,"matchedTradingVolume":9058122.0},{"month":8,"value":27.5,"matchedTradingVolume":1.2952619E7},{"month":9,"value":26.0,"matchedTradingVolume":7353372.0},{"month":10,"value":24.3,"matchedTradingVolume":8545141.0},{"month":11,"value":24.4,"matchedTradingVolume":1.1344333E7},{"month":12,"value":25.0,"matchedTradingVolume":1.3213301E7}],"dividendSpitingHistories":[]},{"symbol":"VCS","companyName":"CTCP Vicostone","type":"HNX30","year":2023,"prices":[{"month":1,"value":57.8,"matchedTradingVolume":1602832.0},{"month":2,"value":55.0,"matchedTradingVolume":1419547.0},{"month":3,"value":52.4,"matchedTradingVolume":733426.0},{"month":4,"value":52.2,"matchedTradingVolume":1070085.0},{"month":5,"value":56.9,"matchedTradingVolume":2587508.0},{"month":6,"value":61.7,"matchedTradingVolume":3409753.0},{"month":7,"value":64.3,"matchedTradingVolume":3504930.0},{"month":8,"value":67.5,"matchedTradingVolume":4021339.0},{"month":9,"value":69.0,"matchedTradingVolume":2404724.0},{"month":10,"value":63.8,"matchedTradingVolume":2062699.0},{"month":11,"value":57.9,"matchedTradingVolume":1492424.0},{"month":12,"value":57.3,"matchedTradingVolume":859008.0}],"dividendSpitingHistories":[{"month":6,"value":2000.0},{"month":12,"value":2000.0}]},{"symbol":"VIG","companyName":null,"type":"HNX30","year":2023,"prices":[{"month":1,"value":6.1,"matchedTradingVolume":3000777.0},{"month":2,"value":6.1,"matchedTradingVolume":2827039.0},{"month":3,"value":5.8,"matchedTradingVolume":6426854.0},{"month":4,"value":6.5,"matchedTradingVolume":1.2815084E7},{"month":5,"value":7.7,"matchedTradingVolume":1.3108227E7},{"month":6,"value":8.7,"matchedTradingVolume":1.5290969E7},{"month":7,"value":8.6,"matchedTradingVolume":1.6843152E7},{"month":8,"value":8.9,"matchedTradingVolume":2.145496E7},{"month":9,"value":10.8,"matchedTradingVolume":2.6101975E7},{"month":10,"value":8.6,"matchedTradingVolume":1.3054237E7},{"month":11,"value":7.9,"matchedTradingVolume":1.2156118E7},{"month":12,"value":8.1,"matchedTradingVolume":7288746.0}],"dividendSpitingHistories":[]}]}'
# futureData = loadDataInput(jsonInput2023)
# exe_experiments(futureData)
# printSolution('DONE hnx30_5years_before')


