#ifndef MANIPULACAO_SINAIS_HPP
#define MANIPULACAO_SINAIS_HPP

#include "config.hpp"
#include "plot.hpp"
#include <chrono>
#include <ctime>

// Para montar um sistema, varios sinais (proximas atividades, suponho)
struct Sinal {
    vector<double> amplitudes;
    vector<int> indices;
    string nome;
    
    Sinal() {}
    Sinal(const vector<double>& amps, const vector<int>& idx, const string& nome_sinal = "")
        : amplitudes(amps), indices(idx), nome(nome_sinal) {}
};

// Operacoes basicas com sinais
Sinal reflexao(const Sinal& sinal);
Sinal mudanca_escala(const Sinal& sinal, int fator);
Sinal alteracao_amplitude(const Sinal& sinal, double ganho);
Sinal deslocamento(const Sinal& sinal, int k);
Sinal soma_sinais(const Sinal& sinal1, const Sinal& sinal2);
Sinal degrau(int tamanho, double amplitude, int inicio = 0);


// Funcoes auxiliares
void plottarSinal(Sinal& sinal);
vector<int> criar_indices(int inicio, int fim);
void normalizar_indices(Sinal& sinal);

#endif
