from pathlib import Path
import matplotlib.pyplot as plt
import control
import numpy as np


PASTA_SCRIPT = Path(__file__).resolve().parent
PASTA_SAIDA = PASTA_SCRIPT / "data"
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

# Faixa de acomodacao: 2%
FAIXA_ACOMODACAO = 0.02

# Limites
REQUISITOS = {
    "caso1": {
        "sobressinal_max": 7.0,
        "tempo_max": 5.0,
        # Tolerancia numerica para considerar o erro estacionario nulo.
        "erro_max": 0.1,
    },
    "caso2": {
        "sobressinal_max": 5.0,
        "tempo_max": 3.0,
        # Tolerancia numerica para considerar o erro estacionario nulo.
        "erro_max": 0.1,
    },
}


# Calcula as metricas de desempenho
def calcular_metricas(sistema, tempo, resposta):
    tempo = np.asarray(tempo, dtype=float).squeeze()
    resposta = np.asarray(resposta, dtype=float).squeeze()

    if tempo.ndim != 1 or resposta.ndim != 1:
        raise ValueError("O tempo e a resposta devem ser vetores unidimensionais.")

    if len(tempo) != len(resposta):
        raise ValueError("O vetor de tempo e o vetor de resposta devem ter o mesmo tamanho.")

    # Valor final obtido pelo ganho em regime permanente do sistema.
    valor_final = float(np.real(control.dcgain(sistema)))

    if not np.isfinite(valor_final):
        raise ValueError("Nao foi possivel calcular um valor final finito para o sistema.")

    if np.isclose(valor_final, 0.0):
        raise ValueError("O valor final do sistema e zero; nao e possivel calcular o sobressinal percentual.")

    # Sobressinal percentual em relacao ao valor final.
    sobressinal = max(
        0.0,
        (np.max(resposta) - valor_final) / abs(valor_final) * 100.0,
    )

    # Tempo de acomodacao considerando a faixa de 2% do valor final.
    faixa = FAIXA_ACOMODACAO * abs(valor_final)
    fora_faixa = np.where(np.abs(resposta - valor_final) > faixa)[0]

    if len(fora_faixa) == 0:
        tempo_acomodacao = float(tempo[0])
    elif fora_faixa[-1] == len(tempo) - 1:
        # A resposta ainda estava fora da faixa no final da simulacao.
        tempo_acomodacao = np.inf
    else:
        # Interpolacao entre a ultima amostra fora da faixa e a primeira dentro.
        indice = fora_faixa[-1]
        limite = valor_final + np.sign(resposta[indice] - valor_final) * faixa

        variacao = resposta[indice + 1] - resposta[indice]
        if np.isclose(variacao, 0.0):
            tempo_acomodacao = float(tempo[indice + 1])
        else:
            fracao = (limite - resposta[indice]) / variacao
            tempo_acomodacao = float(
                tempo[indice]
                + fracao * (tempo[indice + 1] - tempo[indice])
            )

    # Erro em regime permanente para referencia unitaria, em porcentagem.
    erro_estacionario = abs(1.0 - valor_final) * 100.0

    return {
        "valor_final": valor_final,
        "sobressinal": sobressinal,
        "tempo_acomodacao": tempo_acomodacao,
        "erro_estacionario": erro_estacionario,
    }


def imprimir_funcao_transferencia(titulo, sistema):
    print(f"\n{titulo}")
    print(sistema)


def imprimir_resultados(titulo, requisitos, resultados):
    print(f"\n{titulo}")
    print(
        f"Requisitos: Sobressinal <= {requisitos['sobressinal_max']:.2f}%"
        f" | Tempo de acomodacao <= {requisitos['tempo_max']:.2f} s"
        f" | Erro estacionario <= {requisitos['erro_max']:.2f}%\n"
    )

    largura = 82
    print(
        f"{'Controlador':<16}"
        f"{'Valor final':>13}"
        f"{'Mp (%)':>11}"
        f"{'Ts (s)':>12}"
        f"{'Erro est. (%)':>16}"
        f"{'Atende?':>14}"
    )
    print("-" * largura)

    for nome, metricas in resultados.items():
        mp = metricas["sobressinal"]
        ts = metricas["tempo_acomodacao"]
        erro = metricas["erro_estacionario"]

        atende = (
            mp <= requisitos["sobressinal_max"]
            and ts <= requisitos["tempo_max"]
            and erro <= requisitos["erro_max"]
        )

        ts_texto = f"{ts:.3f}" if np.isfinite(ts) else "N/A"

        print(
            f"{nome:<16}"
            f"{metricas['valor_final']:>13.4f}"
            f"{mp:>11.2f}"
            f"{ts_texto:>12}"
            f"{erro:>16.2f}"
            f"{'SIM' if atende else 'NAO':>14}"
        )

        # Indica quais criterios nao foram atendidos.
        falhas = []
        if mp > requisitos["sobressinal_max"]:
            falhas.append("sobressinal")
        if ts > requisitos["tempo_max"]:
            falhas.append("tempo de acomodacao")
        if erro > requisitos["erro_max"]:
            falhas.append("erro estacionario")

        if falhas:
            print(f"{'':<16}Requisitos nao atendidos: {', '.join(falhas)}")

    print("-" * largura)


