# python
# Combine all filtered CSV files into one DataFrame.
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

def combine_filtered_files(input_folder):
    """Combine all filtered CSV files into one DataFrame."""
    input_files = glob.glob(os.path.join(input_folder, "filtered_*.csv"))
    
    combined_data = pd.DataFrame()
    
    for input_file in input_files:
        if os.path.getsize(input_file) > 0:  # Check if the file is not empty
            data = pd.read_csv(input_file)
            combined_data = pd.concat([combined_data, data], ignore_index=True)
        else:
            print(f"Skipping empty file: {input_file}")
    
    return combined_data

def remove_outliers(data, threshold=0.0004):
    """Remove outliers from the data based on the given threshold."""
    median_acceleration = np.median(data['acceleration_m/s^2'])
    deviation = np.abs(data['acceleration_m/s^2'] - median_acceleration)
    filtered_data = data[deviation <= threshold]
    
    return filtered_data

def polynomial_fit(data, degree=2):
    """Perform a polynomial fit to the data."""
    velocities = data['velocity_m/s'].values
    accelerations = data['acceleration_m/s^2'].values
    
    # Polynomial fit
    coefs = np.polyfit(velocities, accelerations, degree)
    
    # Generate polynomial function
    poly = Polynomial(coefs[::-1])
    
    return poly, coefs

def plot_fit(data, poly, coefs):
    """Plot the data and the polynomial fit."""
    velocities = data['velocity_m/s'].values
    accelerations = data['acceleration_m/s^2'].values
    
    # Generate fit line
    velocities_fit = np.linspace(min(velocities), max(velocities), 500)
    accelerations_fit = poly(velocities_fit)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(velocities, accelerations, color='blue', label='Data Points')
    plt.plot(velocities_fit, accelerations_fit, color='red', label='Polynomial Fit')
    
    # Add fitting equation with sufficient precision
    equation = (f"$a = {coefs[0]:.6f} + {coefs[1]:.6f}v + {coefs[2]:.6f}v^2$")
    plt.text(0.05, 0.95, equation, transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='top')
    
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Acceleration (m/s^2)')
    plt.title('Acceleration vs Velocity with Polynomial Fit')
    plt.legend()
    plt.grid(True)
    
    plt.savefig("acceleration_velocity_fit.png")
    plt.show()

def main():
    input_folder = "."  # Current directory; change as needed
    combined_data = combine_filtered_files(input_folder)
    
    if combined_data.empty:
        print("No data to process.")
        return
    
    # Remove outliers
    filtered_data = remove_outliers(combined_data)
    
    # Save combined data
    filtered_data.to_csv("combined_filtered_data.csv", index=False)
    
    # Perform polynomial fit
    poly, coefs = polynomial_fit(filtered_data)
    
    # Save polynomial coefficients
    with open("polynomial_fit_coefficients.csv", "w") as f:
        f.write("Coefficient,Value\n")
        for i, coef in enumerate(coefs):
            f.write(f"a{i},{coef}\n")
    
    # Plot and save the graph
    plot_fit(filtered_data, poly, coefs)
    
    print("Combined data, polynomial fit coefficients, and graph saved.")

if __name__ == "__main__":
    main()