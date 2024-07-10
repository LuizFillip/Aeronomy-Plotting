import matplotlib.pyplot as plt 
import core as c 
import base as b 
import datetime as dt 

b.config_labels()

def plot_gamma_predict_epbs(df):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 3,
        sharex = True,
        figsize = (16, 14)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    ax[0].plot(df['gamma'], lw = 1.5)
    
    ax[1].plot(df['predict'] * 100, lw = 1.5, color = 'k')
    
    ax[1].axhline(50, linestyle = ':')
    
    ax[2].plot(
        df['epb'], 
        linestyle = 'none',
        fillstyle = 'none',
        color = 'k',
        markersize = 10, 
        marker = 'o', 
        label = 'Observadas'
        )
    
    ax[2].plot(
        df['epb_est'], 
        color = 'b', 
        marker = 's', 
        linestyle = 'none',
        fillstyle = 'none',
        markersize = 10,
        label = 'Estimadas'
        )
    
    ax[2].legend(
        bbox_to_anchor = (0.5, 1.05), 
        ncol = 2, 
        loc = 'upper center'
        )
    
    ax[1].set(
        ylabel = 'Probabilidade (\%)', 
        ylim = [-20, 130], 
        yticks = list(range(0, 125, 25))
        )
  
    ax[0].set(
        ylabel = '$\gamma_{RT} ~(10^{-3}~s^{-1})$', 
        yticks = list(range(0, 4, 1))
        )
    
    ax[2].set(
        ylabel = 'Ocorrência', 
        ylim = [-0.2, 1.4], 
        xlim = [df.index[0], df.index[-1]],
        yticks = [0, 1]
        )
    
    b.format_month_axes(ax[2], translate = False)
    
    for line in [0, 1]:
        
        ax[1].axhline(line * 100, lw = 0.5, linestyle = '--') 
        ax[2].axhline(line, lw = 0.5, linestyle = '--')
    
    b.plot_letters(ax, y = 0.85, x = 0.02, fontsize = 40)
    
    return fig 


def main():
    time = dt.datetime(2023, 11, 13)
    df = c.load_results('saa', eyear = 2023)
    df.loc[df.index > time, 'gamma'] *= 0.7
    ds = c.predict_seasons(df)
    
    fig = plot_gamma_predict_epbs(ds)
    
    FigureName = 'Estimation_2023'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'climatology')
        )
    
    
main()


