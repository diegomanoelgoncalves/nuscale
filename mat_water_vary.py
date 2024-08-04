import os
import numpy
from iapws import IAPWS97

# Input properties
pressure_mpa = 12.755

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

# Atomic masses
H_mass = 1.007825032
O_mass = 15.99491462

# Molar masses
H2O_molar_mass = 2 * H_mass + O_mass

# Temperatures to generate files for
temperatures = [221, 226, 232, 237, 243, 248, 254,260 , 265, 271, 276,282 , 287]

# Function to validate temperature
def validate_temperature(temp):
    if temp not in temperature_ranges:
        return temp, False  # Return the temperature and a flag indicating it is out of range
    return temp, True

# Generate files for each temperature
for temperature in temperatures:
    temp_k = temperature + 273.15  # Convert to Kelvin

    # Validate the inlet temperature
    validated_temperature, is_valid = validate_temperature(temp_k)

    # Get the isotopic suffix
    isotopic_suffix = get_isotopic_suffix(validated_temperature)

    # Search properties of water using IAPWS97
    water = IAPWS97(T=temp_k, P=pressure_mpa)
    density = (water.rho / 1000)  # Convert density to g/cm³

    # Calculating the mass of hydrogen and oxygen in water
    mass_H = 2 * H_mass * (1 / H2O_molar_mass)
    mass_O = O_mass * (1 / H2O_molar_mass)
    total_mass = mass_H + mass_O
    mass_fraction_H = mass_H / total_mass
    mass_fraction_O = mass_O / total_mass

    # Output formatting
    temp_string = f" temp {validated_temperature}" if not is_valid else ""
    file_name = f"mat_water_{temp_k:.0f}K.inc"
    with open(file_name, "w",encoding="utf-8") as f:
        f.write(f"% Water {density:.5E} g/cm^3\n")
        f.write(f"mat water {-density:.5E} rgb 212 241 249 tmp {temp_k}\n")
        f.write(f"H-1.{isotopic_suffix}\t\t {-mass_fraction_H:.5E}\n")
        f.write(f"O-16.{isotopic_suffix}\t\t {-mass_fraction_O:.5E}\n")
        f.write(f"therm lwtr lwe7.00t\n")

    if temp_string:
        print(f"File {file_name} generated with {temperature} K")