# 1. Processo Termico
# Planta: G_termico = 1 / (5s + 1)

num_term = [1]
den_term = [5, 1]
G_term = control.TransferFunction(num_term, den_term)

# Controlador proporcional: Cp(s) = 4
Cp1 = control.TransferFunction([4], [1])
T_term_p = control.feedback(Cp1 * G_term, 1)

# Controlador PI: Cpi(s) = 4 + Ki/s
# O valor Ki = 4 atende aos requisitos propostos.
x_pi = 4.0
Cpi = control.TransferFunction([4, x_pi], [1, 0])
T_term_pi = control.feedback(Cpi * G_term, 1)

# Apresentacao das funcoes de transferencia em malha fechada.
print("\n========== FUNCOES DE TRANSFERENCIA - PRIMEIRO CASO ==========")
imprimir_funcao_transferencia("Malha fechada com controlador P:", T_term_p)
imprimir_funcao_transferencia("Malha fechada com controlador PI:", T_term_pi)

# Simulacao da resposta ao degrau.
t_term = np.linspace(0, 20, 1000)
t_p, y_p = control.step_response(T_term_p, t_term)
t_pi, y_pi = control.step_response(T_term_pi, t_term)

plt.figure(figsize=(10, 5))
plt.plot(t_p, y_p, label="Controlador P (Kp=4)", linewidth=2, color="red")
plt.plot(
    t_pi,
    y_pi,
    label=f"Controlador PI (Kp=4, Ki={x_pi})",
    linewidth=2,
    color="blue",
)
plt.axhline(1, color="gray", linestyle="--", label="Referencia (1.0)")
plt.title("Primeiro Caso: Resposta ao Degrau - Processo Termico")
plt.xlabel("Tempo (s)")
plt.ylabel("Saida")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(PASTA_SAIDA / "caso1_resposta_degrau.png", dpi=300, bbox_inches="tight")
plt.close()


# 2. Controle de Posicao
# Planta: G_pos = 1 / (s(s + 2)) = 1 / (s^2 + 2s)
num_pos = [1]
den_pos = [1, 2, 0]
G_pos = control.TransferFunction(num_pos, den_pos)

# Controlador proporcional: Cp(s) = 4
Cp2 = control.TransferFunction([4], [1])
T_pos_p = control.feedback(Cp2 * G_pos, 1)

# Controlador PD: Cpd(s) = Kd*s + Kp
x_pd = 1.5
Cpd = control.TransferFunction([x_pd, 4], [1])
T_pos_pd = control.feedback(Cpd * G_pos, 1)

# Apresentacao das funcoes de transferencia em malha fechada.
print("\n========== FUNCOES DE TRANSFERENCIA - SEGUNDO CASO ==========")
imprimir_funcao_transferencia("Malha fechada com controlador P:", T_pos_p)
imprimir_funcao_transferencia("Malha fechada com controlador PD:", T_pos_pd)

# Simulacao da resposta ao degrau.
t_pos = np.linspace(0, 10, 1000)
t_pp, y_pp = control.step_response(T_pos_p, t_pos)
t_pd, y_pd = control.step_response(T_pos_pd, t_pos)

plt.figure(figsize=(10, 5))
plt.plot(t_pp, y_pp, label="Controlador P (Kp=4)", linewidth=2, color="red")
plt.plot(
    t_pd,
    y_pd,
    label=f"Controlador PD (Kp=4, Kd={x_pd})",
    linewidth=2,
    color="green",
)
plt.axhline(1, color="gray", linestyle="--", label="Referencia (1.0)")
plt.title("Segundo Caso: Resposta ao Degrau - Controle de Posicao")
plt.xlabel("Tempo (s)")
plt.ylabel("Saida")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(PASTA_SAIDA / "caso2_resposta_degrau.png", dpi=300, bbox_inches="tight")
plt.close()


# Resultados do primeiro caso: Processo Termico
resultados_caso1 = {
    "Proporcional": calcular_metricas(T_term_p, t_p, y_p),
    "PI": calcular_metricas(T_term_pi, t_pi, y_pi),
}

imprimir_resultados(
    "PRIMEIRO CASO - PROCESSO TERMICO",
    REQUISITOS["caso1"],
    resultados_caso1,
)


# Resultados do segundo caso: Controle de Posicao
resultados_caso2 = {
    "Proporcional": calcular_metricas(T_pos_p, t_pp, y_pp),
    "PD": calcular_metricas(T_pos_pd, t_pd, y_pd),
}

imprimir_resultados(
    "SEGUNDO CASO - CONTROLE DE POSICAO",
    REQUISITOS["caso2"],
    resultados_caso2,
)

print("\nGraficos salvos na pasta:", PASTA_SAIDA)
print("Arquivos gerados:")
print("-", PASTA_SAIDA / "caso1_resposta_degrau.png")
print("-", PASTA_SAIDA / "caso2_resposta_degrau.png")
print("Cabô")