import os
import numpy as np
import matplotlib.pyplot as plt
from scrip_nuscale import*
#from scrip_nuscale_sbu import* 

# Definindo os caminhos dos arquivos
file_path_m = 'nuscale_0d.c_det.m'
new_file_path_txt = 'nuscale_0d.c_det.txt'

# Checar se o arquivo existe antes de renomear
if os.path.exists(file_path_m):
    os.rename(file_path_m, new_file_path_txt)
    print(f'Renamed {file_path_m} to {new_file_path_txt}')
    file_path = new_file_path_txt
else:
    raise FileNotFoundError(f"The file {file_path_m} does not exist.")

# Definindo dimensões da grade e potência total do sistema
Nx = 80
Ny = 80
Nz = 100
P = power  # Potência total do sistema em watts

# Função para ler dados do detector a partir do arquivo
def read_detector_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        start_reading = False
        for line in file:
            if 'DET1' in line:
                start_reading = True
            elif start_reading:
                if line.strip():
                    parts = line.split()
                    if len(parts) == 12:
                        data.append(parts)
                else:
                    break
    if len(data) == Nx * Ny * Nz:
        data = np.array(data, dtype=float)
    else:
        raise ValueError(f"Expected {Nx * Ny * Nz} rows, but got {len(data)} rows.")
    return data

data = read_detector_data(file_path)  # Ler os dados

# Função para extrair coordenadas do detector a partir do arquivo
def extract_det_coordinates(file_path):
    det1x, det1y, det1z = [], [], []
    with open(file_path, 'r') as file:
        start_collecting = False
        for line in file:
            if 'DET1X' in line or 'DET1Y' in line or 'DET1Z' in line:
                start_collecting = True
                coordinate_type = line.strip().split('=')[0].strip()
            elif start_collecting and '];' in line:
                start_collecting = False
            elif start_collecting and line.strip():
                values = [float(value) for value in line.strip().split()]
                if coordinate_type == 'DET1X':
                    det1x.extend(values)
                elif coordinate_type == 'DET1Y':
                    det1y.extend(values)
                elif coordinate_type == 'DET1Z':
                    det1z.extend(values)
    return np.array(det1x), np.array(det1y), np.array(det1z)

det1x, det1y, det1z = extract_det_coordinates(file_path)  # Extrair coordenadas

# Calcular o número de células
num_cells = len(det1x) // 3

# Reformatar coordenadas para corresponder ao número de células
det1x = det1x[:num_cells * 3].reshape(num_cells, 3)
det1y = det1y[:num_cells * 3].reshape(num_cells, 3)
det1z = det1z[:num_cells * 3].reshape(num_cells, 3)

# Calcular diferenças absolutas entre coordenadas para cada célula
x_diffs = np.abs(det1x[:, 1] - det1x[:, 0])
y_diffs = np.abs(det1y[:, 1] - det1y[:, 0])
z_diffs = np.abs(det1z[:, 1] - det1z[:, 0])

# Calcular o volume de cada célula
volume3_i = x_diffs * y_diffs * z_diffs

# Calcular o volume total
total_volumes = np.sum(volume3_i)

# Calcular as áreas das seções transversais
area_xy = x_diffs * y_diffs  # Área no plano XY
area_xz = x_diffs * z_diffs  # Área no plano XZ
area_yz = y_diffs * z_diffs  # Área no plano YZ

# Extraindo colunas dos dados
x = data[:, 7]  # Coordenadas X
y = data[:, 8]  # Coordenadas Y
z = data[:, 9]  # Coordenadas Z
r = data[:, 10] # Alguns dados relevantes
sum_r = np.sum(r)

# Volumes médios para o cálculo da densidade de potência
volume_i = np.mean(volume3_i)
volumes_i = np.full_like(r, volume_i)

rvij = volumes_i * np.sum(r)

# Cálculo da densidade de potência
power_density_i = ((r * P) / (rvij))  # [W/cm³]
avg_pwd = np.mean(power_density_i)
# Certificar-se de que a área tenha a mesma forma que a densidade de potência
area_xy_full = np.full_like(r, np.mean(area_xy))
area_xz_full = np.full_like(r, np.mean(area_xz))
area_yz_full = np.full_like(r, np.mean(area_yz))

# Cálculo da fluxo linear
linear_flux_xy = power_density_i * area_xy_full  # [W/cm]
linear_flux_xz = power_density_i * area_xz_full  # [W/cm]
linear_flux_yz = power_density_i * area_yz_full  # [W/cm]


# Imprimir os resultados máximos e formas de cada variável
variables = {
    "Nx": Nx,
    "Ny": Ny,
    "Nz": Nz,
    "power[W]": power,
    "inactives_cycles": incyc,
    "population": pop,
    "cycles": cyc,
    "x_diffs[cm]": x_diffs, 
    "y_diffs[cm]": y_diffs, 
    "z_diffs[cm]": z_diffs, 
    "volume3_i[cm³]": volume3_i, 
    "area_xy[cm²]": area_xy,
    "area_xz[cm²]": area_xz,
    "area_yz[cm²]": area_yz,
    "x[cm]": x, 
    "y[cm]": y, 
    "z[cm]": z, 
    "r": r,
    "power_density_i[W/cm³]": power_density_i,
    "average power_density[W/dm³]": avg_pwd,
    "linear_flux_xy[W/cm]": linear_flux_xy,
    "linear_flux_xz[W/cm]": linear_flux_xz,
    "linear_flux_yz[W/cm]": linear_flux_yz
}

