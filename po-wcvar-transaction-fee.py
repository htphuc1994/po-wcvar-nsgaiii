import math
import sys
import time
import random

import pandas as pd
import numpy as np
import datetime
import pywt
from pymoo.core.repair import Repair
from pymoo.core.sampling import Sampling
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga3 import NSGA3, hop
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from scipy.stats import norm
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from assets_returns import *
from constants import TRANS_FEE, BANK_INTEREST_RATE, INITIAL_CASH, DURATION, MAX_STOCKS, TERMINATION_GEN_NUM, \
    TAIL_PROBABILITY_EPSILON, POPULATION_SIZE, REFERENCES_POINTS_NUM, WAVELET_LEVEL, INVESTMENT_INTEREST_EXPECTED
from manual_test_four_stocks import STOCK_DATA_2023_INPUT_3_STOCKS
from stock_data_input_249 import STOCK_DATA_2023_INPUT_249_STOCKS
from wavelet_cvar_utils import compute_wavelet_variance, wavelet_decomposition, calculate_var_from_wavelet_variance, \
    calculate_cvar, cal_po_wCVaR



stock_data = STOCK_DATA_2023_INPUT_249_STOCKS
LEN_STOCK_DATA = len(stock_data)
# stock_data = STOCK_DATA_2023_INPUT_3_STOCKS
# stock_returns = np.column_stack((
#     ABT, ACB, ACL))
# stock_returns = np.column_stack((
#     ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP, BPC, BST, BTS, BVS,
#     CAN, CAP, CCM, CDC, CID, CII, CJC, CLC, CMC, COM, CTB, CTC, CTN, DAC, DAE, DBC, DC4, DCS, DHA,
#     DHG, DHT, DIC, DMC, DPC, DPM, DPR, DQC, DRC, DST, DTC, DTT, DXP, DXV, EBS, FMC, FPT, GIL, GMC,
#     GMD, GTA, HAG, HAP, HAS, HAX, HBC, HCC, HCT, HDC, HEV, HHC, HJS, HMC, HPG, HRC, HSG, HSI, HT1,
#     HTP, HTV, HUT, ICF, IMP, ITA, KBC, KDC, KHP, KKC, KMR, KSH, L10, L18, L43, L61, L62, LAF, LBE,
#     LBM, LCG, LGC, LSS, LTC))
stock_returns = np.column_stack((
    ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP,
    BPC, BST, BTS, BVS, CAN, CAP, CCM, CDC, CID, CII, CJC, CLC, CMC, COM, CTB,
    CTC, CTN, DAC, DAE, DBC, DC4, DCS, DHA, DHG, DHT, DIC, DMC, DPC, DPM, DPR,
    DQC, DRC, DST, DTC, DTT, DXP, DXV, EBS, FMC, FPT, GIL, GMC, GMD, GTA, HAG,
    HAP, HAS, HAX, HBC, HCC, HCT, HDC, HEV, HHC, HJS, HMC, HPG, HRC, HSG, HSI,
    HT1, HTP, HTV, HUT, ICF, IMP, ITA, KBC, KDC, KHP, KKC, KMR, KSH, L10, L18,
    L43, L61, L62, LAF, LBE, LBM, LCG, LGC, LSS, LTC, MCO, MCP, MEC, MHC, MKV,
    MTG, NAV, NBC, NGC, NHC, NSC, NST, NTL, NTP, ONE, OPC, PAC, PAN, PET, PGC,
    PGS, PIT, PJC, PJT, PLC, PMS, PNC, POT, PPC, PSC, PTC, PTS, PVC, PVD, PVE,
    PVG, PVI, PVS, PVT, QTC, RAL, RCL, REE, S12, S55, S99, SAM, SAP, SAV, SBT,
    SC5, SCD, SCJ, SD5, SD6, SD7, SD9, SDA, SDC, SDD, SDN, SDT, SDY, SFC, SFI,
    SFN, SGC, SGD, SJ1, SJD, SJE, SJM, SJS, SMC, SRA, SRB, SSC, SSI, SSM, ST8,
    STB, STC, STP, SVC, SVI, SZL, TBC, TBX, TC6, TCM, TCR, TCT, TDH, TDN, THB,
    THT, TJC, TKU, TMC, TMS, TNA, TNC, TNG, TPC, TPH, TPP, TRA, TRC, TSC, TTC,
    TTF, TV4, TXM, TYA, UIC, UNI, VBH, VC2, VC5, VC6, VC7, VCG, VCS, VDL, VE1,
    VFR, VGP, VGS, VHC, VHG, VIC, VID, VIP, VMC, VNA, VNC, VNE, VNM, VNR, VNS,
    VSC, VSG, VSH, VTB, VTC, VTO, VTS, VTV, YBC))

bank_interest_rate = BANK_INTEREST_RATE
initial_cash = INITIAL_CASH  # 1 bln VND
duration = DURATION  # 12 months
max_stocks = MAX_STOCKS  # Example cardinality constraint
termination_gen_num = TERMINATION_GEN_NUM
tail_probability_epsilon = TAIL_PROBABILITY_EPSILON
population_size = POPULATION_SIZE
BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD = math.pow(1 + BANK_INTEREST_RATE, DURATION) - 1


