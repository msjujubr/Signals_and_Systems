import os
import numpy as np
import matplotlib.pyplot as plt

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)


# Filtro passa-baixa 
def bandpass(w, wn, a, k):
    s = 1j * w
    return k * s / (s**2 + a * s + wn**2)


# Magnitude em decibéis
def magnitude_db(H):
    return 20 * np.log10(np.abs(H))


def phase_deg(H):
    return np.angle(H, deg=True)


def plot_bode(w, H, titulo, marcacoes=None, filename=None):
    mag = magnitude_db(H)
    fase = np.unwrap(np.angle(H)) * 180 / np.pi

    fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Magnitude 
    ax[0].semilogx(w, mag, linewidth=2)
    ax[0].set_title(titulo)
    ax[0].set_ylabel("Magnitude (dB)")
    ax[0].grid(True, which="both", linestyle="--", alpha=0.6)

    # Linha de referencia de 0 dB
    ax[0].axhline(0, linestyle="--", linewidth=1)

    # Fase     
    ax[1].semilogx(w, fase, linewidth=2)
    ax[1].set_xlabel(r"Frequencia $\omega$ (rad/s)")
    ax[1].set_ylabel("Fase (graus)")
    ax[1].grid(True, which="both", linestyle="--", alpha=0.6)

    if marcacoes is not None:
        for ponto in marcacoes:
            ax[0].axvline(ponto, linestyle=":", linewidth=1)
            ax[1].axvline(ponto, linestyle=":", linewidth=1)

    plt.tight_layout()
    
    if filename:
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches="tight")
        print(f"Figura salva em: {filepath}")

    plt.show()


# Sistema Original (G1)
wn1 = 10       # frequencia central
a1 = 5
k1 = 10

# Faixa de frequencias
w = np.logspace(-1, 3, 5000)

# Resposta em frequencia
G1 = bandpass(w, wn1, a1, k1)


# Frequencias
w_maior = 10   # |G1(jw)| > 1


# |G1(jw)| = 1
x1 = (275 - np.sqrt(35625)) / 2
x2 = (275 + np.sqrt(35625)) / 2
w_igual_1 = np.sqrt(x1)
w_igual_2 = np.sqrt(x2)


w_menor = 20 # |G1(jw)| < 1


# Valores nos pontos
pontos = [w_maior, w_igual_1, w_menor]

w0 = 10 # freq central

# O ganho máximo ocorre em ω0
G1_max = abs(bandpass(w0, wn1, a1, k1))

xL = (225 - np.sqrt(10625)) / 2
xH = (225 + np.sqrt(10625)) / 2

wL = np.sqrt(xL)
wH = np.sqrt(xH)

print("PARAMETROS G1")
print(f"Frequencia central ω0 = {w0:.6f} rad/s")
print(f"Ganho máximo           = {G1_max:.6f}")
print(f"Ganho máximo           = {magnitude_db(G1_max):.6f} dB")
print(f"Frequencia de corte ωL = {wL:.6f} rad/s")
print(f"Frequencia de corte ωH = {wH:.6f} rad/s")


plot_bode(w, G1, r"Diagrama de Bode - $G_1(s)=\frac{10s}{s^2+5s+100}$", marcacoes=[wL, w0, wH], filename="bode_g1.png")
plt.figure(figsize=(10, 6))
plt.semilogx(w, magnitude_db(G1), linewidth=2, label=r"$G_1(s)$")


# Linha de 0 dB
plt.axhline(0, linestyle="--", linewidth=1, label="0 dB")

# Pontos utilizados
for freq in pontos:
    H = bandpass(freq, wn1, a1, k1)
    plt.scatter(freq, magnitude_db(H), s=70, zorder=5)
    plt.annotate(f"ω = {freq:.2f}", (freq, magnitude_db(H)), xytext=(8, 8), textcoords="offset points")


plt.xlabel(r"Frequencia $\omega$ (rad/s)")
plt.ylabel("Magnitude (dB)")
plt.title("Pontos analisados de G1")
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()

# Salvando a figura dos pontos em data/
filepath_pontos = os.path.join(output_dir, "pontos_g1.png")
plt.savefig(filepath_pontos, dpi=300, bbox_inches="tight")
print(f"Figura salva em: {filepath_pontos}")





# Segundo Filtro

