import sys

import numpy as np
import datetime
import pywt
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga3 import NSGA3, hop
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from scipy.stats import norm
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from assets_returns import *
from constants import TRANS_FEE, BANK_INTEREST_RATE, INITIAL_CASH, DURATION, MAX_STOCKS, TERMINATION_GEN_NUM, \
    TAIL_PROBABILITY_EPSILON, POPULATION_SIZE, REFERENCES_POINTS_NUM, WAVELET_LEVEL
from stock_data_input_100 import STOCK_DATA_2023_INPUT_100_STOCKS
from stock_data_inputs_251 import STOCK_DATA_2023_INPUT_251_STOCKS


# stock_data = STOCK_DATA_2023_INPUT_251_STOCKS
stock_data = STOCK_DATA_2023_INPUT_100_STOCKS

bank_interest_rate = BANK_INTEREST_RATE
initial_cash = INITIAL_CASH  # 1 bln VND
duration = DURATION  # 12 months
max_stocks = MAX_STOCKS  # Example cardinality constraint
termination_gen_num = TERMINATION_GEN_NUM
tail_probability_epsilon = TAIL_PROBABILITY_EPSILON
population_size = POPULATION_SIZE


def wavelet_decomposition(returns, wavelet='db4', levels=WAVELET_LEVEL):
    """ Decompose asset returns using Discrete Wavelet Transform. """
    coeffs = pywt.wavedec(returns, wavelet, level=levels)
    return coeffs[1:]  # Returning detail coefficients, ignoring approximation


def compute_wavelet_variance(coeffs):
    """ Compute the wavelet variance from detail wavelet coefficients. """
    variances = [np.var(c) for c in coeffs]  # Compute variance of each level
    return np.mean(variances)  # Return the mean of variances across levels


#     """ Estimate portfolio VaR directly from wavelet variances. """
def calculate_var_from_wavelet_variance(wavelet_variance, tail_probability, scaling_factor=1.0):
    """ Estimate portfolio VaR directly from wavelet variances. """
    # Calculate the inverse of the cumulative distribution function for the given confidence level
    z_score = norm.ppf(1 - tail_probability)
    return scaling_factor * z_score * np.sqrt(wavelet_variance)  # Simple model to convert variance to VaR


def calculate_cvar(portfolio_returns, var):
    """ Calculate Conditional Value-at-Risk (CVaR) based on VaR. """
    losses_exceeding_var = [loss for loss in portfolio_returns if loss <= var]
    return np.mean(losses_exceeding_var) if losses_exceeding_var else 0


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
    print(f"Final Cash: {cash:.2f}")
    # for j, stock in enumerate(stock_data):
    #     print(f"Final Holdings: Stock {stock['symbol']}, Amount: {stock_holdings[j]}")


def cal_po_wCVaR(month, stock_holdings, cvar_values, i, stock_data):
    # Calculate CVaR at the beginning of each month
    if 0 < month < duration:
        # returns = np.column_stack((
        #     ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP,
        #     BPC, BST, BTS, BVS, CAN, CAP, CCM, CDC, CID, CII, CJC, CLC, CMC, COM, CTB,
        #     CTC, CTN, DAC, DAE, DBC, DC4, DCS, DHA, DHG, DHT, DIC, DMC, DPC, DPM, DPR,
        #     DQC, DRC, DST, DTC, DTT, DXP, DXV, EBS, FMC, FPT, GIL, GMC, GMD, GTA, HAG,
        #     HAP, HAS, HAX, HBC, HCC, HCT, HDC, HEV, HHC, HJS, HMC, HPG, HRC, HSG, HSI,
        #     HT1, HTP, HTV, HUT, ICF, IMP, ITA, KBC, KDC, KHP, KKC, KMR, KSH, L10, L18,
        #     L43, L61, L62, LAF, LBE, LBM, LCG, LGC, LSS, LTC, MCO, MCP, MEC, MHC, MKV,
        #     MTG, NAV, NBC, NGC, NHC, NSC, NST, NTL, NTP, ONE, OPC, PAC, PAN, PET, PGC,
        #     PGS, PIT, PJC, PJT, PLC, PMS, PNC, POT, PPC, PSC, PTC, PTS, PVC, PVD, PVE,
        #     PVG, PVI, PVS, PVT, QTC, RAL, RCL, REE, S12, S55, S99, SAM, SAP, SAV, SBT,
        #     SC5, SCD, SCJ, SD5, SD6, SD7, SD9, SDA, SDC, SDD, SDN, SDT, SDY, SFC, SFI,
        #     SFN, SGC, SGD, SJ1, SJD, SJE, SJM, SJS, SMC, SRA, SRB, SSC, SSI, SSM, ST8,
        #     STB, STC, STP, SVC, SVI, SZL, TBC, TBX, TC6, TCM, TCR, TCT, TDH, TDN, THB,
        #     THT, TJC, TKU, TMC, TMS, TNA, TNC, TNG, TPC, TPH, TPP, TRA, TRC, TSC, TTC,
        #     TTF, TV4, TXM, TYA, UIC, UNI, VBH, VC2, VC5, VC6, VC7, VCG, VCS, VDL, VE1,
        #     VFR, VGP, VGS, VHC, VHG, VIC, VID, VIP, VMC, VNA, VNC, VNE, VNM, VNR, VNS,
        #     VSC, VSG, VSH, VTB, VTC, VTO, VTS, VTV, YBC))

        returns = np.column_stack((
            ABT,ACB,ACL,AGF,ALT,ANV,ASP,B82,BBC,BBS,BCC,BLF,BMC,BMI,BMP,BPC,BST,BTS,BVS,
            CAN,CAP,CCM,CDC,CID,CII,CJC,CLC,CMC,COM,CTB,CTC,CTN,DAC,DAE,DBC,DC4,DCS,DHA,
            DHG,DHT,DIC,DMC,DPC,DPM,DPR,DQC,DRC,DST,DTC,DTT,DXP,DXV,EBS,FMC,FPT,GIL,GMC,
            GMD,GTA,HAG,HAP,HAS,HAX,HBC,HCC,HCT,HDC,HEV,HHC,HJS,HMC,HPG,HRC,HSG,HSI,HT1,
            HTP,HTV,HUT,ICF,IMP,ITA,KBC,KDC,KHP,KKC,KMR,KSH,L10,L18,L43,L61,L62,LAF,LBE,
            LBM,LCG,LGC,LSS,LTC))

        current_month_prices = []
        for stock_info in stock_data:
            current_month_prices.append(stock_info["prices"][month]["value"]) # month also is the index = month + 1 in "month" field

        returns = np.vstack((returns, np.array(current_month_prices).reshape(1, -1)))

        portfolio_returns = np.dot(returns, stock_holdings)

        wavelet_variance = compute_wavelet_variance(wavelet_decomposition(portfolio_returns))

        portfolio_var = calculate_var_from_wavelet_variance(wavelet_variance, tail_probability_epsilon,
                                                            scaling_factor=initial_cash)

        portfolio_cvar = calculate_cvar(portfolio_returns, portfolio_var)
        cvar_values[i, month] = portfolio_cvar

