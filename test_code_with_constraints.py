import numpy as np
from pymoo.algorithms.moo.nsga3 import NSGA3, BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD, hop
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.core.repair import Repair
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from assets_returns import *
from constants import REFERENCES_POINTS_NUM, POPULATION_SIZE, TERMINATION_GEN_NUM, MAX_STOCKS, DURATION, \
    TAIL_PROBABILITY_EPSILON, BANK_INTEREST_RATE, TRANS_FEE, INITIAL_CASH, INVESTMENT_INTEREST_EXPECTED, \
    BENCHMARK_FINAL_RETURN
from handle_matrix_inputs_for_constraints_based_sol import C, D, Q, stocks_len
from stock_data_input_100 import STOCK_DATA_2023_INPUT_100_STOCKS
from wavelet_cvar_utils import cal_po_wCVaR

stock_data = STOCK_DATA_2023_INPUT_100_STOCKS
LEN_STOCK_DATA = len(stock_data)
# stock_returns = np.column_stack((
#     ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP, BPC))
stock_returns = np.column_stack((
    ABT, ACB, ACL, AGF, ALT, ANV, ASP, B82, BBC, BBS, BCC, BLF, BMC, BMI, BMP, BPC, BST, BTS, BVS,
    CAN, CAP, CCM, CDC, CID, CII, CJC, CLC, CMC, COM, CTB, CTC, CTN, DAC, DAE, DBC, DC4, DCS, DHA,
    DHG, DHT, DIC, DMC, DPC, DPM, DPR, DQC, DRC, DST, DTC, DTT, DXP, DXV, EBS, FMC, FPT, GIL, GMC,
    GMD, GTA, HAG, HAP, HAS, HAX, HBC, HCC, HCT, HDC, HEV, HHC, HJS, HMC, HPG, HRC, HSG, HSI, HT1,
    HTP, HTV, HUT, ICF, IMP, ITA, KBC, KDC, KHP, KKC, KMR, KSH, L10, L18, L43, L61, L62, LAF, LBE,
    LBM, LCG, LGC, LSS, LTC))

class CustomRepair(Repair):
    def _do(self, problem, pop, **kwargs):
        X = pop
        X = X.reshape((X.shape[0], 2, problem.n, problem.tau, 2))  # Reshape to (pop_size, 2, n, tau, binary_decision)

        # Ensure x is binary
        x = X[:, 0, :, :, :]
        x = np.where(x > 0.5, 1, 0)  # Directly set to 0 or 1 based on threshold 0.5
        X[:, 0, :, :, :] = x

        # Ensure y and q are non-negative integers
        y = X[:, 1, :, :, :]
        y = np.maximum(0, np.floor(y))  # Ensure y is at least 0
        X[:, 1, :, :, :] = y

        pop = X.reshape((X.shape[0], -1))
        return pop


