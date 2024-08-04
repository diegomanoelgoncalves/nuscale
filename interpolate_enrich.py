import numpy as np
import matplotlib.pyplot as plt

# Dados de entrada
u235_wt = np.array([1.50, 1.60, 2.50, 2.60, 4.05, 4.55, 2.60])

# Limites de UO2 para as duas regiões
uo2_limits_region1 = (17,20)  # Região 1: UO2% variando de 12% a 20%
uo2_limits_region2 = (16,20)   # Região 2: UO2% variando de 0% a 10%

# Função para interpolar valores de UO2%
def interpolate_uo2(u235_values, uo2_limits):
    u235_min, u235_max = min(u235_values), max(u235_values)
    uo2_min, uo2_max = uo2_limits

    # Interpolação linear
    uo2_values = uo2_min + (u235_values - u235_min) * (uo2_max - uo2_min) / (u235_max - u235_min)
    return uo2_values

# Função para calcular ThO2% baseado na combinação máxima de UO2 e ThO2
def calculate_tho2(uo2_values, max_combined_uo2):
    tho2_values = max_combined_uo2 - uo2_values
    return tho2_values

# Interpolar valores de UO2 para a Região 1
uo2_values_region1 = interpolate_uo2(u235_wt, uo2_limits_region1)

# Interpolar valores de UO2 para a Região 2
uo2_values_region2 = interpolate_uo2(u235_wt, uo2_limits_region2)
tho2_values_region2 = calculate_tho2(uo2_values_region2, 100)  # ThO2 varia de 90% a 100%

# Exibir os resultados
print("Região 1: Interpolação de UO2% para valores de U-235 wt% (12% a 20% UO2):")
for i in range(len(u235_wt)):
    print(f"U-235 wt%: {u235_wt[i]:.2f} -> UO2%: {uo2_values_region1[i]:.2f}")

print("\nRegião 2: Valores combinados de UO2% e ThO2% (0% a 10% UO2 + 90% a 100% ThO2):")
for i in range(len(u235_wt)):
    print(f"U-235 wt%: {u235_wt[i]:.2f} -> UO2%: {uo2_values_region2[i]:.2f}, ThO2%: {tho2_values_region2[i]:.2f}")

# Plotar os resultados
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(u235_wt, uo2_values_region1, 'bo-', label='UO2% Região 1')
plt.xlabel('U-235 wt%')
plt.ylabel('Concentração (%)')
plt.title('Região 1: Interpolação de UO2% (12% a 20% UO2)')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(u235_wt, uo2_values_region2, 'bo-', label='UO2% Região 2')
plt.plot(u235_wt, tho2_values_region2, 'ro-', label='ThO2% Região 2')
plt.xlabel('U-235 wt%')
plt.ylabel('Concentração (%)')
plt.title('Região 2: Valores combinados de UO2% e ThO2% (0% a 10% UO2 + 90% a 100% ThO2)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
