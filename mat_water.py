import os
import re
import numpy
from iapws import IAPWS97
from scrip_nuscale import*
#from scrip_nuscale_sbu import*
# Input enter proprieties temperature e pressure
temp = temp_mod

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
validated_temperature, is_valid = validate_temperature(temp)

# Get the isotopic suffix
isotopic_suffix = get_isotopic_suffix(validated_temperature)

# Atomic masses
H_mass = 1.007825032
O_mass = 15.99491462

# Search proprieties water in IAPWS97
water = IAPWS97(T=temp, P=pressure_mpa)
density=(water.rho/1000)

# Molar masses
H2O_molar_mass = 2*H_mass+O_mass
    
# Calculating the mass of hydrogen and oxygen in water
mass_H = 2 * H_mass * (1 / H2O_molar_mass)
mass_O = O_mass * (1 / H2O_molar_mass)
total_mass = mass_H + mass_O
mass_fraction_H = mass_H / total_mass
mass_fraction_O = mass_O / total_mass
    
# Output formatting
temp_string = f" temp {validated_temperature}" if not is_valid else ""
f=open("mat_water_"+str0(temp)+"K.inc", "w",encoding="utf-8")
f.write(f"% Water {density} g/cm3 \n")
f.write(f"mat water {-density} rgb 212 241 249 tmp {temp}\n")
f.write(f"H-1.{isotopic_suffix}\t\t {-mass_fraction_H:.5E} \n")
f.write(f"O-16.{isotopic_suffix}\t\t {-mass_fraction_O:.5E} \n")
f.write(f"therm lwtr lwe7.10t\n")
print(f"File mat_water"+str0(temp)+"K.inc generated with "+str(temp)+" K")
transfer_file(f"{filepath6}mat_water_"+str0(temp)+"K.inc", f"{filepath5}mat_water_"+str0(temp)+"K.inc")
if temp_string:
    print(f"File mat_water"+str0(temp)+"K.inc generated with "+str(temp)+" K")