# def wavelet_decomposition(returns, wavelet='db4', levels=WAVELET_LEVEL):
#     """ Decompose asset returns using Discrete Wavelet Transform. """
#     coeffs = pywt.wavedec(returns, wavelet, level=levels)
#     return coeffs[1:]  # Returning detail coefficients, ignoring approximation
#
#
# def compute_wavelet_variance(coeffs):
#     """ Compute the wavelet variance from detail wavelet coefficients. """
#     variances = [np.var(c) for c in coeffs]  # Compute variance of each level
#     return np.mean(variances)  # Return the mean of variances across levels
#
#
# #     """ Estimate portfolio VaR directly from wavelet variances. """
# def calculate_var_from_wavelet_variance(wavelet_variance, tail_probability, scaling_factor=1.0):
#     """ Estimate portfolio VaR directly from wavelet variances. """
#     # Calculate the inverse of the cumulative distribution function for the given confidence level
#     z_score = norm.ppf(1 - tail_probability)
#     return scaling_factor * z_score * np.sqrt(wavelet_variance)  # Simple model to convert variance to VaR
#
#
# def calculate_cvar(portfolio_returns, var):
#     """ Calculate Conditional Value-at-Risk (CVaR) based on VaR. """
#     losses_exceeding_var = [loss for loss in portfolio_returns if loss <= var]
#     return np.mean(losses_exceeding_var) if losses_exceeding_var else 0

def print_detail_v2(log, cash, stock_holdings, stock_data):
    # Create an empty DataFrame to store the structured data
    columns = ["Month", "Action", "Stock", "Amount", "Dividends", "BankDeposit"]
    df = pd.DataFrame(columns=columns)

    # Populate the DataFrame with log data
    for entry in log:
        month = entry['Month']
        dividends = entry['Dividends']
        bank_deposit = entry['BankDeposit']

        # Process Buy actions
        if entry["Buy"]:
            for stock, amount in entry["Buy"]:
                df = df.append({
                    "Month": month,
                    "Action": "Buy",
                    "Stock": stock,
                    "Amount": amount,
                    "Dividends": dividends,
                    "BankDeposit": bank_deposit
                }, ignore_index=True)

        # Process Sell actions
        if entry["Sell"]:
            for stock, amount in entry["Sell"]:
                df = df.append({
                    "Month": month,
                    "Action": "Sell",
                    "Stock": stock,
                    "Amount": amount,
                    "Dividends": dividends,
                    "BankDeposit": bank_deposit
                }, ignore_index=True)

        # Add row for Dividends and Bank Deposit only if no Buy or Sell actions
        if not entry["Buy"] and not entry["Sell"]:
            df = df.append({
                "Month": month,
                "Action": "None",
                "Stock": None,
                "Amount": None,
                "Dividends": dividends,
                "BankDeposit": bank_deposit
            }, ignore_index=True)
    # Log final cash and holdings to ensure we do not hold any stocks
    print(f"Final Cash: {cash:.2f} => return: {(cash-initial_cash)/initial_cash:.2f}")
    # import tools.display_dataframe_to_user(name="Investment Log", dataframe=df)


def print_detail(log, cash, stock_holdings, stock_data):
    for entry in log:
        print(f"Month {entry['Month']}:")
        if entry["Buy"]:
            for stock, amount in entry["Buy"]:
                print(f"  Buy: Stock {stock}, Amount: {amount}")
        if entry["Sell"]:
            for stock, amount in entry["Sell"]:
                print(f"  Sell: Stock {stock}, Amount: {amount}")
        print(f"  Dividends: {entry['Dividends']:.2f}")
        print(f"  Bank Deposit: {entry['BankDeposit']:.2f}")
    print("\n")

    # Log final cash and holdings to ensure we do not hold any stocks
    print(f"Final Cash: {cash:.2f} => return: {(cash-initial_cash)/initial_cash:.2f}")
    # for j, stock in enumerate(stock_data):
    #     print(f"Final Holdings: Stock {stock['symbol']}, Amount: {stock_holdings[j]}")


# def cal_po_wCVaR(month, stock_holdings, cvar_values, i, returns):
#     # Calculate CVaR at the beginning of each month
#     if 0 < month < duration:
#         portfolio_returns = np.dot(returns, stock_holdings)
#
#         wavelet_variance = compute_wavelet_variance(wavelet_decomposition(portfolio_returns))
#
#         portfolio_var = calculate_var_from_wavelet_variance(wavelet_variance, tail_probability_epsilon,
#                                                             scaling_factor=initial_cash)
#
#         portfolio_cvar = calculate_cvar(portfolio_returns, portfolio_var)
#         cvar_values[i, month] = portfolio_cvar

