import os
import numpy as np
from matplotlib import pyplot as plt
import serpentTools
from serpentTools.settings import rc
import csv

# Configure Serpent version
rc['serpentVersion'] = '2.1.30'

# File number list and corresponding boron concentrations (in ppm)
numbers = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
boron_concentrations = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]  # in ppm

# Initialize lists to store keff values and BWC results
keff_values = []
bwc_values = []

# Read the keff values from each file
for number in numbers:
    res_file = f'/home/diego/results_ouput/nuscale_sbu_{number}h.c_res.m'
    res = serpentTools.read(res_file)
    keff = res.resdata['absKeff']
    
    # Extract the keff value (handle multidimensional arrays)
    if keff.ndim == 1:
        keff_values.append(keff)
    else:
        keff_values.append(keff[:, 0])

# Calculate the BWC values between successive boron concentrations
for i in range(1, len(keff_values)):
    delta_keff = keff_values[i] - keff_values[i-1]
    delta_boron = boron_concentrations[i] - boron_concentrations[i-1]
    bwc = delta_keff / delta_boron
    bwc_values.append(bwc)

# Define the output file path
output_file_path = 'bwc_keff_results.csv'

# Save BWC values to a CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Boron_Concentration_1', 'Boron_Concentration_2', 'Keff_Diff', 'BWC'])
    for i in range(1, len(bwc_values)):
        csvwriter.writerow([boron_concentrations[i-1], boron_concentrations[i], keff_values[i] - keff_values[i-1], bwc_values[i-1]])

print(f"BWC and Keff differences have been saved to {output_file_path}")

# Plotting the BWC values against boron concentrations
plt.plot(boron_concentrations[1:], bwc_values, marker='o')
plt.xlabel('Boron Concentration (ppm)')
plt.ylabel('BWC')
plt.title('Boron Worth Coefficient (BWC) vs Boron Concentration')
plt.grid(True)
plt.show()
