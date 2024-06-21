import base as b 
import matplotlib.pyplot as plt
import core as c 
import plotting as pl 


b.config_labels()

df = c.load_results('saa', eyear = 2022)
ds = c.split_with_solar_level(df)

def plot_polynomial_fitting(ds):
    
    fig, ax = plt.subplots(
        figsize = (10, 8), 
        dpi = 300
        
        )
    
    
    data, epbs = pl.plot_distribution(
            ax, 
            ds,
            parameter = 'gamma',
            label = 'Distribuição para o máximo solar',
            axis_label = True, 
            translate = True
        )
    
    fit = c.polynomial_fit(data)
    
    ax.plot(
        fit['gamma'], 
        fit['prob'] * 100, color = 'r', lw = 2, 
        label = 'Ajuste polinominal de 4° ordem'
            )
    
    ax.legend(ncol = 1, loc = 'upper center')
    
    return fig
    
fig = plot_polynomial_fitting(ds)

FigureName = 'Ajuste_polinomial'
   
fig.savefig(b.LATEX(FigureName, folder = 'distributions/pt'))
   
   