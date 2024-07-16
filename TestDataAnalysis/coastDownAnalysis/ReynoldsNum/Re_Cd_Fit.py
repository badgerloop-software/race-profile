import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read the CSV file
file_path = r'TestDataAnalysis\coastDownAnalysis\ReynoldsNum\Re_Cd_data.csv'
df = pd.read_csv(file_path)

Re = df['Reynolds_Number'].values
Cd = df['Drag_Coefficient'].values

# Define piecewise function
def piecewise_func(x, a, b, c, d, e, f, x0):
    return np.piecewise(x, [x < x0], 
                        [lambda x: a * np.exp(-b * x) + c,  # Modified exponential for low Re
                         lambda x: d * x**e + f])           # Power law for high Re

# Initial guess for parameters
p0 = [1, 1e-6, 0.1, 5e5, -1, 0.1, np.median(Re)]

# Fit the piecewise function
popt, _ = curve_fit(piecewise_func, Re, Cd, p0=p0, maxfev=10000)

# Generate points for the fitted curve
Re_smooth = np.logspace(np.log10(Re.min()), np.log10(Re.max()), 1000)
Cd_fit = piecewise_func(Re_smooth, *popt)

# Plot the data and fitted curve
plt.figure(figsize=(12, 8))
plt.scatter(Re, Cd, alpha=0.6, label='Data')
plt.plot(Re_smooth, Cd_fit, 'r-', label='Fitted Curve')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Reynolds Number (Re)')
plt.ylabel('Drag Coefficient (Cd)')
plt.title('Reynolds Number vs Drag Coefficient with Piecewise Fit')
plt.legend()
plt.grid(True)

# Create the full equation string with more decimal places
equation = (
    f"Cd = {popt[0]:.8e} * exp(-{popt[1]:.8e} * Re) + {popt[2]:.8e}, for Re < {popt[6]:.8e}\n"
    f"Cd = {popt[3]:.8e} * Re^({popt[4]:.8f}) + {popt[5]:.8e}, for Re >= {popt[6]:.8e}"
)

# Add the equation to the plot
plt.text(0.05, 0.05, equation, transform=plt.gca().transAxes, fontsize=9, verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()

# Print the fitted function parameters
print("Fitted piecewise function:")
print(equation)

# Calculate R-squared
Cd_fit_all = piecewise_func(Re, *popt)
residuals = Cd - Cd_fit_all
ss_res = np.sum(residuals**2)
ss_tot = np.sum((Cd - np.mean(Cd))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"\nR-squared: {r_squared:.8f}")