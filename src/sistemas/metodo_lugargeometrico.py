import control as ct
import matplotlib.pyplot as plt

# Análise Crítica da Saída do Python

# 1. Gráfico Original com Erro (Listagem 1 do roteiro)
# O erro no PDF era usar num = [1, 2]
print("Gerando o Lugar das Raízes da Parte 1 (Código com Erro)...")
num_erro = [1, 2] # Representa (s + 2) 
den = [1, 4, 9, 10, 0] # Representa (s^4 + 4s^3 + 9s^2 + 10s)

G_erro = ct.TransferFunction(num_erro, den)

plt.figure(figsize=(10, 6))
ct.root_locus(G_erro)
plt.title("Lugar das Raízes com Erro - G_erro(s)")
plt.xlabel("Eixo Real")
plt.ylabel("Eixo Imaginário")
plt.grid(True)
plt.savefig('data/lgr_erro.png', dpi=300) # Salva a imagem para usar no relatório
plt.close()


# 2. Gráfico Corrigido
# Função teórica G(s) = (s + 1) / (s(s + 2)(s^2 + 2s + 5))
print("Gerando o Lugar das Raízes da Parte 1 (Código Corrigido)...")
num_corrigido = [1, 1] # Representa (s + 1) - Corrigido

G_corrigido = ct.TransferFunction(num_corrigido, den)

plt.figure(figsize=(10, 6))
ct.root_locus(G_corrigido)
plt.title("Lugar das Raízes Corrigido - G(s)")
plt.xlabel("Eixo Real")
plt.ylabel("Eixo Imaginário")
plt.grid(True)
plt.savefig('data/lgr_corrigido.png', dpi=300) # Salva a imagem para usar no relatório
plt.close()


# Avaliação Rápida da Estabilidade

# 3. Sistema 1: G1(s) = 1 / (s(s + 1)(s + 2))
#    Expandido: s(s^2 + 3s + 2) = s^3 + 3s^2 + 2s
print("Gerando o Lugar das Raízes da Parte 2 - G1(s)...")
num_g1 = [1]
den_g1 = [1, 3, 2, 0]

G1 = ct.TransferFunction(num_g1, den_g1)

plt.figure(figsize=(10, 6))
ct.root_locus(G1)
plt.title("Lugar das Raízes - G1(s)")
plt.xlabel("Eixo Real")
plt.ylabel("Eixo Imaginário")
plt.grid(True)
plt.savefig('data/simulacao_rampa.png', dpi=300) 
plt.close()

# 4. Sistema 2: G2(s) = 1 / (s(s - 1)(s + 2))
#    Expandido: s(s^2 + s - 2) = s^3 + s^2 - 2s
print("Gerando o Lugar das Raízes da Parte 2 - G2(s)...")
num_g2 = [1]
den_g2 = [1, 1, -2, 0]

G2 = ct.TransferFunction(num_g2, den_g2)

plt.figure(figsize=(10, 6))
ct.root_locus(G2)
plt.title("Lugar das Raízes - G2(s)")
plt.xlabel("Eixo Real")
plt.ylabel("Eixo Imaginário")
plt.grid(True)
plt.savefig('data/simulacao_degrau_rampa.png', dpi=300)
plt.close()

print("Todos os gráficos foram gerados e salvos com sucesso!")