for name, var in variables.items():
    if hasattr(var, 'shape'):
        print(f"{name} - shape: {var.shape}, max: {np.max(var)}, min: {np.min(var)}")
    else:
        print(f"{name} - value: {var}")

# Save the results to a text file
output_file = 'res_det.csv'
with open(output_file, 'w') as f:
    for name, var in variables.items():
        if hasattr(var, 'shape'):
            f.write(f"{name} - shape: {var.shape}, max: {np.max(var)}, min: {np.min(var)}\n")
        else:
            f.write(f"{name} - value: {var}\n")
    f.write('\n')

print(f'Results saved to {output_file}')

# Salvando o maior valor de power_density_i em cada ponto correspondente de z
unique_z = np.unique(z)
max_power_density_values = []

output_file_max = 'max_power_density_i.csv'
with open(output_file_max, 'w') as f:
    f.write(f"Z [cm],Max Power Density [W/cm³]\n")
    for z_val in unique_z:
        indices_z = np.where(z == z_val)
        max_power_density_at_z = np.max(power_density_i[indices_z])
        max_power_density_values.append((z_val, max_power_density_at_z))
        f.write(f"{z_val},{max_power_density_at_z}\n")

# Plotagem
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111, projection='3d')
scatter1 = ax1.scatter(x, y, power_density_i, c=power_density_i,cmap='jet', marker='.')
ax1.set_xlabel('Z [cm]')
ax1.set_ylabel('Y [cm]')
ax1.set_zlabel('Densidade de Potência [W/cm]')
fig1.colorbar(scatter1, ax=ax1, label='Densidade de Potência [W/cm]')
ax1.set_title('Distribuição de Densidade de Potência no Plano ZY')
# Adjusting the view to a top-down 2D view
ax1.view_init(elev=90, azim=-90)  # 90 degrees elevation and -90 degrees azimuth
plt.show()

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111, projection='3d')
scatter2 = ax2.scatter(y, z, power_density_i, c=power_density_i,cmap='jet', marker='.')
ax2.set_xlabel('X [cm]')
ax2.set_ylabel('Y [cm]')
ax2.set_zlabel('Densidade de Potência [W/cm]')
fig2.colorbar(scatter2, ax=ax2, label='Densidade de Potência [W/cm]')
ax2.set_title('Distribuição de Densidade de Potência no Plano XY')
# Adjusting the view to a top-down 2D view
ax2.view_init(elev=90, azim=-90)  # 90 degrees elevation and -90 degrees azimuth
plt.show()

'''
fig3 = plt.figure(3)
ax3 = fig3.add_subplot(111, projection='3d')
scatter3 = ax3.scatter(x, y, linear_flux_xy, c=linear_flux_xy, cmap='hot', marker='.')
ax3.set_xlabel('X [cm]')
ax3.set_ylabel('Y [cm]')
ax3.set_zlabel('Fluxo Linear XY [W/cm]')
fig3.colorbar(scatter3, ax=ax3, label='Fluxo Linear XY [W/cm]')
ax3.set_title('Distribuição de Fluxo Linear no Plano XY')
plt.show()

fig4 = plt.figure(4)
ax4 = fig4.add_subplot(111, projection='3d')
scatter4 = ax4.scatter(x, z, linear_flux_xz, c=linear_flux_xz/1e3, cmap='hot', marker='.')
ax4.set_xlabel('X [cm]')
ax4.set_ylabel('Z [cm]')
ax4.set_zlabel('Fluxo Linear XZ [W/cm]')
fig4.colorbar(scatter4, ax=ax4, label='Fluxo Linear XZ [kW/cm]')
ax4.set_title('Distribuição de Fluxo Linear no Plano XZ')
plt.show()

fig5 = plt.figure(5)
ax5 = fig5.add_subplot(111, projection='3d')
scatter5 = ax5.scatter(y, z, linear_flux_yz, c=linear_flux_yz/1e3, cmap='jet', marker='.')
ax5.set_xlabel('Y [cm]')
ax5.set_ylabel('Z [cm]')
ax5.set_zlabel('Fluxo Linear YZ [W/cm]')
fig5.colorbar(scatter5, ax=ax5, label='Fluxo Linear YZ [kW/cm]')
ax5.set_title('Distribuição de Fluxo Linear no Plano YZ')
plt.show()
'''

# Plotagem
plt.figure(figsize=(10, 6))
plt.plot(z, power_density_i, label='Densidade de Potência ao longo de Z')
plt.xlabel('Z [cm]')
plt.ylabel('Densidade de Potência [W/cm³]')
plt.title('Distribuição de Densidade de Potência ao longo do Eixo Z')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(x, power_density_i, label='Densidade de Potência ao longo de Z')
plt.xlabel('Z [cm]')
plt.ylabel('Densidade de Potência [W/cm³]')
plt.title('Distribuição de Densidade de Potência ao longo do Eixo Z')
plt.legend()
plt.grid(True)
plt.show()


