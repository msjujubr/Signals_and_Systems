#include "manipulacao_sinais.hpp"
#include "plot.hpp"

// a) Reflexao: y[n] = x[-n]
Sinal reflexao(const Sinal& sinal) {
    Sinal resultado;
    resultado.nome = "Reflexao - " + sinal.nome;

    resultado.indices.resize(sinal.indices.size());
    resultado.amplitudes = sinal.amplitudes;

    for (size_t i = 0; i < sinal.indices.size(); ++i) {
        resultado.indices[i] = -sinal.indices[i];
    }

    return resultado;
}

// b) Mudanca de Escala: y[n] = x[an]
Sinal mudanca_escala(const Sinal& sinal, double fator) {
    if (fator == 0) return sinal;

    Sinal resultado;
    resultado.nome = "Escala (a=" + to_string(fator) + ") - " + sinal.nome;

    int min_n = static_cast<int>(floor(*min_element(sinal.indices.begin(), sinal.indices.end()) / fator));
    int max_n = static_cast<int>(ceil(*max_element(sinal.indices.begin(), sinal.indices.end()) / fator));

    for (int n = min_n; n <= max_n; ++n) {
        double busca_original = n * fator;

        for (size_t i = 0; i < sinal.indices.size(); ++i) {
            if (abs(sinal.indices[i] - busca_original) < 1e-9) {
                resultado.indices.push_back(n);
                resultado.amplitudes.push_back(sinal.amplitudes[i]);
            }
        }
    }

    return resultado;
}
    
// c) Alteracao de Amplitude: y[n] = A * x[n]
Sinal alteracao_amplitude(const Sinal& sinal, double amp) {
    Sinal resultado;
    resultado.nome = "Alteracao de Amplitude (amp = " + to_string(amp) + ")  - " + sinal.nome;
    resultado.indices = sinal.indices;
    resultado.amplitudes.resize(sinal.amplitudes.size());
    
    for (size_t i = 0; i < sinal.amplitudes.size(); ++i) {
        resultado.amplitudes[i] = sinal.amplitudes[i] * amp;
    }
    
    return resultado;
}

// d) Deslocamento: y[n] = x[n - k]
Sinal deslocamento(const Sinal& sinal, int k) {
    Sinal resultado;
    resultado.nome = "Deslocamento (k = " + to_string(k) + ")  - " + sinal.nome;
    resultado.amplitudes = sinal.amplitudes;
    resultado.indices.resize(sinal.indices.size());
    
    for (size_t i = 0; i < sinal.indices.size(); ++i) {
        resultado.indices[i] = sinal.indices[i] + k;
    }
    
    return resultado;
    
}

// e) Soma de dois sinais: y[n] = x1[n] + x2[n]
Sinal soma_sinais(const Sinal& sinal1, const Sinal& sinal2) {
    Sinal resultado;
    resultado.nome = "Soma: " + sinal1.nome + " + " + sinal2.nome;
    
    // Determinar o intervalo de indices comum
    int idx_min = min(*min_element(sinal1.indices.begin(), sinal1.indices.end()),
                     *min_element(sinal2.indices.begin(), sinal2.indices.end()));
    int idx_max = max(*max_element(sinal1.indices.begin(), sinal1.indices.end()),
                     *max_element(sinal2.indices.begin(), sinal2.indices.end()));
    
    resultado.indices = criar_indices(idx_min, idx_max);
    resultado.amplitudes.assign(resultado.indices.size(), 0.0);
    
    // Adicionar sinal1
    for (size_t i = 0; i < sinal1.indices.size(); ++i) {
        int pos = sinal1.indices[i] - idx_min;
        if (pos >= 0 && static_cast<size_t>(pos) < resultado.amplitudes.size()) {
            resultado.amplitudes[pos] += sinal1.amplitudes[i];
        }
    }
    
    // Adicionar sinal2
    for (size_t i = 0; i < sinal2.indices.size(); ++i) {
        int pos = sinal2.indices[i] - idx_min;
        if (pos >= 0 && static_cast<size_t>(pos) < resultado.amplitudes.size()) {
            resultado.amplitudes[pos] += sinal2.amplitudes[i];
        }
    }
    
    return resultado;
}

// Gerar sinal degrau: u[n]
Sinal degrau(int tamanho, double amplitude, int inicio) {
    Sinal resultado;
    resultado.nome = "Degrau (Amplitude = " + to_string(amplitude) + ")";
    resultado.indices = criar_indices(0, tamanho - 1);
    resultado.amplitudes.resize(tamanho, 0.0);
    
    for (int i = inicio; i < tamanho; ++i) {
        if (i >= 0 && i < tamanho) {
            resultado.amplitudes[i] = amplitude;
        }
    }
    
    return resultado;
}


// Funcao para criar um vetor de indices
vector<int> criar_indices(int inicio, int fim) {
    vector<int> indices;
    for (int i = inicio; i <= fim; ++i) {
        indices.push_back(i);
    }
    return indices;
}

// Normaliza os indices para ficarem continuos
void normalizar_indices(Sinal& sinal) {
    if (sinal.indices.empty()) return;
    vector<int> novos_indices(sinal.indices.size());
    int min_idx = *min_element(sinal.indices.begin(), sinal.indices.end());
    
    for (size_t i = 0; i < sinal.indices.size(); ++i) {
        novos_indices[i] = sinal.indices[i] - min_idx;
    }
    sinal.indices = novos_indices;
}

void plottarSinal(Sinal& sinal){
    auto now = system_clock::now();
    time_t tt = system_clock::to_time_t(now);
    tm tm = *localtime(&tt);

    ostringstream oss;
    oss << put_time(&tm, "%Y%m%d_%H%M%S");
    string date = oss.str();

    replace(sinal.nome.begin(), sinal.nome.end(), ' ', '_');
    string filename = "graphs/" + sinal.nome + "_" + date + ".png";


    Plot_SinaisSistemas plotter;
    plotter.save_as_png(sinal, filename);
}