class PortfolioOptimizationProblem(Problem):

    def __init__(self, n, K, tau, epsilon, alpha, xi, beta, C, D, Q, sigma, INF, Theta):
        self.n = n
        self.K = K
        self.tau = tau
        self.epsilon = epsilon
        self.alpha = alpha
        self.xi = xi
        self.beta = beta
        self.C = C
        self.D = D
        self.Q = Q
        self.sigma = sigma
        self.INF = INF
        self.Theta = Theta

        n_vars = 2 * n * tau * 2  # x and y are (2, n, tau, binary_decision)

        xl = np.zeros(n_vars)
        xu_ = np.zeros((2, n, tau, 2))  # first row for x, second row for y
        expected_cash_after_investment = INITIAL_CASH*(1+INVESTMENT_INTEREST_EXPECTED)
        for j in range(n):
            for t in range(tau):
                for b in range(2):
                    xu_[0, j, t, b] = 1
                    xu_[1, j, t, b] = min(self.Q[j, t], expected_cash_after_investment/C[j, t])
                    # xu_[1, j, t, b] = 100
        # xu = [xu_[0], xu_[1]]
        xu = xu_.reshape(-1)
        # Recalculate the number of constraints
        # n_constr = (
        #         n * tau  # x_{i,j,0} = y_{i,j,0} = 0
        #         + n  # q_{j,0} = y_{0,j,0}
        #         + 1  # theta_{0} = Theta
        #         + n * (tau - 1)  # y_{1,j,t} <= q_{j,t-1}
        #         + tau  # sum_{j=1}^{n} (1+\xi)C_{j,t}y_{0,j,t} <= theta_t
        #         + n * tau  # y_{i,j,t} <= Q_{j,t}
        #         + n * tau  # y_{i,j,t} <= x_{i,j,t} * INF
        #         + n * (tau - 1)  # q_{j,t} = q_{j,t-1} + y_{0,j,t} - y_{1,j,t}
        #         + n * tau  # z_{j,t} = 0 if q_{j,t} <= 0, else 1
        #         + tau  # sum_{j=1}^nz_{j,t} <= K
        #         + n  # dispose of all investments
        # )
        n_constr = 6213

        super().__init__(n_var=n_vars,  # Number of decision variables
                         n_obj=DURATION,  # Number of objectives
                         n_constr=n_constr,  # Number of constraints
                         xl=xl,  # Lower bounds of decision variables
                         xu=xu)  # Upper bounds of decision variables

    def _evaluate(self, X, out, *args, **kwargs):
        # Reshape the decision variable matrix into (population size, 2, n, tau, binary_decision)
        X = X.reshape((X.shape[0], 2, self.n, self.tau, 2))

        # Extract decision variables
        x = X[:, 0, :, :, :]  # Binary indicators for buying (i=0) or selling (i=1)
        y = X[:, 1, :, :, :]  # Amount of stock j purchased (i=0) or sold (i=1)
        q = np.zeros((X.shape[0], self.n, self.tau))  # Quantity of stock j held

        for individual in range(X.shape[0]):
            for j in range(n):
                for t in range(tau):
                    for binary_decision_i in range(2):
                        if y[individual, j, t, binary_decision_i] > 0:
                            if x[individual, j, t, binary_decision_i] > 0:
                                y[individual, j, t, binary_decision_i] = 1
                            else:
                                y[individual, j, t, binary_decision_i] = 0

        # Calculate q
        for t in range(1, self.tau):
            q[:, :, t] = q[:, :, t-1] + y[:, :, t, 0] - y[:, :, t, 1]


        # Objective 2: Maximize theta_tau
        theta = np.zeros((X.shape[0], self.tau))
        theta[:, 0] = self.Theta
        for individual in range(POPULATION_SIZE):
            for t in range(1, self.tau):
                for j in range(n):
                    term1 = (1 + self.alpha) * (theta[individual, t-1] - np.sum((1 + self.xi) * self.C[j, t-1] * y[individual, j, t-1, 0]))
                    term2 = np.sum((1 - self.xi) * self.C[j, t-1] * y[individual, j, t-1, 1])
                    term3 = np.sum(self.D[j, t-1] * q[individual, j, t-2]) if t > 1 else 0
                    theta[individual, t] = term1 + term2 + term3

        # Objective 1: Minimize CVaR
        CVaR_t = np.zeros((X.shape[0], self.tau))
        for individual in range(POPULATION_SIZE):
            returns = stock_returns
            for t in range(1, self.tau):
                current_month_prices = []
                for stock_info in stock_data:
                    current_month_prices.append(stock_info["prices"][t]["value"])  # month also is the index = month + 1 in "month" field

                returns = np.vstack((returns, np.array(current_month_prices).reshape(1, -1)))
                # Calculate CVaR at the beginning of each month
                cal_po_wCVaR(t, q[individual, :, t], CVaR_t, individual, returns, DURATION, TAIL_PROBABILITY_EPSILON, INITIAL_CASH, theta[individual, t])

        out["F"] = np.column_stack((-(theta[:, -1]-INITIAL_CASH)/INITIAL_CASH, CVaR_t[:, 1:]))

        # Constraints
        constraints = []

        # NEW constraint to overcome trivial solutions:
        # theta_{tau} > (BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD+1)*init_cash
        # constraints.append((BENCHMARK_FINAL_RETURN - theta[:, -1]).reshape(X.shape[0], -1))

        # Constraint: q_{j,t} >= 0, y[] >= 0
        constraints.append((-q[:, :, :]).reshape(X.shape[0], -1))
        constraints.append((-y[:, :, :]).reshape(X.shape[0], -1))
        constraints.append((-theta[:, :]).reshape(X.shape[0], -1))

        # Constraint 1: x_{1,j,0} = y_{1,j,0} = 0
        constraints.append((-x[:, :, 0, 1]).reshape(X.shape[0], -1))  # Selling constraint for x
        constraints.append((-y[:, :, 0, 1]).reshape(X.shape[0], -1))  # Selling constraint for y

        # Constraint: q_{j,0} = y_{0,j,0}
        constraints.append((q[:, :, 0] - y[:, :, 0, 0]).reshape(X.shape[0], -1))

        # Constraint: theta_{0} = Theta
        constraints.append((theta[:, 0] - self.Theta).reshape(X.shape[0], -1))

        # Constraint: y_{1,j,t} <= q_{j,t-1}
        for t in range(1, self.tau):
            constraints.append((y[:, :, t, 1] - q[:, :, t-1]).reshape(X.shape[0], -1))

        # Constraint: sum_{j=1}^{n} (1+\xi)C_{j,t}y_{0,j,t} <= theta_t
        for t in range(self.tau):
            for j in range(n):
                constraints.append((np.sum((1 + self.xi) * self.C[j, t] * y[:, j, t, 0]) - theta[:, t]).reshape(X.shape[0], -1))

        # Constraint: y_{i,j,t} <= Q_{j,t}
        for t in range(self.tau):
            for j in range(n):
                for i in range(2):
                    constraints.append((y[:, j, t, i] - self.Q[j, t]).reshape(X.shape[0], -1))

        # Constraint: y_{i,j,t} <= x_{i,j,t} * INF
        for t in range(self.tau):
            for i in range(2):
                constraints.append((y[:, :, t, i] - x[:, :, t, i] * self.INF).reshape(X.shape[0], -1))

        # Constraint: q_{j,t} = q_{j,t-1} + y_{0,j,t} - y_{1,j,t}
        for t in range(1, self.tau):
            constraints.append((q[:, :, t] - (q[:, :, t-1] + y[:, :, t, 0] - y[:, :, t, 1])).reshape(X.shape[0], -1))

        # z_{j,t} = 0 if q_{j,t} <= 0, else 1
        z = np.where(q > 0, 1, 0)

        # Constraint: sum_{j=1}^nz_{j,t} <= K
        for t in range(self.tau):
            constraints.append((np.sum(z[:, :, t], axis=1) - self.K).reshape(X.shape[0], -1))

        # Constraint: dispose of all investments
        constraints.append((y[:, :, self.tau-1, 1] - q[:, :, self.tau-2]).reshape(X.shape[0], -1))

        out["G"] = np.hstack(constraints)


