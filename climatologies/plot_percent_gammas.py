import datetime as dt 
import matplotlib.pyplot as plt
import base as b 
import core as c 
import RayleighTaylor as rt 


b.config_labels()


def plot_percent_gamma_weigths(df, cols):
    
    fig, ax = plt.subplots(
        figsize = (16, 6), 
        dpi = 300
        )

    lb = rt.EquationsFT()

    df = df.resample('1M').mean()

    names = [lb.gravity, lb.drift, lb.winds]

    for i, col in enumerate(cols[1:]):
       
        ax.plot((df[col] / df['gamma']),
                label = names[i], lw = 2
                )
       
    ax.legend(
        ncol = 3, 
        bbox_to_anchor = (0.5, 1.25),
        columnspacing = 0.3,
        loc = "upper center"      
        )

    ax.set(
        ylim = [-0.5, 1],
        xlim = [df.index[0], df.index[-1]],
        ylabel = 'Contribuição em $\gamma_{RT}$', 
        xlabel = 'Anos'
        )
    
    ax.axhline(0, linestyle = '--')
    plt.show()
    
    return fig


def main():
    cols = ['gamma', 'gravity', 'drift', 'winds']
    
    df  = c.gamma(
            site = 'saa', 
            time = dt.time(22, 0), 
            el_upper = True,
            file = 'p2',
            gamma_cols = cols
            )
    
    
    fig = plot_percent_gamma_weigths(df, cols)
    
    FigureName = 'weight_in_each_term'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'climatology'),
        dpi = 400
        )