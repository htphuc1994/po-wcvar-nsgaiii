import matplotlib.pyplot as plt


experiment_16_wcvar = [0.70353, 0.27917, -0.05611, -0.32366, -0.32793, -0.32546, -0.27531, -0.27146, -0.37490, -0.34173, -0.28835]
experiment_17_wcvar = [0.79511, 0.34974, -0.29286, -0.45404, -0.44380, -0.43264, -0.38750, -0.38876, -0.41154, -0.38903, -0.38821]
experiment_18_wcvar = [1.11397, 0.74997, -0.03400, 0.09618, -0.27809, -0.20702, -0.32495, -0.27974, -0.37442, -0.02766, -0.15873]

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
