import re
from collections import defaultdict
import random
from scrip_nuscale import*

# Other parameters
density = 10.43
formula = "UO2"
target_isotope = "U-235"
temperature = f"{temp_fuel}K"  # Kelvin

# Gadolinium parameters
Gd_mass = 155.9221312
O_mass = 15.99491462
Gd2O3 = (2 * Gd_mass + 3 * O_mass)

# Gd2O3 isotopic composition
gd_isotopes = {
    "Gd-152": (0.20) * (151.9197995 / Gd2O3),
    "Gd-154": (2.18) * (153.9208741 / Gd2O3),
    "Gd-155": (14.80) * (154.9226305 / Gd2O3),
    "Gd-156": (20.47) * (155.9221312 / Gd2O3),
    "Gd-157": (15.65) * (156.9239686 / Gd2O3),
    "Gd-158": (24.84) * (157.9241123 / Gd2O3),
    "Gd-160": (21.86) * (159.9270624 / Gd2O3)
}

# Materials and their corresponding color codes and enrichment percentages
materials = {
    "uo_a01": {"color": "rgb 250 165 0", "enrichment":enr_a01},
    "uo_a02": {"color": "rgb 250 215 0", "enrichment": enr_a02},
    "uo_b01": {"color": "rgb 252 0 0", "enrichment": enr_b01},
    "uo_b02": {"color": "rgb 252 228 181", "enrichment": enr_b02},
    "uo_c01": {"color": "rgb 0 0 128", "enrichment": enr_c01},
    "uo_c02g": {"color": "rgb 130 0 50", "enrichment": enr_c02},
    "uo_c02": {"color": "rgb 30 144 250", "enrichment": enr_c02},
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
with open('/home/diego/Principal/input_serpent/isotope_abundances.py', 'r') as file:
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
# Function to calculate mass fractions of UO2 and Gd2O3
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


# Format the temperature for the filename
def format_temperature_for_filename(temperature):
    numeric_temp = int(temperature[:-1])  # Assume that the temperature ends with 'K'
    temp_prefix = numeric_temp // 100
    return f".{temp_prefix:02}c"

# Loop through each material to create corresponding files
for name, properties in materials.items():
    color = properties["color"]
    enrichment = properties["enrichment"]
    filename = f"{name}_{temperature}.inc"
    
    if "uo_c02g" in name:  # Include Gd for specific material
        mass_fraction_U235, mass_fraction_U238, mass_fraction_O, mass_fractions_Gd = cal_mass_fractions_seed_with_gd(enrichment * 100, gd_fraction)
    else:
        adjust_isotope_abundances(isotope_data, 'U', target_isotope, enrichment)
        formula_dict = parse_chemical_formula(formula)
        total_mass = calculate_molecular_mass(formula_dict)
        isotope_mass_fractions = calculate_isotope_mass_fractions(formula_dict, total_mass)
    
    # Writing to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write("% Fuel material " + str(formula) + " " + str(-density) + "g/cm3 \n")
        f.write("mat " + str(name) + " " + str(-density) + " " + str(color) + " burn 1 \n")
        if "uo_c02g" in name:
            f.write(f"U-235{format_temperature_for_filename(temperature)} -{mass_fraction_U235:.5f}\n")
            f.write(f"U-238{format_temperature_for_filename(temperature)} -{mass_fraction_U238:.5f}\n")
            f.write(f"O-16{format_temperature_for_filename(temperature)} -{mass_fraction_O:.5f}\n")
            for iso, fraction in mass_fractions_Gd.items():
                f.write(f"{iso}{format_temperature_for_filename(temperature)} -{fraction:.5f}\n")
        else:
            for isotope, mass_fraction in isotope_mass_fractions.items():
                temp_prefix = format_temperature_for_filename(temperature)
                output_line = f"{isotope}{temp_prefix} -{mass_fraction:.8f}\n"
                f.write(output_line)
                print(output_line.strip())
        print("\n")

transfer_file(f"{filepath6}uo_a01_{temp_fuel}K.inc", f"{filepath5}uo_a01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}uo_a02_{temp_fuel}K.inc", f"{filepath5}uo_a02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}uo_b01_{temp_fuel}K.inc", f"{filepath5}uo_b01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}uo_b02_{temp_fuel}K.inc", f"{filepath5}uo_b02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}uo_c01_{temp_fuel}K.inc", f"{filepath5}uo_c01_{temp_fuel}K.inc")
transfer_file(f"{filepath6}uo_c02_{temp_fuel}K.inc", f"{filepath5}uo_c02_{temp_fuel}K.inc")
transfer_file(f"{filepath6}uo_c02g_{temp_fuel}K.inc", f"{filepath5}uo_c02g_{temp_fuel}K.inc")
transfer_file(f"{filepath6}uo_c03_{temp_fuel}K.inc", f"{filepath5}uo_c03_{temp_fuel}K.inc")
