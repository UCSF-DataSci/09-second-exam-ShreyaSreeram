import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols, mixedlm
from scipy.stats import f_oneway
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

# Setting up argument parser
parser = argparse.ArgumentParser(description="Statistical Analysis for MS Data")
parser.add_argument('--input', type=str, default='ms_data_with_insurance.csv', help='Path to input CSV file')
parser.add_argument('--output', type=str, default='results_summary.txt', help='Path to output summary file')
parser.add_argument('--save_plots', action='store_true', help='Save the plots as PNG files')
args = parser.parse_args()

#data
data = pd.read_csv(args.input)

#initialise a list to collect all outputs for the results file
results_output = []

# Step 1: Analyse walking speed
# Multiple regression: walking_speed ~ education_level + age
walking_speed_model = ols('walking_speed ~ education_level + age', data=data).fit()
results_output.append("=== Multiple Regression: Walking Speed Analysis ===")
results_output.append(str(walking_speed_model.summary()))
print("\n".join(results_output[-2:]))

# Step 2: Analyse costs
# ANOVA for insurance type effect on costs
anova_results = f_oneway(
    data.loc[data['insurance_type'] == 'Basic', 'visit_cost'],
    data.loc[data['insurance_type'] == 'Premium', 'visit_cost'],
    data.loc[data['insurance_type'] == 'Platinum', 'visit_cost']
)
anova_output = f"\n=== ANOVA: Insurance Type Effect on Costs ===\nF-statistic: {anova_results.statistic}, p-value: {anova_results.pvalue}"
results_output.append(anova_output)
print(anova_output)

# statistics for costs
mean_costs = data.groupby('insurance_type')['visit_cost'].mean()
std_costs = data.groupby('insurance_type')['visit_cost'].std()
mean_costs_output = f"\nMean Costs by Insurance Type:\n{mean_costs}"
std_costs_output = f"\nStandard Deviation of Costs by Insurance Type:\n{std_costs}"
results_output.extend([mean_costs_output, std_costs_output])
print(mean_costs_output)
print(std_costs_output)

# Effect size (Cohen's d for two groups as an example: Basic vs Premium)
basic_costs = data.loc[data['insurance_type'] == 'Basic', 'visit_cost']
premium_costs = data.loc[data['insurance_type'] == 'Premium', 'visit_cost']
effect_size = (np.mean(basic_costs) - np.mean(premium_costs)) / np.sqrt(
    (np.std(basic_costs)**2 + np.std(premium_costs)**2) / 2
)
effect_size_output = f"\nEffect Size (Cohen's d for Basic vs Premium): {effect_size:.4f}"
results_output.append(effect_size_output)
print(effect_size_output)

# Step 3: Advanced analysis
# Interaction effect: walking_speed ~ education_level * age
interaction_model = ols('walking_speed ~ education_level * age', data=data).fit()
interaction_output = "\n=== Interaction Effects: Walking Speed Analysis ===\n" + str(interaction_model.summary())
results_output.append(interaction_output)
print(interaction_output)

# Bonus: Mixed-effects model for walking speed
mixed_model = mixedlm('walking_speed ~ education_level + age', data, groups=data['patient_id'])
mixed_model_results = mixed_model.fit()
mixed_model_output = "\n=== Mixed-Effects Model: Walking Speed Analysis ===\n" + str(mixed_model_results.summary())
results_output.append(mixed_model_output)
print(mixed_model_output)

#saving results to the specified output file
with open(args.output, 'w') as f:
    f.write("\n".join(results_output))

#saving the plot if --save_plots is specified
if args.save_plots:
    sns.lmplot(data=data, x='age', y='walking_speed', hue='education_level', col='education_level', height=4)
    plt.savefig('interaction_effects.png')
    print("\nPlots saved as 'interaction_effects.png'")