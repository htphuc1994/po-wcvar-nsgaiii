import matplotlib.pyplot as plt
import numpy as np

def plot_columns():
    # Define the data for four columns
    columns = ['Lower bound', 'VND100 million', 'VND1 billion', 'VND10 billion']

    # quarter
    # values = [0.01812, 0.28552, 0.29994, 0.20635]  # Generate random values between 0 and 1 for the columns
    # half year
    # values = [0.0273055, 0.28858, 0.26191, 0.16046]
    # 1 year

    # the 2nd try
    # quarter
    # values = [0.01812, 0.29034, 0.16607, 0.25116]  # Generate random values between 0 and 1 for the columns
    # half year
    # values = [0.0273055, 0.20915, 0.13659, 0.22311]
    # 1 year
    values = [0.0553567, 0.20202, 0.29067, 0.26279]

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    # plt.bar(columns, values, color=['b', 'g', 'r', 'c'])
    plt.bar(columns, values, color=['tab:blue', 'tab:purple', 'tab:pink', 'tab:orange'])

    # Set y-axis range from 0 to 1
    plt.ylim(0, 1)

    # Add labels and title
    plt.ylabel('Returns')
    plt.title('The connections between initial budgets and returns')

    # Show the plot
    plt.show()

# Call the function to plot the columns
plot_columns()
