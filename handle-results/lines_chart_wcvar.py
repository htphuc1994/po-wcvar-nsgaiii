import matplotlib.pyplot as plt


# experiment_16_wcvar = [-0.05195, -0.02230, 0.00000, -0.06598, -0.15285, -0.17421, -0.18198, -0.19472, -0.23474, -0.22050, -0.15634]
# experiment_17_wcvar = [-0.06927, -0.05053, 0.00000, -0.09575, -0.13952, -0.14686, -0.15465, 0.00000, -0.16851, 0.00000, 0.00000]
# experiment_18_wcvar = [-0.07628, -0.05351, -0.06639, -0.09602, -0.22105, -0.25584, -0.28068, -0.29155, -0.25227, -0.17030, -0.20818]

experiment_16_wcvar = [-0.05161, -0.04564, -0.03823, -0.03736, -0.08171, -0.09899, -0.09587, -0.10494, -0.14168, -0.12687, -0.12770]
experiment_17_wcvar = [-0.06133, -0.04843, -0.06173, -0.08712, -0.16134, -0.17956, -0.18770, -0.20000, -0.20052, -0.17554, -0.15420]
experiment_18_wcvar = [-0.07694, -0.03862, -0.04639, -0.10729, -0.21751, -0.24349, -0.24185, -0.24213, -0.23859, -0.23885, -0.20581]
def plot_multiple_lines(x, y_arrays):
    plt.figure(figsize=(20, 8))

    # Updated line styles list to include 6 styles
    # line_styles = ['-', '--', '-.', ':', 'dashed', 'dashed']
    # num_styles = len(line_styles)

    # for i, y in enumerate(y_arrays):
    #     style = line_styles[i % num_styles]  # Cycle through the line styles
    #     plt.plot(x, y, linestyle=style, label=f'Line {i+1}')

    marker_styles = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h']
    line_colors = ['r', 'm', 'b', 'c', 'y', 'g', 'k', 'orange', 'purple', 'brown']
    # line_colors = ['r', 'r', 'r', 'orange', 'orange', 'orange', 'orange']
    num_markers = len(marker_styles)
    num_lines = len(y_arrays)
    # for i, y in enumerate(y_arrays):
    #     marker = marker_styles[i % num_markers]  # Cycle through the marker styles
    #     plt.plot(x, y, linestyle='-', marker=marker, label=f'Line {i+1}')

    # for i, y in enumerate(y_arrays):
    #     # Plot the line
    #     plt.plot(x, y, linestyle='-', label=f'Line {i+1}')
    #     # Add a single marker at the midpoint of the line
    #     midpoint = len(x) // 2
    #     # if i % 2 == 0:
    #     #     midpoint = midpoint // 2
    #     plt.plot(x[midpoint], y[midpoint], marker=marker_styles[i % num_markers], markersize=10, label=f'Line {i+1}')

    for i, y in enumerate(y_arrays):
        line_name = f'Line {i+1}'
        if i == 0:
            line_name = 'Tail probability ε = 0.2'
        elif i == 1:
            line_name = 'Tail probability ε = 0.1'
        elif i == 2:
            line_name = 'Tail probability ε = 0.05'
        color = line_colors[i % len(line_colors)]  # Cycle through the line colors
        # Plot the line
        plt.plot(x, y, linestyle='-', label='', color=color)
        # Add a single marker at different positions to avoid overlap
        marker_position = len(x) // (num_lines + 1) * (i + 1)
        plt.plot(x[marker_position], y[marker_position], marker=marker_styles[i % num_markers], markersize=10, label=line_name, color=color)


    # Add labels and title
    plt.xlabel('Month', fontsize=16)
    plt.ylabel('WCVaR', fontsize=16)
    plt.title('The relationship between WCVaR and tail probability', fontsize=16)
    plt.legend()

    # Show the plot
    plt.show()


# Example usage
x = list(range(1, 12))  # Array from 1 to 11
# y1 = experiment_1_front_nums
# y2 = experiment_2_front_nums
# y3 = experiment_3_front_nums
# y4 = experiment_4_front_nums
# y5 = experiment_5_front_nums
# y6 = experiment_6_front_nums

y1 = experiment_16_wcvar
y2 = experiment_17_wcvar
y3 = experiment_18_wcvar

# List of y arrays
y_arrays = [y1, y2, y3]

plot_multiple_lines(x, y_arrays)