wn2 = 100
a2 = 50

# a) sem compensacao de ganho
k2_simples = 1
G2_simples = bandpass(w, wn2, a2, k2_simples)
G_cascata_simples = G1 * G2_simples

plot_bode(w, G_cascata_simples, "Cascata: G1(s) × G2(s) sem compensacao", filename="bode_cascata_simples.png")

# duas faixas de passagem
G1_em_100 = abs(bandpass(100, wn1, a1, k1))
k2_corrigido = 50 / G1_em_100

G2_corrigido = bandpass(w, wn2, a2, k2_corrigido)
G_cascata_corrigida = G1 * G2_corrigido



mag_corrigida_db = magnitude_db(G_cascata_corrigida)

# Regiao considerada faixa de passagem
passa = mag_corrigida_db >= -3

# Detectar mudancas entre fora/dentro da faixa
mudancas = np.where(np.diff(np.concatenate(([False], passa, [False])).astype(int)) != 0)[0]
intervalos = []

for i in range(0, len(mudancas), 2):
    inicio = mudancas[i]
    fim = mudancas[i + 1] - 1

    intervalos.append((w[inicio], w[fim]))



fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

mag = magnitude_db(G_cascata_corrigida)
fase = np.unwrap(np.angle(G_cascata_corrigida)) * 180 / np.pi

# Magnitude 
ax[0].semilogx(w, mag, linewidth=2, label="Sistema corrigido")

# Linha de -3 dB
ax[0].axhline(-3, linestyle="--", linewidth=1, label="-3 dB")

# Frequencias dos filtros
ax[0].axvline(10, linestyle=":", linewidth=1, label=r"$\omega_0=10$ rad/s")
ax[0].axvline(100,linestyle=":", linewidth=1, label=r"$\omega=100$ rad/s")

ax[0].set_ylabel("Magnitude (dB)")
ax[0].set_title("Sistema corrigido - Duas faixas de passagem"
)

ax[0].grid(True, which="both", linestyle="--", alpha=0.6)
ax[0].legend()


# Fase 
ax[1].semilogx(w, fase, linewidth=2
)

ax[1].set_xlabel(r"Frequencia $\omega$ (rad/s)")
ax[1].set_ylabel("Fase (graus)")

ax[1].grid(True, which="both", linestyle="--", alpha=0.6)

plt.tight_layout()


filepath_corrigido = os.path.join(output_dir, "bode_cascata_corrigida.png")
plt.savefig(filepath_corrigido, dpi=300, bbox_inches="tight")


# comparacao
plt.figure(figsize=(11, 7))

plt.semilogx(w, magnitude_db(G1), linewidth=2, label="G1 original")

plt.semilogx(w, magnitude_db(G_cascata_simples), linewidth=2, label="Cascata sem compensacao")

plt.semilogx(w, magnitude_db(G_cascata_corrigida), linewidth=2, label="Cascata corrigida")

plt.axhline(-3, linestyle="--", linewidth=1, label="-3 dB")

plt.xlabel(r"Frequencia $\omega$ (rad/s)")
plt.ylabel("Magnitude (dB)")
plt.title("Comparacao dos sistemas")
plt.grid(True, which="both", linestyle="--", alpha=0.6)

plt.legend()
plt.tight_layout()

# Salvando a figura de comparacao em data/
filepath_comp = os.path.join(output_dir, "comparacao_sistemas.png")
plt.savefig(filepath_comp, dpi=300, bbox_inches="tight")
print(f"Figura salva em: {filepath_comp}")


print("RESULTADOS")
print("\nG1(s):")
print("  G1(s) = 10s / (s² + 5s + 100)")
print(f"  ω0 = {w0:.4f} rad/s")
print(f"  ωL = {wL:.4f} rad/s")
print(f"  ωH = {wH:.4f} rad/s")

print("\nPontos da questao:")
print(f"  |G1| > 1 : ω = {w_maior:.4f} rad/s")
print(f"  |G1| = 1 : ω = {w_igual_1:.4f} rad/s")
print(f"  |G1| < 1 : ω = {w_menor:.4f} rad/s")

print("\nFiltro adicional:")
print(f"  G2(s) = {k2_corrigido:.4f}s / ""(s² + 50s + 10000)")

print("\nObjetivo:")
print("  Duas faixas de passagem acima de -3 dB.")