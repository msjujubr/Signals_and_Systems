import matplotlib.pyplot as plt
import control.matlab as ctr
import numpy as np


# RESPOSTA AO DEGRAU - PRATICA 02 (Laboratorio de Teoria de Controle)
# Este laboratório tem como objetivo exercitar algumas funções para poder manipular funções de transferência.

num = 1; den = [4, 1]; G = ctr.tf(num, den); 


# Parâmetros do sistema resistor-capacitor 
R = 10e3       # 10 kΩ
C = 10e-6      # 10 µF
t = R * C    # t = 0.1 s

# Função de Transferência G(s)
# G(s) = 1 / (RC*s + 1)
numG = [1]
denG = [t, 1]
G = ctr.tf(numG, denG)

print("Função de Transferência Original G(s) ---")
print(G)

# Resposta ao degrau de G(s)
info_G = ctr.stepinfo(G)
print("\n--- stepinfo(G) ---")
for key, val in info_G.items():
    print(f"{key}: {val}")

# Função de Transferência do Compensador F(s) e Sistema Compensado T(s)
# F(s) = (0.1*s + 1) / (0.01*s + 1)
numF = [t, 1]
denF = [0.01, 1]
F = ctr.tf(numF, denF)


# T(s) = G(s) * F(s)
T = ctr.minreal(G * F)

print("\n--- Função de Transferência Compensada T(s) ---")
print(T)


# Resposta ao degrau de T(s)
info_T = ctr.stepinfo(T)
print("\n--- stepinfo(T) ---")
for key, val in info_T.items():
    print(f"{key}: {val}")


# Simulação da resposta ao degrau mantendo a mesma escala de tempo
yG, tG = ctr.step(G)
yT, tT = ctr.step(T, T=tG)  # Usa a mesma escala de tempo tG

# Verificação do nível de tensão em t = t (esperado ~63.2%)
idx_t = np.argmin(np.abs(tG - t))
print(f"\nNível de tensão em t = t ({t} s) para G(s): {yG[idx_t]*100:.2f}%")

# Plotagem do gráfico comparativo
plt.figure(figsize=(10, 5))
plt.plot(tG, yG, 'b-', label='Sistema Original G(s)', linewidth=2)
plt.plot(tG, yT, 'r--', label='Sistema Compensado T(s)', linewidth=2)
plt.axvline(x=t, color='gray', linestyle=':', label=f't = $\\t$ ({t}s)')
plt.axhline(y=yG[idx_t], color='gray', linestyle=':')

plt.title('Resposta ao Degrau: Sistema Original G(s) vs. Compensado T(s)')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude / Tensão')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('data/grafico_resposta.png', dpi=300)
print("Gráfico salvo como 'grafico_resposta.png'")