#ifndef PLOT_HPP
#define PLOT_HPP

#include "manipulacao_sinais.hpp"
#include "gplot++.h" 
#include <memory>

struct Sinal;

class Plot_SinaisSistemas {
private:
    std::unique_ptr<Gnuplot> gp;
    
public:
    Plot_SinaisSistemas(bool persist = true);
    
    // Plota um sinal no estilo discreto (pontos/hastes)
    void plot_discrete(const Sinal& sinal);
    
    // Plota dois sinais para comparação
    void plot_comparison(const Sinal& s1, const Sinal& s2);

    // Salva o sinal em um arquivo PNG
    void save_as_png(const Sinal& sinal, const std::string& filename);
};

namespace QuickPlot {
    void plot(const Sinal& sinal);
}


#endif