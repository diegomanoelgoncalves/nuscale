import random
import re
from scrip_nuscale_sbu import *

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
validated_temperature, is_valid = validate_temperature(temp_fuel)

# Get the isotopic suffix
isotopic_suffix = get_isotopic_suffix(validated_temperature)

# Enrichment of seed fuels %w.t UO2
files_seed = [
    ("suo_a01_" + str(temp_fuel) + "K.inc", enrich_sa01, -10.31), 
    ("suo_a02_" + str(temp_fuel) + "K.inc", enrich_sa02, -10.32), 
    ("suo_b01_" + str(temp_fuel) + "K.inc", enrich_sb01, -10.33),
    ("suo_b02_" + str(temp_fuel) + "K.inc", enrich_sb02, -10.34), 
    ("suo_c01_" + str(temp_fuel) + "K.inc", enrich_sc01, -10.35), 
    ("suo_c02_" + str(temp_fuel) + "K.inc", enrich_sc02, -10.36),
    ("suo_c03_" + str(temp_fuel) + "K.inc", enrich_sc03, -10.37)
]

# Enrichment of blanket fuels % UO2 + % ThO2
files_blank = [
    ("btho_a01_" + str(temp_fuel) + "K.inc", enrich_ba01, (100-enrich_sa01), -10.38), 
    ("btho_a02_" + str(temp_fuel) + "K.inc", enrich_ba02, (100-enrich_sa02), -10.39), 
    ("btho_b01_" + str(temp_fuel) + "K.inc", enrich_bb01, (100-enrich_sb01), -10.40),
    ("btho_b02_" + str(temp_fuel) + "K.inc", enrich_bb02, (100-enrich_sb02), -10.41), 
    ("btho_c01_" + str(temp_fuel) + "K.inc", enrich_bc01, (100-enrich_sc01), -10.42), 
    ("btho_c02_" + str(temp_fuel) + "K.inc", enrich_bc02, (100-enrich_sc02), -10.43),
    ("btho_c03_" + str(temp_fuel) + "K.inc", enrich_bc03, (100-enrich_sc03), -10.44)
]

# Adding suo_c02g material with Gd2O3
files_seed_with_gd = [
    ("suo_c02g_" + str(temp_fuel) + "K.inc", enrich_sc02, -10.36)
]

# Function to generate a random RGB color
def generate_random_color():
    return (random.randint(0, 240), random.randint(0, 240), random.randint(0, 240))

# Create colors for identification each material
colors = {file[0]: generate_random_color() for file in files_seed + files_blank + files_seed_with_gd}

# Calculation mass fraction of seed (UO2) materials
def cal_mass_fractions_seed(u235_percentage):
    U235_mass = 235.0439299
    U238_mass = 238.0507882
    O_mass = 15.99491462

    u238_percentage = 100 - u235_percentage

    molar_mass_UO2 = (u235_percentage / 100 * U235_mass + u238_percentage / 100 * U238_mass) + 2 * O_mass

    mass_U235 = (u235_percentage / 100) * U235_mass
    mass_U238 = (u238_percentage / 100) * U238_mass
    mass_O = 2 * O_mass

    mass_fraction_U235 = mass_U235 / molar_mass_UO2
    mass_fraction_U238 = mass_U238 / molar_mass_UO2
    mass_fraction_O = mass_O / molar_mass_UO2

    return mass_fraction_U235, mass_fraction_U238, mass_fraction_O

# Calculation mass fraction of blanket (U,Th)O2 materials
def calc_mass_frac_blank(u_percentage, th_percentage):
    U235_mass = 235.0439299
    U238_mass = 238.0507882
    Th232_mass = 232.0380553
    O16_mass = 15.99491462

    natural_u235_fraction = 0.2
    natural_u238_fraction = 0.8

    u_total_mass = U235_mass * natural_u235_fraction + U238_mass * natural_u238_fraction
    total_oxygen_mass = 2 * O16_mass

    molar_mass_UThO2 = (u_percentage / 100 * u_total_mass + th_percentage / 100 * Th232_mass) + total_oxygen_mass

    molar_fraction_U235 = (u_percentage / 100) * natural_u235_fraction * U235_mass / molar_mass_UThO2
    molar_fraction_U238 = (u_percentage / 100) * natural_u238_fraction * U238_mass / molar_mass_UThO2
    molar_fraction_Th232 = (th_percentage / 100) * Th232_mass / molar_mass_UThO2
    molar_fraction_O16 = total_oxygen_mass / molar_mass_UThO2

    return molar_fraction_U235, molar_fraction_U238, molar_fraction_Th232, molar_fraction_O16

# Gd2O3 isotopic composition
O_mass = 15.99491462
Gd_mass = 155.9221312

Gd2O3 = (2 * Gd_mass + 3 * O_mass)

gd_isotopes = {
    "Gd-152": (0.20) * (151.9197995 / Gd2O3),
    "Gd-154": (2.18) * (153.9208741 / Gd2O3),
    "Gd-155": (14.80) * (154.9226305 / Gd2O3),
    "Gd-156": (20.47) * (155.9221312 / Gd2O3),
    "Gd-157": (15.65) * (156.9239686 / Gd2O3),
    "Gd-158": (24.84) * (157.9241123 / Gd2O3),
    "Gd-160": (21.86) * (159.9270624 / Gd2O3)
}

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
    total_mass = molar_mass_UO2 + (gd_fraction / 100 * total_mass_Gd2O3)

    mass_fraction_U235 = mass_U235 / total_mass
    mass_fraction_U238 = mass_U238 / total_mass
    mass_fraction_O = mass_O / total_mass

    mass_fractions_Gd = {iso: (gd_isotopes[iso] * (gd_fraction / 100)) / total_mass for iso in gd_isotopes}

    return mass_fraction_U235, mass_fraction_U238, mass_fraction_O, mass_fractions_Gd


