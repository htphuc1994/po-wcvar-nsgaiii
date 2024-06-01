import numpy as np
import pywt
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize

from constants import STOCK_DATA_2023_INPUT


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

def calculate_var_from_wavelet_variances(wavelet_variances, weights, scaling_factor=1.0):
    """ Estimate portfolio VaR directly from wavelet variances. """
    weighted_variances = np.dot(wavelet_variances, weights)
    return scaling_factor * np.sqrt(weighted_variances)  # Simple model to convert variance to VaR

def calculate_cvar(portfolio_returns, var):
    """ Calculate Conditional Value-at-Risk (CVaR) based on VaR. """
    losses_exceeding_var = [loss for loss in portfolio_returns if loss <= var]
    return np.mean(losses_exceeding_var) if losses_exceeding_var else 0

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
        xu = np.concatenate([np.array([month_data["matchedTradingVolume"] for month_data in stock["prices"][:duration]]) for stock in stock_data] * 2)

        super().__init__(n_var=2 * self.n_stocks * self.duration, n_obj=self.duration, n_constr=self.duration, xl=xl, xu=xu)

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

                for j in range(n_stocks):
                    stock = self.stock_data[j]
                    stock_symbol = stock['symbol']
                    stock_price = stock["prices"][month]['value']
                    stock_capacity = stock["prices"][month]['matchedTradingVolume']

                    # Prevent sells during dividend months
                    if (month + 1) in [dividend['month'] for dividend in stock['dividendSpitingHistories']]:
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

                    # Process sell decisions
                    if sell_decisions[j] > 0:
                        sell_amount = int(round(min(sell_decisions[j], stock_holdings[j])))
                        transaction_fee = 0.00015 / 100 * stock_price * sell_amount
                        total_sell_proceeds = stock_price * sell_amount - transaction_fee

                        # Defer sale proceeds to the next month
                        deferred_sale_proceeds[i, month + 1] += total_sell_proceeds
                        stock_holdings[j] -= sell_amount
                        monthly_log["Sell"].append((stock_symbol, sell_amount))

                    # Calculate dividends if current month is a dividend month
                    for dividend in stock['dividendSpitingHistories']:
                        if (month + 1) == dividend['month'] and previous_stock_holdings[j] > 0:
                            if month != duration - 1 and sell_decisions[j] <= 0:  # Ensure no dividends are received if stock is sold in the same month
                                dividends = dividend['value'] * previous_stock_holdings[j]
                                # Defer dividends to the next month
                                deferred_dividends[i, month + 1] += dividends
                                monthly_log["Dividends"] += dividends

                # Save the current holdings to use for dividend eligibility in the next month
                previous_stock_holdings = stock_holdings.copy()

                # Check for cardinality constraint violation
                unique_stocks_held = np.sum(stock_holdings > 0)
                if unique_stocks_held > self.max_stocks:
                    cardinality_violations[i, month] = unique_stocks_held - self.max_stocks

                # Calculate CVaR at the beginning of each month
                if month > 0:
                    returns = simulate_asset_returns(n_stocks, 100)
                    wavelet_variances = np.array([compute_wavelet_variance(wavelet_decomposition(returns[:, k])) for k in range(n_stocks)])
                    weights = 1 / wavelet_variances
                    weights /= np.sum(weights)  # Normalize weights

                    portfolio_var = calculate_var_from_wavelet_variances(wavelet_variances, weights, scaling_factor=3.0)
                    portfolio_returns = np.dot(returns, weights)
                    portfolio_cvar = calculate_cvar(portfolio_returns, portfolio_var)
                    cvar_values[i, month] = portfolio_cvar

                monthly_log["BankDeposit"] = cash
                log.append(monthly_log)

            # Ensure all holdings are sold at the end of the last month
            for j in range(n_stocks):
                if stock_holdings[j] > 0:
                    sell_amount = stock_holdings[j]
                    transaction_fee = 0.00015 / 100 * self.stock_data[j]["prices"][duration - 1]['value'] * sell_amount
                    total_sell_proceeds = self.stock_data[j]["prices"][duration - 1]['value'] * sell_amount - transaction_fee
                    cash += total_sell_proceeds
                    stock_holdings[j] = 0
                    log[-1]["Sell"].append((self.stock_data[j]['symbol'], sell_amount))

            total_cash[i] = cash

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
            for j, stock in enumerate(self.stock_data):
                print(f"Final Holdings: Stock {stock['symbol']}, Amount: {stock_holdings[j]}")

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
stock_data = STOCK_DATA_2023_INPUT

bank_interest_rate = 0.45
initial_cash = 100000000  # 100 million VND
duration = 6  # 6 months
max_stocks = 2  # Example cardinality constraint
termination_gen_num = 50

problem = PortfolioOptimizationProblem(stock_data, bank_interest_rate, initial_cash, duration, max_stocks)

ref_dirs = get_reference_directions("energy", problem.n_obj, 150, seed=1)
algorithm = NSGA3(pop_size=100, ref_dirs=ref_dirs)

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
