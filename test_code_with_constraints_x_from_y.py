import numpy as np
import sys
import time
import datetime
from pymoo.algorithms.moo.nsga3 import NSGA3, BANK_INTEREST_RATE_AFTER_N_INVESTMENT_PERIOD, hop
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.core.repair import Repair
from pymoo.core.sampling import Sampling
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

from assets_returns import *
from constants import REFERENCES_POINTS_NUM, POPULATION_SIZE, TERMINATION_GEN_NUM, MAX_STOCKS, DURATION, \
    TAIL_PROBABILITY_EPSILON, BANK_INTEREST_RATE, TRANS_FEE, INITIAL_CASH, INVESTMENT_INTEREST_EXPECTED, \
    BENCHMARK_FINAL_RETURN, LOT_SIZE, REBUILD_Y_SCALING_FACTOR
from handle_matrix_inputs_for_constraints_based_sol import C, D, Q, stock_returns, stock_data, LEN_STOCK_DATA
from wavelet_cvar_utils import cal_po_wCVaR

# Custom initialization ensuring sum(x) = 1 or 0
class CustomSampling(Sampling):

    def _do(self, problem, n_samples, **kwargs):
        # X = super()._do(problem, n_samples, **kwargs)
        # X = np.zeros((POPULATION_SIZE, LEN_STOCK_DATA, tau, 2))
        X = np.random.rand(POPULATION_SIZE, LEN_STOCK_DATA, tau, 2)

        # X = X.reshape((POPULATION_SIZE, problem.n, problem.tau, 2))

        for i in range(POPULATION_SIZE):
            for t in range(problem.tau):
                for b in range(2):
                    sum = np.sum(X[i, :, t, b])
                    if np.random.rand() > 0.5 and sum > 0.0:
                        X[i, :, t, b] /= np.sum(X[i, :, t, b])
                    else:
                        X[i, :, t, b] = 0

        return X.reshape((POPULATION_SIZE, -1))

class CustomRepair(Repair):
    def _do(self, problem, pop, **kwargs):
        X = pop
        X = X.reshape((POPULATION_SIZE, problem.n, problem.tau, 2))  # Reshape to (pop_size, 2, n, tau, binary_decision)
        # X = X.reshape((POPULATION_SIZE, self.n, self.tau, 2))

        for i in range(POPULATION_SIZE):
            for t in range(problem.tau):
                for b in range(2):
                    sum_y = np.sum(X[i, :, t, b])
                    if sum_y > 1:
                        X[i, :, t, b] = X[i, :, t, b] / sum_y  # Normalize to sum to 1
                    elif sum_y < 1e-6:  # A small threshold to treat as zero
                        X[i, :, t, b] = 0  # Set all to zero

        pop = X.reshape((POPULATION_SIZE, -1))
        return pop


