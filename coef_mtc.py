import os
import numpy as np
from matplotlib import pyplot as plt
import serpentTools
from serpentTools.settings import rc
import csv

# Configure Serpent version
rc['serpentVersion'] = '2.1.30'

# File number list and corresponding moderator temperatures (in Kelvin)
numbers = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
temp_mod = [221, 226, 232, 237, 243, 248, 254, 260, 265, 271, 276, 282, 287]  # in Kelvin

# Initialize lists to store keff values and MTC results
keff_values = []
mtc_values = []

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

# Calculate the MTC values between successive moderator temperatures
for i in range(1, len(keff_values)):
    delta_keff = keff_values[i] - keff_values[i-1]
    delta_temp_mod = temp_mod[i] - temp_mod[i-1]
    mtc = delta_keff / delta_temp_mod
    mtc_values.append(mtc)

# Define the output file path
output_file_path = 'mtc_keff_results.csv'

# Save MTC values to a CSV file
with open(output_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Temp_Mod_1', 'Temp_Mod_2', 'Keff_Diff', 'MTC'])
    for i in range(1, len(mtc_values)):
        csvwriter.writerow([temp_mod[i-1], temp_mod[i], keff_values[i] - keff_values[i-1], mtc_values[i-1]])

print(f"MTC and Keff differences have been saved to {output_file_path}")

# Plotting the MTC values against moderator temperatures
plt.plot(temp_mod[1:], mtc_values, marker='o')
plt.xlabel('Moderator Temperature (K)')
plt.ylabel('MTC')
plt.title('Moderator Temperature Coefficient (MTC) vs Temperature')
plt.grid(True)
plt.show()
