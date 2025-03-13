# %%
import os
import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
import scipy.stats as stats

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import ast
from scipy import stats

#%%

# Set data location
current_folder = os.path.dirname(os.path.abspath(__file__))
data_location = os.path.join(current_folder, '../../result/intervention')
os.chdir(data_location)

# Intervention test values
alpha = 0.05  # Keep alpha unchanged
intervention_values = [3, 7, 10, 14]  # Different test values for subplot titles
fig, axes = plt.subplots(4, 1, figsize=(8, 20))  # Create a 2x2 grid of subplots
cumul = True
# Read real data
real_data = pd.read_csv('dataA_per_months.csv')
real = real_data['PHAI_counts']
if cumul:
    real = np.cumsum(real)

# Iterate over the intervention values and plot for each
for i, intervention in enumerate(intervention_values):
    # Read the corresponding intervention test CSV
    run_data = pd.read_csv(f'intervention_test_iso_{intervention}.csv')
    
    # Parse HCW related infections if it's a string
    if isinstance(run_data['HCW_related_infecs'].iloc[0], str):
        run_data['HCW_related_infecs'] = run_data['HCW_related_infecs'].apply(ast.literal_eval)

    # Extract the infection data and compute mean values
    matrix = np.array(run_data['HCW_related_infecs'].tolist())
    mean_values = matrix.mean(axis=0)

    if cumul:
        mean_values = np.cumsum(mean_values)

    # Calculate 95% CI using Poisson distribution
    ci_lower = stats.poisson.ppf(alpha / 2, mean_values)
    ci_upper = stats.poisson.ppf(1 - alpha / 2, mean_values)
    x_values = np.arange(1, len(mean_values))

    # Determine subplot position
    # ax = axes[i // 2, i % 2]  # Grid position based on i
    ax = axes[i]
    # Plot real and average HCW infections
    ax.plot(x_values, real[1:], marker='o', linestyle='-', color='r', label="Real HCW Infections")
    ax.plot(x_values, mean_values[1:], marker='o', linestyle='-', color='b', label="Avg HCW Infections")

    # Fill the confidence interval area
    ax.fill_between(x_values, ci_lower[1:], ci_upper[1:], color='b', alpha=0.2, label="95% CI (Poisson)")
    
    # Set plot labels and title
    ax.set_xlabel("Month")
    ax.set_xticks(x_values)
    ax.set_ylabel("Average Infections")
    ax.set_title(f"Average HCW Related Infections (intervention={intervention})")
    ax.set_ylim(-1, 20)    
    ax.grid(True)
    ax.legend(loc="upper right")
    if cumul:
        ax.set_ylim(-1, 50)
        ax.legend(loc="upper left")


# Adjust layout for better spacing
plt.tight_layout()
plt.show()



# %% CUMULATIVE INCIDENCE

current_folder = os.path.dirname(os.path.abspath(__file__))
data_location = os.path.join(current_folder, '../../result/intervention')
os.chdir(data_location)

run_data = pd.read_csv('intervention_test_iso_14.csv')
real_data = pd.read_csv('dataA_per_months.csv')
if isinstance(run_data['HCW_related_infecs'].iloc[0], str):
    run_data['HCW_related_infecs'] = run_data['HCW_related_infecs'].apply(ast.literal_eval)

matrix = np.array(run_data['HCW_related_infecs'].tolist())
real = real_data['PHAI_counts']

mean_values = matrix.mean(axis=0)

alpha = 0.05 
ci_lower = stats.poisson.ppf(alpha / 2, np.cumsum(mean_values))
ci_upper = stats.poisson.ppf(1 - alpha / 2, np.cumsum(mean_values))

x_values = np.arange(1, len(mean_values))

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(x_values, np.cumsum(real[1:]), marker='o', linestyle='-', color='r', label="Real HCW Infections")
ax1.plot(x_values, np.cumsum(mean_values[1:]), marker='o', linestyle='-', color='b', label="Avg HCW Infections")

ax1.fill_between(x_values, (ci_lower[1:]), (ci_upper[1:]), color='b', alpha=0.2, label="95% CI (Poisson)")
ax1.set_xticks(x_values)
ax1.set_xlabel("Time Step")
ax1.set_ylabel("Average Infections")
ax1.set_title("Average HCW Related Infections Over Time")
ax1.legend(loc="upper left")
ax1.set_ylim(-1, 50)
ax1.grid(True)

plt.show()
# %%
