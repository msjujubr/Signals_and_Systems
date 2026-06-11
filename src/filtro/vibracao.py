import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

f1 = 50    # principal
f2 = 100   # harmonica
f3 = 200   # ruido

A1 = 1.2
A2 = 0.6
A3 = 0.3

L = 2000   # amostras

# frequencias de amostragem
Fs_lista = [300, 500, 1000, 1500, 2000]



# sinal original
fig1, axs = plt.subplots(5, 1, figsize=(10, 12))

for i, Fs in enumerate(Fs_lista):
    T = 1 / Fs
    t = np.arange(L) * T

    x = (A1 * np.sin(2 * np.pi * f1 * t) +
         A2 * np.sin(2 * np.pi * f2 * t) +
         A3 * np.sin(2 * np.pi * f3 * t))

    axs[i].plot(t, x, '-o', markersize=2)
    axs[i].set_title(f'Sinal Original Composto - Fs = {Fs} Hz')
    axs[i].set_xlabel('Tempo (s)')
    axs[i].set_ylabel('Amplitude')
    axs[i].set_xlim(0, 0.1)
    axs[i].grid(True)

fig1.tight_layout()



# 50Hz
fig2, axs = plt.subplots(5, 1, figsize=(10, 12))

for i, Fs in enumerate(Fs_lista):
    T = 1 / Fs
    t = np.arange(L) * T

    x1 = A1 * np.sin(2 * np.pi * f1 * t)

    axs[i].plot(t, x1, '-o', markersize=2)
    axs[i].set_title(f'Componente 50 Hz - Fs = {Fs} Hz')
    axs[i].set_xlabel('Tempo (s)')
    axs[i].set_ylabel('Amplitude')
    axs[i].set_xlim(0, 0.1)
    axs[i].grid(True)

fig2.tight_layout()



# 100Hz
fig3, axs = plt.subplots(5, 1, figsize=(10, 12))

for i, Fs in enumerate(Fs_lista):
    T = 1 / Fs
    t = np.arange(L) * T

    x2 = A2 * np.sin(2 * np.pi * f2 * t)

    axs[i].plot(t, x2, '-o', markersize=2)
    axs[i].set_title(f'Componente 100 Hz - Fs = {Fs} Hz')
    axs[i].set_xlabel('Tempo (s)')
    axs[i].set_ylabel('Amplitude')
    axs[i].set_xlim(0, 0.1)
    axs[i].grid(True)

fig3.tight_layout()



# 200Hz
fig4, axs = plt.subplots(5, 1, figsize=(10, 12))

for i, Fs in enumerate(Fs_lista):
    T = 1 / Fs
    t = np.arange(L) * T

    x3 = A3 * np.sin(2 * np.pi * f3 * t)

    axs[i].plot(t, x3, '-o', markersize=2)
    axs[i].set_title(f'Componente 200 Hz (Ruído) - Fs = {Fs} Hz')
    axs[i].set_xlabel('Tempo (s)')
    axs[i].set_ylabel('Amplitude')
    axs[i].set_xlim(0, 0.1)
    axs[i].grid(True)

fig4.tight_layout()

figuras = [
    (fig1, "figura1_sinal_original.png"),
    (fig2, "figura2_componente_50Hz.png"),
    (fig3, "figura3_componente_100Hz.png"),
    (fig4, "figura4_componente_200Hz.png"),
]

for fig, nome in figuras:
    fig.savefig(output_dir / nome, dpi=300, bbox_inches="tight")

plt.close('all')

print("Figuras geradas com sucesso:")
for _, nome in figuras:
    print(f" - data/{nome}")
