import numpy as np
import pywt
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga3 import NSGA3, hop
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from scipy.stats import norm
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from assets_returns import *
from constants import TRANS_FEE
from stock_data_inputs import STOCK_DATA_2023_INPUT_251_STOCKS


def simulate_asset_returns(num_assets, num_points):
    """ Simulate daily returns for assets. """
    np.random.seed(42)
    return np.random.normal(0.001, 0.01, size=(num_points, num_assets))


def wavelet_decomposition(returns, wavelet='db4', levels=1):
    """ Decompose asset returns using Discrete Wavelet Transform. """
    coeffs = pywt.wavedec(returns, wavelet, level=levels)
    return coeffs[1:]  # Returning detail coefficients, ignoring approximation


def compute_wavelet_variance(coeffs):
    """ Compute the wavelet variance from detail wavelet coefficients. """
    variances = [np.var(c) for c in coeffs]  # Compute variance of each level
    return np.mean(variances)  # Return the mean of variances across levels


# def calculate_var_from_wavelet_variances(wavelet_variances, weights, scaling_factor=1.0):
#     """ Estimate portfolio VaR directly from wavelet variances. """
#     weighted_variances = np.dot(wavelet_variances, weights)
#     return scaling_factor * np.sqrt(weighted_variances)  # Simple model to convert variance to VaR
def calculate_var_from_wavelet_variance(wavelet_variance, tail_probability, scaling_factor=1.0):
    """ Estimate portfolio VaR directly from wavelet variances. """
    # weighted_variances = np.dot(wavelet_variances, weights)
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
    for j, stock in enumerate(stock_data):
        print(f"Final Holdings: Stock {stock['symbol']}, Amount: {stock_holdings[j]}")


class PortfolioOptimizationProblem(Problem):
    def __init__(self, stock_data, bank_interest_rate, initial_cash, duration, max_stocks):
        self.stock_data = stock_data
        self.bank_interest_rate = bank_interest_rate
        self.initial_cash = initial_cash
        self.duration = duration
        self.n_stocks = len(stock_data)
        self.max_stocks = max_stocks

        # Define bounds for the decision variables
        xl = np.zeros(2 * self.n_stocks * self.duration)  # Lower bounds (all zeros, no negative quantities)
        xu = np.concatenate(
            [np.array([month_data["matchedTradingVolume"] for month_data in stock["prices"][:duration]]) for stock in
             stock_data] * 2)

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

        for i in range(X.shape[0]):
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
                        transaction_fee = 0.0015 / 100 * stock_price * buy_amount
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

                # Calculate CVaR at the beginning of each month
                if 0 < month < duration:
                    # returns = simulate_asset_returns(n_stocks, 100)  # todo: past prices + price of the processing month
                    returns = np.column_stack((ABT,ACB,ACL,AGF,ALT,ANV,ASP,B82,BBC,BBS,BCC,BLF,BMC,BMI,BMP,BPC,BST,BTS,BVS,CAN,CAP,CCM,CDC,CID,CII,CJC,CLC,CMC,COM,CTB,CTC,CTN,DAC,DAE,DBC,DC4,DCS,DHA,DHG,DHT,DIC,DMC,DPC,DPM,DPR,DQC,DRC,DST,DTC,DTT,DXP,DXV,EBS,FMC,FPT,GIL,GMC,GMD,GTA,HAG,HAP,HAS,HAX,HBC,HCC,HCT,HDC,HEV,HHC,HJS,HMC,HPG,HRC,HSG,HSI,HT1,HTP,HTV,HUT,ICF,IMP,ITA,KBC,KDC,KHP,KKC,KMR,KSH,L10,L18,L43,L61,L62,LAF,LBE,LBM,LCG,LGC,LSS,LTC,LUT,MCO,MCP,MEC,MHC,MKV,MTG,NAV,NBC,NGC,NHC,NSC,NST,NTL,NTP,ONE,OPC,PAC,PAN,PET,PGC,PGS,PIT,PJC,PJT,PLC,PMS,PNC,POT,PPC,PSC,PTC,PTS,PVC,PVD,PVE,PVG,PVI,PVS,PVT,QTC,RAL,RCL,REE,S12,S55,S99,SAM,SAP,SAV,SBT,SC5,SCD,SCJ,SD5,SD6,SD7,SD9,SDA,SDC,SDD,SDN,SDT,SDY,SFC,SFI,SFN,SGC,SGD,SIC,SJ1,SJD,SJE,SJM,SJS,SMC,SRA,SRB,SSC,SSI,SSM,ST8,STB,STC,STP,SVC,SVI,SZL,TBC,TBX,TC6,TCM,TCR,TCT,TDH,TDN,THB,THT,TJC,TKU,TMC,TMS,TNA,TNC,TNG,TPC,TPH,TPP,TRA,TRC,TSC,TTC,TTF,TV4,TXM,TYA,UIC,UNI,VBH,VC2,VC5,VC6,VC7,VCG,VCS,VDL,VE1,VFR,VGP,VGS,VHC,VHG,VIC,VID,VIP,VMC,VNA,VNC,VNE,VNM,VNR,VNS,VSC,VSG,VSH,VTB,VTC,VTO,VTS,VTV,YBC))
                    # weights = stock_holdings.copy()
                    # sum_weights = np.sum(weights)
                    # weights /= sum_weights  # Normalize weights
                    portfolio_returns = np.dot(returns, stock_holdings)

                    # wavelet_variances = np.array(
                    #     [compute_wavelet_variance(wavelet_decomposition(returns[:, k])) for k in range(n_stocks)])
                    wavelet_variance = compute_wavelet_variance(wavelet_decomposition(portfolio_returns))

                    portfolio_var = calculate_var_from_wavelet_variance(wavelet_variance, tail_probability_epsilon,
                                                                        scaling_factor=initial_cash)

                    portfolio_cvar = calculate_cvar(portfolio_returns, portfolio_var)
                    cvar_values[i, month] = portfolio_cvar

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


