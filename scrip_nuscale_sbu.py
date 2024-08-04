import math
import random
import shutil
import os
import numpy as np
import csv

# Biblioteca da seção de choque
'''
filepath1 = "/home/diego/Principal/Serpent/xs/sss_endfb7u.xsdata"
filepath2 = "/home/diego/Principal/Serpent/xs/sss_endfb7.dec"
filepath3 = "/home/diego/Principal/Serpent/xs/sss_endfb7.nfy"
filepath1 "/home/users/diegogoncalves/Serpent2/xs/sss_endfb7u.xsdata"
filepath2 "/home/users/diegogoncalves/Serpent2/xs/sss_endfb7.dec"
filepath3 "/home/users/diegogoncalves/Serpent2/xs/sss_endfb7.nfy"
filepath1 = "/home/diego-lenovo/principal/Serpent/xs/sss_endfb7u.xsdata"
filepath2 = "/home/diego-lenovo/principal/Serpent/xs/sss_endfb7.dec"
filepath3 = "/home/diego-lenovo/principal/Serpent/xs/sss_endfb7.nfy"
'''

filepath1= "/home/users/diegogoncalves/Serpent2/xs/sss_endfb7u.xsdata"
filepath2= "/home/users/diegogoncalves/Serpent2/xs/sss_endfb7.dec"
filepath3= "/home/users/diegogoncalves/Serpent2/xs/sss_endfb7.nfy"
filepath4 = "include"
filepath5 = "/home/diego/Principal/"
filepath6 = "/home/diego/Principal/"


# Parâmetros neutronicos do modelo
power =160000000
bc = 1
pop = 100000
cyc = 1000
incyc = 100
parts = 50
days=[0.1,1,2,3,5,7,14,21,30,60,90,120,180,240,300,360,420,480,540,600,660,720,780,840]
ind = 4

################## Parâmetros variáveis #################
pressure_mpa = 12.7553
# Boron concentration in ppm
boron_ppm = 1000
# Temperaturas de entrada
temp_mod=600
temp_fuel=900

# Enriquecimentos seed
enrich_sa01 = 17
enrich_sa02 = 17.10
enrich_sb01 = 17.98
enrich_sb02 = 18.08
enrich_sc01 = 19.51
enrich_sc02 = 20
enrich_sc03 = 18.08
# Enriquecimentos blanket
enrich_ba01 = 14
enrich_ba02 = 15.16
enrich_bb01 = 15.64
enrich_bb02 = 16.80
enrich_bc01 = 18.18
enrich_bc02 = 19
enrich_bc03 = 16.80
# Fração w.t% Gd
gd_fraction = 16.0
# Distribuição de Gd/ oitavo
Gd_per_eighth = 3
S2_per_eighth = 3  

# Altura total
total_heigth = 243.561

length_blank = 21.50

length_seed = 10.145
# Diâmetro da vareta combustível físsil (UO2)
radius_seed = 0.26510

# Diâmetro da vareta combustível físsil (U,Th)O2
radius_blank = 0.40521

# Número de varetas de seed
number_seed = 13

# Número de varetas de blank
number_blank = 19

# Passo do seed
pitch_seed = (length_seed/number_seed)

# Passo do blank
pitch_blank = (length_blank/number_blank)

# Altura ativa da parte UOX ou UThOX
heigth_active = 200.000

##### Parâmetros fixos das barras de controle ####
diameter_seed=2*radius_seed
diameter_blank=2*radius_blank

gap_s=0.00825
clad_s=0.06096

gap_b=0.00825
clad_b=0.06096

# Espessura suporte superior
top_nozzle = 9.020  # fixo

# Espaçamento de entrada de água
coolant = 8.481  # fixo

# Fim do pino
end_cap = 1.205  # fixo

# Tamanho das molas
plenum_spring = 13.490  # fixo

# Dimensão da mola teórica
spring = 0.0646  # fixo

# Espessura do suporte inferior
bottom_nozzle = 10.160  # fixo

# Número de assemblies
number_assembly = 7  # fixo

# Região vazia da barra de controle
empty_guide = 8.386  # fixo

# Fim da barra de controle
end_plug = 4.859  # fixo

# Tamanho da região de AgInCd
length_aic = 30.480  # fixo

# Comprimento da barra de controle B4C
length_b4c = 157.480  # fixo

# Parte superior da mola da barra de controle
upper_plenum = 23.176  # fixo

# Raio da barra de controle AIC
radius_aic = radius_seed + 0.0215  # fixo

# Raio da barra de controle B4C
radius_b4c = radius_seed + 0.0215  # fixo

# Raio do revestimento da barra de controle B4C
radius_bar = radius_seed + 0.0787  # fixo

# Verificação para pitch_seed e radius_seed
ratio_seed = pitch_seed / (2 * (radius_seed + gap_s + clad_s))

# Verificação para pitch_blank e radius_blank
ratio_blank = pitch_blank / (2 * (radius_blank + gap_b + clad_b))