def rebuild_y(y):
    return y * REBUILD_Y_SCALING_FACTOR

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

        n_vars = n * tau * 2  # x and y are (2, n, tau, binary_decision)

        xl = np.zeros(n_vars)
        xu_ = np.zeros((n, tau, 2))  # first row for x, second row for y
        # expected_cash_after_investment = INITIAL_CASH*(1+INVESTMENT_INTEREST_EXPECTED)
        for j in range(n):
            for t in range(tau):
                for b in range(2):
                    xu_[j, t, b] = 1
                    # xu_[j, t, b] = min(self.Q[j, t], expected_cash_after_investment/self.C[j, t])  # todo remove hardcode
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
        n_constr = 442

        super().__init__(n_var=n_vars,  # Number of decision variables
                         n_obj=DURATION,  # Number of objectives
                         n_constr=n_constr,  # Number of constraints
                         xl=xl,  # Lower bounds of decision variables
                         xu=xu)  # Upper bounds of decision variables

    def _evaluate(self, X, out, *args, **kwargs):
        # Reshape the decision variable matrix into (population size, 2, n, tau, binary_decision)
        X = X.reshape((POPULATION_SIZE, self.n, self.tau, 2))

        # Extract decision variables
        # x = X[:, 0, :, :, :]  # Binary indicators for buying (i=0) or selling (i=1)
        y = X[:, :, :, :]  # Amount of stock j purchased (i=0) or sold (i=1)
        scale_y = rebuild_y(y)

        q = np.zeros((POPULATION_SIZE, self.n, self.tau))  # Quantity of stock j held

        # Calculate q
        for i in range(POPULATION_SIZE):
            for t in range(0, self.tau):
                for j in range(LEN_STOCK_DATA):
                    # y_0 = 0
                    # y_1 = 0
                    # if x[i, j, t, 0] > 0:
                    y_0 = scale_y[i, j, t, 0]
                    # if x[i, j, t, 1] > 0:
                    y_1 = scale_y[i, j, t, 1]
                    if t <= 0:
                        q[i, j, t] = y_0 - y_1
                    else:
                        q[i, j, t] = q[i, j, t-1] + y_0 - y_1

        # Objective 2: Maximize theta_tau
        theta = np.zeros((POPULATION_SIZE, self.tau+1))
        theta[:, 0] = self.Theta
        for individual in range(POPULATION_SIZE):
            for t in range(1, self.tau+1):
                for j in range(n):
                    term1 = (1 + self.alpha) * (theta[individual, t-1] - np.sum((1 + self.xi) * self.C[j, t-1] * scale_y[individual, j, t-1, 0]))
                    term2 = np.sum((1 - self.xi) * self.C[j, t-1] * scale_y[individual, j, t-1, 1])
                    term3 = np.sum(self.D[j, t-1] * q[individual, j, t-2]) if t > 1 else 0
                    theta[individual, t] = term1 + term2 + term3

        # Objective 1: Minimize CVaR
        CVaR_t = np.zeros((POPULATION_SIZE, self.tau))
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
        # constraints.append((BENCHMARK_FINAL_RETURN - theta[:, -1]).reshape(POPULATION_SIZE, -1))

        # Constraint: scale constraint
        sum_buy = np.zeros((POPULATION_SIZE, tau))
        sum_sell = np.zeros((POPULATION_SIZE, tau))
        for individual in range(POPULATION_SIZE):
            for t in range(self.tau):
                for j in range(LEN_STOCK_DATA):
                    sum_buy[individual, t] = np.sum(y[individual, j, t, 0])
                    sum_sell[individual, t] = np.sum(y[individual, j, t, 1])
        # constraints.append((sum_buy[:, :] - 1).reshape(POPULATION_SIZE, -1))
        # constraints.append(-(sum_buy[:, :]).reshape(POPULATION_SIZE, -1))
        # constraints.append((sum_sell[:, :] - 1).reshape(POPULATION_SIZE, -1))
        # constraints.append(-(sum_sell[:, :]).reshape(POPULATION_SIZE, -1))
        # constraints.append(np.minimum(np.abs(sum_buy[:, :] - 1), np.abs(sum_buy[:, :])).reshape(POPULATION_SIZE, -1))
        # constraints.append(np.minimum(np.abs(sum_sell[:, :] - 1), np.abs(sum_sell[:, :])).reshape(POPULATION_SIZE, -1))

        # Constraint: q_{j,t} >= 0, y[] >= 0
        constraints.append((-q[:, :, :]).reshape(POPULATION_SIZE, -1))
        # constraints.append((-scale_y[:, :, :]).reshape(POPULATION_SIZE, -1))
        constraints.append((-theta[:, :]).reshape(POPULATION_SIZE, -1))

        # Constraint 1: x_{1,j,0} = y_{1,j,0} = 0
        # constraints.append((x[:, :, 0, 1]).reshape(POPULATION_SIZE, -1))  # Selling constraint for x
        constraints.append((scale_y[:, :, 0, 1]).reshape(POPULATION_SIZE, -1))  # Selling constraint for y

        # Constraint 2: q_{j,0} = y_{0,j,0}
        constraints.append((q[:, :, 0] - scale_y[:, :, 0, 0]).reshape(POPULATION_SIZE, -1))

        # Constraint 3: theta_{0} = Theta
        constraints.append((theta[:, 0] - self.Theta).reshape(POPULATION_SIZE, -1))

        # Constraint 4: y_{1,j,t} <= q_{j,t-1}
        for t in range(1, self.tau):
            constraints.append((scale_y[:, :, t, 1] - q[:, :, t-1]).reshape(POPULATION_SIZE, -1))

        # Constraint 5: sum_{j=1}^{n} (1+\xi)C_{j,t}y_{0,j,t} <= theta_t
        for t in range(self.tau):
            for j in range(n):
                constraints.append((np.sum((1 + self.xi) * self.C[j, t] * scale_y[:, j, t, 0]) - theta[:, t]).reshape(POPULATION_SIZE, -1))

        # Constraint 6: y_{i,j,t} <= Q_{j,t}
        for t in range(self.tau):
            for j in range(n):
                for b in range(2):
                    constraints.append((scale_y[:, j, t, b] - self.Q[j, t]).reshape(POPULATION_SIZE, -1))

        # Constraint 7: x_{0,j,t} + x_{1,j,t} \leq 1
        # for t in range(self.tau):
        #     constraints.append((x[:, :, t, 0] + x[:, :, t, 1] - 1).reshape(POPULATION_SIZE, -1))

        # Constraint 8: y_{i,j,t} <= x_{i,j,t} * INF
        # for t in range(self.tau):
        #     for b in range(2):
        #         constraints.append((y[:, :, t, b] - x[:, :, t, b] * self.INF).reshape(POPULATION_SIZE, -1))

        # Constraint 9: q_{j,t} = q_{j,t-1} + y_{0,j,t} - y_{1,j,t}
        for t in range(1, self.tau):
            constraints.append((q[:, :, t] - (q[:, :, t-1] + scale_y[:, :, t, 0] - scale_y[:, :, t, 1])).reshape(POPULATION_SIZE, -1))

        # z_{j,t} = 0 if q_{j,t} <= 0, else 1
        z = np.where(q > 0, 1, 0)

        # Constraint 10: sum_{j=1}^nz_{j,t} <= K
        for t in range(self.tau):
            constraints.append((np.sum(z[:, :, t], axis=1) - self.K).reshape(POPULATION_SIZE, -1))

        # Constraint: dispose of all investments \tau - 1
        constraints.append((scale_y[:, :, self.tau-1, 1] - q[:, :, self.tau-2]).reshape(POPULATION_SIZE, -1))
        constraints.append((q[:, :, self.tau-1]).reshape(POPULATION_SIZE, -1))
        constraints.append((scale_y[:, :, self.tau-1, 0]).reshape(POPULATION_SIZE, -1))  # cannot buy

        out["G"] = np.hstack(constraints)


