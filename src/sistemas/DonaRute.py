import numpy as np
import matplotlib.pyplot as plt
import control as ct
import sympy as sp


# Analise Simbolica de K____________________________________________

K_sym = sp.Symbol('K', real=True)
s_sym = sp.Symbol('s')

# Equacao caracteristica original: s^3 + 2s^2 + s + K = 0
poly_abs = s_sym**3 + 2*s_sym**2 + s_sym + K_sym

print(f"\nPolinomio caracteristico original: P(s) = {poly_abs}")
print("Linhas da Tabela de Routh:")
print("s^3 | 1, 1")
print("s^2 | 2, K")
print("s^1 | (2 - K)/2")
print("s^0 | K")
print("-> Condicões de Estabilidade Absoluta: 0 < K < 2 (K_crit = 2.0)\n")

# Substituicao para Estabilidade Relativa: s = s_hat - 0.25
s_hat = sp.Symbol('s_hat')
poly_rel = poly_abs.subs(s_sym, s_hat - 0.25).expand()
poly_rel_scaled = (poly_rel * 64).expand()

print(f"Polinomio deslocado (s = s_hat - 0.25) * 64:")
print(f"P_rel(s_hat) = {poly_rel_scaled}")
print("Linhas da Tabela de Routh Relativa:")
print("s_hat^3 | 64, 12")
print("s_hat^2 | 80, 64*K - 9")
print("s_hat^1 | 19.2 - 51.2*K")
print("s_hat^0 | 64*K - 9")
print("-> Condicões de Estabilidade Relativa: 0.140625 < K < 0.375\n")


# SIMULACAO DO SISTEMA EM MALHA FECHADA____________________________________________

# Definicao dos ganhos K
cases = [
    {
        "K": 0.25,
        "label": "K_robusto = 0.25 (Estabilidade Relativa)",
        "file_prefix": "k_robusto",
        "t_final": 20
    },
    {
        "K": 2.0,
        "label": "K_crit = 2.0 (Limite de Estabilidade)",
        "file_prefix": "k_critico",
        "t_final": 30
    },
    {
        "K": 3.0,
        "label": "K_instavel = 3.0 (Instavel)",
        "file_prefix": "k_instavel",
        "t_final": 15
    }
]


# Analise dos polos e resposta ao degrau____________________________________________

# Variavel Laplace da biblioteca control
s = ct.TransferFunction.s

for case in cases:
    K_val = case["K"]
    label = case["label"]
    t_final = case["t_final"]

    # Funcao de transferência em malha aberta: G(s) = K / (s * (s + 1)^2)
    G = K_val / (s * (s + 1)**2)
    
    # Funcao de transferência em malha fechada: T(s) = G(s) / (1 + G(s))
    T = ct.feedback(G, 1)

    poles = T.poles()
    print(f"\n--- Caso: {label} ---")
    print(f"Ganho K: {K_val}")
    print("Polos em malha fechada:")
    for p in poles:
        print(f"  p = {p.real:.4f} + {p.imag:.4f}j")

    plt.figure(figsize=(6, 5))
    ct.pole_zero_plot(T)
    
    # Reta vertical indicando a fronteira de estabilidade relativa (s = -0.25)
    plt.axvline(-0.25, color='red', linestyle='--', label=r'Fronteira $\sigma = -0.25$')
    plt.axvline(0, color='black', linestyle=':', alpha=0.7)
    plt.axhline(0, color='black', linestyle=':', alpha=0.7)
    
    plt.title(f"Mapa de Polos e Zeros\n({label})")
    plt.xlabel("Eixo Real (Re)")
    plt.ylabel("Eixo Imaginario (Im)")
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='upper right')
    plt.tight_layout()
    
    filename_pz = f"data/{case['file_prefix']}_pzmap.png"
    plt.savefig(filename_pz, dpi=300)
    print(f"Salvo: {filename_pz}")
    plt.close()




    plt.figure(figsize=(6, 5))
    t = np.linspace(0, t_final, 1000)
    t, y = ct.step_response(T, t)

    plt.plot(t, y, label=f'K = {K_val}', color='blue', linewidth=1.8)
    plt.axhline(1.0, color='black', linestyle='--', label='Referência (Degrau Unitario)')
    
    plt.title(f"Resposta ao Degrau Unitario\n({label})")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Saida y(t)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='best')
    plt.tight_layout()
    filename_step = f"data/{case['file_prefix']}_step.png"
    plt.savefig(filename_step, dpi=300)
    print(f"Salvo: {filename_step}")
    plt.close()
