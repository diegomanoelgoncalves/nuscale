import os
import numpy as np
from matplotlib import pyplot as plt
import serpentTools
from serpentTools.settings import rc
import csv

# Configure Serpent version
rc['serpentVersion'] = '2.1.30'

# File number list and corresponding fuel temperatures (in Kelvin)
numbers = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]
temp = [26.85, 126.85, 226.85, 326.85, 426.85, 526.85, 626.85, 726.85, 826.85, 926.85, 1026.85, 1126.85, 1226.85]  # in Kelvin

# Initialize lists to store keff values and FTC results
keff_values = []
ftc_values = []

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

# Calculate the FTC values between successive temperatures
for i in range(1, len(keff_values)):
    delta_keff = keff_values[i] - keff_values[i-1]
    delta_temp = temp[i] - temp[i-1]
    ftc = delta_keff / delta_temp
    ftc_values.append(ftc)

# Define the output file path
output_file_path = 'ftc_keff_results.csv'

# Save FTC values to a CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Temp_1', 'Temp_2', 'Keff_Diff', 'FTC'])
    for i in range(1, len(ftc_values)):
        csvwriter.writerow([temp[i-1], temp[i], keff_values[i] - keff_values[i-1], ftc_values[i-1]])

print(f"FTC and Keff differences have been saved to {output_file_path}")

# Plotting the FTC values against fuel temperatures
plt.plot(temp[1:], ftc_values, marker='o')
plt.xlabel('Fuel Temperature (K)')
plt.ylabel('FTC')
plt.title('Fuel Temperature Coefficient (FTC) vs Temperature')
plt.grid(True)
plt.show()
