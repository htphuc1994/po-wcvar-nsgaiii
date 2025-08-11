import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['Quarterly', 'Semi-annual', 'Annual']
bank_deposit = [0.01356084112, 0.0273055, 0.0553567]
vnd_100_million = [0.1299755845029, 0.2375978239234, 0.1768924271947]
vnd_1_billion = [0.1212324546927, 0.2224426299007, 0.2606602962920]
vnd_10_billion = [0.1082098667781, 0.1184999557781, 0.1683081132788]

# Convert to percentages
bank_deposit = [x * 100 for x in bank_deposit]
vnd_100_million = [x * 100 for x in vnd_100_million]
vnd_1_billion = [x * 100 for x in vnd_1_billion]
vnd_10_billion = [x * 100 for x in vnd_10_billion]

# colors_plate = ["#FFB000", "#FF3030", "#FF33CC", "#C000FF", "#00E5FF", "#00FFBF"]
# Bar settings
bar_width = 0.35
x = np.arange(len(categories))
color_bank = "#FFB000"
color_100m = "#FF3030"
color_1b = "#FF33CC"
color_10b = "#C000FF"

# Chart 1: Bank deposit vs VND 1 billion
plt.figure(figsize=(7,6))
plt.bar(x - bar_width/2, bank_deposit, width=bar_width, label='Bank Deposit', color=color_bank, hatch='x')
plt.bar(x + bar_width/2, vnd_1_billion, width=bar_width, label='VND 1 Billion', color=color_1b, hatch='//')
plt.xlabel('Investment Period', fontsize=24)
plt.ylabel('Return (%)', fontsize=24)
# plt.title('Bank Deposit vs VND 1 Billion', fontsize=20)
plt.xticks(x, categories, fontsize=24, rotation=15, ha='right')
plt.ylim(0, 30)
plt.legend(fontsize=20)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()


# Chart 2: Bank deposit vs VND 10 billion
plt.figure(figsize=(7,6))
plt.bar(x - bar_width/2, bank_deposit, width=bar_width, label='Bank Deposit', color=color_bank, hatch='x')
plt.bar(x + bar_width/2, vnd_10_billion, width=bar_width, label='VND 10 Billion', color=color_10b, hatch='\\\\')
plt.xlabel('Investment Period', fontsize=24)
plt.ylabel('Return (%)', fontsize=24)
# plt.title('Bank Deposit vs VND 10 Billion', fontsize=20)
plt.xticks(x, categories, fontsize=24, rotation=15, ha='right')
plt.yticks(fontsize=24)
plt.ylim(0, 30)
plt.legend(fontsize=20)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()



bar_width = 0.16
x = np.arange(len(categories))
colors = ["#FFB000", "#FF3030", "#FF33CC", "#C000FF"]
# 'x', '//', '\\\\', '||'
plt.figure(figsize=(8,6))
plt.bar(x - 3 * bar_width, bank_deposit, width=bar_width, label='Bank Deposit', color=colors[0], hatch='x')
plt.bar(x - 2 * bar_width, vnd_100_million, width=bar_width, label='VND 100 Mln', color=colors[1], hatch='//')
plt.bar(x - bar_width, vnd_1_billion, width=bar_width, label='VND 1 Bln', color=colors[2], hatch='\\\\')
plt.bar(x, vnd_10_billion, width=bar_width, label='VND 10 Bln', color=colors[3], hatch='||')
plt.xlabel('Investment Period', fontsize=24)
plt.ylabel('Return (%)', fontsize=24)
# plt.title('Returns by Investment Strategy and Period', fontsize=20)
plt.xticks(x, categories, fontsize=24, rotation=10, ha='right')
plt.yticks(fontsize=24)
plt.ylim(0, 30)
plt.legend(fontsize=20)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()