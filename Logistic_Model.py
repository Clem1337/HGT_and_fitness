import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Define the Logistic growth model function
def logistic(t, K, r, t0):
    return K / (1 + np.exp(-r * (t - t0)))

# Read data file
data = pd.read_csv('Logistic_Growth_Model.csv')

# Extract the time column (assuming the first column is time)
time = data['Time'].values

# Extract OD value columns for each strain (assuming columns from the second column onwards are OD values for each strain)
OD_data = data.drop(columns=['Time']).values  # Remove the time column and get the OD data matrix

# Store fitting results for each strain
results = []

# Fit each column (i.e., each strain)
for i in range(OD_data.shape[1]):  # Iterate through all strains
    OD = OD_data[:, i]  # OD values for the current strain
    initial_guess = [max(OD), 0.1, time[len(time)//2]]  # Initial guess values: K=maximum value, r=0.1, t0=middle time
    try:
        # Perform fitting
        popt, _ = curve_fit(logistic, time, OD, p0=initial_guess)
        K_fit, r_fit, t0_fit = popt
        results.append((K_fit, r_fit, t0_fit))
        print(f"Fitting parameters for strain {i+1}: K = {K_fit}, r = {r_fit}, t0 = {t0_fit}")
    except Exception as e:
        print(f"Strain {i+1} fitting failed: {e}")

# Save the fitting results as a DataFrame
results_df = pd.DataFrame(results, columns=['K', 'r', 't0'])

# Save fitting parameters to CSV file
results_df.to_csv('Fitting_Parameter_Results.csv', index=False)

print("Fitting process completed, results saved as 'Fitting_Parameter_Results.csv'.")
