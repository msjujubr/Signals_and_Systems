from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")  # salvar graficos
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import find_peaks


# configuracoes e arquivos output
PASTA_SCRIPT = Path(__file__).resolve().parent

if str(PASTA_SCRIPT) not in sys.path:
    sys.path.insert(0, str(PASTA_SCRIPT))

PASTA_SAIDA = PASTA_SCRIPT / "resultados_pratica12"
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

# Planta conhecida: G1(s) = (s + 4) / ((s + 1)(s + 2)(s + 3))
NUM_G1 = np.array([1.0, 4.0])
DEN_G1 = np.polymul(np.polymul([1.0, 1.0], [1.0, 2.0]), [1.0, 3.0])

# Dados da planta conhecida
TEMPO_G1 = np.linspace(0.0, 20.0, 10001)
REFERENCIA_DEGRAU = 1.0

# Dados para busca do ganho
K_MIN = 0
K_MAX = 100
TEMPO_DESCONHECIDO = np.linspace(0.0, 100.0, 10001)


# funcoes auxiliares
def salvar_figura(nome: str) -> None:
    caminho = PASTA_SAIDA / nome
    plt.tight_layout()
    plt.savefig(caminho, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Grafico salvo: {caminho}")


# simula a resposta ao degrau unitario
def simular_degrau(
    num: np.ndarray,
    den: np.ndarray,
    tempo: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    sistema = signal.TransferFunction(
        np.asarray(num, dtype=float),
        np.asarray(den, dtype=float),
    )
    t, y = signal.step(sistema, T=np.asarray(tempo, dtype=float))
    return np.asarray(t), np.asarray(y).squeeze()


# soma em ordem decrescente de pot
def somar_polinomios(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.polyadd(np.asarray(a, dtype=float), np.asarray(b, dtype=float))


# gera C(s)G(s)/(1 + C(s)G(s))
def fechar_malha_pid(
    num_planta: np.ndarray,
    den_planta: np.ndarray,
    kp: float,
    ti: float,
    td: float,
) -> tuple[np.ndarray, np.ndarray]:
    # Controlador Ideal: C(s) = Kp * (Td*Ti*s^2 + Ti*s + 1) / (Ti*s)
    if kp < 0:
        raise ValueError("Kp nao negativo")
    if ti <= 0:
        raise ValueError("Ti positivo")

    num_c = kp * np.array([td * ti, ti, 1.0], dtype=float)
    den_c = np.array([ti, 0.0], dtype=float)
    num_aberta = np.polymul(num_c, num_planta)
    den_aberta = np.polymul(den_c, den_planta)
    den_fechada = somar_polinomios(den_aberta, num_aberta)
    return num_aberta, den_fechada


# calcula tempo de subida, sobressinal, acomodacao e erro final
def calcular_metricas(
    tempo: np.ndarray,
    resposta: np.ndarray,
    referencia: float = 1.0,
) -> dict[str, float]:
    t = np.asarray(tempo, dtype=float).squeeze()
    y = np.asarray(resposta, dtype=float).squeeze()

    metricas = {
        "Tempo de subida (s)": math.nan,
        "Sobressinal maximo (%)": math.nan,
        "Tempo de acomodacao 2% (s)": math.nan,
        "Erro em regime permanente": math.nan,
        "Valor final estimado": math.nan,
    }

    # acomodacao 2%
    if t.size < 2 or y.size != t.size or not np.all(np.isfinite(y)):
        return metricas

    # Estima o valor final pela media dos ultimos 5% das amostras.
    n_final = max(5, int(0.05 * len(y)))
    valor_final = float(np.mean(y[-n_final:]))
    metricas["Valor final estimado"] = valor_final
    metricas["Erro em regime permanente"] = abs(float(referencia) - valor_final)

    delta_final = valor_final - float(y[0])
    if abs(delta_final) > 1e-10:
        resposta_normalizada = (y - y[0]) / delta_final
        idx_10 = np.flatnonzero(resposta_normalizada >= 0.1)
        idx_90 = np.flatnonzero(resposta_normalizada >= 0.9)
        if idx_10.size and idx_90.size:
            t10, t90 = float(t[idx_10[0]]), float(t[idx_90[0]])
            if t90 >= t10:
                metricas["Tempo de subida (s)"] = t90 - t10

        pico_normalizado = float(np.max(resposta_normalizada))
        metricas["Sobressinal maximo (%)"] = max(
            0.0,
            (pico_normalizado - 1.0) * 100.0,
        )

    # Faixa de acomodacao de 2% do valor de referência ou da amplitude observada.
    escala = max(abs(valor_final), abs(float(referencia)), float(np.ptp(y)), 1e-12)
    faixa = 0.02 * escala
    fora = np.flatnonzero(np.abs(y - valor_final) > faixa)

    if fora.size == 0:
        metricas["Tempo de acomodacao 2% (s)"] = 0.0
    elif fora[-1] < len(t) - 1:  # se ainda estiver fora da faixa,
        metricas["Tempo de acomodacao 2% (s)"] = float(t[fora[-1] + 1])

    return metricas


def imprimir_metricas(titulo: str, metricas: dict[str, float]) -> None:
    print(f"\n{titulo}")
    for nome, valor in metricas.items():
        if np.isfinite(valor):
            print(f"  {nome}: {valor:.5g}")
        else:
            print(f"  {nome}: nao determinado na janela de simulacao")


def plotar_resposta(
    tempo: np.ndarray,
    resposta: np.ndarray,
    titulo: str,
    nome_arquivo: str,
    rotulo: str = "Resposta",
    referencia: float | None = 1.0,
) -> None:
    plt.figure(figsize=(8.5, 4.8))
    plt.plot(tempo, resposta, label=rotulo, linewidth=1.8)
    if referencia is not None:
        plt.axhline(referencia, linestyle="--", linewidth=1.0, label="Referência")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Saida")
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura(nome_arquivo)


# PRIMEIRO METODO (PLANTA CONHECIDA)
def primeiro_metodo_zn() -> dict[str, float]:
    tempo, resposta = simular_degrau(NUM_G1, DEN_G1, TEMPO_G1)

    # a derivada da resposta ao degrau e a resposta ao impulso.
    # seu maximo marca o ponto de inflexao da curva em S (tangente)
    sistema = signal.TransferFunction(NUM_G1, DEN_G1)
    _, resposta_impulso = signal.impulse(sistema, T=tempo)
    indice_inflexao = int(np.argmax(resposta_impulso))
    t_i = float(tempo[indice_inflexao])
    y_i = float(resposta[indice_inflexao])
    inclinacao = float(resposta_impulso[indice_inflexao])
    ganho_estatico = float(resposta[-1])

    if inclinacao <= 0:
        raise RuntimeError("inclinacao <= 0 no ponto de inflexao.")

    # intersecoes da tangente com y = 0 e y = K
    L = t_i - y_i / inclinacao
    t_intersecao_K = t_i + (ganho_estatico - y_i) / inclinacao
    T = t_intersecao_K - L
    if L <= 0 or T <= 0:
        raise RuntimeError(f"T/L invalido(s): L={L:.5g}, T={T:.5g}.")

    # Tabela 01
    kp = 1.2 * T / L
    ti = 2.0 * L
    td = 0.5 * L

    print("\n-> Primeiro Metodo (Planta Conhecida)")
    print(f"G1(s) = (s + 4) / ((s + 1)(s + 2)(s + 3))")
    print(f"Ganho estatico K = {ganho_estatico:.6g}")
    print(f"Ponto de inflexao: t = {t_i:.6g} s; c(t) = {y_i:.6g}")
    print(f"Inclinacao da tangente = {inclinacao:.6g}")
    print(f"L = {L:.6g} s; T = {T:.6g} s")
    print(f"PID inicial: Kp = {kp:.6g}; Ti = {ti:.6g} s; Td = {td:.6g} s")

    # Grafico: resposta em malha aberta, tangente e marcacoes L e T
    y_tangente = y_i + inclinacao * (tempo - t_i)
    plt.figure(figsize=(8.5, 4.8))
    plt.plot(tempo, resposta, label="Resposta ao degrau de G1(s)", linewidth=1.8)
    mascara_tangente = (tempo >= max(0.0, L - 0.1)) & (tempo <= t_intersecao_K + 0.2)
    plt.plot(
        tempo[mascara_tangente],
        y_tangente[mascara_tangente],
        "--",
        label="Tangente no ponto de inflexao",
    )
    plt.axhline(ganho_estatico, linestyle=":", linewidth=1.2, label=f"K = {ganho_estatico:.3g}")
    plt.axhline(0.0, color="black", linewidth=0.8)
    plt.axvline(L, linestyle="--", linewidth=1.0)
    plt.axvline(t_intersecao_K, linestyle="--", linewidth=1.0)
    plt.annotate(
        f"L = {L:.3f} s",
        xy=(L, 0),
        xytext=(0.25, 0.27),
        textcoords="data",
        arrowprops={"arrowstyle": "->"},
    )
    plt.annotate(
        f"T = {T:.3f} s",
        xy=((L + t_intersecao_K) / 2, 0.01),
        xytext=(2.7, 0.18),
        textcoords="data",
        ha="left",
        arrowprops={"arrowstyle": "->"},
    )
    plt.xlabel("Tempo (s)")
    plt.ylabel("Saida")
    plt.title("Primeiro metodo de Ziegler-Nichols: metodo da tangente")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("01_planta_conhecida_tangente.png")

    # PID
    num_cl, den_cl = fechar_malha_pid(NUM_G1, DEN_G1, kp, ti, td)
    t_pid, y_pid = simular_degrau(num_cl, den_cl, TEMPO_G1)
    metricas_pid = calcular_metricas(t_pid, y_pid, REFERENCIA_DEGRAU)
    imprimir_metricas("Resposta em malha fechada com o PID inicial", metricas_pid)
    plotar_resposta(
        t_pid,
        y_pid,
        "Planta conhecida com PID de Ziegler-Nichols",
        "02_pid_planta_conhecida.png",
    )

    # parametros e metricas
    configuracoes = [
        ("Kp", [0.5 * kp, kp, 1.5 * kp], "03_variacao_Kp.png", "Variacao individual de Kp"),
        ("Ti", [0.5 * ti, ti, 1.5 * ti], "04_variacao_Ti.png", "Variacao individual de Ti"),
        ("Td", [0.5 * td, td, 1.5 * td], "05_variacao_Td.png", "Variacao individual de Td"),
    ]

    for parametro, valores, nome_grafico, titulo in configuracoes:
        plt.figure(figsize=(8.5, 4.8))
        for fator, valor in zip([0.5, 1.0, 1.5], valores):
            kp_i, ti_i, td_i = kp, ti, td
            if parametro == "Kp":
                kp_i = float(valor)
            elif parametro == "Ti":
                ti_i = float(valor)
            else:
                td_i = float(valor)

            num_i, den_i = fechar_malha_pid(NUM_G1, DEN_G1, kp_i, ti_i, td_i)
            t_i_v, y_i_v = simular_degrau(num_i, den_i, TEMPO_G1)
            metricas_i = calcular_metricas(t_i_v, y_i_v, REFERENCIA_DEGRAU)
            rotulo = f"{parametro} = {valor:.4g} ({fator:.1f}x)"
            plt.plot(t_i_v, y_i_v, label=rotulo, linewidth=1.5)

            print(f"\nVariacao individual: {rotulo}")
            print(f"  Kp = {kp_i:.5g}; Ti = {ti_i:.5g} s; Td = {td_i:.5g} s")
            imprimir_metricas("  Metricas da resposta", metricas_i)

        plt.axhline(REFERENCIA_DEGRAU, linestyle="--", linewidth=1.0, label="Referência")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Saida")
        plt.title(titulo)
        plt.grid(True, alpha=0.3)
        plt.legend()
        salvar_figura(nome_grafico)

    return {"L": L, "T": T, "K": ganho_estatico, "Kp": kp, "Ti": ti, "Td": td}


def extrair_vetor_resposta(resultado: Any, tempo_esperado: np.ndarray) -> np.ndarray:
    n = len(tempo_esperado)

    # Objetos de resposta da biblioteca python-control.
    if hasattr(resultado, "outputs"):
        vetor = np.asarray(resultado.outputs).squeeze()
        if vetor.size == n:
            return vetor.astype(float)
    if hasattr(resultado, "y"):
        vetor = np.asarray(resultado.y).squeeze()
        if vetor.size == n:
            return vetor.astype(float)

    if isinstance(resultado, (tuple, list)):
        candidatos: list[np.ndarray] = []
        for item in resultado:
            try:
                arr = np.asarray(item, dtype=float).squeeze()
            except (TypeError, ValueError):
                continue
            if arr.ndim == 1 and arr.size == n:
                candidatos.append(arr)
        if candidatos:
            # Se o retorno for (tempo, saida)
            for candidato in candidatos:
                if not np.allclose(candidato, tempo_esperado, rtol=1e-5, atol=1e-8):
                    return candidato.astype(float)
            return candidatos[-1].astype(float)

    arr = np.asarray(resultado, dtype=float).squeeze()
    if arr.ndim == 1 and arr.size == n:
        return arr.astype(float)
    if arr.ndim == 2 and n in arr.shape:
        if arr.shape[-1] == n:
            return arr.reshape(-1, n)[-1].astype(float)
        return arr.reshape(n, -1)[:, -1].astype(float)

    raise ValueError(f"Esperava uma saída com {n} amostras; retorno com formato {arr.shape}.")


def obter_resposta_degrau_desconhecido(modulo: Any, tempo: np.ndarray) -> np.ndarray:
    funcao = getattr(modulo, "resposta_degrau", None)
    if funcao is None:
        funcao = getattr(modulo, "resposta_ao_degrau", None)
    if funcao is None:
        raise AttributeError("2ZN: obter resposta degrau desconhecido")

    retorno = funcao(tempo)
    return extrair_vetor_resposta(retorno, tempo)


def obter_resposta_malha_fechada(
    modulo: Any,
    controlador: Any,
    tempo: np.ndarray,
    referencia: np.ndarray,
) -> np.ndarray:
    funcao = getattr(modulo, "testar_malha_fechada", None)
    if funcao is not None:
        retorno = funcao(controlador, tempo, referencia)
    else:
        funcao = getattr(modulo, "resposta_malha_fechada", None)
        if funcao is None:
            raise AttributeError("Erro 2ZN: obter resposta malha fechada")
        retorno = funcao(controlador, tempo)

    return extrair_vetor_resposta(retorno, tempo)


# estima a razao entre amplitudes de extremos consecutivos na regiao final
# ~1 (oscilacao sustentada); <1 (decaimento); >1 (crescimento).
def analisar_razao_picos(
    tempo: np.ndarray,
    resposta: np.ndarray,
) -> tuple[float, int, np.ndarray, np.ndarray]:
    t = np.asarray(tempo, dtype=float)
    y = np.asarray(resposta, dtype=float)
    if y.size != t.size or not np.all(np.isfinite(y)):
        return math.nan, 0, np.array([]), np.array([], dtype=int)

    baseline = float(np.median(y[int(0.85 * len(y)):]))
    z = y - baseline
    escala = float(np.max(np.abs(z)))
    if escala < 1e-8:
        return math.nan, 0, np.array([]), np.array([], dtype=int)

    distancia = max(1, int(0.005 * len(y)))
    limite = int(0.2 * len(y))
    prominencia = max(1e-8, 0.01 * escala)

    picos_detectados, _ = find_peaks(
        z,
        distance=distancia,
        prominence=prominencia,
    )
    vales_detectados, _ = find_peaks(
        -z,
        distance=distancia,
        prominence=prominencia,
    )

    picos_validos = picos_detectados[picos_detectados >= limite]
    vales_validos = vales_detectados[vales_detectados >= limite]

    extremos = np.sort(np.concatenate((picos_validos, vales_validos)))
    amplitudes = np.abs(z[extremos])

    # remocao de extremos proximos do ruido
    razoes = []
    for indices in (picos_validos, vales_validos):
        amplitudes_tipo = np.abs(z[indices])
        if amplitudes_tipo.size >= 2:
            razoes.extend(
                amplitudes_tipo[1:] / np.maximum(amplitudes_tipo[:-1], 1e-12)
            )

    if not razoes:
        return math.nan, int(extremos.size), amplitudes, extremos

    # utiliza os ultimos ciclos para estabilidade marginal.
    razoes = razoes[-min(8, len(razoes)):]
    return float(np.median(razoes)), int(extremos.size), amplitudes, extremos


# Testa Kp inteiro entre 0 e 100 e escolhe o ganho mais proximo de oscilacao sustentada
def buscar_ganho_critico(
    modulo: Any,
    ct: Any,
) -> tuple[int, np.ndarray, np.ndarray, list[dict[str, Any]]]:
    tempo = TEMPO_DESCONHECIDO
    referencia = np.ones_like(tempo)
    registros: list[dict[str, Any]] = []
    respostas: dict[int, np.ndarray] = {}

    chave_razao = "Razão mediana entre amplitudes"
    chave_extremos = "Número de extremos considerados"
    chave_instabilidade = "Possível instabilidade"

    print("\nTestando ganhos proporcionais inteiros entre 0 e 100...")
    for kp_teste in range(K_MIN, K_MAX + 1):
        controlador_p = ct.TransferFunction([float(kp_teste)], [1.0])
        try:
            y = obter_resposta_malha_fechada(modulo, controlador_p, tempo, referencia)
            respostas[kp_teste] = y
            razao, n_extremos, amplitudes, _ = analisar_razao_picos(tempo, y)

            amplitude_final = (
                float(np.max(np.abs(y[int(0.9 * len(y)):])) )
                if np.all(np.isfinite(y)) else math.inf
            )
            amplitude_inicial = (
                float(np.max(np.abs(y[:max(5, int(0.1 * len(y)))])))
                if np.all(np.isfinite(y)) else 0.0
            )
            cresce_sem_limite = (
                not np.isfinite(amplitude_final)
                or amplitude_final > 25.0 * max(amplitude_inicial, 1.0)
            )
            registros.append({
                "Kp testado": kp_teste,
                chave_razao: razao,
                chave_extremos: n_extremos,
                "Amplitude máxima nos 10% finais": amplitude_final,
                chave_instabilidade: cresce_sem_limite,
            })
        except Exception as exc:
            print(f"  Kp={kp_teste}: falha na simulacao ({exc})")
            registros.append({
                "Kp testado": kp_teste,
                chave_razao: math.nan,
                chave_extremos: 0,
                "Amplitude máxima nos 10% finais": math.nan,
                chave_instabilidade: True,
            })

    candidatos = [
        r for r in registros
        if np.isfinite(r[chave_razao])
        and r[chave_extremos] >= 4
        and not r[chave_instabilidade]
    ]

    if candidatos:
        melhor = min(
            candidatos,
            key=lambda r: abs(r[chave_razao] - 1.0),
        )
        kcrit = int(melhor["Kp testado"])
        razao_melhor = float(melhor[chave_razao])
        if not (0.80 <= razao_melhor <= 1.20):
            print("2ZN: sem ganho com razao entre picos muito próxima de 1")

    else:  # so tem candidatos possivelmente instaveis
        candidatos = [
            r for r in registros
            if np.isfinite(r[chave_razao])
        ]
        if not candidatos:
            raise RuntimeError("2ZN: sem oscilacoes na faixa de Kp=0 a 100")
        melhor = min(
            candidatos,
            key=lambda r: abs(r[chave_razao] - 1.0),
        )
        kcrit = int(melhor["Kp testado"])

    print(f"Kcrit estimado = {kcrit} (ganho inteiro com razao de amplitudes mais próxima de 1)")
    ycrit = respostas.get(kcrit)
    if ycrit is None:
        ycrit = obter_resposta_malha_fechada(
            modulo,
            ct.TransferFunction([float(kcrit)], [1.0]),
            tempo,
            referencia,
        )
    return kcrit, tempo, ycrit, registros


def segundo_metodo_zn() -> None:
    ct = importlib.import_module("control")
    try:
        sistema = importlib.import_module("sistema_desconhecido")
    except Exception as exc:
        print(f"sistema_desconhecido.pyc ({exc})")
        return

    tempo = TEMPO_DESCONHECIDO
    referencia = np.ones_like(tempo)

    try:
        y_aberta = obter_resposta_degrau_desconhecido(sistema, tempo)
        plotar_resposta(
            tempo,
            y_aberta,
            "Resposta ao degrau da planta desconhecida",
            "06_planta_desconhecida_degrau.png",
            rotulo="Planta desconhecida",
            referencia=None,
        )
    except Exception as exc:
        print(f"2zn: {exc}")

    kcrit, tempo, ycrit, registros = buscar_ganho_critico(sistema, ct)
    razao_critica, n_extremos, amplitudes, indices_extremos = analisar_razao_picos(tempo, ycrit)
    pcrit = math.nan

    if len(indices_extremos) >= 3:
        periodos = np.diff(tempo[indices_extremos])
        if len(periodos) >= 2:
            pcrit = float(2.0 * np.median(periodos))

    # Tabela de Ziegler-Nichols, 2º metodo: Kp=0,6Kcrit; Ti=0,5Pcrit; Td=0,125Pcrit.
    picos_periodo, _ = find_peaks(
        ycrit,
        distance=max(1, int(0.005 * len(ycrit))),
    )
    picos_periodo = picos_periodo[picos_periodo >= int(0.2 * len(ycrit))]

    # Refina o período usando os picos (maximos locais) quando existirem.
    if len(picos_periodo) >= 3:
        pcrit = float(np.median(np.diff(tempo[picos_periodo])))
    elif len(indices_extremos) >= 3:
        # Como extremos consecutivos alternam pico/vale, 2*delta estima o período.
        pcrit = float(2.0 * np.median(np.diff(tempo[indices_extremos])))

    # Marcar extremos para que o período crítico possa ser conferido visualmente.
    plt.figure(figsize=(8.5, 4.8))
    plt.plot(tempo, ycrit, label=f"Kp = Kcrit = {kcrit}", linewidth=1.6)
    plt.axhline(1.0, linestyle="--", linewidth=1.0, label="Referência")
    if len(picos_periodo) >= 2:
        plt.plot(tempo[picos_periodo], ycrit[picos_periodo], "o", markersize=3.5, label="Picos")
        if np.isfinite(pcrit):
            p0, p1 = picos_periodo[-2], picos_periodo[-1]
            plt.annotate(
                f"Pcrit ≈ {pcrit:.3g} s",
                xy=(tempo[p1], ycrit[p1]),
                xytext=(tempo[p0], ycrit[p1] * 0.9),
                arrowprops={"arrowstyle": "->"},
            )

    plt.xlabel("Tempo (s)")
    plt.ylabel("Saida")
    plt.title("Oscilacao para estimativa do ganho critico")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("07_oscilacao_ganho_critico.png")

    if not np.isfinite(pcrit) or pcrit <= 0:
        print("periodo critico invalido")
        return

    # Tabela 02
    kp_pid = 0.6 * kcrit
    ti_pid = 0.5 * pcrit
    td_pid = 0.125 * pcrit
    print(f"Periodo critico Pcrit estimado = {pcrit:.6g} s")
    print(f"PID pelo 2º metodo: Kp = {kp_pid:.6g}; Ti = {ti_pid:.6g} s; Td = {td_pid:.6g} s")
    print(f"Razao mediana entre amplitudes na oscilacao critica = {razao_critica:.5g}")

    controlador_pid = ct.TransferFunction(
        [kp_pid * ti_pid * td_pid, kp_pid * ti_pid, kp_pid],
        [ti_pid, 0.0],
    )

    y_pid = obter_resposta_malha_fechada(sistema, controlador_pid, tempo, referencia)
    plotar_resposta(
        tempo,
        y_pid,
        "Planta desconhecida em malha fechada com PID de Ziegler-Nichols",
        "08_pid_planta_desconhecida.png",
        rotulo="Saida com PID",
        referencia=1.0,
    )

    valor_final = float(np.mean(y_pid[-max(5, int(0.05 * len(y_pid))):]))
    desvio = y_pid - valor_final
    distancia = max(1, int(0.003 * len(desvio)))
    prominencia = max(1e-8, 0.01 * np.max(np.abs(desvio)))

    picos_positivos_detectados, _ = find_peaks(
        desvio,
        distance=distancia,
        prominence=prominencia,
    )
    picos_negativos_detectados, _ = find_peaks(
        -desvio,
        distance=distancia,
        prominence=prominencia,
    )

    picos_positivos = picos_positivos_detectados[
        picos_positivos_detectados >= int(0.02 * len(desvio))
    ]
    picos_negativos = picos_negativos_detectados[
        picos_negativos_detectados >= int(0.02 * len(desvio))
    ]

    amplitudes_positivas = np.abs(desvio[picos_positivos])
    amplitudes_negativas = np.abs(desvio[picos_negativos])

    razoes_decaimento = []
    for amplitudes_tipo in (amplitudes_positivas, amplitudes_negativas):
        if len(amplitudes_tipo) >= 2:
            razoes_decaimento.extend(
                amplitudes_tipo[1:] / np.maximum(amplitudes_tipo[:-1], 1e-12)
            )

    razoes_decaimento = np.asarray(razoes_decaimento, dtype=float)
    razao_decaimento_mediana = (
        float(np.median(razoes_decaimento))
        if razoes_decaimento.size
        else math.nan
    )
    regra_25 = bool(
        np.isfinite(razao_decaimento_mediana)
        and 0.15 <= razao_decaimento_mediana <= 0.35
    )
    print("\nVerificacao da regra de decaimento entre picos:")
    if razoes_decaimento.size:
        razoes_formatadas = ", ".join(
            f"{razao:.3f}" for razao in razoes_decaimento[:8]
        )
        print("  razoes entre amplitudes consecutivas:", razoes_formatadas)
        resultado_regra = "sim" if regra_25 else "nao"
        print(f"  razao mediana = {razao_decaimento_mediana:.4g}; "
              f"regra aproximadamente atendida? {resultado_regra}" )
    else:
        print("  Nao obteve pelo menos dois picos validos para comparacao.")

    metricas_pid = calcular_metricas(tempo, y_pid, REFERENCIA_DEGRAU)
    imprimir_metricas("Metricas do PID na planta desconhecida", metricas_pid)


def main() -> None:
    print(f"Os resultados serao salvos em: {PASTA_SAIDA}")
    primeiro_metodo_zn()
    segundo_metodo_zn()
    print("\nCabo :)")


if __name__ == "__main__":
    main()