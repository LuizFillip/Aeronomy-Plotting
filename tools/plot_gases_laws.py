# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 10:51:50 2024

@author: Luiz
"""

import numpy as np
import matplotlib.pyplot as plt


def isotermas():
    # Constante universal dos gases
    R = 8.314  # J/(mol·K)
    
    # Parâmetros iniciais
    n = 1.0  # número de mols
    temperaturas = [300, 400, 500]  # temperaturas em Kelvin
    volumes = np.linspace(0.1, 10, 100)  # volumes em litros
    
    # Converter volume para m³ (1 litro = 0.001 m³)
    volumes_m3 = volumes * 0.001
    
    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    
    for T in temperaturas:
        # Calcular pressão para cada temperatura
        pressao = (n * R * T) / volumes_m3
        plt.plot(volumes, pressao, label=f"T = {T} K")
    
    # Configurações do gráfico
    plt.title("Gráfico $p \\times V$ para Gases Ideais", fontsize=16)
    plt.xlabel("Volume (L)", fontsize=14)
    plt.ylabel("Pressão (Pa)", fontsize=14)
    plt.yscale("log")  # Escala logarítmica para pressão
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # Exibir o gráfico
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Constante universal dos gases
R = 8.314  # J/(mol·K)

# Parâmetros iniciais
n = 1.0  # número de mols
T_isotermicas = [300, 400]  # temperaturas para transformações isotérmicas (K)
P_isobaricas = [101325, 202650]  # pressões para transformações isobáricas (Pa)
V_isocoricas = [2, 5]  # volumes fixos para transformações isocóricas (L)

# Intervalo de volume e pressão
volumes = np.linspace(0.1, 10, 100)  # volumes em litros
volumes_m3 = volumes * 0.001  # converter para m³
pressao = np.linspace(1e4, 2.5e5, 100)  # pressão em Pa

# Criar o gráfico
plt.figure(figsize=(10, 6))

# Transformações isotérmicas
for T in T_isotermicas:
    p_isotermica = (n * R * T) / volumes_m3
    plt.plot(volumes, p_isotermica, label=f"Isotérmica (T={T} K)", linestyle="-")

# Adicionar setas para isotérmicas
for T in T_isotermicas:
    p_isotermica = (n * R * T) / volumes_m3
    for i in range(10, len(volumes), 30):  # Adicionar algumas setas
        plt.annotate("", xy=(volumes[i + 1], p_isotermica[i + 1]),
                     xytext=(volumes[i], p_isotermica[i]),
                     arrowprops=dict(arrowstyle="->", color="blue", lw=1.5))

# Transformações isobáricas
for P in P_isobaricas:
    V_isobarica = (n * R * T_isotermicas[0]) / P  # volume correspondente a T inicial
    plt.hlines(P, min(volumes), max(volumes), label=f"Isobárica (P={P} Pa)", linestyle="--", color="orange")

# Adicionar setas para isobáricas
for P in P_isobaricas:
    plt.annotate("", xy=(5, P), xytext=(2, P),
                 arrowprops=dict(arrowstyle="->", color="orange", lw=1.5))

# Transformações isocóricas
for V in V_isocoricas:
    p_isocorica = (n * R * pressao) / (V * 0.001)  # pressão em função de temperatura
    plt.vlines(V, min(pressao), max(pressao), label=f"Isocórica (V={V} L)", linestyle=":", color="green")

# Adicionar setas para isocóricas
for V in V_isocoricas:
    plt.annotate("", xy=(V, 1.5e5), xytext=(V, 1e5),
                 arrowprops=dict(arrowstyle="->", color="green", lw=1.5))

# Configurações do gráfico
plt.title("Transformações Termodinâmicas: $p \\times V$", fontsize=16)
plt.xlabel("Volume (L)", fontsize=14)
plt.ylabel("Pressão (Pa)", fontsize=14)
plt.yscale("log")  # Escala logarítmica para pressão
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend(fontsize=12)
plt.tight_layout()

# Exibir o gráfico
plt.show()
