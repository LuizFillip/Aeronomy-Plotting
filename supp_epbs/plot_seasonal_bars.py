import matplotlib.pyplot as plt 
import core as c
import base as b
import plotting as pl 

b.sci_format(fontsize = 25)


def plot_seasonal_bars(ds):

    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        'quiet': '#32CD32'      # verde
    }
    ds = ds.reindex(range(1, 13), fill_value = 0)
    
    fig, ax = plt.subplots(dpi = 300, figsize = (12, 6))
    ds.plot(
        kind='bar',
        stacked=True,
        ax = ax,
        color=[colors[c] for c in ds.columns]
    )
    
    ax.set(
        ylim = [0, 30],
        xticklabels = b.month_names(language = 'en'),
        ylabel = 'Number of cases', 
        xlabel = 'Months'
        )
    
    plt.xticks(rotation = 0)
    
    pl.legend_for_sym_h(
        ax, 
        quiet = True, 
        ncol = 2, 
        loc = 'upper center'       
        )
    
    fig.align_ylabels()
    
    return fig
    

def main():
    
    ds = c.seasonal_data(
        col_dst = 'sym_min',
        col_kp = 'kp_max'
        )
    
    fig = plot_seasonal_bars(ds)
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Suppression_stastistical\\June-2024-latex-templates\\'
    
    FigureName = 'seasonal_bars_by_storm'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 300)
    
# main()
