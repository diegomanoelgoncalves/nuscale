import random
import os
import re 
import matplotlib.pyplot as plt
from iapws import IAPWS97
from scrip_nuscale import*
#from scrip_nuscale_sbu import*

inlet_temperature=temp_mod
# Create water instance at specified temperature and pressure
water = IAPWS97(T=temp_mod, P=pressure_mpa)

# Get the density in kg/m3
density = water.rho
# Define the temperature ranges and corresponding isotopic names
temperature_ranges = [300, 600, 900, 1200, 1500, 1800]
isotopic_suffixes = {
    300: "03c",
    600: "06c",
    900: "09c",
    1200: "12c",
    1500: "15c",
    1800: "18c"
}

# Function to get the isotopic suffix based on temperature
def get_isotopic_suffix(temp):
    closest_temp = max([t for t in temperature_ranges if t <= temp], default=300)
    return isotopic_suffixes[closest_temp]

# Function to validate temperature
def validate_temperature(temp):
    if temp not in temperature_ranges:
        return temp, False  # Return the temperature and a flag indicating it is out of range
    return temp, True

# Validate the inlet temperature
validated_temperature, is_valid = validate_temperature(inlet_temperature)

# Get the isotopic suffix
isotopic_suffix = get_isotopic_suffix(validated_temperature)

# Calculate the density of water at the given temperature using IAPWS
water_props = IAPWS97(T=validated_temperature - 273.15, P=0.1)  # Pressure in MPa, adjust as necessary
density_H2O = (water_props.rho/1000)  # Density in kg/m^3

# Definition of atomic masses
H_mass = 1.007825032
O_mass = 15.99491462
B10_mass = 10.01293686
B11_mass = 11.00930517

# Definition of boron isotopic abundances
B10_abundance = 19.10 / 100
B11_abundance = 80.90 / 100  # Correction of value to 80.90%

# Definition of molar masses
H2O_molar_mass = 18.01056468
H3BO3_molar_mass = 61.81931895

# Density of solutions
density_H3BO3 = 1.44  # g/cm^3
density_solution = 1.0022  # g/cm^3

# Calculation of the mass of solution in 1 liter (considering solution density)
mass_solution = 1000 * density_solution  # g

# Boron concentration in grams per liter
mass_boron = (boron_ppm / 1e6) * mass_solution  # g

# Concentration of H3BO3 required to provide the amount of boron
mass_H3BO3 = mass_boron / (B10_abundance * B10_mass / H3BO3_molar_mass + B11_abundance * B11_mass / H3BO3_molar_mass)

# Amount of B10 and B11 present
mass_B10 = mass_H3BO3 * (B10_abundance * B10_mass / H3BO3_molar_mass)
mass_B11 = mass_H3BO3 * (B11_abundance * B11_mass / H3BO3_molar_mass)

# Amount of water remaining in the solution
mass_water = mass_solution - mass_H3BO3

# Calculating the mass of hydrogen and oxygen in water and in H3BO3
mass_H = (2 * H_mass * (mass_water / H2O_molar_mass)) + (3 * H_mass * (mass_H3BO3 / H3BO3_molar_mass))
mass_O = (O_mass * (mass_water / H2O_molar_mass)) + (3 * O_mass * (mass_H3BO3 / H3BO3_molar_mass))

# Calculating the mass fraction of each component
total_mass = mass_H + mass_O + mass_B10 + mass_B11
mass_fraction_H = mass_H / total_mass
mass_fraction_O = mass_O / total_mass
mass_fraction_B10 = mass_B10 / total_mass
mass_fraction_B11 = mass_B11 / total_mass

# Output formatting
temp_string = f" temp {validated_temperature}" if not is_valid else ""
f=open(f"mat_water_"+str(boron_ppm)+"ppm_"+str(temp_mod)+"K.inc", "w",encoding="utf-8")
f.write(f"% Water + Boron solution "+str(boron_ppm)+" \n")
f.write(f"mat water {-density_H2O} rgb 128 197 222 \n")
f.write(f"H-1.{isotopic_suffix}\t {-mass_fraction_H:.5E} \n")
f.write(f"O-16.{isotopic_suffix}\t {-mass_fraction_O:.5E} \n")
f.write(f"B-10.{isotopic_suffix}\t {-mass_fraction_B10:.5E} \n")
f.write(f"B-11.{isotopic_suffix}\t {-mass_fraction_B11:.5E} \n")
f.write(f"therm lwtr lwe7.00t\n")
if temp_string:
    print(f"{temp_string}")