class PortfolioOptimizationProblem(Problem):
    def __init__(self, stock_data, bank_interest_rate, initial_cash, duration, max_stocks):
        self.stock_data = stock_data
        self.bank_interest_rate = bank_interest_rate
        self.initial_cash = initial_cash
        self.duration = duration
        self.n_stocks = len(stock_data)
        self.max_stocks = max_stocks

        # Define bounds for the decision variables
        # xl: half left (hl) is buy decisions | half right (hr) is sell decisions
        # In hl portion: n months buy stock1 | n months buy stock2...
        # In hr portion: n months sell stock1 | n months sell stock2...
        xl = np.zeros(2 * self.n_stocks * self.duration)  # Lower bounds (all zeros, no negative quantities)

        sell_xu = []
        for stock in stock_data:
            month_prices = sorted(stock["prices"], key=lambda x: x['month'])
            for month_price in month_prices:
                if month_price["month"] > self.duration:
                    break
                sell_xu.append(month_price["matchedTradingVolume"])
        xu = sell_xu + sell_xu

        super().__init__(n_var=2 * self.n_stocks * self.duration, n_obj=self.duration, n_constr=self.duration, xl=xl,
                         xu=xu)

    def _evaluate(self, X, out, *args, **kwargs):
        n_stocks = self.n_stocks
        duration = self.duration
        total_cash = np.zeros(X.shape[0])
        cvar_values = np.zeros((X.shape[0], duration))
        cardinality_violations = np.zeros((X.shape[0], duration))
        deferred_dividends = np.zeros((X.shape[0], duration + 1))
        deferred_sale_proceeds = np.zeros((X.shape[0], duration + 1))

        for i in range(X.shape[0]): # processing the i-th individual
            cash = self.initial_cash
            stock_holdings = np.zeros(n_stocks)
            previous_stock_holdings = np.zeros(n_stocks)  # To track holdings from the previous month
            log = []

            for month in range(duration):
                # Update cash with bank interest
                if month != 0:
                    cash *= (1 + self.bank_interest_rate / 100)

                # Add deferred dividends and sale proceeds from the previous month
                cash += deferred_dividends[i, month]
                cash += deferred_sale_proceeds[i, month]

                # Calculate CVaR at the beginning of each month
                cal_po_wCVaR(month, stock_holdings, cvar_values, i, stock_data)

                buy_decisions = X[i, month * n_stocks:(month + 1) * n_stocks]
                sell_decisions = X[i, (duration + month) * n_stocks:(duration + month + 1) * n_stocks]

                # Prevent buys in the last month
                if month == duration - 1:
                    buy_decisions[:] = 0

                monthly_log = {"Month": month + 1, "Buy": [], "Sell": [], "Dividends": 0, "BankDeposit": 0}
                aggregated_sell_decisions = np.zeros(n_stocks)

                for j in range(n_stocks):
                    stock = self.stock_data[j]
                    stock_symbol = stock['symbol']
                    stock_price = stock["prices"][month]['value']
                    stock_capacity = stock["prices"][month]['matchedTradingVolume']

                    # Prevent sells during dividend months
                    if (month + 1) in [dividend['month'] for dividend in stock['dividendSpitingHistories']]:
                        sell_decisions[j] = 0
                    # print(f"{buy_decisions[j]};{sell_decisions[j]}")
                    if (buy_decisions[j] > 0 and
                            ((round(buy_decisions[j]) == round(sell_decisions[j])) or
                             (round(buy_decisions[j]) >= stock_capacity and round(
                                 sell_decisions[j]) >= stock_capacity) or
                             ((round(buy_decisions[j]) + stock_holdings[j] - int(
                                 round(min(sell_decisions[j], stock_capacity))) <= 0)))):
                        sell_decisions[j] = 0

                    # Process buy decisions
                    if buy_decisions[j] > 0:
                        buy_amount = int(round(min(buy_decisions[j], stock_capacity)))
                        transaction_fee = TRANS_FEE / 100 * stock_price * buy_amount
                        total_buy_cost = stock_price * buy_amount + transaction_fee

                        # Ensure we do not buy more than the available cash
                        if total_buy_cost <= cash:
                            cash -= total_buy_cost
                            stock_holdings[j] += buy_amount
                            monthly_log["Buy"].append((stock_symbol, buy_amount))

                    # Aggregate sell decisions
                    if sell_decisions[j] > 0:
                        sell_amount = int(round(min(sell_decisions[j], stock_holdings[j])))
                        aggregated_sell_decisions[j] += sell_amount

                    # Calculate dividends if current month is a dividend month
                    for dividend in stock['dividendSpitingHistories']:
                        if (month + 1) == dividend['month'] and previous_stock_holdings[j] > 0:
                            if month != duration - 1 and aggregated_sell_decisions[
                                j] <= 0:  # Ensure no dividends are received if stock is sold in the same month
                                dividends = dividend['value'] * previous_stock_holdings[j]
                                # Defer dividends to the next month
                                deferred_dividends[i, month + 1] += dividends
                                monthly_log["Dividends"] += dividends

                # Process aggregated sell decisions
                for j in range(n_stocks):
                    if aggregated_sell_decisions[j] > 0:
                        sell_amount = aggregated_sell_decisions[j]
                        transaction_fee = TRANS_FEE / 100 * stock_price * sell_amount
                        total_sell_proceeds = stock_price * sell_amount - transaction_fee

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

            # Ensure all holdings are sold at the end of the last month
            for j in range(n_stocks):
                remaining_sell_amount = stock_holdings[j]
                if remaining_sell_amount > 0:
                    for m in range(duration - 1, -1, -1):
                        stock_price = self.stock_data[j]["prices"][m]['value']
                        stock_capacity = self.stock_data[j]["prices"][m]['matchedTradingVolume']
                        sell_amount = min(remaining_sell_amount, stock_capacity)
                        transaction_fee = TRANS_FEE / 100 * stock_price * sell_amount
                        total_sell_proceeds = stock_price * sell_amount - transaction_fee
                        cash += total_sell_proceeds
                        remaining_sell_amount -= sell_amount
                        if sell_amount > 0:
                            log[m]["Sell"].append((self.stock_data[j]['symbol'], sell_amount))
                        if remaining_sell_amount <= 0:
                            break

                    stock_holdings[j] = 0

            total_cash[i] = cash

            # print_detail(log, cash, stock_holdings, stock_data)

        out["F"] = np.column_stack((-total_cash, cvar_values[:, 1:]))
        out["G"] = cardinality_violations

