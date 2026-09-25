import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Configurações visuais dos gráficos para estilo acadêmico
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.autolayout': True
})


print("--- 1. Sistema Tipo 0 (Degrau) ---")

# Definição dos Vetores de Tempo
t = np.linspace(0, 2, 2000)
r_step = np.ones_like(t)  # Degrau Unitário

# G0(s) = 10 / (s + 2) -> T0(s) = G0/(1+G0) = 10 / (s + 12)
num_T0 = [10]
den_T0 = [1, 12]
sys_T0 = signal.TransferFunction(num_T0, den_T0)

# G_extra(s) = 100 / (s + 2) -> T_extra(s) = 100 / (s + 102)
num_Textra = [100]
den_Textra = [1, 102]
sys_Textra = signal.TransferFunction(num_Textra, den_Textra)

# Simulações no domínio do tempo
_, y_T0, _ = signal.lsim(sys_T0, U=r_step, T=t)
_, y_Textra, _ = signal.lsim(sys_Textra, U=r_step, T=t)

# Sinal de Erro: e(t) = r(t) - y(t)
e_T0 = r_step - y_T0
e_Textra = r_step - y_Textra

print(f"Erro em regime (K=10)  -> Teórico: {1/6:.4f} | Simulado: {e_T0[-1]:.4f}")
print(f"Erro em regime (K=100) -> Teórico: {1/51:.4f} | Simulado: {e_Textra[-1]:.4f}\n")

# Plota Gráficos da Seção 1
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Subplot 1: Resposta ao Degrau
ax1.plot(t, r_step, 'k--', label='Referência $r(t) = 1$')
ax1.plot(t, y_T0, 'b-', label='Saída $y(t)$ ($K=10$)')
ax1.plot(t, y_Textra, 'r-', label='Saída $y(t)$ ($K=100$)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Resposta ao Degrau Unitário - Sistema Tipo 0')
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend(loc='lower right')

# Subplot 2: Sinal de Erro
ax2.plot(t, e_T0, 'b-', label='Erro $e(t)$ ($K=10$)')
ax2.plot(t, e_Textra, 'r-', label='Erro $e(t)$ ($K=100$)')
ax2.axhline(1/6, color='b', linestyle=':', alpha=0.7, label='Limit $e_{ss}=0.1667$')
ax2.axhline(1/51, color='r', linestyle=':', alpha=0.7, label='Limit $e_{ss}=0.0196$')
ax2.set_xlabel('Tempo (s)')
ax2.set_ylabel('Erro $e(t)$')
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend(loc='upper right')

plt.savefig('data/simulacao_tipo0_ganhos.png', dpi=300)
plt.close()


print("--- 2. Sistema Tipo 0 (Rampa) ---")

# Ajuste do tempo para visualização da divergência do erro
t_rampa = np.linspace(0, 5, 5000)
r_ramp = t_rampa  # Entrada Rampa Unitária r(t) = t

# Simulação com G0(s)
_, y_ramp_T0, _ = signal.lsim(sys_T0, U=r_ramp, T=t_rampa)
e_ramp_T0 = r_ramp - y_ramp_T0

print(f"Erro ao final da simulação (t=5s): {e_ramp_T0[-1]:.4f} (Divergindo para inf)\n")

# Plota Gráficos da Seção 2
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

ax1.plot(t_rampa, r_ramp, 'k--', label='Rampa $r(t) = t$')
ax1.plot(t_rampa, y_ramp_T0, 'b-', label='Saída $y(t)$ ($G_0(s)$)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Resposta à Rampa Unitária - Sistema Tipo 0 ($K=10$)')
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend(loc='upper left')

ax2.plot(t_rampa, e_ramp_T0, 'm-', label='Erro $e(t) = r(t) - y(t)$')
ax2.set_xlabel('Tempo (s)')
ax2.set_ylabel('Erro $e(t)$')
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend(loc='upper left')

plt.savefig('data/simulacao_tipo0_rampa.png', dpi=300)
plt.close()


print("--- 3. Sistema Tipo 1 (Degrau e Rampa) ---")

# G1(s) = 10 / (s^2 + 2s) -> T1(s) = 10 / (s^2 + 2s + 10)
num_T1 = [10]
den_T1 = [1, 2, 10]
sys_T1 = signal.TransferFunction(num_T1, den_T1)

# Simulação Degrau
t_deg_t1 = np.linspace(0, 3, 3000)
r_deg_t1 = np.ones_like(t_deg_t1)
_, y_deg_T1, _ = signal.lsim(sys_T1, U=r_deg_t1, T=t_deg_t1)
e_deg_T1 = r_deg_t1 - y_deg_T1

# Simulação Rampa
t_ramp_t1 = np.linspace(0, 5, 5000)
r_ramp_t1 = t_ramp_t1
_, y_ramp_T1, _ = signal.lsim(sys_T1, U=r_ramp_t1, T=t_ramp_t1)
e_ramp_T1 = r_ramp_t1 - y_ramp_T1

print(f"Erro Degrau Tipo 1 -> Teórico: 0.0000 | Simulado: {e_deg_T1[-1]:.4f}")
print(f"Erro Rampa  Tipo 1 -> Teórico: {1/5:.4f} | Simulado: {e_ramp_T1[-1]:.4f}\n")

# Plota Gráficos da Seção 3
fig, axes = plt.subplots(2, 2, figsize=(10, 6))

# Subplot 1: Resposta ao Degrau (Tipo 1)
axes[0, 0].plot(t_deg_t1, r_deg_t1, 'k--', label='Ref $r(t)=1$')
axes[0, 0].plot(t_deg_t1, y_deg_T1, 'g-', label='Saída $y(t)$')
axes[0, 0].set_title('Entrada Degrau - Sistema Tipo 1')
axes[0, 0].set_ylabel('Amplitude')
axes[0, 0].grid(True, linestyle=':', alpha=0.7)
axes[0, 0].legend()

# Subplot 2: Erro ao Degrau (Tipo 1)
axes[1, 0].plot(t_deg_t1, e_deg_T1, 'g-', label='Erro $e(t)$')
axes[1, 0].axhline(0, color='k', linestyle=':', alpha=0.5)
axes[1, 0].set_xlabel('Tempo (s)')
axes[1, 0].set_ylabel('Erro $e(t)$')
axes[1, 0].grid(True, linestyle=':', alpha=0.7)
axes[1, 0].legend()

# Subplot 3: Resposta à Rampa (Tipo 1)
axes[0, 1].plot(t_ramp_t1, r_ramp_t1, 'k--', label='Ref $r(t)=t$')
axes[0, 1].plot(t_ramp_t1, y_ramp_T1, 'c-', label='Saída $y(t)$')
axes[0, 1].set_title('Entrada Rampa - Sistema Tipo 1')
axes[0, 1].grid(True, linestyle=':', alpha=0.7)
axes[0, 1].legend()

# Subplot 4: Erro à Rampa (Tipo 1)
axes[1, 1].plot(t_ramp_t1, e_ramp_T1, 'c-', label='Erro $e(t)$')
axes[1, 1].axhline(0.2, color='r', linestyle=':', label='Lim $e_{ss}=0.2$')
axes[1, 1].set_xlabel('Tempo (s)')
axes[1, 1].grid(True, linestyle=':', alpha=0.7)
axes[1, 1].legend()

plt.savefig('data/simulacao_tipo1_degrau_rampa.png', dpi=300)
plt.close()

print("Simulações concluídas e gráficos salvos com sucesso!")