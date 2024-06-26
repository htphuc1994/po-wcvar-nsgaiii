import numpy as np
import pywt
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize

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
        xu = np.array([stock['trading_capacity'] for stock in stock_data] * 2 * self.duration)  # Upper bounds (max trading capacity)

        super().__init__(n_var=2 * self.n_stocks * self.duration, n_obj=self.duration, n_constr=1 + self.n_stocks * self.duration, xl=xl, xu=xu)

    def _evaluate(self, X, out, *args, **kwargs):
        n_stocks = self.n_stocks
        duration = self.duration
        total_cash = np.zeros(X.shape[0])
        cvar_values = np.zeros((X.shape[0], duration))
        cardinality_violations = np.zeros(X.shape[0])
        buy_sell_violations = np.zeros((X.shape[0], n_stocks * duration))

        for i in range(X.shape[0]):
            cash = self.initial_cash
            stock_holdings = np.zeros(n_stocks)
            log = []

            for month in range(duration):
                # Update cash with bank interest
                if month != 0:
                    cash *= (1 + self.bank_interest_rate / 100)

                buy_decisions = X[i, month * n_stocks:(month + 1) * n_stocks]
                sell_decisions = X[i, (duration + month) * n_stocks:(duration + month + 1) * n_stocks]

                # Check for simultaneous buy and sell decisions for each stock
                for j in range(n_stocks):
                    buy_sell_violations[i, month * n_stocks + j] = int((buy_decisions[j] > 0) and (sell_decisions[j] > 0))

                monthly_log = {"Month": month + 1, "Buy": [], "Sell": [], "Dividends": 0, "BankDeposit": 0}

                for j in range(n_stocks):
                    stock_symbol = self.stock_data[j]['symbol']
                    # Process buy decisions
                    if buy_decisions[j] > 0 and sell_decisions[j] == 0:  # Ensure no simultaneous buy and sell
                        buy_amount = min(buy_decisions[j], self.stock_data[j]['trading_capacity'])
                        cash -= self.stock_data[j]['price'] * buy_amount
                        stock_holdings[j] += buy_amount
                        monthly_log["Buy"].append((stock_symbol, buy_amount))

                    # Process sell decisions
                    if sell_decisions[j] > 0 and buy_decisions[j] == 0:  # Ensure no simultaneous buy and sell
                        sell_amount = min(sell_decisions[j], stock_holdings[j])
                        cash += self.stock_data[j]['price'] * sell_amount
                        stock_holdings[j] -= sell_amount
                        monthly_log["Sell"].append((stock_symbol, sell_amount))

                    # Calculate dividends if current month is a dividend month
                    if (month + 1) in self.stock_data[j]['dividend_months']:
                        if stock_holdings[j] > 0:
                            dividends = self.stock_data[j]['dividend_yield'] * stock_holdings[j] * self.stock_data[j]['price']
                            cash += dividends
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

            total_cash[i] = cash
            # Check for cardinality constraint violation
            held_stocks = np.sum(stock_holdings > 0)
            if held_stocks > self.max_stocks:
                cardinality_violations[i] = held_stocks - self.max_stocks

        out["F"] = np.column_stack((-total_cash, cvar_values[:, 1:]))
        out["G"] = np.column_stack((cardinality_violations, buy_sell_violations))

stock_data = [
    {"symbol": "A", "price": 32000, "dividend_yield": 0.15, "dividend_months": [5, 9], "trading_capacity": 800},
    {"symbol": "B", "price": 13500, "dividend_yield": 0.06, "dividend_months": [5, 11], "trading_capacity": 5000},
    {"symbol": "C", "price": 20000, "dividend_yield": 0.06, "dividend_months": [8, 9], "trading_capacity": 5000},
    {"symbol": "D", "price": 53500, "dividend_yield": 0.26, "dividend_months": [5, 11], "trading_capacity": 5000},
    {"symbol": "E", "price": 23500, "dividend_yield": 0.06, "dividend_months": [1, 5, 8], "trading_capacity": 5000},
    {"symbol": "F", "price": 13500, "dividend_yield": 0.08, "dividend_months": [2, 11], "trading_capacity": 5000},
    {"symbol": "G", "price": 73500, "dividend_yield": 0.16, "dividend_months": [3, 12], "trading_capacity": 5000},
    {"symbol": "H", "price": 3500, "dividend_yield": 0.46, "dividend_months": [4, 6], "trading_capacity": 5000},
    {"symbol": "I", "price": 63500, "dividend_yield": 0.56, "dividend_months": [7, 11], "trading_capacity": 5000},
    # Add more stocks as needed
]
bank_interest_rate = 0.45
initial_cash = 100000000  # 100 million VND
duration = 6  # 6 months
max_stocks = 8  # Example cardinality constraint

problem = PortfolioOptimizationProblem(stock_data, bank_interest_rate, initial_cash, duration, max_stocks)

ref_dirs = get_reference_directions("energy", problem.n_obj, 150, seed=1)
algorithm = NSGA3(pop_size=100, ref_dirs=ref_dirs)

res = minimize(problem,
               algorithm,
               termination=('n_gen', 2239),
               seed=1,
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
