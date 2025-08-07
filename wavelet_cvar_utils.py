import numpy as np
import pywt
import constants


def wavelet_decomposition(returns):
    """ Decompose asset returns using Discrete Wavelet Transform. """
    cA4, cD4, cD3, cD2, cD1 = pywt.wavedec(returns, 'db1', level=4)
    cA3, cD3, cD2, cD1 = pywt.wavedec(returns, 'db1', level=3)
    cA2, cD2, cD1 = pywt.wavedec(returns, 'db1', level=2)
    cA1, cD1 = pywt.wavedec(returns, 'db1', level=1)
    if constants.WAVELET_LEVEL == 4:
        return cA4
    elif constants.WAVELET_LEVEL == 3:
        return cA3
    elif constants.WAVELET_LEVEL == 2:
        return cA2
    elif constants.WAVELET_LEVEL == 1:
        return cA1

def historical_var_from_wavelet(coeffs, tail_probability):
    """
    Historical-simulation VaR.
    returns : 1-D array-like of *percentage* or *cash* returns
    alpha   : tail probability ε  (0.05 for 95 % VaR)
    Returns a positive loss figure (same units as `returns`).
    """
    coeffs = np.asarray(coeffs)
    var_quantile = np.percentile(coeffs, 100 * tail_probability)   # α-quantile (left tail)
    return var_quantile

def calculate_wcvar(coeffs, var):
    """ Calculate Conditional Value-at-Risk (CVaR) based on VaR. """
    losses_exceeding_var = [loss for loss in coeffs if (loss <= var and loss < 0)]
    return -np.mean(losses_exceeding_var) if losses_exceeding_var else 0


def cal_po_wCVaR(month, stock_holdings, cvar_values, i, returns, duration, tail_probability_epsilon, initial_cash, beginning_month_cash):
    # Calculate CVaR at the beginning of each month
    if 0 < month < duration:
        portfolio_returns = np.dot(returns, stock_holdings) + beginning_month_cash
        portfolio_return_rates = (portfolio_returns - initial_cash)/initial_cash

        coeffs = wavelet_decomposition(portfolio_return_rates)

        portfolio_var = historical_var_from_wavelet(coeffs, tail_probability_epsilon)


        portfolio_cvar = calculate_wcvar(coeffs, portfolio_var)
        cvar_values[i, month] = portfolio_cvar
