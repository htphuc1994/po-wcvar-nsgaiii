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
        xu = np.array([month_data["matchedTradingVolume"] for stock in stock_data for month_data in stock["prices"]] * 2)  # Upper bounds (max trading capacity)

        super().__init__(n_var=2 * self.n_stocks * self.duration, n_obj=self.duration, n_constr=1, xl=xl, xu=xu)

    def _evaluate(self, X, out, *args, **kwargs):
        n_stocks = self.n_stocks
        duration = self.duration
        total_cash = np.zeros(X.shape[0])
        cvar_values = np.zeros((X.shape[0], duration))
        cardinality_violations = np.zeros(X.shape[0])
        deferred_dividends = np.zeros((X.shape[0], duration + 1))
        deferred_sale_proceeds = np.zeros((X.shape[0], duration + 1))

        for i in range(X.shape[0]):
            cash = self.initial_cash
            stock_holdings = np.zeros(n_stocks)
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
                        if (month + 1) == dividend['month']:
                            if stock_holdings[j] > 0:
                                dividends = dividend['value'] * stock_holdings[j]
                                # Defer dividends to the next month
                                deferred_dividends[i, month + 1] += dividends
                                monthly_log["Dividends"] += dividends

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
                    transaction_fee = 0.00015 / 100 * stock["prices"][duration - 1]['value'] * sell_amount
                    total_sell_proceeds = stock["prices"][duration - 1]['value'] * sell_amount - transaction_fee
                    cash += total_sell_proceeds
                    stock_holdings[j] = 0
                    log[-1]["Sell"].append((stock['symbol'], sell_amount))

            total_cash[i] = cash
            # Check for cardinality constraint violation
            held_stocks = np.sum(stock_holdings > 0)
            if held_stocks > self.max_stocks:
                cardinality_violations[i] = held_stocks - self.max_stocks

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

        out["F"] = np.column_stack((-total_cash, cvar_values[:, 1:]))
        out["G"] = np.column_stack((cardinality_violations))

# Sample stock data based on provided structure
stock_data = STOCK_DATA_2023_INPUT

bank_interest_rate = 0.45
initial_cash = 100000000  # 100 million VND
duration = 6  # 6 months
max_stocks = 20  # Example cardinality constraint

problem = PortfolioOptimizationProblem(stock_data, bank_interest_rate, initial_cash, duration, max_stocks)

ref_dirs = get_reference_directions("energy", problem.n_obj, 150, seed=1)
algorithm = NSGA3(pop_size=100, ref_dirs=ref_dirs)

res = minimize(problem,
               algorithm,
               termination=('n_gen', 239),
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