def my_solve():
    problem = PortfolioOptimizationProblem(stock_data, bank_interest_rate, initial_cash, duration, max_stocks)

    ref_dirs = get_reference_directions("energy", problem.n_obj, REFERENCES_POINTS_NUM, seed=1)
    algorithm = NSGA3(pop_size=population_size, ref_dirs=ref_dirs)

    res = minimize(problem,
                   algorithm,
                   termination=('n_gen', termination_gen_num),
                   seed=10,
                   save_history=True,
                   verbose=True)

    F = res.pop.get("F")

    # calculate the fronts of the population
    fronts, rank = NonDominatedSorting().do(F, return_rank=True, n_stop_if_ranked=population_size)

    hop_solution = res.pop[hop(res.pop, fronts[0])[0]]
    print("Objectives =", ["%.2f" % v for v in hop_solution.F])
    print("Solution details =", ["%.2f" % v for v in hop_solution.X])


# Open a file in write mode
timestamp = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
unique_filename = f"output-{timestamp}.txt"
with open(unique_filename, 'w') as f:
    print("Starting..")
    # Save the original standard output
    original_stdout = sys.stdout

    # Redirect standard output to the file
    sys.stdout = f
    print("Starting to write..")
    my_solve()

    sys.stdout = original_stdout

print("DONE - Thank you")
