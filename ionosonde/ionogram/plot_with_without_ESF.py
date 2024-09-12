import plotting as pl 
import matplotlib.pyplot as plt 
import base as b 

b.config_labels()

path = 'E:\\ionogram\\20131224S\\'

def plot_ionogram(ax, fname):
    pl.plot_single_ionogram(
            path + fname, 
            ax, 
            label = True, 
            ylabel_position = "left",
            aspect = 'auto', 
            title = False
            )
    
def plot_with_without_ESF():
    
    fig, ax = plt.subplots(
        ncols = 2, 
        dpi = 300, 
        figsize = (16, 10)
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    plot_ionogram(ax[0], 'SAA0K_20131224(358)215000.PNG')
    plot_ionogram(ax[1], 'SAA0K_20131224(358)235000.PNG')
    
    ax[1].set(yticklabels = [], 
              ylabel = '', 
              xlabel = '', 
              title = '23h50 UT - Com ESF')
    ax[0].set(xlabel = '', 
              title = '21h50 UT - Sem ESF')
    
    
    b.plot_letters(ax, y = 1.1, x = -0.1, fontsize = 40)
    
    fig.text(0.35, 0.01, 'Frequência (MHz)')
    fig.suptitle('24 de dezembro de 2013', y = 1.1)
    return fig 

def main():
    fig = plot_with_without_ESF()
    
    FigureName = '20131224_with_without_ESF'
    fig.savefig(
            b.LATEX(FigureName, folder = 'Iono'),
            dpi = 400
            )