class CustomSampling(Sampling):

    def _do(self, problem, n_samples, **kwargs):
        # pop = np.array(pop, dtype=int)
        pop = np.zeros((POPULATION_SIZE, problem.n_var))
        for i in range(POPULATION_SIZE):
            for j in range(problem.n_var):
                if problem.xu[j] == 0:
                    pop[i, j] = 0
                else:
                    pop[i, j] = random.choice(range(math.floor(problem.xu[j])))

        n_stocks = LEN_STOCK_DATA
        investment_duration = DURATION
        total_cash = np.zeros(pop.shape[0])
        # cvar_values = np.zeros((pop.shape[0], investment_duration))
        # cardinality_violations = np.zeros((pop.shape[0], investment_duration))
        deferred_dividends = np.zeros((pop.shape[0], investment_duration + 1))
        deferred_sale_proceeds = np.zeros((pop.shape[0], investment_duration + 1))

        for i in range(pop.shape[0]):  # processing the i-th individual
            cash = INITIAL_CASH
            stock_holdings = np.zeros(n_stocks)
            previous_stock_holdings = np.zeros(n_stocks)  # To track holdings from the previous month

            # returns = stock_returns

            duration_plus_1 = investment_duration + 1  # we just collect $$$ after the investment.
            for month in range(duration_plus_1):
                # Update cash with bank interest
                if cash < 0:
                    print("ERROR somewhere then cash < 0")
                if month != 0 and cash > 0:
                    cash *= (1 + BANK_INTEREST_RATE)

                # Add deferred dividends and sale proceeds from the previous month
                if deferred_dividends[i, month] < 0 or deferred_sale_proceeds[i, month] < 0:
                    print("ERROR somewhere then deferred_dividends or deferred_sale_proceeds < 0")
                # if deferred_dividends[i, month] > 0 or deferred_sale_proceeds[i, month] > 0:
                #     print("ACK: Received cash")
                cash += deferred_dividends[i, month]
                cash += deferred_sale_proceeds[i, month]
                if month == investment_duration:
                    break

                # if 0 < month < investment_duration:
                #     current_month_prices = []
                #     for stock_info in stock_data:
                #         current_month_prices.append(stock_info["prices"][month][
                #                                         "value"])  # month also is the index = month + 1 in "month" field
                #
                #     returns = np.vstack((returns, np.array(current_month_prices).reshape(1, -1)))
                #     # Calculate CVaR at the beginning of each month
                #     cal_po_wCVaR(month, stock_holdings, cvar_values, i, returns, duration, tail_probability_epsilon, initial_cash, cash)

                buy_decisions = pop[i, month * n_stocks:(month + 1) * n_stocks]
                sell_decisions = pop[i, (investment_duration + month) * n_stocks:(investment_duration + month + 1) * n_stocks]

                # Prevent buys in the last month
                if month == investment_duration - 1:
                    buy_decisions[:] = 0

                # monthly_log = {"Month": month + 1, "Buy": [], "Sell": [], "Dividends": 0, "BankDeposit": 0}
                aggregated_sell_decisions = np.zeros(n_stocks)  # store $$$

                for j in range(n_stocks):
                    stock = stock_data[j]
                    stock_symbol = stock['symbol']
                    stock_price = stock["prices"][month]['value']
                    stock_capacity = stock["prices"][month]['matchedTradingVolume']

                    # Prevent sells during dividend months
                    if month == 0 or ((month + 1) in [dividend['month'] for dividend in stock['dividendSpitingHistories']]):
                        sell_decisions[j] = 0
                    # print(f"{buy_decisions[j]};{sell_decisions[j]}")
                    if (buy_decisions[j] > 0 and
                            ((np.floor(buy_decisions[j]) == np.floor(sell_decisions[j])) or
                             (np.floor(buy_decisions[j]) >= stock_capacity and np.floor(
                                 sell_decisions[j]) >= stock_capacity) or
                             ((np.floor(buy_decisions[j]) + stock_holdings[j] - int(np.floor(min(sell_decisions[j], stock_capacity))) <= 0)))):
                        sell_decisions[j] = 0

                    # Process buy decisions
                    if buy_decisions[j] > 0:
                        buy_amount = int(np.floor(min(buy_decisions[j], stock_capacity)))

                        buy_amount_restricted_by_current_cash = np.floor(cash/stock_price/(1 + TRANS_FEE))
                        buy_amount = int(np.floor(min(buy_amount, buy_amount_restricted_by_current_cash)))
                        buy_decisions[j] = buy_amount
                        transaction_fee = TRANS_FEE * stock_price * buy_amount
                        total_buy_cost = stock_price * buy_amount + transaction_fee

                        if np.count_nonzero(stock_holdings) >= MAX_STOCKS and stock_holdings[
                            j] <= 0:  # cardinality check
                            break
                        # Ensure we do not buy more than the available cash
                        if total_buy_cost <= cash:
                            cash -= total_buy_cost
                            stock_holdings[j] += buy_amount
                            # monthly_log["Buy"].append((stock_symbol, buy_amount))

                    # Aggregate sell decisions
                    if sell_decisions[j] > 0:
                        sell_amount = int(np.floor(min(sell_decisions[j], np.floor(stock_holdings[j]))))
                        aggregated_sell_decisions[j] += sell_amount

                    # Calculate dividends if current month is a dividend month
                    for dividend in stock['dividendSpitingHistories']:
                        if (month + 1) == dividend['month'] and previous_stock_holdings[j] > 0:
                            if month != investment_duration - 1 and aggregated_sell_decisions[
                                j] <= 0:  # Ensure no dividends are received if stock is sold in the same month
                                dividends = dividend['value'] * previous_stock_holdings[j] / 1000  # kVND
                                # Defer dividends to the next month
                                deferred_dividends[i, month + 1] += dividends
                                # monthly_log["Dividends"] += dividends

                # Process aggregated sell decisions
                for j in range(n_stocks):
                    stock_price = stock_data[j]["prices"][month]['value']
                    if aggregated_sell_decisions[j] > 0:
                        sell_amount = aggregated_sell_decisions[j]
                        transaction_fee = TRANS_FEE * sell_amount * stock_price
                        total_sell_proceeds = sell_amount * stock_price - transaction_fee

                        # Defer sale proceeds to the next month
                        deferred_sale_proceeds[i, month + 1] += total_sell_proceeds
                        stock_holdings[j] -= sell_amount
                        # monthly_log["Sell"].append((stock_data[j]['symbol'], sell_amount))

                # Save the current holdings to use for dividend eligibility in the next month
                previous_stock_holdings = stock_holdings.copy()

                # Check for cardinality constraint violation
                unique_stocks_held = np.sum(stock_holdings > 0)
                # if unique_stocks_held > self.max_stocks:
                #     cardinality_violations[i, month] = unique_stocks_held - self.max_stocks

                # monthly_log["BankDeposit"] = cash
                # log.append(monthly_log)

                pop[i, month * n_stocks:(month + 1) * n_stocks] = buy_decisions
                pop[i,
                (investment_duration + month) * n_stocks:(investment_duration + month + 1) * n_stocks] = sell_decisions

            # Ensure all holdings are sold at the end of the last month
            for j in range(n_stocks):
                remaining_sell_amount = stock_holdings[j]
                if remaining_sell_amount > 0:
                    for m in range(investment_duration - 1, -1, -1):
                        sell_decisions = pop[i,
                                         (investment_duration + m) * n_stocks:(investment_duration + m + 1) * n_stocks]

                        stock_price = stock_data[j]["prices"][m]['value']
                        stock_capacity = stock_data[j]["prices"][m]['matchedTradingVolume']

                        new_capacity = stock_capacity - sell_decisions[j]
                        if new_capacity < 0:
                            new_capacity = 0
                        sell_amount = min(np.floor(remaining_sell_amount), new_capacity)
                        if sell_amount <= 0:
                            continue
                        transaction_fee = TRANS_FEE * stock_price * sell_amount
                        total_sell_proceeds = stock_price * sell_amount - transaction_fee
                        cash += total_sell_proceeds * (1 + bank_interest_rate)
                        remaining_sell_amount -= sell_amount
                        if sell_amount > 0:
                            # log[m]["Sell"].append((stock_data[j]['symbol'], sell_amount))
                            sell_decisions[j] = sell_decisions[j] + sell_amount

                            pop[i, (investment_duration + m) * n_stocks:(
                                                                                investment_duration + m + 1) * n_stocks] = sell_decisions
                        if remaining_sell_amount <= 0:
                            break

                    stock_holdings[j] = 0
            # End investment so collect money

            total_cash[i] = cash
            # if total_cash[i] > initial_cash * (1 + bank_interest_rate):
            #     print(f"ACK>> OK total_cash[{i}] = {cash}")

            # print_detail(log, cash, stock_holdings, stock_data)

        # Store the manipulated solution using the index of the solution
        # idx = kwargs.get('idx')
        # if idx is not None:
        #     self.manipulated_solutions[idx] = X
        return pop

