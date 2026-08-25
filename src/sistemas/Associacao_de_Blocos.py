import control.matlab as ctr

# ASSOCIACAO DE BLOCOS - PRATICA 01 (Laboratorio de Teoria de Controle)
# Este laboratório tem como objetivo exercitar algumas funções para poder manipular funções de transferência.


# Funcoes de Transferencia de primeira ordem
s = ctr.tf('s')
G1 = 1 / (s+2)
G2 = 1 / (s+5)


def sistema_cascata(): 
    G_br = G1 * G2 
    G_bi = ctr.series(G1, G2)

    print('Saida Cascata Bruta-----------\n', G_br)
    print('Saida Cascata Biblioteca------\n', G_bi)
    

def sistema_paralelo(): 
    G_br = G1 + G2 
    G_bi = ctr.parallel(G1, G2)

    print('Saida Paralelo Bruto----------\n', G_br)
    print('Saida Paralelo Biblioteca-----\n', G_bi)
    

def sistema_retroalimentado(): 
    G_br = G1 / (1 + G1 * G2)
    G_bi = ctr.feedback(G1, G2)

    print('Saida Retroalimentada Bruta---\n', G_br)
    print('Saida Retroalimentada Biblioteca\n', G_bi)
    

def sistema_retroalimentado_tunado(): 
    GA = ctr.tf(G1)
    GB = ctr.tf(G2)
    G_br = GA / (1 + GA * GB)
    G_bi = ctr.feedback(GA, GB) # Feedback simplifica, trolla o sistema, ainda sim ambas as funções são equivalentes

    print(G_br)
    print(G_bi)



if __name__ == '__main__':
    #  G_brutal, G_bilioteca

    sistema_cascata()
    print("--------------------------------\n")
    sistema_paralelo()
    print("--------------------------------\n")
    sistema_retroalimentado()
    print("--------------------------------\n")
    sistema_retroalimentado_tunado()