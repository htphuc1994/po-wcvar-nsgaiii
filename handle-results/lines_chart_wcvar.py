import matplotlib.pyplot as plt

# times 269717.43988990784 478950.51288604736 500027.0240306854
experiment_16_wcvar = [-0.0499329865989, -0.0417631430254, -0.0347779703387, -0.0296061636330, -0.0807314629339, -0.0857072061730, -0.0849493493231, -0.0989324802687, -0.0863442311379, -0.0940563867041, -0.1024835227685]
experiment_17_wcvar = [-0.0917358669545, -0.0778480600597, -0.1006420485193, -0.1065393263344, -0.1071618753253, -0.1276505873478, 0.0000000000000, 0.0000000000000, -0.1395104042318, -0.1076460732002, -0.1236991237182]
experiment_18_wcvar = [-0.1518859513838, -0.1353593829326, -0.1283448605513, -0.1271934989048, -0.2801609564646, -0.2649228400655, -0.2660545284715, -0.2551655982476, -0.2331117418145, -0.1934132175836, -0.1862648517133]

def plot_multiple_lines(x, y_arrays):
    plt.figure(figsize=(15, 7))

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
            line_name = 'ε = 0.2'
        elif i == 1:
            line_name = 'ε = 0.1'
        elif i == 2:
            line_name = 'ε = 0.05'
        color = line_colors[i % len(line_colors)]  # Cycle through the line colors
        # Plot the line
        plt.plot(x, y, linestyle='-', label='', color=color)
        # Add a single marker at different positions to avoid overlap
        marker_position = len(x) // (num_lines + 1) * (i + 1)
        plt.plot(x[marker_position], y[marker_position], marker=marker_styles[i % num_markers], markersize=24, label=line_name, color=color)


    # Add labels and title
    plt.xlabel('Month', fontsize=24)
    plt.ylabel('WCVaR', fontsize=24)
    # plt.title('The relationship between WCVaR and tail probability', fontsize=24)
    plt.legend(fontsize=24)

    plt.tick_params(axis='y', labelsize=24)
    plt.tick_params(axis='x', labelsize=24)
    plt.grid(True)
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
