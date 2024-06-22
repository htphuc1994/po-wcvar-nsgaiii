import numpy as np
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.core.repair import Repair


class BinaryRepair(Repair):
    def _do(self, problem, pop, **kwargs):
        X = pop
        X = X.reshape((X.shape[0], problem.n, problem.tau, 3))
        x = X[:, :, :, 0]
        x = np.round(x)  # Round to nearest integer (0 or 1)
        X[:, :, :, 0] = x
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

        super().__init__(n_var=n * tau * 3,  # Number of decision variables
                         n_obj=2,           # Number of objectives
                         n_constr=n * tau * 5 + 4 + tau, # Number of constraints
                         xl=np.zeros(n * tau * 3), # Lower bounds of decision variables
                         xu=np.ones(n * tau * 3))  # Upper bounds of decision variables

    def _evaluate(self, X, out, *args, **kwargs):
        # Reshape the decision variable matrix into (population size, n, tau, 3)
        X = X.reshape((X.shape[0], self.n, self.tau, 3))

        # Extract decision variables
        x = X[:, :, :, 0]  # First type of decision variable (binary)
        y = X[:, :, :, 1]  # Second type of decision variable
        q = X[:, :, :, 2]  # Third type of decision variable

        # Objective 1: Minimize CVaR
        CVaR_t = np.zeros((X.shape[0], self.tau - 1))
        for t in range(1, self.tau):
            VaR_t = self.Theta * np.percentile(self.sigma, 1 - self.epsilon)
            CVaR_t[:, t-1] = (1 / self.epsilon) * np.mean(np.maximum(0, VaR_t - self.sigma[t-1]))
        obj1 = np.sum(CVaR_t, axis=1)

        # Objective 2: Maximize theta_tau
        theta = np.zeros((X.shape[0], self.tau))
        theta[:, 0] = self.Theta
        for t in range(1, self.tau):
            term1 = (1 + self.alpha) * (theta[:, t-1] - np.sum((1 + self.xi) * self.C[:, t-1] * y[:, :, t-1], axis=1))
            term2 = np.sum((1 - self.xi) * self.C[:, t-1] * y[:, :, t-1], axis=1)
            term3 = np.sum(self.beta * self.D[:, t-1] * q[:, :, t-2], axis=1) if t > 1 else 0
            theta[:, t] = term1 + term2 + term3

        obj2 = -theta[:, -1]

        out["F"] = np.column_stack([obj1, obj2])

        # Constraints
        constraints = []

        # Constraint: x_{1,j,0} = y_{1,j,0} = 0
        constraints.append(x[:, :, 0].reshape(-1, 1))
        constraints.append(y[:, :, 0].reshape(-1, 1))

        # Constraint: q_{j,0} = y_{0,j,0}
        constraints.append((q[:, :, 0] - y[:, :, 0]).reshape(-1, 1))

        # Constraint: theta_{0} = Theta
        constraints.append((theta[:, 0] - self.Theta).reshape(-1, 1))

        # Constraint: y_{1,j,t} <= q_{j,t-1}
        for t in range(1, self.tau):
            constraints.append((y[:, :, t] - q[:, :, t-1]).reshape(-1, 1))

        # Constraint: sum_{j=1}^{n} (1+\xi)C_{j,t}y_{0,j,t} <= theta_t
        for t in range(self.tau):
            constraints.append((np.sum((1 + self.xi) * self.C[:, t] * y[:, :, t], axis=1) - theta[:, t]).reshape(-1, 1))

        # Constraint: y_{i,j,t} <= Q_{j,t}
        for t in range(self.tau):
            constraints.append((y[:, :, t] - self.Q[:, t]).reshape(-1, 1))

        # Constraint: y_{i,j,t} <= x_{i,j,t} * INF
        for t in range(self.tau):
            constraints.append((y[:, :, t] - x[:, :, t] * self.INF).reshape(-1, 1))

        # Constraint: q_{j,t} = q_{j,t-1} + y_{0,j,t} - y_{1,j,t}
        for t in range(1, self.tau):
            constraints.append((q[:, :, t] - (q[:, :, t-1] + y[:, :, t] - y[:, :, t])).reshape(-1, 1))

        # Constraint: z_{j,t} = 0 if q_{j,t} <= 0, else 1
        z = np.where(q > 0, 1, 0)
        for t in range(self.tau):
            constraints.append((z[:, :, t] - (q[:, :, t] > 0).astype(int)).reshape(-1, 1))

        # Constraint: sum_{j=1}^nz_{j,t} <= K
        for t in range(self.tau):
            constraints.append((np.sum(z[:, :, t], axis=1) - self.K).reshape(-1, 1))

        # Constraint: dispose of all investments
        constraints.append((y[:, :, self.tau-1] - q[:, :, self.tau-2]).reshape(-1, 1))

        out["G"] = np.hstack(constraints)


# Define the parameters (example values)
n = 10  # Stock quantity
K = 5  # Preferred quantity of stock kinds to be retained
tau = 12  # Decision-making period in months
epsilon = 0.05  # Tail probability
alpha = 0.01  # Monthly bank interest rate
xi = 0.02  # Transaction fee percentage
beta = 0.03  # Share dividend price
C = np.random.rand(n, tau)  # Stock prices
D = np.random.rand(n, tau)  # Dividend payout ratios
Q = np.random.randint(1, 100, size=(n, tau))  # Highest amount of stock traded
sigma = np.random.rand(tau)  # Wavelet portfolio variance
INF = 1e6  # A significantly high value
Theta = 10000  # Initial idle cash

# Define the reference directions
ref_dirs = get_reference_directions("das-dennis", 2, n_partitions=12)

# Initialize the algorithm with BinaryRepair
algorithm = NSGA3(pop_size=92, ref_dirs=ref_dirs, repair=BinaryRepair())

# Define the problem
problem = PortfolioOptimizationProblem(n, K, tau, epsilon, alpha, xi, beta, C, D, Q, sigma, INF, Theta)

# Minimize the problem using NSGA-III
res = minimize(problem,
               algorithm,
               termination=('n_gen', 200),
               seed=1,
               save_history=True,
               verbose=True)

# Print the results
print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
