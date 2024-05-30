import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.optimize import minimize
from pymoo.problems import get_problem
from pymoo.visualization.scatter import Scatter

# Generate reference directions
ref_dirs = get_reference_directions("energy", 3, 150, seed=1)

# Create a 3D scatter plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(ref_dirs[:, 0], ref_dirs[:, 1], ref_dirs[:, 1], c='purple', marker='.', label='Reference Directions')
#
# # Add labels and legend
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# ax.legend()
#
# # Show the plot
# plt.show()

Scatter().add(ref_dirs).show()

# create the algorithm object
algorithm = NSGA3(pop_size=92, ref_dirs=ref_dirs)
# execute the optimization
res = minimize(get_problem("dtlz1"),
               algorithm,
               seed=1,
               termination=('n_gen', 600))