class CustomRepair(Repair):
    def _do(self, problem, pop, **kwargs):
        pop = np.array(pop, dtype=int)
        n_stocks = LEN_STOCK_DATA
        investment_duration = DURATION
        total_cash = np.zeros(pop.shape[0])
        # cvar_values = np.zeros((pop.shape[0], investment_duration))
        # cardinality_violations = np.zeros((pop.shape[0], investment_duration))
        deferred_dividends = np.zeros((pop.shape[0], investment_duration + 1))
        deferred_sale_proceeds = np.zeros((pop.shape[0], investment_duration + 1))

        for i in range(pop.shape[0]):  # processing the i-th individual
            cash = INITIAL_CASH
            stock_holdings = np.zeros(n_stocks)
            previous_stock_holdings = np.zeros(n_stocks)  # To track holdings from the previous month
            log = []

            returns = stock_returns

            duration_plus_1 = investment_duration + 1  # we just collect $$$ after the investment.
            for month in range(duration_plus_1):
                # Update cash with bank interest
                if cash < 0:
                    print("ERROR somewhere then cash < 0")
                if month != 0 and cash > 0:
                    cash *= (1 + BANK_INTEREST_RATE)

                # Add deferred dividends and sale proceeds from the previous month
                if deferred_dividends[i, month] < 0 or deferred_sale_proceeds[i, month] < 0:
                    print("ERROR somewhere then deferred_dividends or deferred_sale_proceeds < 0")
                # if deferred_dividends[i, month] > 0 or deferred_sale_proceeds[i, month] > 0:
                #     print("ACK: Received cash")
                cash += deferred_dividends[i, month]
                cash += deferred_sale_proceeds[i, month]
                if month == investment_duration:
                    break

                # if 0 < month < investment_duration:
                #     current_month_prices = []
                #     for stock_info in stock_data:
                #         current_month_prices.append(stock_info["prices"][month][
                #                                         "value"])  # month also is the index = month + 1 in "month" field
                #
                #     returns = np.vstack((returns, np.array(current_month_prices).reshape(1, -1)))
                #     # Calculate CVaR at the beginning of each month
                #     cal_po_wCVaR(month, stock_holdings, cvar_values, i, returns, duration, tail_probability_epsilon, initial_cash, cash)

                buy_decisions = pop[i, month * n_stocks:(month + 1) * n_stocks]
                sell_decisions = pop[i,
                                 (investment_duration + month) * n_stocks:(investment_duration + month + 1) * n_stocks]

                # Prevent buys in the last month
                if month == investment_duration - 1:
                    buy_decisions[:] = 0

                # monthly_log = {"Month": month + 1, "Buy": [], "Sell": [], "Dividends": 0, "BankDeposit": 0}
                aggregated_sell_decisions = np.zeros(n_stocks)  # store $$$

                for j in range(n_stocks):
                    stock = stock_data[j]
                    stock_symbol = stock['symbol']
                    stock_price = stock["prices"][month]['value']
                    stock_capacity = stock["prices"][month]['matchedTradingVolume']

                    # Prevent sells during dividend months
                    if month == 0 or ((month + 1) in [dividend['month'] for dividend in stock['dividendSpitingHistories']]):
                        sell_decisions[j] = 0
                    # print(f"{buy_decisions[j]};{sell_decisions[j]}")
                    if (buy_decisions[j] > 0 and
                            ((np.floor(buy_decisions[j]) == np.floor(sell_decisions[j])) or
                             (np.floor(buy_decisions[j]) >= stock_capacity and np.floor(
                                 sell_decisions[j]) >= stock_capacity) or
                             ((np.floor(buy_decisions[j]) + stock_holdings[j] - int(
                                 np.floor(min(sell_decisions[j], stock_capacity))) <= 0)))):
                        sell_decisions[j] = 0

                    # Process buy decisions
                    if buy_decisions[j] > 0:
                        buy_amount = int(np.floor(min(buy_decisions[j], stock_capacity)))

                        buy_amount_restricted_by_current_cash = np.floor(cash/stock_price/(1 + TRANS_FEE))
                        buy_amount = int(np.floor(min(buy_amount, buy_amount_restricted_by_current_cash)))
                        buy_decisions[j] = buy_amount
                        transaction_fee = TRANS_FEE * stock_price * buy_amount
                        total_buy_cost = stock_price * buy_amount + transaction_fee

                        if np.count_nonzero(stock_holdings) >= MAX_STOCKS and stock_holdings[
                            j] <= 0:  # cardinality check
                            break
                        # Ensure we do not buy more than the available cash
                        if total_buy_cost <= cash:
                            cash -= total_buy_cost
                            stock_holdings[j] += buy_amount
                            # monthly_log["Buy"].append((stock_symbol, buy_amount))

                    # Aggregate sell decisions
                    if sell_decisions[j] > 0:
                        sell_amount = int(np.floor(min(sell_decisions[j], np.floor(stock_holdings[j]))))
                        aggregated_sell_decisions[j] += sell_amount

                    # Calculate dividends if current month is a dividend month
                    for dividend in stock['dividendSpitingHistories']:
                        if (month + 1) == dividend['month'] and previous_stock_holdings[j] > 0:
                            if month != investment_duration - 1 and aggregated_sell_decisions[
                                j] <= 0:  # Ensure no dividends are received if stock is sold in the same month
                                dividends = dividend['value'] * previous_stock_holdings[j] / 1000  # kVND
                                # Defer dividends to the next month
                                deferred_dividends[i, month + 1] += dividends
                                # monthly_log["Dividends"] += dividends

                # Process aggregated sell decisions
                for j in range(n_stocks):
                    stock_price = stock_data[j]["prices"][month]['value']
                    if aggregated_sell_decisions[j] > 0:
                        sell_amount = aggregated_sell_decisions[j]
                        transaction_fee = TRANS_FEE * sell_amount * stock_price
                        total_sell_proceeds = sell_amount * stock_price - transaction_fee

                        # Defer sale proceeds to the next month
                        deferred_sale_proceeds[i, month + 1] += total_sell_proceeds
                        stock_holdings[j] -= sell_amount
                        # monthly_log["Sell"].append((stock_data[j]['symbol'], sell_amount))

                # Save the current holdings to use for dividend eligibility in the next month
                previous_stock_holdings = stock_holdings.copy()

                # Check for cardinality constraint violation
                unique_stocks_held = np.sum(stock_holdings > 0)
                # if unique_stocks_held > self.max_stocks:
                #     cardinality_violations[i, month] = unique_stocks_held - self.max_stocks

                # monthly_log["BankDeposit"] = cash
                # log.append(monthly_log)

                pop[i, month * n_stocks:(month + 1) * n_stocks] = buy_decisions
                pop[i,
                (investment_duration + month) * n_stocks:(investment_duration + month + 1) * n_stocks] = sell_decisions

            # Ensure all holdings are sold at the end of the last month
            for j in range(n_stocks):
                remaining_sell_amount = stock_holdings[j]
                if remaining_sell_amount > 0:
                    for m in range(investment_duration - 1, -1, -1):
                        sell_decisions = pop[i,
                                         (investment_duration + m) * n_stocks:(investment_duration + m + 1) * n_stocks]

                        stock_price = stock_data[j]["prices"][m]['value']
                        stock_capacity = stock_data[j]["prices"][m]['matchedTradingVolume']

                        new_capacity = stock_capacity - sell_decisions[j]
                        if new_capacity < 0:
                            new_capacity = 0
                        sell_amount = min(np.floor(remaining_sell_amount), new_capacity)
                        if sell_amount <= 0:
                            continue
                        transaction_fee = TRANS_FEE * stock_price * sell_amount
                        total_sell_proceeds = stock_price * sell_amount - transaction_fee
                        cash += total_sell_proceeds * (1 + bank_interest_rate)
                        remaining_sell_amount -= sell_amount
                        if sell_amount > 0:
                            # log[m]["Sell"].append((stock_data[j]['symbol'], sell_amount))
                            sell_decisions[j] = sell_decisions[j] + sell_amount

                            pop[i, (investment_duration + m) * n_stocks:(
                                                                              investment_duration + m + 1) * n_stocks] = sell_decisions
                        if remaining_sell_amount <= 0:
                            break

                    stock_holdings[j] = 0
            # End investment so collect money

            total_cash[i] = cash
            # if total_cash[i] > initial_cash * (1 + bank_interest_rate):
            #     print(f"ACK>> OK total_cash[{i}] = {cash}")

            # print_detail(log, cash, stock_holdings, stock_data)

        # Store the manipulated solution using the index of the solution
        # idx = kwargs.get('idx')
        # if idx is not None:
        #     self.manipulated_solutions[idx] = X
        return pop