# Example stock data with monthly prices and trading capacities
stock_data = [
    {
        "symbol": "BCC",
        "companyName": "CTCP Xi măng Bỉm Sơn",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {"month": 1, "value": 11.6, "matchedTradingVolume": 16898285},
            {"month": 2, "value": 12.7, "matchedTradingVolume": 26045742},
            {"month": 3, "value": 12.4, "matchedTradingVolume": 20300759},
            {"month": 4, "value": 12.4, "matchedTradingVolume": 13811487},
            {"month": 5, "value": 13.3, "matchedTradingVolume": 20730116},
            {"month": 6, "value": 14.5, "matchedTradingVolume": 24793471},
            {"month": 7, "value": 14.6, "matchedTradingVolume": 22653644},
            {"month": 8, "value": 14.6, "matchedTradingVolume": 21295205},
            {"month": 9, "value": 13, "matchedTradingVolume": 9862493},
            {"month": 10, "value": 12.2, "matchedTradingVolume": 6465571},
            {"month": 11, "value": 9.8, "matchedTradingVolume": 5608050},
            {"month": 12, "value": 9.6, "matchedTradingVolume": 3821733}
        ],
        "dividendSpitingHistories": [{"month": 8, "value": 500}]
    },
    {
        "symbol": "BVS",
        "companyName": "CTCP Chứng khoán Bảo Việt",
        "type": "HNX30",
        "year": 2023,
        "prices": [
            {"month": 1, "value": 21, "matchedTradingVolume": 1438111},
            {"month": 2, "value": 19, "matchedTradingVolume": 1854612},
            {"month": 3, "value": 19.1, "matchedTradingVolume": 3134602},
            {"month": 4, "value": 20.2, "matchedTradingVolume": 3958340},
            {"month": 5, "value": 23.8, "matchedTradingVolume": 9386680},
            {"month": 6, "value": 25.3, "matchedTradingVolume": 14453718},
            {"month": 7, "value": 27, "matchedTradingVolume": 13688213},
            {"month": 8, "value": 28.8, "matchedTradingVolume": 13880792},
            {"month": 9, "value": 30.7, "matchedTradingVolume": 9906439},
            {"month": 10, "value": 26.9, "matchedTradingVolume": 6689071},
            {"month": 11, "value": 26, "matchedTradingVolume": 3668846},
            {"month": 12, "value": 26.1, "matchedTradingVolume": 3959357}
        ],
        "dividendSpitingHistories": [{"month": 10, "value": 1000}]
    },
    # Additional stocks can be added here
]
stock_data = STOCK_DATA_2023_INPUT_251_STOCKS

bank_interest_rate = 0.45
initial_cash = 100000000  # 100 million VND
duration = 6  # 6 months
max_stocks = 251  # Example cardinality constraint
termination_gen_num = 50
tail_probability_epsilon = 0.05
population_size = 100

problem = PortfolioOptimizationProblem(stock_data, bank_interest_rate, initial_cash, duration, max_stocks)

ref_dirs = get_reference_directions("energy", problem.n_obj, 1000, seed=1)
algorithm = NSGA3(pop_size=population_size, ref_dirs=ref_dirs)

res = minimize(problem,
               algorithm,
               termination=('n_gen', termination_gen_num),
               seed=10,
               save_history=True,
               verbose=True)

# Log the best solution found
best_solution = res.X
best_return = -res.F[:, 0]  # Negate to get the original positive value
best_cvar = res.F[:, 1:]

print("Best solution found:")
print("X =", best_solution)
print("F (Returns) =", ["%.2f" % r for r in best_return])
print("F (CVaR) =", best_cvar)



#-------
# final_population = res.pop
# F = final_population.get("F")
# CV = final_population.get("CV")
# feasible = np.where(CV <= 0)[0]
# front_no = final_population.get("rank")
#
# # Get the individuals in the first front
# first_front_indices = np.where(front_no == 0)[0]
# first_front_individuals = final_population[first_front_indices]

F = res.pop.get("F")

# calculate the fronts of the population
fronts, rank = NonDominatedSorting().do(F, return_rank=True, n_stop_if_ranked=population_size)

hop_solution = res.pop[hop(res.pop, fronts[0])[0]]
# print(f"objectives = {hop_solution.F}")
print("Objectives =", ["%.2f" % v for v in hop_solution.F])
print(f"solution details = {hop_solution.X}")

print("DONE - Thank you")