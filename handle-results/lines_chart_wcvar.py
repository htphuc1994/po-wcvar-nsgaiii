import matplotlib.pyplot as plt


experiment_16_wcvar = [-0.0799941251113, -0.0624838278440, -0.0770781785811, -0.0973908297994, -0.1703395559946, -0.1749092950463, -0.2051275115310, -0.2126103396827, -0.1535334549885, -0.1554683746421, -0.1226948556745]
experiment_17_wcvar = [-0.0994126674844, -0.0811817347237, -0.0923284172030, -0.1159419770614, -0.1526474170200, -0.1189507289163, -0.1456712125883, -0.1712629192675, -0.1647816121144, 0.0000000000000, -0.2891212696685]
experiment_18_wcvar = [-0.1271267877000, -0.1042148884496, -0.0898989047201, -0.1501892389714, -0.1703190076643, -0.1667092083732, -0.1660104600299, 0.0000000000000, 0.0000000000000, -0.1647300028646, -0.3313638671293]

# experiment_16_wcvar = [-0.0549587520840, -0.0548883833496, -0.0657814681197, -0.0861692387455, -0.2260372171343, -0.2382464533307, -0.2427123887526, -0.2594892971419, -0.2485834267962, -0.2536365833644, -0.2494584529520]
# experiment_17_wcvar = [-0.0852970422420, -0.0703588217340, -0.0552638389049, -0.0912689930982, -0.1560039768726, -0.1494465867136, -0.1487306113099, -0.1795522197365, -0.1788078614515, -0.1254772688280, -0.2937740536645]
# experiment_18_wcvar = [-0.1422847290370, -0.1628387805533, -0.1454382609237, -0.2068994367970, -0.1755747400348, -0.1791792200318, -0.1629288921032, 0.0000000000000, -0.1367516262772, 0.0000000000000, 0.0000000000000]

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
        plt.plot(x[marker_position], y[marker_position], marker=marker_styles[i % num_markers], markersize=12, label=line_name, color=color)


    # Add labels and title
    plt.xlabel('Month', fontsize=16)
    plt.ylabel('WCVaR', fontsize=16)
    plt.title('The relationship between WCVaR and tail probability', fontsize=16)
    plt.legend(fontsize=16)

    plt.tick_params(axis='y', labelsize=16)
    plt.tick_params(axis='x', labelsize=16)
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