class PortfolioOptimizationProblem(Problem):
    def __init__(self, _stock_data, _bank_interest_rate, _initial_cash, _duration, _max_stocks):
        self.stock_data = _stock_data
        self.bank_interest_rate = _bank_interest_rate
        self.initial_cash = _initial_cash
        self.duration = _duration
        self.n_stocks = len(_stock_data)
        self.max_stocks = _max_stocks

        # Define bounds for the decision variables
        # xl: half left (hl) is buy decisions | half right (hr) is sell decisions
        # In hl portion: self.duration months buy stock1 | self.duration months buy stock2...
        # In hr portion: self.duration months sell stock1 | self.duration months sell stock2...
        xl = np.zeros(2 * self.n_stocks * self.duration, dtype=int)  # Lower bounds (all zeros, no negative quantities)

        sell_xu = []
        expected_cash_after_investment = INITIAL_CASH*(1+INVESTMENT_INTEREST_EXPECTED)
        for stock in _stock_data:
            month_prices = sorted(stock["prices"], key=lambda x: x['month'])
            for month_price in month_prices:
                if month_price["month"] > self.duration:
                    break
                sell_xu.append(min(int(month_price["matchedTradingVolume"]), int(expected_cash_after_investment/month_price["value"])))
        xu = sell_xu + sell_xu

        super().__init__(n_var=2 * self.n_stocks * self.duration, n_obj=self.duration, n_constr=self.duration + 1,
                         xl=xl,
                         xu=xu,
                         type_var=int)
        # self.manipulated_solutions = []

    def _evaluate(self, X, out, *args, **kwargs):
        # X = np.array(X, dtype=int)
        n_stocks = self.n_stocks
        investment_duration = self.duration
        total_cash = np.zeros(X.shape[0])
        cvar_values = np.zeros((X.shape[0], investment_duration))
        cardinality_violations = np.zeros((X.shape[0], investment_duration))
        deferred_dividends = np.zeros((X.shape[0], investment_duration + 1))
        deferred_sale_proceeds = np.zeros((X.shape[0], investment_duration + 1))

        for i in range(X.shape[0]):  # processing the i-th individual
            cash = self.initial_cash
            stock_holdings = np.zeros(n_stocks)
            previous_stock_holdings = np.zeros(n_stocks)  # To track holdings from the previous month
            log = []

            returns = stock_returns

            duration_plus_1 = investment_duration + 1  # we just collect $$$ after the investment.
            for month in range(duration_plus_1):
                # Update cash with bank interest
                if cash < 0:
                    print("ERROR somewhere then cash < 0")
                if month != 0 and cash > 0:
                    cash *= (1 + self.bank_interest_rate)

                # Add deferred dividends and sale proceeds from the previous month
                if deferred_dividends[i, month] < 0 or deferred_sale_proceeds[i, month] < 0:
                    print("ERROR somewhere then deferred_dividends or deferred_sale_proceeds < 0")
                # if deferred_dividends[i, month] > 0 or deferred_sale_proceeds[i, month] > 0:
                #     print("ACK: Received cash")
                cash += deferred_dividends[i, month]
                cash += deferred_sale_proceeds[i, month]
                if month == investment_duration:
                    break

                if 0 < month < investment_duration:
                    current_month_prices = []
                    for stock_info in stock_data:
                        current_month_prices.append(stock_info["prices"][month]["value"])  # month also is the index = month + 1 in "month" field

                    returns = np.vstack((returns, np.array(current_month_prices).reshape(1, -1)))
                    # Calculate CVaR at the beginning of each month
                    cal_po_wCVaR(month, stock_holdings, cvar_values, i, returns, duration, tail_probability_epsilon, initial_cash, cash)

                buy_decisions = X[i, month * n_stocks:(month + 1) * n_stocks]
                sell_decisions = X[i, (investment_duration + month) * n_stocks:(investment_duration + month + 1) * n_stocks]

                # Prevent buys in the last month
                if month == investment_duration - 1:
                    buy_decisions[:] = 0

                monthly_log = {"Month": month + 1, "Buy": [], "Sell": [], "Dividends": 0, "BankDeposit": 0}
                aggregated_sell_decisions = np.zeros(n_stocks)  # store $$$

                for j in range(n_stocks):
                    stock = self.stock_data[j]
                    stock_symbol = stock['symbol']
                    stock_price = stock["prices"][month]['value']
                    stock_capacity = stock["prices"][month]['matchedTradingVolume']

                    # Prevent sells during dividend months
                    if month == 0 or (
                            (month + 1) in [dividend['month'] for dividend in stock['dividendSpitingHistories']]):
                        sell_decisions[j] = 0
                    # print(f"{buy_decisions[j]};{sell_decisions[j]}")
                    if (buy_decisions[j] > 0 and
                            ((np.floor(buy_decisions[j]) == np.floor(sell_decisions[j])) or
                             (np.floor(buy_decisions[j]) >= stock_capacity and np.floor(sell_decisions[j]) >= stock_capacity) or
                             (np.floor(buy_decisions[j]) + stock_holdings[j] - int(np.floor(min(0 if math.isnan(sell_decisions[j]) else sell_decisions[j], stock_capacity))) <= 0))):
                        sell_decisions[j] = 0

                    # Process buy decisions
                    if buy_decisions[j] > 0:
                        buy_amount = int(np.floor(min(buy_decisions[j], stock_capacity)))

                        buy_amount_restricted_by_current_cash = np.floor(cash/stock_price/(1 + TRANS_FEE))
                        buy_amount = int(np.floor(min(buy_amount, buy_amount_restricted_by_current_cash)))
                        buy_decisions[j] = buy_amount
                        transaction_fee = TRANS_FEE * stock_price * buy_amount
                        total_buy_cost = stock_price * buy_amount + transaction_fee

                        if np.count_nonzero(stock_holdings) >= MAX_STOCKS and stock_holdings[
                            j] <= 0:  # cardinality check
                            break
                        # Ensure we do not buy more than the available cash
                        if total_buy_cost <= cash:
                            cash -= total_buy_cost
                            stock_holdings[j] += buy_amount
                            monthly_log["Buy"].append((stock_symbol, buy_amount))

                    # Aggregate sell decisions
                    if sell_decisions[j] > 0:
                        sell_amount = int(np.floor(min(sell_decisions[j], np.floor(stock_holdings[j]))))
                        aggregated_sell_decisions[j] += sell_amount

                    # Calculate dividends if current month is a dividend month
                    for dividend in stock['dividendSpitingHistories']:
                        if (month + 1) == dividend['month'] and previous_stock_holdings[j] > 0:
                            if month != investment_duration - 1 and aggregated_sell_decisions[j] <= 0:  # Ensure no dividends are received if stock is sold in the same month
                                dividends = dividend['value'] * previous_stock_holdings[j] / 1000  # kVND
                                # Defer dividends to the next month
                                deferred_dividends[i, month + 1] += dividends
                                monthly_log["Dividends"] += dividends

                # Process aggregated sell decisions
                for j in range(n_stocks):
                    stock_price = self.stock_data[j]["prices"][month]['value']
                    if aggregated_sell_decisions[j] > 0:
                        sell_amount = aggregated_sell_decisions[j]
                        transaction_fee = TRANS_FEE * sell_amount * stock_price
                        total_sell_proceeds = sell_amount * stock_price - transaction_fee

                        # Defer sale proceeds to the next month
                        deferred_sale_proceeds[i, month + 1] += total_sell_proceeds
                        stock_holdings[j] -= sell_amount
                        monthly_log["Sell"].append((self.stock_data[j]['symbol'], sell_amount))

                # Save the current holdings to use for dividend eligibility in the next month
                previous_stock_holdings = stock_holdings.copy()

                # Check for cardinality constraint violation
                unique_stocks_held = np.sum(stock_holdings > 0)
                if unique_stocks_held > self.max_stocks:
                    cardinality_violations[i, month] = unique_stocks_held - self.max_stocks

                monthly_log["BankDeposit"] = cash
                log.append(monthly_log)

                X[i, month * n_stocks:(month + 1) * n_stocks] = buy_decisions
                X[i,(investment_duration + month) * n_stocks:(investment_duration + month + 1) * n_stocks] = sell_decisions

            # Ensure all holdings are sold at the end of the last month
            for j in range(n_stocks):
                remaining_sell_amount = stock_holdings[j]
                if remaining_sell_amount > 0:
                    for m in range(investment_duration - 1, -1, -1):
                        sell_decisions = X[i,(investment_duration + m) * n_stocks:(investment_duration + m + 1) * n_stocks]

                        stock_price = self.stock_data[j]["prices"][m]['value']
                        stock_capacity = self.stock_data[j]["prices"][m]['matchedTradingVolume']

                        new_capacity = stock_capacity - sell_decisions[j]
                        if new_capacity < 0:
                            new_capacity = 0
                        sell_amount = min(np.floor(remaining_sell_amount), new_capacity)
                        if sell_amount <= 0:
                            continue
                        transaction_fee = TRANS_FEE * stock_price * sell_amount
                        total_sell_proceeds = stock_price * sell_amount - transaction_fee
                        cash += total_sell_proceeds * (1 + bank_interest_rate)
                        remaining_sell_amount -= sell_amount
                        if sell_amount > 0:
                            log[m]["Sell"].append((self.stock_data[j]['symbol'], sell_amount))
                            if math.isnan(sell_decisions[j]) or math.isnan(sell_amount):
                                sell_decisions[j] = 0
                            sell_decisions[j] = sell_decisions[j] + sell_amount

                            X[i, (investment_duration + m) * n_stocks:(investment_duration + m + 1) * n_stocks] = sell_decisions
                        if remaining_sell_amount <= 0:
                            break

                    stock_holdings[j] = 0
            # End investment so collect money

            total_cash[i] = cash
            # if total_cash[i] > initial_cash * (1 + bank_interest_rate):
            #     print(f"ACK>> OK total_cash[{i}] = {cash}")

            if cash > (1 + BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD) * initial_cash:
                print_detail(log, cash, stock_holdings, stock_data)

        # Store the manipulated solution using the index of the solution
        # idx = kwargs.get('idx')
        # if idx is not None:
        #     self.manipulated_solutions[idx] = X
        # self.manipulated_solutions.clear()
        # self.manipulated_solutions.extend(X)

        out["F"] = np.column_stack((-(total_cash-initial_cash)/initial_cash, cvar_values[:, 1:]))
        returns_constraint = total_cash - (1 + INVESTMENT_INTEREST_EXPECTED) * initial_cash
        # returns_constraint = total_cash - initial_cash
        out["G"] = np.column_stack((returns_constraint, cardinality_violations))
        # out["G"] = cardinality_violations


