import numpy as np
import pywt
from scipy.stats import norm
from constants import WAVELET_LEVEL


def wavelet_decomposition(returns, wavelet='db4', levels=WAVELET_LEVEL):
    """ Decompose asset returns using Discrete Wavelet Transform. """
    coeffs = pywt.wavedec(returns, wavelet, level=levels)
    return coeffs[WAVELET_LEVEL:]  # Returning detail coefficients, ignoring approximation


def compute_wavelet_variance(coeffs):
    """ Compute the wavelet variance from detail wavelet coefficients. """
    variances = [np.var(c) for c in coeffs]  # Compute variance of each level
    return np.mean(variances)  # Return the mean of variances across levels


#     """ Estimate portfolio VaR directly from wavelet variances. """
def calculate_var_from_wavelet_variance(wavelet_variance, tail_probability, scaling_factor=1.0):
    """ Estimate portfolio VaR directly from wavelet variances. """
    # Calculate the inverse of the cumulative distribution function for the given confidence level
    z_score = norm.ppf(1 - tail_probability)
    return scaling_factor * 1/z_score * np.sqrt(wavelet_variance)  # Simple model to convert variance to VaR


def calculate_cvar(portfolio_returns, var):
    """ Calculate Conditional Value-at-Risk (CVaR) based on VaR. """
    losses_exceeding_var = [loss for loss in portfolio_returns if loss <= var]
    return -np.mean(losses_exceeding_var) if losses_exceeding_var else 0

def cal_po_wCVaR(month, stock_holdings, cvar_values, i, returns, duration, tail_probability_epsilon, initial_cash, beginning_month_cash):
    # Calculate CVaR at the beginning of each month
    if 0 < month < duration:
        portfolio_returns = np.dot(returns, stock_holdings) + beginning_month_cash
        portfolio_returns = (portfolio_returns - initial_cash)/initial_cash
        wavelet_variance = compute_wavelet_variance(wavelet_decomposition(portfolio_returns))

        portfolio_var = calculate_var_from_wavelet_variance(wavelet_variance, tail_probability_epsilon,
                                                            scaling_factor=initial_cash)

        portfolio_cvar = calculate_cvar(portfolio_returns, portfolio_var)
        cvar_values[i, month] = portfolio_cvar
