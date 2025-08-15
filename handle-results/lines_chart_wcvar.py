import matplotlib.pyplot as plt
import numpy as np

# times 269717.43988990784 478950.51288604736 500027.0240306854
# experiment_16_wcvar = [0.0094778556483, 0.0128910763445, 0.0211688197572, 0.0367642146726, 0.4318107209885, 0.0736346007213, 0.0347919326395, 0.0828811278003, 0.5999259719843, 0.0401892115252, 0.1832985582213]
# experiment_17_wcvar = [0.0237125666346, 0.0105774182424, 0.0236672646602, 0.0367298014355, 0.1047085053299, 0.0544324035503, 0.0505865546549, 0.0127942663551, 0.0251530680701, 0.1357152637856, 0.2424220446296]
experiment_18_wcvar = [0.0466248357068, 0.1083775739944, 0.0370360611675, 0.0556696153217, 0.4644641852379, 0.0571190746216, 0.0373664903986, 0.0382387879305, 0.0413876139766, 0.0971398193703, 1.0099607393124]


# experiment_16_wcvar = [0.0421014036240, 0.0084619680637, 0.0177320022005, 0.0304182657730, 0.2659854473244, 0.0314626469324, 0.0349613469390, 0.0130588947040, 0.0229176369555, 0.0532528028324, 0.1722622887248]
experiment_17_wcvar = [0.0738949473029, 0.0263565213853, 0.2013353529073, 0.0523494602487, 0.0755547013381, 0.0523536321787, 0.0426378129426, 0.0252262606930, 0.0340296906213, 0.0300817154720, 0.5765645102652]
# experiment_18_wcvar = [0.1074622348728, 0.0495402016103, 0.0224632798364, 0.0530648283941, 0.0547474950460, 0.4741989066168, 0.6357499135359, 0.0545928419541, 0.0251246459130, 0.0689069017529, 0.2768331462916]

experiment_16_wcvar = [0.0509728452038, 0.0041667928782, 0.0173634397614, 0.0269219133609, 0.7019113367392, 0.0518577228724, 0.0237363619563, 0.0268941565913, 0.0206831399290, 0.0306892114138, 0.1300191589815]
# experiment_17_wcvar = [0.0844067707848, 0.0601691243322, 0.1103334360652, 0.1351192057674, 0.2698416692405, 0.0790624565541, 0.1120595944982, 0.0603304177460, 0.0575807741018, 0.0840608588615, 0.0951212699264]
# experiment_18_wcvar = [0.0954047914613, 0.0277686313050, 0.2261100946900, 0.0228211112230, 0.0444265202736, 0.0484958137333, 0.0705972228356, 0.0156173725013, 0.0163107790886, 0.0490078491990, 0.5915496585934]


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