# Function to clean the name inside the file
def clean_content_name(content):
    cleaned_content = re.sub(r'_\d+K', '', content)
    cleaned_content = cleaned_content.replace(".inc", "")  # Remove .inc from the name
    return cleaned_content

# Loop materials of density and enrichment
for file, u235_percentage, density in files_seed:
    mass_fraction_U235, mass_fraction_U238, mass_fraction_O = cal_mass_fractions_seed(u235_percentage)
    with open(file, "w", encoding="utf-8") as f:
        content_name = clean_content_name(file.replace('.inc.c', ''))
        temp_string = f" temp {validated_temperature}" if not is_valid else ""
        f.write(f" % Fuel Seed UO2 %w.t  \n")
        f.write(f"mat {content_name} {density:.2f} burn 1{temp_string} \n")
        f.write(f"U-235.{isotopic_suffix}\t{-mass_fraction_U235:.8f}\n")
        f.write(f"U-238.{isotopic_suffix}\t{-mass_fraction_U238:.8f}\n")
        f.write(f"O-16.{isotopic_suffix}\t{-mass_fraction_O:.8f}\n")

for file, u_percentage, th_percentage, density in files_blank:
    molar_fraction_U235, molar_fraction_U238, molar_fraction_Th232, molar_fraction_O16 = calc_mass_frac_blank(u_percentage, th_percentage)
    with open(file, "w", encoding="utf-8") as f:
        content_name = clean_content_name(file.replace('.inc.c', ''))
        temp_string = f" temp {validated_temperature}" if not is_valid else ""
        f.write(f" % Fuel Blanket UO2+ThO2 %w.t  \n")
        f.write(f"mat {content_name} {density:.2f} burn 1{temp_string} \n")
        f.write(f"U-235.{isotopic_suffix}\t{-molar_fraction_U235:.8f}\n")
        f.write(f"U-238.{isotopic_suffix}\t{-molar_fraction_U238:.8f}\n")
        f.write(f"Th-232.{isotopic_suffix}\t{-molar_fraction_Th232:.8f}\n")
        f.write(f"O-16.{isotopic_suffix}\t{-molar_fraction_O16:.8f}\n")

# Loop for suo_c02g material with Gd2O3

for base_file, u235_percentage, density in files_seed_with_gd:
    # Remove extra temperature and .inc addition
    file = f"{base_file}"  # Use the base file name directly
    mass_fraction_U235, mass_fraction_U238, mass_fraction_O, mass_fractions_Gd = cal_mass_fractions_seed_with_gd(u235_percentage, gd_fraction)
    
    with open(file, "w", encoding="utf-8") as f:
        color = colors[base_file]
        content_name = clean_content_name(base_file.replace('.inc', ''))
        temp_string = f" temp {validated_temperature}" if not is_valid else ""
        f.write(f"% UO2 + {gd_fraction} Gd2O3 \n")
        f.write(f"mat {content_name} {density:.4f} rgb {color[0]} {color[1]} {color[2]} burn 1{temp_string} \n")
        f.write(f"U-235.{isotopic_suffix}\t{-mass_fraction_U235:.8f}\n")
        f.write(f"U-238.{isotopic_suffix}\t{-mass_fraction_U238:.8f}\n")
        f.write(f"O-16.{isotopic_suffix}\t{-mass_fraction_O:.8f}\n")
        for iso, fraction in mass_fractions_Gd.items():
            f.write(f"{iso}.{isotopic_suffix}\t{-fraction:.8f}\n")

print("Files created successfully.")

transfer_file(f"{filepath6}suo_a01_{temp_fuel}K.inc", f"{filepath5}suo_a01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}suo_a02_{temp_fuel}K.inc", f"{filepath5}suo_a02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}suo_b01_{temp_fuel}K.inc", f"{filepath5}suo_b01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}suo_b02_{temp_fuel}K.inc", f"{filepath5}suo_b02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}suo_c01_{temp_fuel}K.inc", f"{filepath5}suo_c01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}suo_c02_{temp_fuel}K.inc", f"{filepath5}suo_c02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}suo_c02g_{temp_fuel}K.inc", f"{filepath5}suo_c02g_{temp_fuel}K.inc")
transfer_file(f"{filepath6}suo_c03_{temp_fuel}K.inc", f"{filepath5}suo_c03_{temp_fuel}K.inc")
transfer_file(f"{filepath6}btho_a01_{temp_fuel}K.inc", f"{filepath5}btho_a01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}btho_a02_{temp_fuel}K.inc", f"{filepath5}btho_a02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}btho_b01_{temp_fuel}K.inc", f"{filepath5}btho_b01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}btho_b02_{temp_fuel}K.inc", f"{filepath5}btho_b02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}btho_c01_{temp_fuel}K.inc", f"{filepath5}btho_c01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}btho_c02_{temp_fuel}K.inc", f"{filepath5}btho_c02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}btho_c03_{temp_fuel}K.inc", f"{filepath5}btho_c03_{temp_fuel}K.inc")