def my_solve():
    problem = PortfolioOptimizationProblem(stock_data, bank_interest_rate, initial_cash, duration, max_stocks)

    ref_dirs = get_reference_directions("energy", problem.n_obj, REFERENCES_POINTS_NUM, seed=1)
    # algorithm = NSGA3(pop_size=population_size, ref_dirs=ref_dirs, repair=CustomRepair())
    algorithm = NSGA3(pop_size=population_size, ref_dirs=ref_dirs, sampling=CustomSampling())

    res = minimize(problem,
                   algorithm,
                   termination=('n_gen', termination_gen_num),
                   seed=10,
                   save_history=True,
                   verbose=True)

    F = res.pop.get("F")
    # F = problem.manipulated_solutions

    # calculate the fronts of the population
    fronts, rank = NonDominatedSorting().do(F, return_rank=True, n_stop_if_ranked=population_size)

    # remove solutions with their returns < trivial solution (only bank deposits)
    front_0 = [individual for individual in res.pop[fronts[0]] if
               -individual.F[0] > BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD]

    # hop_solution = res.pop[hop(res.pop, front_0)[0]]
    len_front_0 = len(front_0)
    if len_front_0 <= 0:
        print("No HOP solution found.")
        return
    hop_solution = front_0[hop(front_0, np.arange(len_front_0))[0]]

    # len_F = len(F)
    # hop_solution_index = 0
    # for i in range(len_F):
    #     if all(a == b for a, b in zip(F[i], hop_solution.F)):
    #         hop_solution_index = i
    #         break
    # hop_solution_index = F.index(hop_solution.F)

    print("Objectives =", ["%.5f" % v for v in hop_solution.F])
    # solution_details = np.array(hop_solution.X, dtype=int)
    # solution_details = problem.manipulated_solutions[hop_solution_index]
    # print("Solution details =", [v for v in solution_details])


# Open a file in write mode
def execute():
    timestamp = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    unique_filename = f"output-{timestamp}.txt"
    with open("output/" + unique_filename, 'w') as f:
        start = time.time()
        # Save the original standard output
        original_stdout = sys.stdout

        # Redirect standard output to the file
        sys.stdout = f
        print("Starting to write..")
        my_solve()

        end = time.time()
        print("The time of execution of above program is :",
              (end - start) * 10 ** 3, "ms")

        sys.stdout = original_stdout

for i in range(3):
    print(f"Starting loop i={i}...")
    execute()
print("DONE - Thank you")
