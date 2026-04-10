#include "manipulacao_sinais.hpp"
#include <iostream>
#include <vector>

using namespace std;

/*
    CRONOLOGIA:
    Tarefa I (SS): Manipulacao de Sinais (10/04/2026)
*/

int cabecalho_inicio();
void cabecalho_manipulacaoSS();

int main() {
    while (true) {
        int op = cabecalho_inicio();
        if (op == 0) break;

        switch (op) {
            case 1:
                cabecalho_manipulacaoSS();
                break;

            default:
                cout << "Opcao invalida!\n";
                break;
        }
    }

    return 0;
}

int cabecalho_inicio() {
    int opcao;

    do {
        cout << "\nESCOLHA QUAL TAREFA:\n";
        cout << "1) Manipulacao de Sinais\n";
        cout << "0) Encerrar projeto\n";
        cout << "Opcao: ";
        cin >> opcao;

    } while (opcao < 0 || opcao > 1);

    return opcao;
}

void cabecalho_manipulacaoSS() {
    int n;

    cout << "\nDigite o tamanho do sinal: ";
    cin >> n;

    vector<double> amplitudes(n);

    cout << "Digite as amplitudes:\n";
    for (int i = 0; i < n; i++) {
        cin >> amplitudes[i];
    }

    // FIX: Create indices vector
    vector<int> indices = criar_indices(0, n-1);
    Sinal sinal(amplitudes, indices, "Astolfo");

    plottarSinal(sinal);

    int opcao;

    while (true)
    {
        cout << "\nMANIPULACAO DE SINAIS:\n";
        cout << "1) Reflexao\n";
        cout << "2) Mudanca de Escala\n";
        cout << "3) Mudanca de Amplitude\n";
        cout << "4) Deslocamento\n";
        cout << "5) Soma com Degrau\n";
        cout << "0) Voltar\n";
        cout << "Opcao: ";
        cin >> opcao;

        switch (opcao) {

            case 1: {
                Sinal novo = reflexao(sinal);
                cout << "\nReflexao:\n";
                plottarSinal(novo);  // Added missing plot
                break;
            }

            case 2: {
                double fator;
                cout << "Fator de escala: ";
                cin >> fator;

                Sinal novo = mudanca_escala(sinal, fator);

                cout << "\nEscala:\n";
                plottarSinal(novo);

                break;
            }

            case 3: {
                double ganho;
                cout << "Ganho: ";
                cin >> ganho;

                Sinal novo = alteracao_amplitude(sinal, ganho);

                cout << "\nAmplitude:\n";
                plottarSinal(novo);  // Added missing plot
                break;
            }

            case 4: {
                int k;
                cout << "Deslocamento: ";
                cin >> k;

                Sinal novo = deslocamento(sinal, k);

                cout << "\nDeslocamento:\n";
                plottarSinal(novo);  // Added missing plot
                break;
            }

            case 5: {
                double amp;
                cout << "Amplitude do degrau: ";
                cin >> amp;

                Sinal deg = degrau(n, amp, 0);
                Sinal soma = soma_sinais(sinal, deg);

                cout << "\nSoma com degrau:\n";
                plottarSinal(soma);  // Added missing plot
                break;
            }

            case 0:
                cout << "Voltando...\n";
                break;

            default:
                cout << "Opcao invalida!\n";
                break;
        }
        
        if (opcao == 0) break;  // Exit the while loop when user chooses 0
    }
}