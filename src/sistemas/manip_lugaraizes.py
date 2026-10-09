import control as ct
import matplotlib.pyplot as plt
import numpy as np
import os


# CONFIGURAÇÃO
# Garante que a pasta data exista
os.makedirs("data", exist_ok=True)


# Acompanhando os polos de acordo com o ganho K
num_G1 = [1]
den_G1 = [1, 6, 8, 0]

G1 = ct.TransferFunction(num_G1, den_G1)

K_values = [2, 10, 50, 250]

plt.figure(figsize=(10, 6))

# Lugar Geométrico das Raízes
ct.root_locus(
    G1,
    plot=True,
    title="Lugar Geométrico das Raízes - G1(s)"
)

# Polos para cada valor de K
for k in K_values:

    # Sistema em malha fechada:
    sys_cl = ct.feedback(k * G1, 1)

    poles = ct.poles(sys_cl)

    plt.plot(
        np.real(poles),
        np.imag(poles),
        'x',
        markersize=10,
        markeredgewidth=2,
        label=f'K = {k}'
    )

# Limite de estabilidade
K_lim_G1 = 48

plt.axvline(
    0,
    linestyle='--',
    linewidth=1
)

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    'data/lgr_G1.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()

print(
    f"Limite de estabilidade de G1(s): "
    f"K = {K_lim_G1}"
)

print()


# Acrescentando zeros para modificar o LGR
num_G2 = [1]
den_G2 = [1, -3, 2]

G2 = ct.TransferFunction(
    num_G2,
    den_G2
)


# Adição de dois zeros no semiplano esquerdo
num_G2_mod = [1, 7, 12]

G2_mod = ct.TransferFunction(
    num_G2_mod,
    den_G2
)


# Gráfico G2 original
plt.figure(figsize=(8, 6))

ct.root_locus(
    G2,
    plot=True,
    title="Lugar Geométrico das Raízes - G2(s) Original"
)

plt.grid(True)
plt.tight_layout()

plt.savefig(
    'data/lgr_G2_antes.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()


# Gráfico G2 modificado
plt.figure(figsize=(8, 6))

ct.root_locus(
    G2_mod,
    plot=True,
    title="Lugar Geométrico das Raízes - G2(s) com zeros em -3 e -4"
)

plt.grid(True)
plt.tight_layout()

# Ajuste manual dos limites dos eixos para evitar distorção
plt.xlim(-5, 3)
plt.ylim(-2, 2) 

plt.savefig(
    'data/lgr_G2_depois.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()


# Reposicionando polos para aumentar a faixa estável
num_G3 = [1]
den_G3 = [1, 6, 11, 6]

G3 = ct.TransferFunction(
    num_G3,
    den_G3
)

# LIMITE DE ESTABILIDADE DO SISTEMA ORIGINAL
print(
    f"Limite de estabilidade de G3(s) original: "
    f"K = {K_lim_G3_orig}"
)


# REPOSICIONAMENTO DO POLO
K_lim_G3_mod = 2 * K_lim_G3_orig

p_roots = np.roots(
    [3, 7, -114]
)

# Seleciona a raiz positiva
p = p_roots[p_roots > 0][0]

print(
    "Polo original: s = -3"
)

print(
    f"Novo polo: s = {-p:.4f}"
)

print(
    f"Novo limite de estabilidade: "
    f"K = {K_lim_G3_mod}"
)


# SISTEMA G3 MODIFICADO
den_G3_mod = [
    1,
    3 + p,
    2 + 3 * p,
    2 * p
]

G3_mod = ct.TransferFunction(
    num_G3,
    den_G3_mod
)


# PONTOS DE CRUZAMENTO DO EIXO IMAGINÁRIO
imag_G3 = np.sqrt(11)

poles_G3_cross = [
    1j * imag_G3,
    -1j * imag_G3
]



# G3 modificado
imag_G3_mod = np.sqrt(
    2 + 3 * p
)

poles_G3_mod_cross = [
    1j * imag_G3_mod,
    -1j * imag_G3_mod
]


# GRÁFICO G3 ORIGINAL
plt.figure(figsize=(8, 6))

ct.root_locus(
    G3,
    plot=True,
    title="Lugar Geométrico das Raízes - G3(s) Original"
)

# Marca os polos no cruzamento do eixo imaginário
plt.plot(
    np.real(poles_G3_cross),
    np.imag(poles_G3_cross),
    'o',
    markersize=8,
    markeredgewidth=2,
    label=f'Cruzamento: K = {K_lim_G3_orig}'
)

# Eixo imaginário
plt.axvline(
    0,
    linestyle='--',
    linewidth=1
)

plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginária')

plt.grid(True)
plt.legend()
plt.tight_layout()

# ESTE É O ARQUIVO NECESSÁRIO PARA O LATEX:
plt.savefig(
    'data/lgr_g3_antes.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()


# GRÁFICO G3 MODIFICADO
plt.figure(figsize=(8, 6))

ct.root_locus(
    G3_mod,
    plot=True,
    title=(
        "Lugar Geométrico das Raízes - G3(s) Modificado\n"
        f"Polo deslocado para s = {-p:.2f}"
    )
)

# Marca os polos no cruzamento do eixo imaginário
plt.plot(
    np.real(poles_G3_mod_cross),
    np.imag(poles_G3_mod_cross),
    'o',
    markersize=8,
    markeredgewidth=2,
    label=f'Cruzamento: K = {K_lim_G3_mod}'
)

# Eixo imaginário
plt.axvline(
    0,
    linestyle='--',
    linewidth=1
)

plt.xlabel('Parte Real')
plt.ylabel('Parte Imaginária')

plt.grid(True)
plt.legend()
plt.tight_layout()

# ESTE É O ARQUIVO NECESSÁRIO PARA O LATEX:
plt.savefig(
    'data/lgr_g3_depois.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()