# Define the parameters (example values)
n = LEN_STOCK_DATA  # Stock quantity
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
# algorithm = NSGA3(pop_size=POPULATION_SIZE, ref_dirs=ref_dirs, repair=CustomRepair(), sampling=CustomSampling())
algorithm = NSGA3(pop_size=POPULATION_SIZE, ref_dirs=ref_dirs, sampling=CustomSampling())
# algorithm = NSGA3(pop_size=POPULATION_SIZE, ref_dirs=ref_dirs)


def m_solve():
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
        return
    hop_solution = front_0[hop(front_0, np.arange(len_front_0))[0]]
    print("Objectives =", ["%.6f" % v for v in hop_solution.F])
    print("Solution details =", ["%.1f" % v for v in hop_solution.X])


# Open a file in write mode
def execute():
    timestamp = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    unique_filename = f"output-{timestamp}.txt"
    with open("output/constraints-violations-restrain" + unique_filename, 'w') as f:
        start = time.time()
        # Save the original standard output
        # original_stdout = sys.stdout
        #
        # # Redirect standard output to the file
        # sys.stdout = f
        # print("Starting to write..")
        m_solve()

        end = time.time()
        print("The time of execution of above program is :",
              (end - start) * 10 ** 3, "ms")

        # sys.stdout = original_stdout


if __name__ == "__main__":
    for i in range(30):
        print(f"Starting loop i={i}...")
        execute()
    print("DONE - Thank you")