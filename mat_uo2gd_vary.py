import numpy as np
import re
import random
from collections import defaultdict
from scrip_nuscale import *
from mat_uo2gd import *

# Extracted data points from the graph (Temperature in K, Density in Mg/m³)
data = [
    (300, 10.8), (600, 10.6), (900, 10.4), (1200, 10.2), (1500, 10.0),
    (1800, 9.8), (2100, 9.6), (2400, 9.4), (2700, 9.2), (3000, 9.0)
]

# Convert data to numpy arrays
temperatures, densities = zip(*data)
temperatures = np.array(temperatures)
densities = np.array(densities)

# Fit a polynomial to the data
coefficients = np.polyfit(temperatures, densities, 2)  # Second-degree polynomial
poly = np.poly1d(coefficients)

def density_function(temp):
    return poly(temp)

# Define a function to shift the polynomial to start at 10.39 at 300K
def shifted_density_function(temp):
    shift = 10.39 - poly(300)
    return poly(temp) + shift

# Gadolinium parameters
Gd_mass = 155.9221312
O_mass = 15.99491462
Gd2O3 = (2 * Gd_mass + 3 * O_mass)

# Gd2O3 isotopic composition
gd_isotopes = {
    "Gd-152": 0.0020 * (151.9197995 / Gd2O3),
    "Gd-154": 0.0218 * (153.9208741 / Gd2O3),
    "Gd-155": 0.1480 * (154.9226305 / Gd2O3),
    "Gd-156": 0.2047 * (155.9221312 / Gd2O3),
    "Gd-157": 0.1565 * (156.9239686 / Gd2O3),
    "Gd-158": 0.2484 * (157.9241123 / Gd2O3),
    "Gd-160": 0.2186 * (159.9270624 / Gd2O3)
}

# Materials and their corresponding color codes and enrichment percentages
materials = {
    "uo_a01": {"color": "rgb 250 165 0", "enrichment": enr_a01},
    "uo_a02": {"color": "rgb 250 215 0", "enrichment": enr_a02},
    "uo_b01": {"color": "rgb 255 0 0", "enrichment": enr_b01},
    "uo_b02": {"color": "rgb 255 228 181", "enrichment": enr_b02},
    "uo_c01": {"color": "rgb 0 0 128", "enrichment": enr_c01},
    "uo_c02": {"color": "rgb 30 144 255", "enrichment": enr_c02},
    "uo_c03": {"color": "rgb 135 206 250", "enrichment": enr_c03}
}

# Function to parse the isotope data from text
def parse_isotope_data(raw_data):
    isotope_dict = defaultdict(dict)
    lines = raw_data.strip().split('\n')
    for line in lines[1:]:  # Skip the header if there is one
        parts = re.split(r'\|\s*', line.strip())
        if len(parts) >= 4:
            element_mass = parts[1].split('-')
            if len(element_mass) == 2:
                element, mass_number = element_mass[0].strip(), element_mass[1].strip()
                try:
                    mass = float(parts[2].strip())
                    abundance = float(parts[3].strip())
                except ValueError:
                    continue  # Ignore lines where conversion to float fails
                isotope_dict[element][f"{element}-{mass_number}"] = (mass, abundance)
    return isotope_dict

# Read and parse isotope data
with open('isotope_abundances.py', 'r') as file:
    isotope_abundances_content = file.read()
isotope_data = parse_isotope_data(isotope_abundances_content)

# Adjust the isotope abundances for the target isotope
def adjust_isotope_abundances(data, element, isotope, percentage):
    total_abundance = sum([info[1] for info in data[element].values()])
    remaining_abundance = total_abundance - percentage
    for iso in data[element]:
        if iso == isotope:
            data[element][iso] = (data[element][iso][0], percentage)
        else:
            data[element][iso] = (data[element][iso][0], data[element][iso][1] * (remaining_abundance / (total_abundance - data[element][isotope][1])))

# Functions for parsing formulas and calculating masses
def parse_chemical_formula(formula):
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    formula_dict = {element: int(count) if count else 1 for element, count in elements}
    return formula_dict

def calculate_molecular_mass(formula_dict):
    total_mass = 0
    for element, count in formula_dict.items():
        for isotope, (mass, abundance) in isotope_data[element].items():
            total_mass += mass * abundance * count
    return total_mass

def calculate_isotope_mass_fractions(formula_dict, total_mass):
    isotope_mass_fractions = defaultdict(float)
    for element, count in formula_dict.items():
        for isotope, (mass, abundance) in isotope_data[element].items():
            isotope_mass_fractions[isotope] += mass * abundance * count / total_mass
    return isotope_mass_fractions

