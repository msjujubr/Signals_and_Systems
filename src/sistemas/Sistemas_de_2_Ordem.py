import numpy as np
import matplotlib.pyplot as plt
import control.matlab as ctrl

wn = 10
zetas = [0, 0.5, 1, 2]

print("Parâmetros para diferentes valores de Zeta ---") # parâmetros de oscilação

plt.figure(figsize=(10, 6))

for z in zetas:
    # Função de Transferência de Segundo Grau
    num = [wn**2]
    den = [1, 2*z*wn, wn**2]
    sys = ctrl.tf(num, den)
    
    # Obtendo a resposta ao degrau
    y, t = ctrl.step(sys)
    plt.plot(t, y, label=rf'$\zeta$ = {z}')
    # Extraindo os parâmetros
    info = ctrl.stepinfo(sys)
    
    print(f"\nZeta = {z}:")
    print(f"  Tempo de Subida (tr): {info['RiseTime']:.4f} s")
    print(f"  Máximo Sobressinal (Mp): {info['Overshoot']:.2f} %")
    print(f"  Tempo de Acomodação (ts): {info['SettlingTime']:.4f} s")

# Configurando o primeiro gráfico
plt.title(r'Resposta ao Degrau para Diferentes Coeficientes de Amortecimento ($\zeta$)')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
plt.savefig('data/grafico_zetas.png') 


# Otimização do sistema (inserção de amortecimento)
print("Buscando Zeta para: tr < 0.17 | Mp <= 30% | ts < 0.90")

melhor_zeta = None

# Varrendo possíveis valores de zeta entre 0.1 e 0.9
for z_teste in np.arange(0.1, 0.99, 0.01):
    num = [wn**2]
    den = [1, 2*z_teste*wn, wn**2]
    sys_teste = ctrl.tf(num, den)
    
    info_teste = ctrl.stepinfo(sys_teste)
    tr = info_teste['RiseTime']
    mp = info_teste['Overshoot']
    ts = info_teste['SettlingTime']
    
    # Verificando os critérios do roteiro
    if tr < 0.17 and mp <= 30 and ts < 0.90:
        melhor_zeta = z_teste
        print(f"\nValor ideal de Zeta encontrado: {melhor_zeta:.2f}")
        print(f"  Tempo de Subida (tr): {tr:.4f} s")
        print(f"  Máximo Sobressinal (Mp): {mp:.2f} %")
        print(f"  Tempo de Acomodação (ts): {ts:.4f} s")
        break

if melhor_zeta is not None:
    # Gerando o gráfico do sistema otimizado
    num_opt = [wn**2]
    den_opt = [1, 2*melhor_zeta*wn, wn**2]
    sys_opt = ctrl.tf(num_opt, den_opt)
    y_opt, t_opt = ctrl.step(sys_opt)
    
    plt.figure(figsize=(8, 5))
    plt.plot(t_opt, y_opt, color='green', linewidth=2, label=rf'$\zeta$ Otimizado = {melhor_zeta:.2f}')
    
    plt.axhline(1, color='black', linestyle='--', alpha=0.5) # Linha de referência (degrau unitário)
    plt.title('Resposta ao Degrau - Sistema Otimizado')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.savefig('data/grafico_otimizado.png') 

else:
    print("\nNão foi encontrado um Zeta que satisfaça todos os requisitos simultaneamente.")