import matplotlib.pyplot as plt

# times 269717.43988990784 478950.51288604736 500027.0240306854
experiment_16_wcvar = [0.0094778556483, 0.0128910763445, 0.0211688197572, 0.0367642146726, 0.4318107209885, 0.0736346007213, 0.0347919326395, 0.0828811278003, 0.5999259719843, 0.0401892115252, 0.1832985582213]
experiment_17_wcvar = [0.0237125666346, 0.0105774182424, 0.0236672646602, 0.0367298014355, 0.1047085053299, 0.0544324035503, 0.0505865546549, 0.0127942663551, 0.0251530680701, 0.1357152637856, 0.2424220446296]
experiment_18_wcvar = [0.0466248357068, 0.1083775739944, 0.0370360611675, 0.0556696153217, 0.4644641852379, 0.0571190746216, 0.0373664903986, 0.0382387879305, 0.0413876139766, 0.0971398193703, 1.0099607393124]

def plot_multiple_lines(x, y_arrays):
    plt.figure(figsize=(15, 7))

    # Updated line styles list to include 6 styles
    # line_styles = ['-', '--', '-.', ':', 'dashed', 'dashed']
    # num_styles = len(line_styles)

    # for i, y in enumerate(y_arrays):
    #     style = line_styles[i % num_styles]  # Cycle through the line styles
    #     plt.plot(x, y, linestyle=style, label=f'Line {i+1}')

    marker_styles = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h']
    line_colors = ["#FFB000", "#FF3030", "#FF33CC", "#C000FF", "#00E5FF", "#00FFBF"]
    # line_colors = ['r', 'm', 'b', 'c', 'y', 'g', 'k', 'orange', 'purple', 'brown']
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
    plt.ylabel('WCVaR (Logarithmic Scale)', fontsize=24)
    # plt.title('The relationship between WCVaR and tail probability', fontsize=24)
    plt.legend(fontsize=24)

    plt.yscale('log')

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
