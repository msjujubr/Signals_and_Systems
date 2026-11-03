from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

PASTA_SAIDA = Path("resultados_pratica11")
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

# G(s) = 10 / (s^3 + 6s^2 + 11s + 6)
NUM_BASE = [10.0]
DEN = [1.0, 6.0, 11.0, 6.0]

# Aproxima as frequências em que y cruza o valor alvo
def cruzamentos(x, y, alvo):  
    indices = np.where((y[:-1] - alvo) * (y[1:] - alvo) <= 0)[0]
    pontos = []
    for i in indices:
        if y[i + 1] == y[i]:
            log_x = np.log10(x[i])
        else:
            frac = (alvo - y[i]) / (y[i + 1] - y[i])
            log_x = np.log10(x[i]) + frac * (
                np.log10(x[i + 1]) - np.log10(x[i])
            )
        pontos.append(10 ** log_x)
    return pontos


# Gera o diagrama de Bode e marca as margens para ganho 10
def gerar_bode(): 
    K = 10.0
    num = [K * valor for valor in NUM_BASE]
    sistema = signal.TransferFunction(num, DEN)

    w = np.logspace(-2, 3, 3000)
    w, magnitude_db, fase_graus = signal.bode(sistema, w=w)

    fig, (ax_mag, ax_fase) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax_mag.semilogx(w, magnitude_db, linewidth=2)
    ax_mag.axhline(0, linestyle="--", linewidth=1, label="0 dB")
    ax_mag.set_title("Diagrama de Bode — K = 10")
    ax_mag.set_ylabel("Magnitude (dB)")
    ax_mag.grid(True, which="both", linestyle=":")
    ax_mag.legend()

    ax_fase.semilogx(w, fase_graus, linewidth=2)
    ax_fase.axhline(-180, linestyle="--", linewidth=1, label="−180°")
    ax_fase.set_xlabel("Frequência (rad/s)")
    ax_fase.set_ylabel("Fase (graus)")
    ax_fase.grid(True, which="both", linestyle=":")
    ax_fase.legend()

    cruzamento_ganho = cruzamentos(w, magnitude_db, 0.0)
    cruzamento_fase = cruzamentos(w, fase_graus, -180.0)

    if cruzamento_ganho:
        wg = cruzamento_ganho[0]
        fase_wg = np.interp(np.log10(wg), np.log10(w), fase_graus)
        margem_fase = 180.0 + fase_wg
        ax_mag.plot(wg, 0, "o")
        ax_fase.plot(wg, fase_wg, "o")
        ax_fase.annotate(
            f"MF ≈ {margem_fase:.1f}°",
            xy=(wg, fase_wg),
            xytext=(wg * 1.35, fase_wg + 18),
            arrowprops={"arrowstyle": "->"},
        )
    else:
        margem_fase = np.inf

    if cruzamento_fase:
        wp = cruzamento_fase[0]
        mag_wp = np.interp(np.log10(wp), np.log10(w), magnitude_db)
        margem_ganho_db = -mag_wp
        margem_ganho = 10 ** (margem_ganho_db / 20.0)
        ax_mag.plot(wp, mag_wp, "o")
        ax_mag.annotate(
            f"MG ≈ {margem_ganho_db:.1f} dB",
            xy=(wp, mag_wp),
            xytext=(wp * 1.25, mag_wp + 12),
            arrowprops={"arrowstyle": "->"},
        )
    else:
        margem_ganho_db = np.inf
        margem_ganho = np.inf

    fig.tight_layout()
    caminho = PASTA_SAIDA / "bode_K10.png"
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print("\\nMargens aproximadas para K = 10:")
    print(f"Margem de fase: {margem_fase:.3f} graus")
    print(f"Margem de ganho: {margem_ganho_db:.3f} dB")
    if cruzamento_ganho:
        print(f"Frequência de cruzamento de ganho: {cruzamento_ganho[0]:.5f} rad/s")
    if cruzamento_fase:
        print(f"Frequência de cruzamento de fase: {cruzamento_fase[0]:.5f} rad/s")
    print(f"Gráfico salvo em: {caminho.resolve()}")

# Plota os polos de malha fechada conforme K varia.
# 1 + K G(s) = 0
# s^3 + 6s^2 + 11s + 6 + 10K = 0
  
def gerar_lugar_das_raizes():
    K_valores = np.concatenate(([0.0], np.logspace(-3, 3, 1200)))
    polos = []

    for K in K_valores:
        coeficientes = [1.0, 6.0, 11.0, 6.0 + 10.0 * K]
        polos.append(np.roots(coeficientes))

    polos = np.asarray(polos)

    fig, ax = plt.subplots(figsize=(10, 7))
    for ramo in range(3):
        ax.plot(polos[:, ramo].real, polos[:, ramo].imag, linewidth=1.8)

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1, linestyle="--")
    ax.set_title("Lugar das Raízes — realimentação unitária negativa")
    ax.set_xlabel("Parte real")
    ax.set_ylabel("Parte imaginária")
    ax.grid(True, which="both", linestyle=":")
    ax.set_xlim(min(-8, np.min(polos.real) - 0.5), max(1, np.max(polos.real) + 0.5))
    ax.set_ylim(min(-8, np.min(polos.imag) - 0.5), max(8, np.max(polos.imag) + 0.5))

    fig.tight_layout()
    caminho = PASTA_SAIDA / "lugar_das_raizes.png"
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfico salvo em: {caminho.resolve()}")


if __name__ == "__main__":
    gerar_bode()
    gerar_lugar_das_raizes()
    print("\\nConcluído. Os gráficos PNG estão na pasta resultados_pratica11.")