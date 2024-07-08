import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# experiment 7
n_gen = list(range(1, 201))
front_num_Array = [3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
n_nds_Array = [8, 12, 3, 5, 7, 7, 10, 12, 7, 7, 8, 6, 7, 10, 13, 14, 11, 11, 17, 20, 20, 8, 17, 3, 6, 5, 10, 11, 5, 8, 4, 7, 7, 8, 13, 17, 14, 12, 10, 11, 18, 27, 21, 23, 28, 16, 19, 4, 7, 10, 13, 15, 17, 19, 18, 17, 19, 20, 21, 18, 20, 9, 11, 6, 11, 13, 14, 18, 18, 20, 15, 15, 15, 13, 16, 16, 13, 14, 15, 18, 17, 19, 12, 15, 15, 15, 17, 19, 9, 9, 8, 10, 8, 10, 13, 14, 15, 8, 12, 17, 22, 23, 20, 18, 17, 17, 14, 22, 24, 23, 18, 20, 20, 19, 24, 10, 8, 28, 22, 21, 21, 23, 20, 20, 22, 19, 21, 24, 26, 25, 19, 23, 29, 27, 30, 28, 29, 33, 33, 31, 30, 27, 26, 29, 26, 28, 28, 21, 22, 23, 24, 26, 25, 30, 30, 30, 31, 33, 29, 32, 30, 31, 31, 34, 32, 31, 32, 28, 34, 31, 31, 32, 31, 34, 34, 35, 31, 31, 29, 32, 29, 29, 28, 31, 19, 26, 26, 24, 24, 25, 23, 25, 18, 21, 19, 17, 17, 21, 17, 18]
eps = [None, 0.2759140546, 0.7708429302, 0.2993459157, 0.3436836401, 0.606876653, 0.355129778, 0.1517838936, 0.8050211997, 0.3644439739, 0.2574241405, 0.2633411864, 0.3567792321, 0.1663281122, 0.1046246408, 0.2758447606, 0.289965917, 0.2184942628, 0.1210112938, 0.1319590243, 0.1544850724, 0.1475968974, 0.0996593602, 3.352618925, 0.8272148904, 1.7370622054, 0.6769116799, 0.222122504, 1.5216311565, 0.6198969174, 1.5608227785, 0.6094355961, 0.0, 0.5543190116, 0.3475357738, 0.2510400833, 0.2575547466, 0.2048059914, 0.1610875216, 0.2167734294, 0.2207747322, 0.5497799505, 0.1246762749, 0.0189164469, 0.1503695165, 0.3787661615, 0.1295437997, 0.8318560236, 0.59991501, 0.0558325832, 0.318433136, 0.1647354015, 0.3057550109, 0.1149309176, 0.0881491227, 0.1692735565, 0.16984429, 0.1534312755, 0.2021382859, 0.1039425965, 0.1951505969, 0.3034599393, 0.3684307523, 0.3650715552, 0.7226467256, 0.2057534794, 0.1879793464, 0.0830704298, 0.1735005392, 0.0739277229, 0.3017934415, 0.1248916714, 0.2116618505, 0.2254520038, 0.1793012131, 0.2184738371, 0.0044809647, 0.0944562316, 0.1162874912, 0.0426802709, 0.0396381885, 0.0378721384, 0.1411963358, 0.0574443192, 0.0171550219, 0.0433058366, 0.070748716, 0.2654102152, 0.8592361522, 0.1604615137, 0.0, 0.1053530642, 0.1172605507, 0.0508337957, 0.0242051121, 0.1036009076, 0.296283675, 0.4210271448, 0.3787495423, 0.2052750583, 0.0507081212, 0.0795413423, 0.2176097382, 0.0782072967, 0.165779013, 0.0765522081, 0.386348249, 0.2771812108, 0.0418086326, 0.043632863, 0.1541058202, 0.0824155009, 0.191388192, 0.1670052148, 0.1236802542, 0.2192544108, 0.3032423565, 0.1236802542, 0.077061169, 0.0797938732, 0.0260226458, 0.1599705274, 0.0283075945, 0.1902942937, 0.0694005373, 0.0089594654, 0.2350166143, 0.1902942937, 0.1739078876, 0.0257398166, 0.2350166143, 0.1770998912, 0.0382665014, 0.0665628275, 0.0624087262, 0.0632144093, 0.0751378022, 0.0733824094, 0.1983031657, 0.247354308, 0.1139711865, 0.1983031657, 0.0413139146, 0.0430943092, 0.1868006987, 0.1765893981, 0.2144609236, 0.0691628947, 0.0478012824, 0.1370056544, 0.0148366777, 0.0066561136, 0.1668900559, 0.0176062737, 0.0434043755, 0.0798282271, 0.0451038059, 0.049467149, 0.0085854609, 0.020114295, 0.1727643296, 0.1860912107, 0.0087374748, 0.012193342, 0.0129894738, 0.0131604208, 0.128460087, 0.1903259031, 0.0137531182, 0.0293413551, 0.0660893865, 0.0232863536, 0.0097422656, 0.0346547057, 0.3051402452, 0.0492938451, 0.0096294995, 4.1147697362, 0.8044877772, 0.1080723331, 0.7205454856, 0.1157879702, 0.0243323157, 0.0306796607, 0.0868655708, 0.0136572947, 0.0998403612, 0.0891001153, 0.0319847922, 0.1390750974, 0.0906083532, 0.0294221391, 0.0225462221, 0.1849174509, 0.022210793, 0.0227153183, 0.0289673699, 0.122779304, 0.0025305788, 0.0401610577]
indicators = ['-', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'f', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'ideal', 'ideal', 'nadir', 'nadir', 'ideal', 'nadir', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'ideal', 'nadir', 'nadir', 'ideal', 'nadir', 'ideal', 'ideal', 'f', 'f', 'ideal', 'ideal']


# Convert None to NaN for plotting purposes
eps = [float('nan') if v is None else v for v in eps]

# Create a color map for the indicators
color_map = {
    '-': 'gray',
    'ideal': 'b',
    'f': 'g',
    'nadir': 'r'
}

# Assign colors based on the indicators
colors = [color_map[indicator] for indicator in indicators]

# Plotting the line through all points
plt.figure(figsize=(15, 5))
plt.plot(n_gen, eps, linestyle='-', color='gray', label='Epsilon Indicator Line')

# Plotting the epsilon values over generations with corresponding colors
marker = 'o'
for i in range(len(n_gen)):
    if indicators[i] == 'ideal':
        marker = 'o'
    elif indicators[i] == 'f':
        marker = 'p'
    else:
        marker = 'h'
    plt.plot(n_gen[i], eps[i], marker=marker, color=colors[i])

# Custom legend
custom_lines = [
    Line2D([0], [0], color=color_map['-'], marker='o', linestyle='-', label='Epsilon Indicator'),
    Line2D([0], [0], color=color_map['ideal'], marker='o', linestyle='None', label='ideal'),
    Line2D([0], [0], color=color_map['f'], marker='p', linestyle='None', label='f'),
    Line2D([0], [0], color=color_map['nadir'], marker='h', linestyle='None', label='nadir')]

plt.legend(handles=custom_lines, loc='best')

# Adding labels and title
plt.xlabel('Generation (n_gen)')
plt.ylabel('Epsilon Indicator (eps)')
plt.title('Epsilon Indicator Over Generations')
plt.grid(True)

# Show plot
plt.show()
