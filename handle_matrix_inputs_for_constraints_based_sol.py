import numpy as np

from constants import DURATION
from stock_data_input_16 import STOCK_DATA_2023_INPUT_16_STOCKS
from wavelet_cvar_utils import cal_po_wCVaR
from assets_returns import *

stock_data = STOCK_DATA_2023_INPUT_16_STOCKS
LEN_STOCK_DATA = len(stock_data)
stock_returns = np.column_stack((
    ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP, BPC))
# stock_returns = np.column_stack((
#     ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP, BPC, BST, BTS, BVS,
#     CAN, CAP, CCM, CDC, CID, CII, CJC, CLC, CMC, COM, CTB, CTC, CTN, DAC, DAE, DBC, DC4, DCS, DHA,
#     DHG, DHT, DIC, DMC, DPC, DPM, DPR, DQC, DRC, DST, DTC, DTT, DXP, DXV, EBS, FMC, FPT, GIL, GMC,
#     GMD, GTA, HAG, HAP, HAS, HAX, HBC, HCC, HCT, HDC, HEV, HHC, HJS, HMC, HPG, HRC, HSG, HSI, HT1,
#     HTP, HTV, HUT, ICF, IMP, ITA, KBC, KDC, KHP, KKC, KMR, KSH, L10, L18, L43, L61, L62, LAF, LBE,
#     LBM, LCG, LGC, LSS, LTC))

# from stock_data_input_100 import STOCK_DATA_2023_INPUT_100_STOCKS
#
# stocks_len = len(STOCK_DATA_2023_INPUT_100_STOCKS)

# Initialize matrices
C = np.zeros((LEN_STOCK_DATA, DURATION))
Q = np.zeros((LEN_STOCK_DATA, DURATION))
D = np.zeros((LEN_STOCK_DATA, DURATION))

# Populate matrices
for i, stock in enumerate(stock_data):
    for price_info in stock["prices"]:
        if price_info["month"] > DURATION:
            break
        month = price_info["month"] - 1
        C[i, month] = price_info["value"]
        Q[i, month] = price_info["matchedTradingVolume"]
    for dividend_info in stock["dividendSpitingHistories"]:
        if dividend_info["month"] > DURATION:
            break
        month = dividend_info["month"] - 1
        D[i, month] = dividend_info["value"]/1000.0

