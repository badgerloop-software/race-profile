import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Constants (replace with actual values if different)
m = 1000  # mass of vehicle (kg)
g = 9.81  # gravitational acceleration (m/s^2)
A = 2.0   # frontal area of vehicle (m^2)

# Read the CSV file
file_path = r'TestDataAnalysis\coastDownAnalysis\ReynoldsNum\output_with_reynolds.csv'
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty")
    exit(1)
except pd.errors.ParserError:
    print("Error: Unable to parse the CSV file")
    exit(1)

# Extract relevant columns
v = df.iloc[:, 1]  # speed (m/s)
rho = df.iloc[:, 5] / 1000  # air density (convert g/m^3 to kg/m^3)
mu = df.iloc[:, 6]  # air viscosity (assuming it's in correct units, e.g., kg/(m·s))
Re = df.iloc[:, 7]  # Reynolds number

# Calculate acceleration
a = -0.000001 + 0.000012*v - 0.00025*v**2

# Calculate rolling resistance coefficient
C_RR = 0.0017 * np.exp(0.0054 * v)

# Calculate total force
F_total = m * a

# Calculate rolling resistance force
F_rolling = m * g * C_RR

# Calculate drag force
F_drag = -(F_total - F_rolling)

# Calculate drag coefficient (Cd)
Cd = 2 * F_drag / (rho * v**2 * A)



# Save the Re and Cd data to a new CSV file
output_df = pd.DataFrame({'Reynolds_Number': Re, 'Drag_Coefficient': Cd})
output_path = 'TestDataAnalysis\\coastDownAnalysis\\ReynoldsNum\\Re_Cd_data.csv'
output_df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")

# Basic statistical analysis
print("\nBasic Statistical Analysis:")
print(f"Mean Cd: {Cd.mean():.4f}")
print(f"Median Cd: {Cd.median():.4f}")
print(f"Standard Deviation of Cd: {Cd.std():.4f}")
print(f"Min Cd: {Cd.min():.4f}")
print(f"Max Cd: {Cd.max():.4f}")

# Additional analysis
print("\nAdditional Analysis:")
print(f"Average air density: {rho.mean():.4f} kg/m^3")
print(f"Average air viscosity: {mu.mean():.4e} kg/(m·s)")
print(f"Reynolds number range: {Re.min():.2e} to {Re.max():.2e}")