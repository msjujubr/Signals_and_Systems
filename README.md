# Sinais e Sistemas (Estudos)

![C++](https://img.shields.io/badge/Linguagem-C++-green.svg)
![Make](https://img.shields.io/badge/Compilacao-Make-orange)
![VSCode](https://img.shields.io/badge/IDE-VSCode-informational)
![ISO](https://img.shields.io/badge/ISO-Linux-blueviolet)


***Este repositório consiste na documentação dos conceitos aprendidos e implementações na disciplina Sinais e Sistemas. Foram documentados teorias e códigos relacionados as atividades realizadas durante a disciplina sobre **sinais discretos unidimensionais*****

***O sistema foi desenvolvido em **C++**, permitindo entrada interativa de dados e geração automática de gráficos para análise dos resultados.***





 
<div align="center"> <table> <tr> <td>
 
### 📖 Sumário
- [Compilação, Entradas e Saídas](#compilação-entradas-e-saidas)
  - [MakeFile](#makefile)
  - [Input.dat](#input.dat)
  - [Output.dat](#outputdat)
- [Sinais e Sistemas](#sinais-e-sistemas)
  - [Manipulação de Sinais](#manipulacao-de-sinais)
- [Referências](#referências)

</td> <td>

 <img src="Img/sumario.png" width="400">

</td> </tr> </table> </div>



## Compilação, Entradas e Saídas

### Makefile
O programa é executado por um Makefile, arquivo de texto que automatiza o processo de compilação, que interage com todos os arquivos dentro da pasta "src". 
Este apresenta os seguintes comandos:

&nbsp;&nbsp;&nbsp;&nbsp;**make:** Compila o projeto

&nbsp;&nbsp;&nbsp;&nbsp;**make clean:** Remove os arquivos

&nbsp;&nbsp;&nbsp;&nbsp;**make run:** Compila o projeto (se necessário) e depois executa o programa.

&nbsp;&nbsp;&nbsp;&nbsp;**make c:** make clean + make run

[Script do Makefile utilizado (C++)](Makefile)

### Entradas 


A interação com o sistema é realizada via terminal, através de **menus (cabeçalhos)** que guiam o usuário durante a execução do programa.

Inicialmente, o usuário escolhe qual tarefa deseja executar:

         ESCOLHA QUAL TAREFA:
          1)Manipulacao de Sinais
          0)Encerrar projeto


Após selecionar a opção de manipulação de sinais, o sistema solicita:

- O tamanho do sinal discreto
- Os valores das amplitudes

Exemplo:

         Digite o tamanho do sinal: 5
         Digite as amplitudes:
         1 2 3 4 5


Em seguida, um novo cabeçalho é exibido com as operações disponíveis:

        
         MANIPULACAO DE SINAIS:
          1)Reflexao
          2)Mudanca de Escala
          3)Mudanca de Amplitude
          4)Deslocamento
          5)Soma com Degrau
          0)Voltar

O usuário pode navegar entre as opções e aplicar múltiplas operações sobre o sinal, retornando ao menu principal sempre que desejar. Dessa forma, o sistema funciona de maneira interativa e modular, permitindo ao usuário escolher dinamicamente qual atividade executar.

### Geração dos Gráficos
Todo o sistema pode gerar representações gráficas dos sinais manipulados.  
Os gráficos são automaticamente salvos na pasta: [graphs](graphs/). Os arquivos são gerados no formato `.png` e são nomeados com nomes únicos baseados no tipo de operação e timestamp.


#### Gnuplot e gplot++

O sistema utiliza a biblioteca `gplot++` como interface para comunicação com o **Gnuplot**, responsável pela geração dos gráficos dos sinais.

A biblioteca `gplot++` é *header-only*, ou seja, não requer instalação complexa — basta incluir o arquivo `gplot++.h` no projeto.

---

#### Instalação do Gnuplot

Antes de executar o projeto, é necessário ter o **Gnuplot** instalado e disponível no `PATH` do sistema. No Linux, pode ser instalado via gerenciador de pacotes:

                            sudo apt-get install gnuplot

- O Gnuplot deve estar corretamente configurado no `PATH`, caso contrário os gráficos não serão gerados
- Cada execução gera arquivos únicos (com timestamp) na pasta `graphs/`


## Sinais e Sistemas


### Estrutura dos Sinais

Cada sinal é representado por:

- `indices` → valores do eixo discreto `n`
- `amplitudes` → valores do sinal `x[n]`
- `nome` → identificação do sinal



### Manipulação de Sinais

O sistema implementa operações fundamentais sobre sinais discretos, permitindo análise e visualização gráfica dos resultados.


Cada operação implementada no código gera automaticamente um arquivo .png na pasta graphs/, permitindo a visualização e análise dos resultados. Abaixo está a relação entre as funções desenvolvidas e seus respectivos fundamentos teóricos:


| Operação               | Descrição                                               |
|------------------------|---------------------------------------------------------|
| [`Reversão`](https://github.com/msjujubr/Atividade01/blob/main/src/config.cpp#L260)  | Espelhamento do sinal em torno do eixo vertical.Considerando um sinal original definido no intervalo n∈[0,N], o sinal refletido passa a existir no intervalo n∈[−N,0].|
| [`Mudança de Escala`](https://github.com/msjujubr/Atividade01/blob/main/src/config.cpp#L28) | Altera a taxa de amostragem percebida do sinal.  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   Compressão (quando o fator > 1)&nbsp;&nbsp;&nbsp; Expansão (quando o fator < 1)|
| [`Mudança de Amplitude`](https://github.com/msjujubr/Atividade01/blob/main/src/config.cpp#L8)     | Multiplica cada amostra x[n] por um valor escalar. 
| [`Deslocamento Temporal`](https://github.com/msjujubr/Atividade01/blob/main/src/config.cpp#L265)    | Deslocamento do sinal ao longo do eixo x (x[n-k]). Isso implica que o sinal está atrasado (+k) ou que o sinal está adiantado (-k) |
| [`Somatório de Sinais`](https://github.com/msjujubr/Atividade01/blob/main/src/config.cpp#L265)    | Soma de entre dois sinais. No sistema, realiza a soma ponto a ponto |
| [`Degrau`](https://github.com/msjujubr/Atividade01/blob/main/src/config.cpp#L265)    | Gera um sinal degrau com amplitude definida a partir de um índice inicial |
| [`Impulso`](https://github.com/msjujubr/Atividade01/blob/main/src/config.cpp#L265)    | Gera um impulso discreto em uma posição específica                  |


As implementações permitem observar propriedades importantes dos sinais:

* **Reflexão** evidencia simetria temporal
* **Escala** altera a densidade de amostragem percebida
* **Amplitude** modifica energia/potência do sinal
* **Deslocamento** altera posicionamento temporal sem mudar forma
* **Soma com degrau** simula resposta a entradas básicas



# Referências
- [1]&#58; LATHI, B. P. Sinais e Sistemas Lineares. 2. ed. Porto Alegre: Bookman, 2007.
- [2]&#58; 
  *Oppenheim, A. V., & Willsky, A. S. Sinais e Sistemas.*
- [3]&#58; http://www.gnuplot.info/ 
  *Documentação Gnuplot*
<div> 
  <a href="https://www.youtube.com/@msjujubr" target="_blank"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>
  <a href="https://instagram.com/msjujubr" target="_blank"><img src="https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white" target="_blank"></a>
 	<a href="https://www.twitch.tv/msjujubr" target="_blank"><img src="https://img.shields.io/badge/Twitch-9146FF?style=for-the-badge&logo=twitch&logoColor=white" target="_blank"></a>
  <a href = "mailto:juliamourasouza10@gmail.com"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
  <a href="https://www.linkedin.com/in/msjujubr/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
</div>