# Define the parameters (example values)
n = stocks_len  # Stock quantity
K = MAX_STOCKS  # Preferred quantity of stock kinds to be retained
tau = DURATION  # Decision-making period in months
epsilon = TAIL_PROBABILITY_EPSILON  # Tail probability
alpha = BANK_INTEREST_RATE  # Monthly bank interest rate
xi = TRANS_FEE  # Transaction fee percentage
beta = 10  # Share dividend price
# C = np.random.rand(n, tau)  # Stock prices
# D = np.random.rand(n, tau)  # Dividend payout ratios
# Q = np.random.randint(1, 100, size=(n, tau))  # Highest amount of stock traded
sigma = np.random.rand(tau)  # Wavelet portfolio variance
INF = 1e6  # A significantly high value
Theta = INITIAL_CASH  # Initial idle cash

# Define the problem
problem = PortfolioOptimizationProblem(n, K, tau, epsilon, alpha, xi, beta, C, D, Q, sigma, INF, Theta)

# Define the reference directions
ref_dirs = get_reference_directions("energy", problem.n_obj, REFERENCES_POINTS_NUM, seed=1)

# Initialize the algorithm with CustomRepair
algorithm = NSGA3(pop_size=POPULATION_SIZE, ref_dirs=ref_dirs, repair=CustomRepair())

# Minimize the problem using NSGA-III
res = minimize(problem,
               algorithm,
               termination=('n_gen', TERMINATION_GEN_NUM),
               seed=1,
               save_history=True,
               verbose=True)
# Print the results
print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))

F = res.pop.get("F")
fronts, rank = NonDominatedSorting().do(F, return_rank=True, n_stop_if_ranked=POPULATION_SIZE)
front_0 = [individual for individual in res.pop[fronts[0]] if
           -individual.F[0] > BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD]
len_front_0 = len(front_0)
if len_front_0 <= 0:
    print("No HOP solution found.")
hop_solution = front_0[hop(front_0, np.arange(len_front_0))[0]]
print("Objectives =", ["%.6f" % v for v in hop_solution.F])
print("Solution details =", ["%.1f" % v for v in hop_solution.X])