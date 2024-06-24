import numpy as np

from constants import DURATION
from stock_data_input_16 import STOCK_DATA_2023_INPUT_16_STOCKS

stocks_len = len(STOCK_DATA_2023_INPUT_16_STOCKS)

# Initialize matrices
C = np.zeros((stocks_len, DURATION))
Q = np.zeros((stocks_len, DURATION))
D = np.zeros((stocks_len, DURATION))

# Populate matrices
for i, stock in enumerate(STOCK_DATA_2023_INPUT_16_STOCKS):
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

# print("DONE!")
