#include "plot.hpp"
#include "manipulacao_sinais.hpp" 

Plot_SinaisSistemas::Plot_SinaisSistemas(bool persist) {
    gp = make_unique<Gnuplot>("gnuplot", persist);
    
    if (!gp->ok()) {
        cerr << "Erro: Nao foi possivel conectar ao Gnuplot!" << endl;
    }
}

void Plot_SinaisSistemas::plot_discrete(const Sinal& sinal) {
    if (!gp->ok()) return;

    gp->reset();
    gp->set_title(sinal.nome);
    gp->set_xlabel("n (indice)");
    gp->set_ylabel("Amplitude");
    
    gp->plot(sinal.indices, sinal.amplitudes, sinal.nome, Gnuplot::LineStyle::POINTS);
    gp->show();
}

void Plot_SinaisSistemas::plot_comparison(const Sinal& s1, const Sinal& s2) {
    if (!gp->ok()) return;

    gp->reset();
    gp->set_title("Comparacao de Sinais");
    
    gp->plot(s1.indices, s1.amplitudes, s1.nome, Gnuplot::LineStyle::LINESPOINTS);
    gp->plot(s2.indices, s2.amplitudes, s2.nome, Gnuplot::LineStyle::LINESPOINTS);
    
    gp->show();
}

void QuickPlot::plot(const Sinal& sinal) {
    Plot_SinaisSistemas sp;
    sp.plot_discrete(sinal);
}


#include <limits>

void Plot_SinaisSistemas::save_as_png(const Sinal& sinal, const string& filename) {
    if (!gp->ok()) return;

    gp->reset();
    gp->redirect_to_png(filename, "1200,800");

    gp->set_title(sinal.nome);
    gp->set_xlabel("n (indice)");
    gp->set_ylabel("Amplitude");


    vector<double> x_imp;
    vector<double> y_imp;

    double nan = numeric_limits<double>::quiet_NaN();

    for (size_t i = 0; i < sinal.indices.size(); i++) {
        x_imp.push_back(sinal.indices[i]);
        y_imp.push_back(0);

        x_imp.push_back(sinal.indices[i]);
        y_imp.push_back(sinal.amplitudes[i]);

        x_imp.push_back(nan);
        y_imp.push_back(nan);
    }

    gp->plot(x_imp, y_imp, "hastes", Gnuplot::LineStyle::LINES);
    gp->plot(sinal.indices, sinal.amplitudes, "pontos", Gnuplot::LineStyle::POINTS);

    gp->show();
    gp.reset();

    cout << "Gráfico salvo com sucesso em: " << filename << endl;
}