# Funções para matrizes
def rg(num):
    if num % 2 == 0:
        return range(-num // 2, num // 2)
    else:
        return range(-num // 2 + 1, num // 2 + 1)

def rm(num):
    if num % 2 == 0:
        return str1(-num // 2) + ":" + str1((num // 2) - 1)
    else:
        return str1(-num // 2 + 1) + ":" + str1(num // 2)

def str0(nl):
    return "{:.0f}".format(nl)
def str_(nl):
    return "{:.4f}".format(nl)

def str1(nl):
    return "{:.3f}".format(nl)

def str2(nl):
    return "{:.2f}".format(nl)

# Transfer file to destination folder
def transfer_file(src_path, dest_path):
    try:
        if not os.path.isfile(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

        if os.path.isdir(dest_path):
            dest_file_path = os.path.join(dest_path, os.path.basename(src_path))
        else:
            dest_file_path = dest_path

        shutil.move(src_path, dest_file_path)
        print(f"File transferred from {src_path} to {dest_file_path}")
    except Exception as e:
        print(f"Error: {e}")

def verificar_paridade(numero):
    if numero % 2 == 0:
        return f"{numero} é par."
    else:
        return f"{numero} é ímpar."
    
# Gera as posições para o gadolínio
def generate_positions(mid_point, Gd_per_octant):
    positions = set()
    while len(positions) < Gd_per_octant:
        rand_x = random.randint(0, mid_point - 1)
        rand_y = random.randint(0, mid_point - 1)
        positions.add((rand_x, rand_y))
    return positions
def generate_positions2(mid_point, elements_per_octant, excluded_positions=None):
    positions = set()
    while len(positions) < elements_per_octant:
        rand_x = random.randint(0, mid_point - 1)
        rand_y = random.randint(0, mid_point - 1)
        if excluded_positions is None or (rand_x, rand_y) not in excluded_positions:
            positions.add((rand_x, rand_y))
    return positions
# Gera a matrix com um padrão específico de distribuição do gadolínio
def gen_pattern_gd(Ns, Gd_positions, G_value, S_value):
    adjusted_Ns = Ns
    matrix = np.full((adjusted_Ns, adjusted_Ns), S_value)
    mid_point = adjusted_Ns // 2

    for pos in Gd_positions:
        x, y = pos
        # Primeiro oitavo (superior esquerdo)
        matrix[x, y] = G_value
        # Segundo oitavo (superior centro-esquerdo, espelhado no eixo y do primeiro)
        matrix[y, x] = G_value
        # Terceiro oitavo (superior centro-direito, espelhado no eixo y do segundo)
        matrix[y, adjusted_Ns - 1 - x] = G_value
        # Quarto oitavo (superior direito, espelhado no eixo y do terceiro)
        matrix[x, adjusted_Ns - 1 - y] = G_value
        # Quinto oitavo (inferior direito, espelhado no eixo x do quarto)
        matrix[adjusted_Ns - 1 - x, adjusted_Ns - 1 - y] = G_value
        # Sexto oitavo (inferior centro-direito, espelhado no eixo y do quinto)
        matrix[adjusted_Ns - 1 - y, adjusted_Ns - 1 - x] = G_value
        # Sétimo oitavo (inferior centro-esquerdo, espelhado no eixo y do sexto)
        matrix[adjusted_Ns - 1 - y, x] = G_value
        # Oitavo oitavo (inferior esquerdo, espelhado no eixo y do sétimo)
        matrix[adjusted_Ns - 1 - x, y] = G_value

    if Ns % 2 != 0:
        center = Ns // 2
        for i in range(adjusted_Ns):
            matrix[center, i] = S_value
            matrix[i, center] = S_value

    matrix_string = ""
    for i in range(adjusted_Ns):
        matrix_string += "       "
        for j in range(adjusted_Ns):
            matrix_string += matrix[i, j] + " "
        matrix_string += "\n"
    matrix_string += "\n"

    return matrix_string

def gen_pattern_gd2(Ns, Gd_positions, S_positions, G_value, S1_value, S2_value):
    adjusted_Ns = Ns
    matrix = np.full((adjusted_Ns, adjusted_Ns), S1_value)
    mid_point = adjusted_Ns // 2

    # Distribuição do gadolínio (G_value)
    for pos in Gd_positions:
        x, y = pos
        matrix[x, y] = G_value
        matrix[y, x] = G_value
        matrix[y, adjusted_Ns - 1 - x] = G_value
        matrix[x, adjusted_Ns - 1 - y] = G_value
        matrix[adjusted_Ns - 1 - x, adjusted_Ns - 1 - y] = G_value
        matrix[adjusted_Ns - 1 - y, adjusted_Ns - 1 - x] = G_value
        matrix[adjusted_Ns - 1 - y, x] = G_value
        matrix[adjusted_Ns - 1 - x, y] = G_value

    # Distribuição do S2 (S2_value)
    for pos in S_positions:
        x, y = pos
        matrix[x, y] = S2_value
        matrix[y, x] = S2_value
        matrix[y, adjusted_Ns - 1 - x] = S2_value
        matrix[x, adjusted_Ns - 1 - y] = S2_value
        matrix[adjusted_Ns - 1 - x, adjusted_Ns - 1 - y] = S2_value
        matrix[adjusted_Ns - 1 - y, adjusted_Ns - 1 - x] = S2_value
        matrix[adjusted_Ns - 1 - y, x] = S2_value
        matrix[adjusted_Ns - 1 - x, y] = S2_value

    if Ns % 2 != 0:
        center = Ns // 2
        for i in range(adjusted_Ns):
            matrix[center, i] = S1_value
            matrix[i, center] = S1_value

    matrix_string = ""
    for i in range(adjusted_Ns):
        matrix_string += "       "
        for j in range(adjusted_Ns):
            matrix_string += matrix[i, j] + " "
        matrix_string += "\n"
    matrix_string += "\n"

    return matrix_string

mid_point = number_seed // 2
Gd_positions = generate_positions(mid_point, Gd_per_eighth)
S_positions = generate_positions2(mid_point, S2_per_eighth, excluded_positions=Gd_positions)

################## Cálculo das dimensões #################
# Comprimento da região de seed
#length_seed = number_seed * pitch_seed

# Comprimento da região de blanket
#length_blank = number_blank * pitch_blank

# Cálculo de volumes seed
vol_seed = (math.pi * radius_seed ** 2) * heigth_active

# Cálculo de volumes blank
vol_blank = (math.pi * radius_blank ** 2) * heigth_active

# Cálculo de volumes seed subdividida
vol_sub_seed = (vol_seed / parts)

# Cálculo de volumes blank subdividida
vol_sub_blank = (vol_blank / parts)

# Cálculo de volumes do moderador seed
vol_seed_mod = heigth_active * (pitch_seed ** 2) - vol_seed

# Cálculo de volumes do moderador blank
vol_blank_mod = heigth_active * (pitch_blank ** 2) - vol_blank

# Cálculo de razão vm/vf seed
ratio_vm_vf_seed = (vol_seed_mod / vol_seed)

# Cálculo de razão vm/vf blank
ratio_vm_vf_blank = (vol_blank_mod / vol_blank)
#### Parâmetros dos refletores e casco ###########

# quadrado do conjunto de ec's
square_barrel=(number_assembly*length_blank)

#raio interno do refletor do nucleo
core_barrel_id=((number_assembly*length_blank))+38.0424

#raio externo do refletor do nucleo
core_barrel_od=core_barrel_id+10.1600

# raio interno vaso de pressão do reator
rpv_id=core_barrel_od+57.7753

# raio externo vaso de pressão do reator
rpv_od=rpv_id+34.4153
# Função para verificar se os parâmetros são válidos
matrix_string_gd1 = gen_pattern_gd(number_seed, Gd_positions, 'G0', 'S1')
matrix_string_gd2 = gen_pattern_gd(number_seed, Gd_positions, 'G0', 'S2')
matrix_string_gd3 = gen_pattern_gd(number_seed, Gd_positions, 'G0', 'S3')
matrix_string_gd4 = gen_pattern_gd(number_seed, Gd_positions, 'G0', 'S4')
matrix_string_gd5 = gen_pattern_gd(number_seed, Gd_positions, 'G0', 'S5')
matrix_string_gd6 = gen_pattern_gd2(number_seed, Gd_positions, S_positions, 'G0', 'S6', 'S7')
matrix_string_gd7 = gen_pattern_gd(number_seed, Gd_positions, 'G0', 'S8')
################ Depletion History ####################
########################################################
with open("nuscale_sbu_"+str(ind)+"h.c", "w",encoding="utf-8") as f:
    f.write("/***NuScale Reactor Seed-Blanket***/\n")
    f.write("%individuo:"+str(ind)+"\n")
    f.write("\n")
    f.write("%vol seed[cm^3]:"+str1(vol_seed)+"\n")
    f.write("%vol blank[cm^3]:"+str1(vol_blank)+"\n")
    f.write("%vol mod.seed[cm^3]:"+str1(vol_seed_mod)+"\n")
    f.write("%vol mod.blank[cm^3]:"+str1(vol_blank_mod)+"\n")
    f.write("%ratio vm_vf blank[-]:"+str1(ratio_vm_vf_blank)+"\n")
    f.write("%ratio vm_vf seed[-]:"+str1(ratio_vm_vf_seed)+"\n")
    f.write("%gap blank[-]:"+str1(gap_b)+"\n")
    f.write("%gap seed[-]:"+str1(gap_s)+"\n")
    f.write("%clad blank[-]:"+str1(clad_b)+"\n")
    f.write("%clad seed[-]:"+str1(clad_s)+"\n")
    f.write("%ratio P/D blank[-]:"+str1(ratio_blank)+"\n")
    f.write("%ratio P/D seed[-]:"+str1(ratio_seed)+"\n")
    f.write("\n")
    f.write("/****Volumes materials***/\n")
    f.write("include/nuscale_sbu_"+str(ind)+"o.c.mvol \n")
    f.write("\n")
    f.write("/****Materials***/\n")
    f.write("\n")
    f.write("include/mat_B4C.inc\n")
    f.write("include/mat_AIC.inc\n")
    f.write("include/mat_inconel625.inc\n")
    f.write("include/mat_ss304.inc\n")
    f.write("include/mat_ss304l.inc\n")
    f.write("include/mat_zircaloy4.inc\n")
    f.write("include/mat_water_"+str(temp_mod)+"K.inc\n")
    f.write("include/mat_helium.inc\n")
    f.write("include/mat_m5.inc\n")
    f.write("include/mat_air.inc\n")
    f.write("include/mat_ss508.inc\n")
    f.write("\n")
    f.write("/****Materials fuels***/\n")
    f.write("\n")
    f.write("include/suo_a01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_a02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_b01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_b02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c02g_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c03_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_a01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_a02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_b01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_b02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c03_"+str(temp_fuel)+"K.inc\n")
    f.write("\n")
    f.write("/*** Axial surfaces for fuel rods ***/\n")
    f.write("/*** Surface bottom nozzle lower***/\n")
    f.write("surf 1 pz "+str1(-total_heigth/2)+" \n")
    f.write("\n")
    f.write("/*** Surface bottom nozzle top***/\n")
    f.write("surf 2 pz "+str1(-total_heigth/2 + bottom_nozzle)+"\n")
    f.write("\n")
    f.write("/*** Surface end cap top***/\n")
    f.write("surf 3 pz "+str1(-total_heigth/2 + (bottom_nozzle+end_cap))+"\n")
    f.write("\n")
    f.write("/*** Surface UOX***/\n")
    f.write("surf 4 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+" \n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 5 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring))+"\n")
    f.write("\n")
    f.write("/*** Surface end cap***/\n")
    f.write("surf 6 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring+end_cap))+" \n")
    f.write("\n")
    f.write("/*** Surface coolant***/\n")
    f.write("surf 7 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring+coolant))+" \n")
    f.write("\n")
    f.write("/*** Surface top nozzle***/\n")
    f.write("surf 8 pz "+str1(total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surface outside Lattice***/\n")
    f.write("surf 9 cuboid "+str_(-length_seed/2)+" "+str_(length_seed/2)+" "+str_(-length_seed/2)+" "+str_(length_seed/2)+" "+str1(-total_heigth/2)+" "+str1(total_heigth/2)+"\n")
    f.write("surf 10 cuboid "+str_(-length_blank/2)+" "+str_(length_blank/2)+" "+str_(-length_blank/2)+" "+str_(length_blank/2)+" "+str1((-total_heigth)/2-0.05)+" "+str1((total_heigth)/2+0.05)+"\n")
    f.write("\n")
    f.write("/*** Surface outside Lattice***/\n")
    f.write("surf 11 inf\n")
    f.write("\n")
    f.write("/*** Axial surfaces for bar control ***/\n")
    f.write("/*** Surface bottom nozzle lower***/\n")
    f.write("surf 12 pz "+str1(-total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surface bottom nozzle top***/\n")
    f.write("surf 13 pz "+str1(-total_heigth/2 + bottom_nozzle)+"\n")
    f.write("\n")
    f.write("/*** Surface end cap top***/\n")
    f.write("surf 14 pz "+str1(-total_heigth/2 + (bottom_nozzle+end_cap))+"\n")
    f.write("\n")
    f.write("/*** Surface AIC***/\n")
    f.write("surf 15 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+"\n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 16 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+plenum_spring)+"\n")
    f.write("\n")
    f.write("/*** Surface B4C***/\n")
    f.write("surf 17 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+plenum_spring+length_b4c)+"\n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 18 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+length_b4c+upper_plenum)+"\n")
    f.write("\n")
    f.write("/*** Surface top nozzle***/\n")
    f.write("surf 19 pz "+str1(total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surfaces outside core***/\n")
    f.write("surf 20 cuboid "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str1(-total_heigth/2)+" "+str1(total_heigth/2)+" \n")
    f.write("surf 21 cuboid "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str2(-total_heigth/2)+" "+str2(total_heigth/2)+" \n")
    f.write("surf 22 cylz 0.0 0.0 "+str_((core_barrel_id)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 23 cylz 0.0 0.0 "+str_((core_barrel_od)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 24 cylz 0.0 0.0 "+str_((rpv_id)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 25 cylz 0.0 0.0 "+str_((rpv_od)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("\n")
    f.write("/*** Pin definitions Seed Rod***/\n")
    f.write("pin psuo_a01\n")
    f.write("suo_a01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_a02\n")
    f.write("suo_a02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_b01\n")
    f.write("suo_b01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_b02\n")
    f.write("suo_b02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c01\n")
    f.write("suo_c01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c02\n")
    f.write("suo_c02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c02g\n")
    f.write("suo_c02g  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c03\n")
    f.write("suo_c03  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spplenum\n")
    f.write("m5      "+str_(spring)+"\n")
    f.write("helium  "+str_(radius_seed+gap_s)+"\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+" \n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spendcap\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spcoolant\n")
    f.write("water   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+" \n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spss304\n")
    f.write("ss304l   "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("/*** Pin definitions blanket Rod***/\n")
    f.write("pin pbtho_a01\n")
    f.write("btho_a01  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_a02\n")
    f.write("btho_a02   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_b01\n")
    f.write("btho_b01   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_b02\n")
    f.write("btho_b02  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c01\n")
    f.write("btho_c01  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c02\n")
    f.write("btho_c02   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c03\n")
    f.write("btho_c03   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpplenum\n")
    f.write("m5         "+str_(spring)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpendcap\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpcoolant\n")
    f.write("water      "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpss304\n")
    f.write("ss304l     "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin G0\n")
    f.write("water    "+str_(radius_seed)+"\n")
    f.write("water    "+str_(radius_seed+gap_b)+"\n")
    f.write("m5       "+str_(radius_seed+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("/*** Pin definitions Control Rod***/\n")
    f.write("\n")
    f.write("pin pempty\n")
    f.write("helium  "+str_(radius_aic)+"\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin pendplug\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin paic\n")
    f.write("AIC     "+str_(radius_aic)+"\n")
    f.write("helium  "+str_(radius_aic+gap_b)+"\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin pb4c\n")
    f.write("B4C    "+str_(radius_b4c)+"\n")
    f.write("helium "+str_(radius_b4c+gap_b)+"\n")
    f.write("ss304l "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin xx\n")
    f.write("ss304l\n")
    f.write("\n")
    f.write("pin ww\n")
    f.write("water\n")
    f.write("\n")
    f.write("/** Burn options **/\n")
    f.write("\n")
    f.write("div suo_a01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+" \n")
    f.write("div suo_a02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_b01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_b02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c03 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_a01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_b01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_b02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c03 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div AIC subz "+str(parts)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+" \n")
    f.write("div B4C subz "+str(parts)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+length_b4c)+"\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A001 S1 ss304l             -2\n")
    f.write("cell A002 S1 fill spendcap       2  -3\n")
    f.write("cell A003 S1 fill psuo_a01       3  -4\n")
    f.write("cell A004 S1 fill spplenum       4  -5\n")
    f.write("cell A005 S1 fill spendcap       5  -6\n")
    f.write("cell A006 S1 fill spcoolant      6  -7\n")
    f.write("cell A007 S1 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A008 B1 ss304l             -2\n")
    f.write("cell A009 B1 fill bpendcap       2  -3\n")
    f.write("cell A010 B1 fill pbtho_a01      3  -4\n")
    f.write("cell A011 B1 fill bpplenum       4  -5\n")
    f.write("cell A012 B1 fill bpendcap       5  -6\n")
    f.write("cell A013 B1 fill bpcoolant      6  -7\n")
    f.write("cell A014 B1 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A015 BC ss304l            -13\n")
    f.write("cell A016 BC fill pendplug      13  -14\n")
    f.write("cell A017 BC fill paic          14  -15\n")
    f.write("cell A018 BC fill pb4c          15  -16\n")
    f.write("cell A019 BC fill pendplug      16  -17\n")
    f.write("cell A020 BC fill pempty        17  -18\n")
    f.write("cell A021 BC ss304l             18\n")
    f.write("\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 101  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("    ")  # Indentação para o começo da linha
        for j in range(number_blank):
            f.write('B1 ')  # Cada elemento na linha
        f.write("\n")  # Nova linha
    f.write("lat 102  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd1 + '\n')
    f.write("\n")
    f.write("cell A900 FA01 fill 102 -9\n")
    f.write("cell A901 FA01 fill 101 -10 9\n")
    f.write("cell A902 A01 fill FA01 -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A022 S2 ss304l             -2\n")
    f.write("cell A023 S2 fill spendcap       2  -3\n")
    f.write("cell A024 S2 fill psuo_a02       3  -4\n")
    f.write("cell A025 S2 fill spplenum       4  -5\n")
    f.write("cell A026 S2 fill spendcap       5  -6\n")
    f.write("cell A027 S2 fill spcoolant      6  -7\n")
    f.write("cell A028 S2 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A029 B2 ss304l             -2\n")
    f.write("cell A030 B2 fill bpendcap       2  -3\n")
    f.write("cell A031 B2 fill pbtho_a02      3  -4\n")
    f.write("cell A032 B2 fill bpplenum       4  -5\n")
    f.write("cell A033 B2 fill bpendcap       5  -6\n")
    f.write("cell A034 B2 fill bpcoolant      6  -7\n")
    f.write("cell A035 B2 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 201  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B2 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 202  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd2 + '\n')
    f.write("\n")
    f.write("cell A800 FA02 fill 202 -9 \n")
    f.write("cell A801 FA02 fill 201 -10 9   \n")
    f.write("cell A802 A02 fill FA02  -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A036 S3 ss304l             -2\n")
    f.write("cell A037 S3 fill spendcap       2  -3\n")
    f.write("cell A038 S3 fill psuo_b01       3  -4\n")
    f.write("cell A039 S3 fill spplenum       4  -5\n")
    f.write("cell A040 S3 fill spendcap       5  -6\n")
    f.write("cell A041 S3 fill spcoolant      6  -7\n")
    f.write("cell A042 S3 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A043 B3 ss304l             -2\n")
    f.write("cell A044 B3 fill bpendcap       2  -3\n")
    f.write("cell A045 B3 fill pbtho_b01      3  -4\n")
    f.write("cell A046 B3 fill bpplenum       4  -5\n")
    f.write("cell A047 B3 fill bpendcap       5  -6\n")
    f.write("cell A048 B3 fill bpcoolant      6  -7\n")
    f.write("cell A049 B3 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 301  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B3 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 302  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd3 + '\n')
    f.write("\n")
    f.write("cell A700 FB01 fill 302 -9\n")
    f.write("cell A701 FB01 fill 301 -10 9\n")
    f.write("cell A702 B01 fill FB01  -10 \n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A050 S4 ss304l             -2\n")
    f.write("cell A051 S4 fill spendcap       2  -3\n")
    f.write("cell A052 S4 fill psuo_b02       3  -4\n")
    f.write("cell A053 S4 fill spplenum       4  -5\n")
    f.write("cell A054 S4 fill spendcap       5  -6\n")
    f.write("cell A055 S4 fill spcoolant      6  -7\n")
    f.write("cell A056 S4 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A057 B4 ss304l             -2\n")
    f.write("cell A058 B4 fill bpendcap       2  -3\n")
    f.write("cell A059 B4 fill pbtho_b02      3  -4\n")
    f.write("cell A060 B4 fill bpplenum       4  -5\n")
    f.write("cell A061 B4 fill bpendcap       5  -6\n")
    f.write("cell A062 B4 fill bpcoolant      6  -7\n")
    f.write("cell A063 B4 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 401  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B4 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 402  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd4 + '\n')
    f.write("\n")
    f.write("cell A600 FB2 fill 402 -9 \n")
    f.write("cell A601 FB2 fill 401 -10 9 \n")
    f.write("cell A603 B02 fill FB2 -10 \n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A064 S5 ss304l             -2\n")
    f.write("cell A065 S5 fill spendcap       2  -3\n")
    f.write("cell A066 S5 fill psuo_c01       3  -4\n")
    f.write("cell A067 S5 fill spplenum       4  -5\n")
    f.write("cell A068 S5 fill spendcap       5  -6\n")
    f.write("cell A069 S5 fill spcoolant      6  -7\n")
    f.write("cell A070 S5 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A071 B5 ss304l             -2\n")
    f.write("cell A072 B5 fill bpendcap       2  -3\n")
    f.write("cell A073 B5 fill pbtho_c01      3  -4\n")
    f.write("cell A074 B5 fill bpplenum       4  -5\n")
    f.write("cell A075 B5 fill bpendcap       5  -6\n")
    f.write("cell A076 B5 fill bpcoolant      6  -7\n")
    f.write("cell A077 B5 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 501  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B5 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 502  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd5 + '\n')
    f.write("\n")
    f.write("cell A500 FC01 fill 502 -9\n")
    f.write("cell A501 FC01 fill 501 -10 9\n")
    f.write("cell A503 C01 fill FC01  -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A078 S6 ss304l             -2\n")
    f.write("cell A079 S6 fill spendcap       2  -3\n")
    f.write("cell A080 S6 fill psuo_c02       3  -4\n")
    f.write("cell A081 S6 fill spplenum       4  -5\n")
    f.write("cell A082 S6 fill spendcap       5  -6\n")
    f.write("cell A083 S6 fill spcoolant      6  -7\n")
    f.write("cell A084 S6 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A085 B6 ss304l             -2\n")
    f.write("cell A086 B6 fill bpendcap       2  -3\n")
    f.write("cell A087 B6 fill pbtho_c02      3  -4\n")
    f.write("cell A088 B6 fill bpplenum       4  -5\n")
    f.write("cell A089 B6 fill bpendcap       5  -6\n")
    f.write("cell A090 B6 fill bpcoolant      6  -7\n")
    f.write("cell A091 B6 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A092 S7 ss304l             -2\n")
    f.write("cell A093 S7 fill spendcap       2  -3\n")
    f.write("cell A094 S7 fill psuo_c02g      3  -4\n")
    f.write("cell A095 S7 fill spplenum       4  -5\n")
    f.write("cell A096 S7 fill spendcap       5  -6\n")
    f.write("cell A097 S7 fill spcoolant      6  -7\n")
    f.write("cell A098 S7 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 601  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B6 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 602  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd6 + '\n')
    f.write("\n")
    f.write("cell A400 FC02 fill 602 -9\n")
    f.write("cell A401 FC02 fill 601 -10 9\n")
    f.write("cell A403 C02 fill FC02 -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A099 S8 ss304l             -2\n")
    f.write("cell A101 S8 fill spendcap       2  -3\n")
    f.write("cell A102 S8 fill psuo_c03       3  -4\n")
    f.write("cell A103 S8 fill spplenum       4  -5\n")
    f.write("cell A104 S8 fill spendcap       5  -6\n")
    f.write("cell A105 S8 fill spcoolant      6  -7\n")
    f.write("cell A106 S8 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A107 B7 ss304l             -2\n")
    f.write("cell A108 B7 fill bpendcap       2  -3\n")
    f.write("cell A109 B7 fill pbtho_c03      3  -4\n")
    f.write("cell A110 B7 fill bpplenum       4  -5\n")
    f.write("cell A111 B7 fill bpendcap       5  -6\n")
    f.write("cell A112 B7 fill bpcoolant      6  -7\n")
    f.write("cell A113 B7 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 701  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B7 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 702  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd7 + '\n')
    f.write("\n")
    f.write("cell A300 FC03 fill 702 -9\n")
    f.write("cell A301 FC03 fill 701 -10 9\n")
    f.write("cell A303 C03 fill FC03 -10\n")
    f.write("\n")
    f.write("/************************\n")
    f.write(" * Core Configuration\n")
    f.write(" ************************/\n")
    f.write("lat core1 1 0.0 0.0 "+str(number_assembly)+" "+str(number_assembly)+"  "+str_(length_blank)+"\n")
    f.write(" HHH HHH C01 B02 C01 HHH HHH \n")
    f.write(" HHH C02 B01 A01 B01 C02 HHH \n")
    f.write(" C01 B01 A02 A01 A02 B01 C01 \n")
    f.write(" B02 A01 A01 C03 A01 A01 B02 \n")
    f.write(" C01 B01 A02 A01 A02 B01 C01 \n")
    f.write(" HHH C02 B01 A01 B01 C02 HHH \n")
    f.write(" HHH HHH C01 B02 C01 HHH HHH \n")
    f.write("\n")
    f.write("cell EC018 CORE fill core1  -21\n")
    f.write("cell EC019 CORE ss304l      21\n")
    f.write("\n")
    f.write("cell 8 0 fill CORE    -22\n")
    f.write("cell 9 0 ss304         22 -23\n")
    f.write("cell 10 0 water        23 -24\n")
    f.write("cell 11 0 ss508        24 -25\n")
    f.write("cell 12 0 outside        25  \n")
    f.write("cell E015 HHH ss304l  -11\n")
    f.write("\n")
    f.write("\n")
    f.write("/**Plot Graphs*/\n")
    f.write("plot 3 5000 5000\n")
    f.write("plot 2 1500 3000\n")
    f.write("\n")
    f.write("/***Run Parameters***/\n")
    f.write("\n")
    f.write(f"set pop {pop} {cyc} {incyc}\n")
    f.write(f"set bc {bc}\n")
    f.write(f"set power {power}\n")
    f.write(f"set title \"nuscale-sbu-{ind+1}\" \n")
    f.write("\n")
    f.write("/*** Detector that calculates the pin power distribution in the assembly***/\n")
    f.write(f"ene	1	3	10000	1.00E-09	255\n")
    f.write("\n")
    f.write("/****Cross Section Library***/\n")
    f.write(f"set acelib \"{filepath1}\"\n")
    f.write(f"set declib \"{filepath2}\"\n")
    f.write(f"set nfylib \"{filepath3}\"\n")
    f.write("\n")
    f.write("/*** Moviment bar control***/\n")
    f.write("trans u G0 0 0 0\n")
    f.write("trans u BC 0 0 10\n")
    f.write("/*** Reproductibility***/\n")
    f.write("set repro 2\n")
    f.write("\n")
    f.write("/*** Lost Particles***/\n")
    f.write("set lost -1\n")
    f.write("\n")
    f.write("/*** Depletion history***/\n")
    f.write("set opti 1 \n")
    f.write("dep daytot                                                         \n")
    for step in days:
        f.write(f"{step}\n")
    f.write("\n")
    f.write("/*** Set inventary ***/\n")
    f.write("set inventory\n")
    f.write("430990\n")
    f.write("501260\n")
    f.write("340790\n")
    f.write("400930\n")
    f.write("551350\n")
    f.write("461070\n")
    f.write("531290\n")
    f.write("932370\n")
    f.write("952410\n")
    f.write("962440\n")
    f.write("631550\n")
    f.write("360850\n")
    f.write("380900\n")
    f.write("551370\n")
    f.write("621510\n")
    f.write("501200\n")
    f.write("501220\n")
    f.write("902320\n")
    f.write("902330\n")
    f.write("902340\n")
    f.write("912310\n")
    f.write("912320\n")
    f.write("912330\n")
    f.write("912340\n")
    f.write("922320\n")
    f.write("922330\n")
    f.write("922340\n")
    f.write("922350\n")
    f.write("922360\n")
    f.write("922380\n")
    f.write("932370\n")
    f.write("942380\n")
    f.write("942390\n")
    f.write("942400\n")
    f.write("942410\n")
    f.write("942420\n")
    f.write("952410\n")
    f.write("952420\n")
    f.write("952430\n")
    f.write("420990\n")
    f.write("430990\n")
    f.write("441010\n")
    f.write("451030\n")
    f.write("471090\n")
    f.write("551330\n")
    f.write("621470\n")
    f.write("621490\n")
    f.write("621500\n")
    f.write("621510\n")
    f.write("621520\n")
    f.write("601430\n")
    f.write("601450\n")
    f.write("631530\n")
    f.write("641550\n")
    f.write("541260\n")
    f.write("561330\n")
    f.write("541280\n")
    f.write("541290\n")
    f.write("541300\n")
    f.write("541310\n")
    f.write("541320\n")
    f.write("541330\n")
    f.write("541360\n")
    f.write("541340\n")
    f.write("541350\n")
    f.write("481060\n")
    f.write("481080\n")
    f.write("481100\n")
    f.write("481110\n")
    f.write("481120\n")
    f.write("481130\n")
    f.write("481140\n")
    f.write("481160\n")
    f.write("50110\n")
    f.write("50100\n")
    f.write("set printm 1 0\n")
    f.write("\n")
    f.write("/***Calculating material volumes***/\n")
    f.write("set mcvol 100000000 \n")
####################Detector Definitions###################################
###########################################################################
with open("nuscale_sbu_"+str(ind)+"d.c", "w",encoding="utf-8") as f: 
    f.write("/***NuScale Reactor Seed-Blanket***/\n")
    f.write("%individuo:"+str(ind)+"\n")
    f.write("\n")
    f.write("%vol seed[cm^3]:"+str1(vol_seed)+"\n")
    f.write("%vol blank[cm^3]:"+str1(vol_blank)+"\n")
    f.write("%vol mod.seed[cm^3]:"+str1(vol_seed_mod)+"\n")
    f.write("%vol mod.blank[cm^3]:"+str1(vol_blank_mod)+"\n")
    f.write("%ratio vm_vf blank[-]:"+str1(ratio_vm_vf_blank)+"\n")
    f.write("%ratio vm_vf seed[-]:"+str1(ratio_vm_vf_seed)+"\n")
    f.write("%gap blank[-]:"+str1(gap_b)+"\n")
    f.write("%gap seed[-]:"+str1(gap_s)+"\n")
    f.write("%clad blank[-]:"+str1(clad_b)+"\n")
    f.write("%clad seed[-]:"+str1(clad_s)+"\n")
    f.write("%ratio P/D blank[-]:"+str1(ratio_blank)+"\n")
    f.write("%ratio P/D seed[-]:"+str1(ratio_seed)+"\n")
    f.write("\n")
    f.write("/****Volumes materials***/\n")
    f.write("include/nuscale_sbu_"+str(ind)+"o.c.mvol \n")
    f.write("\n")
    f.write("/****Materials***/\n")
    f.write("\n")
    f.write("include/mat_B4C.inc\n")
    f.write("include/mat_AIC.inc\n")
    f.write("include/mat_inconel625.inc\n")
    f.write("include/mat_ss304.inc\n")
    f.write("include/mat_ss304l.inc\n")
    f.write("include/mat_zircaloy4.inc\n")
    f.write("include/mat_water_"+str(temp_mod)+"K.inc\n")
    f.write("include/mat_helium.inc\n")
    f.write("include/mat_m5.inc\n")
    f.write("include/mat_air.inc\n")
    f.write("include/mat_ss508.inc\n")
    f.write("\n")
    f.write("/****Materials fuels***/\n")
    f.write("\n")
    f.write("include/suo_a01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_a02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_b01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_b02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c02g_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c03_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_a01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_a02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_b01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_b02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c03_"+str(temp_fuel)+"K.inc\n")
    f.write("\n")
    f.write("/*** Axial surfaces for fuel rods ***/\n")
    f.write("/*** Surface bottom nozzle lower***/\n")
    f.write("surf 1 pz "+str1(-total_heigth/2)+" \n")
    f.write("\n")
    f.write("/*** Surface bottom nozzle top***/\n")
    f.write("surf 2 pz "+str1(-total_heigth/2 + bottom_nozzle)+"\n")
    f.write("\n")
    f.write("/*** Surface end cap top***/\n")
    f.write("surf 3 pz "+str1(-total_heigth/2 + (bottom_nozzle+end_cap))+"\n")
    f.write("\n")
    f.write("/*** Surface UOX***/\n")
    f.write("surf 4 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+" \n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 5 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring))+"\n")
    f.write("\n")
    f.write("/*** Surface end cap***/\n")
    f.write("surf 6 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring+end_cap))+" \n")
    f.write("\n")
    f.write("/*** Surface coolant***/\n")
    f.write("surf 7 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring+coolant))+" \n")
    f.write("\n")
    f.write("/*** Surface top nozzle***/\n")
    f.write("surf 8 pz "+str1(total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surface outside Lattice***/\n")
    f.write("surf 9 cuboid "+str_(-length_seed/2)+" "+str_(length_seed/2)+" "+str_(-length_seed/2)+" "+str_(length_seed/2)+" "+str1(-total_heigth/2)+" "+str1(total_heigth/2)+"\n")
    f.write("surf 10 cuboid "+str_(-length_blank/2)+" "+str_(length_blank/2)+" "+str_(-length_blank/2)+" "+str_(length_blank/2)+" "+str1((-total_heigth)/2-0.05)+" "+str1((total_heigth)/2+0.05)+"\n")
    f.write("\n")
    f.write("/*** Surface outside Lattice***/\n")
    f.write("surf 11 inf\n")
    f.write("\n")
    f.write("/*** Axial surfaces for bar control ***/\n")
    f.write("/*** Surface bottom nozzle lower***/\n")
    f.write("surf 12 pz "+str1(-total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surface bottom nozzle top***/\n")
    f.write("surf 13 pz "+str1(-total_heigth/2 + bottom_nozzle)+"\n")
    f.write("\n")
    f.write("/*** Surface end cap top***/\n")
    f.write("surf 14 pz "+str1(-total_heigth/2 + (bottom_nozzle+end_cap))+"\n")
    f.write("\n")
    f.write("/*** Surface AIC***/\n")
    f.write("surf 15 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+"\n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 16 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+plenum_spring)+"\n")
    f.write("\n")
    f.write("/*** Surface B4C***/\n")
    f.write("surf 17 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+plenum_spring+length_b4c)+"\n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 18 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+length_b4c+upper_plenum)+"\n")
    f.write("\n")
    f.write("/*** Surface top nozzle***/\n")
    f.write("surf 19 pz "+str1(total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surfaces outside core***/\n")
    f.write("surf 20 cuboid "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str1(-total_heigth/2)+" "+str1(total_heigth/2)+" \n")
    f.write("surf 21 cuboid "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str2(-total_heigth/2)+" "+str2(total_heigth/2)+" \n")
    f.write("surf 22 cylz 0.0 0.0 "+str_((core_barrel_id)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 23 cylz 0.0 0.0 "+str_((core_barrel_od)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 24 cylz 0.0 0.0 "+str_((rpv_id)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 25 cylz 0.0 0.0 "+str_((rpv_od)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("\n")
    f.write("/*** Pin definitions Seed Rod***/\n")
    f.write("pin psuo_a01\n")
    f.write("suo_a01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_a02\n")
    f.write("suo_a02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_b01\n")
    f.write("suo_b01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_b02\n")
    f.write("suo_b02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c01\n")
    f.write("suo_c01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c02\n")
    f.write("suo_c02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c02g\n")
    f.write("suo_c02g  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c03\n")
    f.write("suo_c03  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spplenum\n")
    f.write("m5      "+str_(spring)+"\n")
    f.write("helium  "+str_(radius_seed+gap_s)+"\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+" \n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spendcap\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spcoolant\n")
    f.write("water   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+" \n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spss304\n")
    f.write("ss304l   "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("/*** Pin definitions blanket Rod***/\n")
    f.write("pin pbtho_a01\n")
    f.write("btho_a01  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_a02\n")
    f.write("btho_a02   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_b01\n")
    f.write("btho_b01   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_b02\n")
    f.write("btho_b02  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c01\n")
    f.write("btho_c01  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c02\n")
    f.write("btho_c02   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c03\n")
    f.write("btho_c03   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpplenum\n")
    f.write("m5         "+str_(spring)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpendcap\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpcoolant\n")
    f.write("water      "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpss304\n")
    f.write("ss304l     "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin G0\n")
    f.write("water     "+str_(radius_seed)+"\n")
    f.write("water    "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("/*** Pin definitions Control Rod***/\n")
    f.write("\n")
    f.write("pin pempty\n")
    f.write("helium  "+str_(radius_aic)+"\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin pendplug\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin paic\n")
    f.write("AIC     "+str_(radius_aic)+"\n")
    f.write("helium  "+str_(radius_aic+gap_b)+"\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin pb4c\n")
    f.write("B4C    "+str_(radius_b4c)+"\n")
    f.write("helium "+str_(radius_b4c+gap_s)+"\n")
    f.write("ss304l "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin xx\n")
    f.write("ss304l\n")
    f.write("\n")
    f.write("pin ww\n")
    f.write("water\n")
    f.write("\n")
    f.write("/** Burn options **/\n")
    f.write("\n")
    f.write("div suo_a01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+" \n")
    f.write("div suo_a02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_b01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_b02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c03 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_a01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_b01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_b02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c03 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div AIC subz "+str(parts)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+" \n")
    f.write("div B4C subz "+str(parts)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+length_b4c)+"\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A001 S1 ss304l             -2\n")
    f.write("cell A002 S1 fill spendcap       2  -3\n")
    f.write("cell A003 S1 fill psuo_a01       3  -4\n")
    f.write("cell A004 S1 fill spplenum       4  -5\n")
    f.write("cell A005 S1 fill spendcap       5  -6\n")
    f.write("cell A006 S1 fill spcoolant      6  -7\n")
    f.write("cell A007 S1 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A008 B1 ss304l             -2\n")
    f.write("cell A009 B1 fill bpendcap       2  -3\n")
    f.write("cell A010 B1 fill pbtho_a01      3  -4\n")
    f.write("cell A011 B1 fill bpplenum       4  -5\n")
    f.write("cell A012 B1 fill bpendcap       5  -6\n")
    f.write("cell A013 B1 fill bpcoolant      6  -7\n")
    f.write("cell A014 B1 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A015 BC ss304l            -13\n")
    f.write("cell A016 BC fill pendplug      13  -14\n")
    f.write("cell A017 BC fill paic          14  -15\n")
    f.write("cell A018 BC fill pb4c          15  -16\n")
    f.write("cell A019 BC fill pendplug      16  -17\n")
    f.write("cell A020 BC fill pempty        17  -18\n")
    f.write("cell A021 BC ss304l             18\n")
    f.write("\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 101  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("    ")  # Indentação para o começo da linha
        for j in range(number_blank):
            f.write('B1 ')  # Cada elemento na linha
        f.write("\n")  # Nova linha
    f.write("lat 102  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd1 + '\n')
    f.write("\n")
    f.write("cell A900 FA01 fill 102 -9\n")
    f.write("cell A901 FA01 fill 101 -10 9\n")
    f.write("cell A902 A01 fill FA01 -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A022 S2 ss304l             -2\n")
    f.write("cell A023 S2 fill spendcap       2  -3\n")
    f.write("cell A024 S2 fill psuo_a02       3  -4\n")
    f.write("cell A025 S2 fill spplenum       4  -5\n")
    f.write("cell A026 S2 fill spendcap       5  -6\n")
    f.write("cell A027 S2 fill spcoolant      6  -7\n")
    f.write("cell A028 S2 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A029 B2 ss304l             -2\n")
    f.write("cell A030 B2 fill bpendcap       2  -3\n")
    f.write("cell A031 B2 fill pbtho_a02      3  -4\n")
    f.write("cell A032 B2 fill bpplenum       4  -5\n")
    f.write("cell A033 B2 fill bpendcap       5  -6\n")
    f.write("cell A034 B2 fill bpcoolant      6  -7\n")
    f.write("cell A035 B2 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 201  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B2 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 202  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd2 + '\n')
    f.write("\n")
    f.write("cell A800 FA02 fill 202 -9 \n")
    f.write("cell A801 FA02 fill 201 -10 9   \n")
    f.write("cell A802 A02 fill FA02  -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A036 S3 ss304l             -2\n")
    f.write("cell A037 S3 fill spendcap       2  -3\n")
    f.write("cell A038 S3 fill psuo_b01       3  -4\n")
    f.write("cell A039 S3 fill spplenum       4  -5\n")
    f.write("cell A040 S3 fill spendcap       5  -6\n")
    f.write("cell A041 S3 fill spcoolant      6  -7\n")
    f.write("cell A042 S3 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A043 B3 ss304l             -2\n")
    f.write("cell A044 B3 fill bpendcap       2  -3\n")
    f.write("cell A045 B3 fill pbtho_b01      3  -4\n")
    f.write("cell A046 B3 fill bpplenum       4  -5\n")
    f.write("cell A047 B3 fill bpendcap       5  -6\n")
    f.write("cell A048 B3 fill bpcoolant      6  -7\n")
    f.write("cell A049 B3 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 301  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B3 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 302  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd3 + '\n')
    f.write("\n")
    f.write("cell A700 FB01 fill 302 -9\n")
    f.write("cell A701 FB01 fill 301 -10 9\n")
    f.write("cell A702 B01 fill FB01  -10 \n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A050 S4 ss304l             -2\n")
    f.write("cell A051 S4 fill spendcap       2  -3\n")
    f.write("cell A052 S4 fill psuo_b02       3  -4\n")
    f.write("cell A053 S4 fill spplenum       4  -5\n")
    f.write("cell A054 S4 fill spendcap       5  -6\n")
    f.write("cell A055 S4 fill spcoolant      6  -7\n")
    f.write("cell A056 S4 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A057 B4 ss304l             -2\n")
    f.write("cell A058 B4 fill bpendcap       2  -3\n")
    f.write("cell A059 B4 fill pbtho_b02      3  -4\n")
    f.write("cell A060 B4 fill bpplenum       4  -5\n")
    f.write("cell A061 B4 fill bpendcap       5  -6\n")
    f.write("cell A062 B4 fill bpcoolant      6  -7\n")
    f.write("cell A063 B4 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 401  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B4 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 402  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd4 + '\n')
    f.write("\n")
    f.write("cell A600 FB2 fill 402 -9 \n")
    f.write("cell A601 FB2 fill 401 -10 9 \n")
    f.write("cell A603 B02 fill FB2 -10 \n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A064 S5 ss304l             -2\n")
    f.write("cell A065 S5 fill spendcap       2  -3\n")
    f.write("cell A066 S5 fill psuo_c01       3  -4\n")
    f.write("cell A067 S5 fill spplenum       4  -5\n")
    f.write("cell A068 S5 fill spendcap       5  -6\n")
    f.write("cell A069 S5 fill spcoolant      6  -7\n")
    f.write("cell A070 S5 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A071 B5 ss304l             -2\n")
    f.write("cell A072 B5 fill bpendcap       2  -3\n")
    f.write("cell A073 B5 fill pbtho_c01      3  -4\n")
    f.write("cell A074 B5 fill bpplenum       4  -5\n")
    f.write("cell A075 B5 fill bpendcap       5  -6\n")
    f.write("cell A076 B5 fill bpcoolant      6  -7\n")
    f.write("cell A077 B5 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 501  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B5 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 502  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd5 + '\n')
    f.write("\n")
    f.write("cell A500 FC01 fill 502 -9\n")
    f.write("cell A501 FC01 fill 501 -10 9\n")
    f.write("cell A503 C01 fill FC01  -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A078 S6 ss304l             -2\n")
    f.write("cell A079 S6 fill spendcap       2  -3\n")
    f.write("cell A080 S6 fill psuo_c02       3  -4\n")
    f.write("cell A081 S6 fill spplenum       4  -5\n")
    f.write("cell A082 S6 fill spendcap       5  -6\n")
    f.write("cell A083 S6 fill spcoolant      6  -7\n")
    f.write("cell A084 S6 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A085 B6 ss304l             -2\n")
    f.write("cell A086 B6 fill bpendcap       2  -3\n")
    f.write("cell A087 B6 fill pbtho_c02      3  -4\n")
    f.write("cell A088 B6 fill bpplenum       4  -5\n")
    f.write("cell A089 B6 fill bpendcap       5  -6\n")
    f.write("cell A090 B6 fill bpcoolant      6  -7\n")
    f.write("cell A091 B6 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A092 S7 ss304l             -2\n")
    f.write("cell A093 S7 fill spendcap       2  -3\n")
    f.write("cell A094 S7 fill psuo_c02g      3  -4\n")
    f.write("cell A095 S7 fill spplenum       4  -5\n")
    f.write("cell A096 S7 fill spendcap       5  -6\n")
    f.write("cell A097 S7 fill spcoolant      6  -7\n")
    f.write("cell A098 S7 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 601  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B6 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 602  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd6 + '\n')
    f.write("\n")
    f.write("cell A400 FC02 fill 602 -9\n")
    f.write("cell A401 FC02 fill 601 -10 9\n")
    f.write("cell A403 C02 fill FC02 -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A099 S8 ss304l             -2\n")
    f.write("cell A101 S8 fill spendcap       2  -3\n")
    f.write("cell A102 S8 fill psuo_c03       3  -4\n")
    f.write("cell A103 S8 fill spplenum       4  -5\n")
    f.write("cell A104 S8 fill spendcap       5  -6\n")
    f.write("cell A105 S8 fill spcoolant      6  -7\n")
    f.write("cell A106 S8 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A107 B7 ss304l             -2\n")
    f.write("cell A108 B7 fill bpendcap       2  -3\n")
    f.write("cell A109 B7 fill pbtho_c03      3  -4\n")
    f.write("cell A110 B7 fill bpplenum       4  -5\n")
    f.write("cell A111 B7 fill bpendcap       5  -6\n")
    f.write("cell A112 B7 fill bpcoolant      6  -7\n")
    f.write("cell A113 B7 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 701  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B7 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 702  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd7 + '\n')
    f.write("\n")
    f.write("cell A300 FC03 fill 702 -9\n")
    f.write("cell A301 FC03 fill 701 -10 9\n")
    f.write("cell A303 C03 fill FC03 -10\n")
    f.write("\n")
    f.write("/************************\n")
    f.write(" * Core Configuration\n")
    f.write(" ************************/\n")
    f.write("lat core1 1 0.0 0.0 "+str(number_assembly)+" "+str(number_assembly)+"  "+str_(length_blank)+"\n")
    f.write(" HHH HHH C01 B02 C01 HHH HHH \n")
    f.write(" HHH C02 B01 A01 B01 C02 HHH \n")
    f.write(" C01 B01 A02 A01 A02 B01 C01 \n")
    f.write(" B02 A01 A01 C03 A01 A01 B02 \n")
    f.write(" C01 B01 A02 A01 A02 B01 C01 \n")
    f.write(" HHH C02 B01 A01 B01 C02 HHH \n")
    f.write(" HHH HHH C01 B02 C01 HHH HHH \n")
    f.write("\n")
    f.write("cell EC018 CORE fill core1  -21\n")
    f.write("cell EC019 CORE ss304l      21\n")
    f.write("\n")
    f.write("cell 8 0 fill CORE    -22\n")
    f.write("cell 9 0 ss304         22 -23\n")
    f.write("cell 10 0 water        23 -24\n")
    f.write("cell 11 0 ss508        24 -25\n")
    f.write("cell 12 0 outside        25  \n")
    f.write("cell E015 HHH ss304l  -11\n")
    f.write("\n")
    f.write("\n")
    f.write("/**Plot Graphs*/\n")
    f.write("plot 3 5000 5000\n")
    f.write("mesh 3 5000 5000\n")
    f.write("plot 2 1500 3000\n")
    f.write("\n")
    f.write("/***Run Parameters***/\n")
    f.write("\n")
    f.write(f"set pop {pop} {cyc} {incyc}\n")
    f.write(f"set bc {bc}\n")
    f.write(f"set power {power}\n")
    f.write(f"set title \"nuscale-sbu-{ind+1}\" \n")
    f.write("/*** Moviment bar control***/\n")
    f.write("trans u G0 0 0 0\n")
    f.write("trans u BC 0 0 10\n")
    f.write("/***Calculation detector***/\n")
    f.write("det 1\n")
    f.write(f"dr -6 void\n")
    f.write(f"dx {str1(-core_barrel_id/2 )} {str1(core_barrel_id/2 )} 80\n")
    f.write(f"dy {str1(-core_barrel_id/2 )} {str1(core_barrel_id/2 )} 80\n")
    f.write(f"dz {str1(-total_heigth / 2)} {str1(total_heigth / 2)} 100\n")
    f.write("\n")
    f.write("/*** Detector that calculates the pin power distribution in the assembly***/\n")
    f.write(f"ene	1	3	10000	1.00E-09	255\n")
    f.write("\n")
    f.write("/****Cross Section Library***/\n")
    f.write(f"set acelib \"{filepath1}\"\n")
    f.write(f"set declib \"{filepath2}\"\n")
    f.write(f"set nfylib \"{filepath3}\"\n")
    f.write("\n")
    f.write("/*** Moviment bar control***/\n")
    f.write("trans u G0 0 0 0\n")
    f.write("trans u BC 0 0 10\n")
    f.write("/*** Reproductibility***/\n")
    f.write("set repro 2\n")
    f.write("\n")
    f.write("/*** Lost Particles***/\n")
    f.write("set lost -1\n")
    f.write("\n")
    f.write("/*** Depletion history***/\n")
    f.write("set printm 1 0\n")
    f.write("set opti 1 \n")
    f.write("\n")
    f.write("/*** Cross section Data***/\n")
    f.write(f"set xsplot 10000 1.00E-09 10000 \n")
    f.write("\n")
    f.write("/*** Calculation material volumes***/\n")
    f.write("set mcvol 100000000 \n")
############## Calculate Volumes #####################
#####################################################
with open("nuscale_sbu_"+str(ind)+"o.c", "w",encoding="utf-8") as f: 
    f.write("/***NuScale Reactor Seed-Blanket***/\n")
    f.write("%individuo:"+str(ind)+"\n")
    f.write("\n")
    f.write("%vol seed[cm^3]:"+str1(vol_seed)+"\n")
    f.write("%vol blank[cm^3]:"+str1(vol_blank)+"\n")
    f.write("%vol mod.seed[cm^3]:"+str1(vol_seed_mod)+"\n")
    f.write("%vol mod.blank[cm^3]:"+str1(vol_blank_mod)+"\n")
    f.write("%ratio vm_vf blank[-]:"+str1(ratio_vm_vf_blank)+"\n")
    f.write("%ratio vm_vf seed[-]:"+str1(ratio_vm_vf_seed)+"\n")
    f.write("%gap blank[-]:"+str1(gap_b)+"\n")
    f.write("%gap seed[-]:"+str1(gap_s)+"\n")
    f.write("%clad blank[-]:"+str1(clad_b)+"\n")
    f.write("%clad seed[-]:"+str1(clad_s)+"\n")
    f.write("%ratio P/D blank[-]:"+str1(ratio_blank)+"\n")
    f.write("%ratio P/D seed[-]:"+str1(ratio_seed)+"\n")
    f.write("\n")
    f.write("/****Volumes materials***/\n")
    f.write("include/nuscale_sbu_"+str(ind)+"o.c.mvol \n")
    f.write("\n")
    f.write("/****Materials***/\n")
    f.write("\n")
    f.write("include/mat_B4C.inc\n")
    f.write("include/mat_AIC.inc\n")
    f.write("include/mat_inconel625.inc\n")
    f.write("include/mat_ss304.inc\n")
    f.write("include/mat_ss304l.inc\n")
    f.write("include/mat_zircaloy4.inc\n")
    f.write("include/mat_water_"+str(temp_mod)+"K.inc\n")
    f.write("include/mat_helium.inc\n")
    f.write("include/mat_m5.inc\n")
    f.write("include/mat_air.inc\n")
    f.write("include/mat_ss508.inc\n")
    f.write("\n")
    f.write("/****Materials fuels***/\n")
    f.write("\n")
    f.write("include/suo_a01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_a02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_b01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_b02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c02g_"+str(temp_fuel)+"K.inc\n")
    f.write("include/suo_c03_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_a01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_a02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_b01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_b02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c01_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c02_"+str(temp_fuel)+"K.inc\n")
    f.write("include/btho_c03_"+str(temp_fuel)+"K.inc\n")
    f.write("\n")
    f.write("/*** Axial surfaces for fuel rods ***/\n")
    f.write("/*** Surface bottom nozzle lower***/\n")
    f.write("surf 1 pz "+str1(-total_heigth/2)+" \n")
    f.write("\n")
    f.write("/*** Surface bottom nozzle top***/\n")
    f.write("surf 2 pz "+str1(-total_heigth/2 + bottom_nozzle)+"\n")
    f.write("\n")
    f.write("/*** Surface end cap top***/\n")
    f.write("surf 3 pz "+str1(-total_heigth/2 + (bottom_nozzle+end_cap))+"\n")
    f.write("\n")
    f.write("/*** Surface UOX***/\n")
    f.write("surf 4 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+" \n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 5 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring))+"\n")
    f.write("\n")
    f.write("/*** Surface end cap***/\n")
    f.write("surf 6 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring+end_cap))+" \n")
    f.write("\n")
    f.write("/*** Surface coolant***/\n")
    f.write("surf 7 pz "+str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active+plenum_spring+coolant))+" \n")
    f.write("\n")
    f.write("/*** Surface top nozzle***/\n")
    f.write("surf 8 pz "+str1(total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surface outside Lattice***/\n")
    f.write("surf 9 cuboid "+str_(-length_seed/2)+" "+str_(length_seed/2)+" "+str_(-length_seed/2)+" "+str_(length_seed/2)+" "+str1(-total_heigth/2)+" "+str1(total_heigth/2)+"\n")
    f.write("surf 10 cuboid "+str_(-length_blank/2)+" "+str_(length_blank/2)+" "+str_(-length_blank/2)+" "+str_(length_blank/2)+" "+str1((-total_heigth)/2-0.05)+" "+str1((total_heigth)/2+0.05)+"\n")
    f.write("\n")
    f.write("/*** Surface outside Lattice***/\n")
    f.write("surf 11 inf\n")
    f.write("\n")
    f.write("/*** Axial surfaces for bar control ***/\n")
    f.write("/*** Surface bottom nozzle lower***/\n")
    f.write("surf 12 pz "+str1(-total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surface bottom nozzle top***/\n")
    f.write("surf 13 pz "+str1(-total_heigth/2 + bottom_nozzle)+"\n")
    f.write("\n")
    f.write("/*** Surface end cap top***/\n")
    f.write("surf 14 pz "+str1(-total_heigth/2 + (bottom_nozzle+end_cap))+"\n")
    f.write("\n")
    f.write("/*** Surface AIC***/\n")
    f.write("surf 15 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+"\n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 16 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+plenum_spring)+"\n")
    f.write("\n")
    f.write("/*** Surface B4C***/\n")
    f.write("surf 17 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+plenum_spring+length_b4c)+"\n")
    f.write("\n")
    f.write("/*** Surface plenum spring***/\n")
    f.write("surf 18 pz "+str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+length_b4c+upper_plenum)+"\n")
    f.write("\n")
    f.write("/*** Surface top nozzle***/\n")
    f.write("surf 19 pz "+str1(total_heigth/2)+"\n")
    f.write("\n")
    f.write("/*** Surfaces outside core***/\n")
    f.write("surf 20 cuboid "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str1(-total_heigth/2)+" "+str1(total_heigth/2)+" \n")
    f.write("surf 21 cuboid "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str_(-(square_barrel)/2)+" "+str_((square_barrel)/2)+" "+str2(-total_heigth/2)+" "+str2(total_heigth/2)+" \n")
    f.write("surf 22 cylz 0.0 0.0 "+str_((core_barrel_id)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 23 cylz 0.0 0.0 "+str_((core_barrel_od)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 24 cylz 0.0 0.0 "+str_((rpv_id)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("surf 25 cylz 0.0 0.0 "+str_((rpv_od)/2)+" "+str2(-total_heigth/2-0.004)+" "+ str2(total_heigth/2+0.004)+"\n")
    f.write("\n")
    f.write("/*** Pin definitions Seed Rod***/\n")
    f.write("pin psuo_a01\n")
    f.write("suo_a01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_a02\n")
    f.write("suo_a02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_b01\n")
    f.write("suo_b01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_b02\n")
    f.write("suo_b02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c01\n")
    f.write("suo_c01  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c02\n")
    f.write("suo_c02  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c02g\n")
    f.write("suo_c02g  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin psuo_c03\n")
    f.write("suo_c03  "+str_(radius_seed)+"\n")
    f.write("helium   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spplenum\n")
    f.write("m5      "+str_(spring)+"\n")
    f.write("helium  "+str_(radius_seed+gap_s)+"\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+" \n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spendcap\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spcoolant\n")
    f.write("water   "+str_(radius_seed+gap_s)+"\n")
    f.write("m5      "+str_(radius_seed+gap_s+clad_s)+" \n")
    f.write("water\n")
    f.write("\n")
    f.write("pin spss304\n")
    f.write("ss304l   "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("/*** Pin definitions blanket Rod***/\n")
    f.write("pin pbtho_a01\n")
    f.write("btho_a01  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_a02\n")
    f.write("btho_a02   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_b01\n")
    f.write("btho_b01   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_b02\n")
    f.write("btho_b02  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c01\n")
    f.write("btho_c01  "+str_(radius_blank)+"\n")
    f.write("helium    "+str_(radius_blank+gap_b)+"\n")
    f.write("m5        "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c02\n")
    f.write("btho_c02   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin pbtho_c03\n")
    f.write("btho_c03   "+str_(radius_blank)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpplenum\n")
    f.write("m5         "+str_(spring)+"\n")
    f.write("helium     "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpendcap\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpcoolant\n")
    f.write("water      "+str_(radius_blank+gap_b)+"\n")
    f.write("m5         "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin bpss304\n")
    f.write("ss304l     "+str_(radius_blank+gap_b+clad_b)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("pin G0\n")
    f.write("water    "+str_(radius_seed)+"\n")
    f.write("water    "+str_(radius_seed+gap_s)+"\n")
    f.write("m5       "+str_(radius_seed+gap_s+clad_s)+"\n")
    f.write("water\n")
    f.write("\n")
    f.write("/*** Pin definitions Control Rod***/\n")
    f.write("\n")
    f.write("pin pempty\n")
    f.write("helium  "+str_(radius_aic)+"\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin pendplug\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin paic\n")
    f.write("AIC     "+str_(radius_aic)+"\n")
    f.write("helium  "+str_(radius_aic+gap_b)+"\n")
    f.write("ss304l  "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin pb4c\n")
    f.write("B4C    "+str_(radius_b4c)+"\n")
    f.write("helium "+str_(radius_b4c+gap_b)+"\n")
    f.write("ss304l "+str_(radius_bar)+"\n")
    f.write("void\n")
    f.write("\n")
    f.write("pin xx\n")
    f.write("ss304l\n")
    f.write("\n")
    f.write("pin ww\n")
    f.write("water\n")
    f.write("\n")
    f.write("/** Burn options **/\n")
    f.write("\n")
    f.write("div suo_a01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+" \n")
    f.write("div suo_a02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_b01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_b02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div suo_c03 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_a01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_b01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_b02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c01 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c02 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div btho_c03 subz "+str(parts)+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap))+" "+ str1(-total_heigth/2+(bottom_nozzle+end_cap+heigth_active))+"\n")
    f.write("div AIC subz "+str(parts)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+" \n")
    f.write("div B4C subz "+str(parts)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic)+" "+ str1((-total_heigth/2)+bottom_nozzle+empty_guide+end_plug+length_aic+length_b4c)+"\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A001 S1 ss304l             -2\n")
    f.write("cell A002 S1 fill spendcap       2  -3\n")
    f.write("cell A003 S1 fill psuo_a01       3  -4\n")
    f.write("cell A004 S1 fill spplenum       4  -5\n")
    f.write("cell A005 S1 fill spendcap       5  -6\n")
    f.write("cell A006 S1 fill spcoolant      6  -7\n")
    f.write("cell A007 S1 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A008 B1 ss304l             -2\n")
    f.write("cell A009 B1 fill bpendcap       2  -3\n")
    f.write("cell A010 B1 fill pbtho_a01      3  -4\n")
    f.write("cell A011 B1 fill bpplenum       4  -5\n")
    f.write("cell A012 B1 fill bpendcap       5  -6\n")
    f.write("cell A013 B1 fill bpcoolant      6  -7\n")
    f.write("cell A014 B1 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A015 BC ss304l            -13\n")
    f.write("cell A016 BC fill pendplug      13  -14\n")
    f.write("cell A017 BC fill paic          14  -15\n")
    f.write("cell A018 BC fill pb4c          15  -16\n")
    f.write("cell A019 BC fill pendplug      16  -17\n")
    f.write("cell A020 BC fill pempty        17  -18\n")
    f.write("cell A021 BC ss304l             18\n")
    f.write("\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 101  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("    ")  # Indentação para o começo da linha
        for j in range(number_blank):
            f.write('B1 ')  # Cada elemento na linha
        f.write("\n")  # Nova linha
    f.write("lat 102  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd1 + '\n')
    f.write("\n")
    f.write("cell A900 FA01 fill 102 -9\n")
    f.write("cell A901 FA01 fill 101 -10 9\n")
    f.write("cell A902 A01 fill FA01 -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A022 S2 ss304l             -2\n")
    f.write("cell A023 S2 fill spendcap       2  -3\n")
    f.write("cell A024 S2 fill psuo_a02       3  -4\n")
    f.write("cell A025 S2 fill spplenum       4  -5\n")
    f.write("cell A026 S2 fill spendcap       5  -6\n")
    f.write("cell A027 S2 fill spcoolant      6  -7\n")
    f.write("cell A028 S2 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A029 B2 ss304l             -2\n")
    f.write("cell A030 B2 fill bpendcap       2  -3\n")
    f.write("cell A031 B2 fill pbtho_a02      3  -4\n")
    f.write("cell A032 B2 fill bpplenum       4  -5\n")
    f.write("cell A033 B2 fill bpendcap       5  -6\n")
    f.write("cell A034 B2 fill bpcoolant      6  -7\n")
    f.write("cell A035 B2 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 201  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B2 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 202  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd2 + '\n')
    f.write("\n")
    f.write("cell A800 FA02 fill 202 -9 \n")
    f.write("cell A801 FA02 fill 201 -10 9   \n")
    f.write("cell A802 A02 fill FA02  -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A036 S3 ss304l             -2\n")
    f.write("cell A037 S3 fill spendcap       2  -3\n")
    f.write("cell A038 S3 fill psuo_b01       3  -4\n")
    f.write("cell A039 S3 fill spplenum       4  -5\n")
    f.write("cell A040 S3 fill spendcap       5  -6\n")
    f.write("cell A041 S3 fill spcoolant      6  -7\n")
    f.write("cell A042 S3 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A043 B3 ss304l             -2\n")
    f.write("cell A044 B3 fill bpendcap       2  -3\n")
    f.write("cell A045 B3 fill pbtho_b01      3  -4\n")
    f.write("cell A046 B3 fill bpplenum       4  -5\n")
    f.write("cell A047 B3 fill bpendcap       5  -6\n")
    f.write("cell A048 B3 fill bpcoolant      6  -7\n")
    f.write("cell A049 B3 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 301  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B3 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 302  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd3 + '\n')
    f.write("\n")
    f.write("cell A700 FB01 fill 302 -9\n")
    f.write("cell A701 FB01 fill 301 -10 9\n")
    f.write("cell A702 B01 fill FB01  -10 \n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A050 S4 ss304l             -2\n")
    f.write("cell A051 S4 fill spendcap       2  -3\n")
    f.write("cell A052 S4 fill psuo_b02       3  -4\n")
    f.write("cell A053 S4 fill spplenum       4  -5\n")
    f.write("cell A054 S4 fill spendcap       5  -6\n")
    f.write("cell A055 S4 fill spcoolant      6  -7\n")
    f.write("cell A056 S4 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A057 B4 ss304l             -2\n")
    f.write("cell A058 B4 fill bpendcap       2  -3\n")
    f.write("cell A059 B4 fill pbtho_b02      3  -4\n")
    f.write("cell A060 B4 fill bpplenum       4  -5\n")
    f.write("cell A061 B4 fill bpendcap       5  -6\n")
    f.write("cell A062 B4 fill bpcoolant      6  -7\n")
    f.write("cell A063 B4 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 401  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B4 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 402  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write("\n")
    f.write(matrix_string_gd4 + '\n')
    f.write("\n")
    f.write("cell A600 FB2 fill 402 -9 \n")
    f.write("cell A601 FB2 fill 401 -10 9 \n")
    f.write("cell A603 B02 fill FB2 -10 \n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A064 S5 ss304l             -2\n")
    f.write("cell A065 S5 fill spendcap       2  -3\n")
    f.write("cell A066 S5 fill psuo_c01       3  -4\n")
    f.write("cell A067 S5 fill spplenum       4  -5\n")
    f.write("cell A068 S5 fill spendcap       5  -6\n")
    f.write("cell A069 S5 fill spcoolant      6  -7\n")
    f.write("cell A070 S5 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A071 B5 ss304l             -2\n")
    f.write("cell A072 B5 fill bpendcap       2  -3\n")
    f.write("cell A073 B5 fill pbtho_c01      3  -4\n")
    f.write("cell A074 B5 fill bpplenum       4  -5\n")
    f.write("cell A075 B5 fill bpendcap       5  -6\n")
    f.write("cell A076 B5 fill bpcoolant      6  -7\n")
    f.write("cell A077 B5 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 501  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B5 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 502  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd5 + '\n')
    f.write("\n")
    f.write("cell A500 FC01 fill 502 -9\n")
    f.write("cell A501 FC01 fill 501 -10 9\n")
    f.write("cell A503 C01 fill FC01  -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A078 S6 ss304l             -2\n")
    f.write("cell A079 S6 fill spendcap       2  -3\n")
    f.write("cell A080 S6 fill psuo_c02       3  -4\n")
    f.write("cell A081 S6 fill spplenum       4  -5\n")
    f.write("cell A082 S6 fill spendcap       5  -6\n")
    f.write("cell A083 S6 fill spcoolant      6  -7\n")
    f.write("cell A084 S6 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A085 B6 ss304l             -2\n")
    f.write("cell A086 B6 fill bpendcap       2  -3\n")
    f.write("cell A087 B6 fill pbtho_c02      3  -4\n")
    f.write("cell A088 B6 fill bpplenum       4  -5\n")
    f.write("cell A089 B6 fill bpendcap       5  -6\n")
    f.write("cell A090 B6 fill bpcoolant      6  -7\n")
    f.write("cell A091 B6 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A092 S7 ss304l             -2\n")
    f.write("cell A093 S7 fill spendcap       2  -3\n")
    f.write("cell A094 S7 fill psuo_c02g      3  -4\n")
    f.write("cell A095 S7 fill spplenum       4  -5\n")
    f.write("cell A096 S7 fill spendcap       5  -6\n")
    f.write("cell A097 S7 fill spcoolant      6  -7\n")
    f.write("cell A098 S7 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 601  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B6 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 602  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd6 + '\n')
    f.write("\n")
    f.write("cell A400 FC02 fill 602 -9\n")
    f.write("cell A401 FC02 fill 601 -10 9\n")
    f.write("cell A403 C02 fill FC02 -10\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for seed rod***/\n")
    f.write("\n")
    f.write("cell A099 S8 ss304l             -2\n")
    f.write("cell A101 S8 fill spendcap       2  -3\n")
    f.write("cell A102 S8 fill psuo_c03       3  -4\n")
    f.write("cell A103 S8 fill spplenum       4  -5\n")
    f.write("cell A104 S8 fill spendcap       5  -6\n")
    f.write("cell A105 S8 fill spcoolant      6  -7\n")
    f.write("cell A106 S8 ss304l              7\n")
    f.write("\n")
    f.write("/*** Verical layers (cells) for blanket rod***/\n")
    f.write("\n")
    f.write("cell A107 B7 ss304l             -2\n")
    f.write("cell A108 B7 fill bpendcap       2  -3\n")
    f.write("cell A109 B7 fill pbtho_c03      3  -4\n")
    f.write("cell A110 B7 fill bpplenum       4  -5\n")
    f.write("cell A111 B7 fill bpendcap       5  -6\n")
    f.write("cell A112 B7 fill bpcoolant      6  -7\n")
    f.write("cell A113 B7 ss304l              7\n")
    f.write("\n")
    f.write("/*** Lattice ***/\n")
    f.write("lat 701  1  0.0 0.0 "+str(number_blank)+" "+str(number_blank)+"  "+ str_(pitch_blank)+"\n")
    for i in range(number_blank):
        f.write("") # Indentation for the beginning of the row
        for j in range(number_blank):
            f.write('B7 ')  # Each element in the row
        f.write("\n")  # Newline after each row
    f.write("\n")
    f.write("lat 702  1 0.0 0.0 "+str(number_seed)+" "+str(number_seed)+"  "+ str_(pitch_seed)+"\n")
    f.write(matrix_string_gd7 + '\n')
    f.write("\n")
    f.write("cell A300 FC03 fill 702 -9\n")
    f.write("cell A301 FC03 fill 701 -10 9\n")
    f.write("cell A303 C03 fill FC03 -10\n")
    f.write("\n")
    f.write("/************************\n")
    f.write(" * Core Configuration\n")
    f.write(" ************************/\n")
    f.write("lat core1 1 0.0 0.0 "+str(number_assembly)+" "+str(number_assembly)+"  "+str_(length_blank)+"\n")
    f.write(" HHH HHH C01 B02 C01 HHH HHH \n")
    f.write(" HHH C02 B01 A01 B01 C02 HHH \n")
    f.write(" C01 B01 A02 A01 A02 B01 C01 \n")
    f.write(" B02 A01 A01 C03 A01 A01 B02 \n")
    f.write(" C01 B01 A02 A01 A02 B01 C01 \n")
    f.write(" HHH C02 B01 A01 B01 C02 HHH \n")
    f.write(" HHH HHH C01 B02 C01 HHH HHH \n")
    f.write("\n")
    f.write("cell EC018 CORE fill core1  -21\n")
    f.write("cell EC019 CORE ss304l      21\n")
    f.write("\n")
    f.write("cell 8 0 fill CORE    -22\n")
    f.write("cell 9 0 ss304         22 -23\n")
    f.write("cell 10 0 water        23 -24\n")
    f.write("cell 11 0 ss508        24 -25\n")
    f.write("cell 12 0 outside        25  \n")
    f.write("cell E015 HHH ss304l  -11\n")
    f.write("\n")
    f.write("\n")
    f.write("/**Plot Graphs*/\n")
    f.write("plot 3 5000 5000\n")
    f.write("plot 2 1500 5000\n")
    f.write("\n")
    f.write("/***Run Parameters***/\n")
    f.write("\n")
    f.write(f"set pop {pop} {cyc} {incyc}\n")
    f.write(f"set bc {bc}\n")
    f.write(f"set power {power}\n")
    f.write(f"set title \"nuscale-sbu-{ind+1}\" \n")
    f.write("\n")
    f.write("/*** Moviment bar control***/\n")
    f.write("trans u G0 0 0 0\n")
    f.write("trans u BC 0 0 10\n")
    f.write("/****Cross Section Library***/\n")
    f.write(f"set acelib \"{filepath1}\"\n")
    f.write(f"set declib \"{filepath2}\"\n")
    f.write(f"set nfylib \"{filepath3}\"\n")

# Transferência dos arquivos para a pasta de destino
transfer_file(f"{filepath6}nuscale_sbu_0o.c", f"{filepath5}nuscale_sbu_0o.c")
transfer_file(f"{filepath6}nuscale_sbu_0d.c", f"{filepath5}nuscale_sbu_0d.c")
transfer_file(f"{filepath6}nuscale_sbu_0h.c", f"{filepath5}nuscale_sbu_0h.c")

# Writing to CSV file
variables = {
    "Parameters Design": "Unit[cm]",
    "total_heigth": total_heigth,
    "radius_seed": radius_seed,
    "radius_blank": radius_blank,
    "number_seed": number_seed,
    "number_blank": number_blank,
    "pitch_seed": pitch_seed,
    "pitch_blank": pitch_blank,
    "heigth_active": heigth_active,
    "diameter_seed": diameter_seed,
    "diameter_blank": diameter_blank,
    "gap_s": gap_s,
    "clad_s": clad_s,
    "gap_b": gap_b,
    "clad_b": clad_b,
    "top_nozzle": top_nozzle,
    "coolant": coolant,
    "end_cap": end_cap,
    "plenum_spring": plenum_spring,
    "spring": spring,
    "bottom_nozzle": bottom_nozzle,
    "number_assembly": number_assembly,
    "empty_guide": empty_guide,
    "end_plug": end_plug,
    "length_aic": length_aic,
    "length_b4c": length_b4c,
    "upper_plenum": upper_plenum,
    "radius_aic": radius_aic,
    "radius_b4c": radius_b4c,
    "radius_bar": radius_bar,
    "ratio_seed": ratio_seed,
    "ratio_blank": ratio_blank,
    "length_seed": length_seed,
    "length_blank": length_blank,
    "vol_seed": vol_seed,
    "vol_blank": vol_blank,
    "vol_sub_seed": vol_sub_seed,
    "vol_sub_blank": vol_sub_blank,
    "vol_seed_mod": vol_seed_mod,
    "vol_blank_mod": vol_blank_mod,
    "ratio_vm_vf_seed": ratio_vm_vf_seed,
    "ratio_vm_vf_blank": ratio_vm_vf_blank,
    "square_barrel": square_barrel,
    "core_barrel_id": core_barrel_id,
    "core_barrel_od": core_barrel_od,
    "rpv_id": rpv_id,
    "rpv_od": rpv_od
}

with open(f'{filepath6}design_nuscale_sbu.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Variable", "Value"])
    for key, value in variables.items():
        writer.writerow([key, value])

print("Arquivos gerados e transferidos.")
print(f"Os arquivos criados e deverao ser rodados dessa forma\n")
print(f"./sss2 -omp 24 -checkvolumes 100000000 nuscale_sbu_"+str(ind)+"o.c ;./sss2 -omp 24 nuscale_sbu_"+str(ind)+"d.c  ;./sss2 -omp 24 nuscale_sbu_"+str(ind)+"h.c \n")