# Calculation mass fraction of seed (UO2 + Gd2O3) materials
def cal_mass_fractions_seed_with_gd(u235_percentage, gd_fraction):
    U235_mass = 235.0439299
    U238_mass = 238.0507882
    O_mass = 15.99491462

    u238_percentage = 100 - u235_percentage
    molar_mass_UO2 = (u235_percentage / 100 * U235_mass + u238_percentage / 100 * U238_mass) + 2 * O_mass

    mass_U235 = (u235_percentage / 100) * U235_mass
    mass_U238 = (u238_percentage / 100) * U238_mass
    mass_O = 2 * O_mass

    total_mass_Gd2O3 = sum(gd_isotopes[iso] for iso in gd_isotopes)
    total_mass = molar_mass_UO2 + (gd_fraction * total_mass_Gd2O3)

    mass_fraction_U235 = mass_U235 / total_mass
    mass_fraction_U238 = mass_U238 / total_mass
    mass_fraction_O = mass_O / total_mass

    mass_fractions_Gd = {iso: (gd_isotopes[iso] * gd_fraction) / total_mass for iso in gd_isotopes}

    return mass_fraction_U235, mass_fraction_U238, mass_fraction_O, mass_fractions_Gd

# Function to get the isotopic suffix based on temperature
def get_isotopic_suffix(temp):
    temperature_ranges = [300, 600, 900, 1200, 1500, 1800]
    isotopic_suffixes = {
        300: "03c",
        600: "06c",
        900: "09c",
        1200: "12c",
        1500: "15c",
        1800: "18c"
    }
    closest_temp = max([t for t in temperature_ranges if t <= temp], default=300)
    return isotopic_suffixes[closest_temp]

# Function to check if a temperature is in the predefined list
def is_predefined_temperature(temp):
    return temp in [300, 600, 900, 1200, 1500, 1800]

# Loop through each material to create corresponding files
inlet_temperatures = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800]  # New temperature ranges

gd_fraction = 0.03  # Example Gd fraction, can be adjusted

for temp in inlet_temperatures:
    for name, properties in materials.items():
        color = properties["color"]
        enrichment = properties["enrichment"]
        
        if name == "uo_c02":
            # Create both uo_c02 and uo_c02g files
            for suffix in ["", "g"]:
                filename = f"{name}{suffix}_{temp}K.inc"
                mass_fraction_U235, mass_fraction_U238, mass_fraction_O, mass_fractions_Gd = cal_mass_fractions_seed_with_gd(enrichment * 100, gd_fraction)
                density_value = density_function(temp)

                # Writing to the file
                with open(filename, "w", encoding="utf-8") as f:
                    temp_string = f" tmp {temp}" if not is_predefined_temperature(temp) else ""
                    f.write(f"% Fuel material UO2 + Gd2O3 {temp}K {density_value:.2f}g/cm3 \n")
                    f.write(f"mat {name}{suffix} {-density_value:.2f} {color} burn 1{temp_string} \n")
                    f.write(f"U-235{get_isotopic_suffix(temp)} -{mass_fraction_U235:.5f}\n")
                    f.write(f"U-238{get_isotopic_suffix(temp)} -{mass_fraction_U238:.5f}\n")
                    f.write(f"O-16{get_isotopic_suffix(temp)} -{mass_fraction_O:.5f}\n")
                    for iso, fraction in mass_fractions_Gd.items():
                        f.write(f"{iso}{get_isotopic_suffix(temp)} -{fraction:.5f}\n")
                print(f"File {filename} created successfully.")
        else:
            # Create the other material files
            filename = f"{name}_{temp}K.inc"
            adjust_isotope_abundances(isotope_data, 'U', 'U-235', enrichment)
            formula_dict = parse_chemical_formula('UO2')  # Assuming UO2 as the formula for others
            total_mass = calculate_molecular_mass(formula_dict)
            isotope_mass_fractions = calculate_isotope_mass_fractions(formula_dict, total_mass)
            density_value = density_function(temp)

            # Writing to the file
            with open(filename, "w", encoding="utf-8") as f:
                temp_string = f" tmp {temp}" if not is_predefined_temperature(temp) else ""
                f.write(f"% Fuel material UO2 {temp}K {density_value:.2f}g/cm3 \n")
                f.write(f"mat {name} {-density_value:.2f} {color} burn 1{temp_string} \n")
                for isotope, mass_fraction in isotope_mass_fractions.items():
                    isotopic_suffix = get_isotopic_suffix(temp)
                    output_line = f"{isotope}.{isotopic_suffix} -{mass_fraction:.5f}\n"
                    f.write(output_line)
                    print(output_line.strip())
            print(f"File {filename} created successfully.")

print("All files created successfully.")
