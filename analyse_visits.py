import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Step 1: Load and preprocess data
data = pd.read_csv('ms_data.csv')
data['visit_date'] = pd.to_datetime(data['visit_date'])
data = data.sort_values(['patient_id', 'visit_date']).reset_index(drop=True)

# Step 2: Assign insurance type and calculate visit costs
# Read insurance types and create a dictionary to assign consistent insurance types
insurance_types = pd.read_table('insurance.lst')['insurance_type'].tolist()
patient_ids = data['patient_id'].unique()
insurance_mapping = {patient_id: np.random.choice(insurance_types) for patient_id in patient_ids}

# Add insurance type and visit costs to the DataFrame
data['insurance_type'] = data['patient_id'].map(insurance_mapping)

# Define a cost mapping for the insurance types
cost_means = {'Basic': 1000, 'Premium': 750, 'Platinum': 500}
data['visit_cost'] = data['insurance_type'].map(cost_means) * np.random.uniform(0.8, 1.2, len(data))
data['visit_cost'] = data['visit_cost'].round(2)

# Save the modified dataset for future use
data.to_csv('ms_data_with_insurance.csv', index=False)

# Step 3: Calculate summary statistics
# Mean walking speed by education level
mean_speed_by_education = data.groupby('education_level')['walking_speed'].mean()

# Mean visit cost by insurance type
mean_cost_by_insurance = data.groupby('insurance_type')['visit_cost'].mean()

# Display summary statistics
print("Mean Walking Speed by Education Level:")
print(mean_speed_by_education, "\n")

print("Mean Visit Cost by Insurance Type:")
print(mean_cost_by_insurance, "\n")

# Step 4: Perform linear regression on walking speed vs age
X = sm.add_constant(data['age'])
y = data['walking_speed']
regression_model = sm.OLS(y, X).fit()

# Display regression results
print("=== Linear Regression for Walking Speed by Age ===")
print(regression_model.summary())