import control as ctl
import matplotlib.pyplot as plt
import numpy as np

# Configuracao de estilo para os graficos
plt.style.use(
    'seaborn-v0_8-whitegrid'
    if 'seaborn-v0_8-whitegrid' in plt.style.available
    else 'default'
)

# Sistemas em Cascata


# Definicao das funcões de transferencia G_A e G_B
# G_A(j_omega) = 1 / (1 + j_omega / 20) -> G_A(s) = 1 / (1 + s / 20)
num_a = [1]
den_a = [1/20, 1]
GA = ctl.TransferFunction(num_a, den_a)

# G_B(j_omega) = 1 + j_omega / 200 -> G_B(s) = 1 + s / 200
num_b = [1/200, 1]
den_b = [1]
GB = ctl.TransferFunction(num_b, den_b)

# Associacao em cascata: G_CASCATA = G_A * G_B
GCascata = GA * GB

# Vetor de frequencias (omega) de 0.1 a 10000 rad/s em escala logarítmica
omega = np.logspace(-1, 4, 1000)

# Calculando a resposta em frequencia para os tres sistemas
mag_a, phase_a, omega_out = ctl.bode_plot(GA, omega, Hz=False, dB=True, plot=False)
mag_b, phase_b, _ = ctl.bode_plot(GB, omega, Hz=False, dB=True, plot=False)
mag_c, phase_c, _ = ctl.bode_plot(GCascata, omega, Hz=False, dB=True, plot=False)

# Convertendo magnitude para Decibeis (dB) para analises numericas
mag_a_dB = 20 * np.log10(mag_a)
mag_b_dB = 20 * np.log10(mag_b)
mag_c_dB = 20 * np.log10(mag_c)

# Exemplo de verificacao de pontos na mesma frequencia (ex: omega = 10 rad/s)
idx = np.argmin(np.abs(omega_out - 10))
print(f"Para w = {omega_out[idx]:.2f} rad/s:")
print(f"  |GA| (dB) = {mag_a_dB[idx]:.2f} dB")
print(f"  |GB| (dB) = {mag_b_dB[idx]:.2f} dB")
print(f"  |GCascata| (dB) = {mag_c_dB[idx]:.2f} dB (Soma em dB: {mag_a_dB[idx] + mag_b_dB[idx]:.2f} dB)")


# Projeto de um Sistema por Bode
# Especificacões do projeto:
# 1. De omega = 0 ate omega = 10: magnitude = -20 dB -> Ganho K = 0.1 (-20 dB)
# 2. De omega = 10 ate omega = 1000: rampa de subida de +20 dB/dec -> Zero em omega = 10
# 3. De omega = 1000 em diante: rampa de descida de -20 dB/dec -> Dois polos em omega = 1000 
#    (para transacionar de uma inclinacao de +20 dB/dec para -20 dB/dec, precisamos de uma queda líquida de -40 dB/dec).

K = 0.1  # Ganho inicial (-20 dB)
sys_K = ctl.TransferFunction([K], [1])
sys_zero = ctl.TransferFunction([1/10, 1], [1])          # Zero em w = 10
sys_polo1 = ctl.TransferFunction([1], [1/1000, 1])       # 1º Polo em w = 1000
sys_polo2 = ctl.TransferFunction([1], [1/1000, 1])       # 2º Polo em w = 1000

# Funcao de transferencia total projetada
G_projeto = sys_K * sys_zero * sys_polo1 * sys_polo2

print("Funcao de Transferencia Projetada G(s):")
print(G_projeto)


# GRAFICOS

# Grafico 1: Sistemas em Cascata
plt.figure(figsize=(10, 8))
plt.suptitle("Diagramas de Bode - Sistemas em Cascata", fontsize=14)

plt.subplot(2, 1, 1)
plt.semilogx(omega_out, mag_a_dB, label='GA(jω)', linestyle='--')
plt.semilogx(omega_out, mag_b_dB, label='GB(jω)', linestyle='-.')
plt.semilogx(omega_out, mag_c_dB, label='GCascata(jω)', linewidth=2)
plt.ylabel('Magnitude (dB)')
plt.title('Diagrama de Magnitude')
plt.legend()
plt.grid(True, which="both", ls="--")

plt.subplot(2, 1, 2)
plt.semilogx(omega_out, np.degrees(phase_a), label='GA(jω)', linestyle='--')
plt.semilogx(omega_out, np.degrees(phase_b), label='GB(jω)', linestyle='-.')
plt.semilogx(omega_out, np.degrees(phase_c), label='GCascata(jω)', linewidth=2)
plt.ylabel('Fase (graus)')
plt.xlabel('Frequência (rad/s)')
plt.title('Diagrama de Fase')
plt.legend()
plt.grid(True, which="both", ls="--")

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Salvar o grafico em PNG
plt.savefig("bode_sistemas_cascata.png", dpi=300, bbox_inches="tight")
plt.close()


# Grafico 2: Sistema Projetado

# Obter os dados da resposta em frequência sem exibir o grafico
mag_p, phase_p, omega_p = ctl.bode_plot(
    G_projeto,
    omega,
    Hz=False,
    dB=True,
    plot=False
)

# Converter magnitude para decibéis
mag_p_dB = 20 * np.log10(mag_p)

plt.figure(figsize=(10, 8))
plt.suptitle("Diagrama de Bode - Sistema Projetado (Seção 3)", fontsize=14)

plt.subplot(2, 1, 1)
plt.semilogx(omega_p, mag_p_dB, label='G_projeto(jω)')
plt.ylabel('Magnitude (dB)')
plt.title('Diagrama de Magnitude')
plt.legend()
plt.grid(True, which="both", ls="--")

plt.subplot(2, 1, 2)
plt.semilogx(omega_p, np.degrees(phase_p), label='G_projeto(jω)')
plt.ylabel('Fase (graus)')
plt.xlabel('Frequência (rad/s)')
plt.title('Diagrama de Fase')
plt.legend()
plt.grid(True, which="both", ls="--")

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Salvar o grafico em PNG
plt.savefig("bode_sistema_projetado.png", dpi=300, bbox_inches="tight")
plt.close()

print("Graficos salvos com sucesso:")
print("- bode_sistemas_cascata.png")
print("- bode_sistema_projetado.png")