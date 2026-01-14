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
        xlabel = 'Months',
        title = 'Total of EPBs supressions by SYM-H'
        )
    
    plt.xticks(rotation = 0)
    
    pl.legend_for_sym_h(ax, quiet = True)
    fig.align_ylabels()
    
    return fig
    

def main():
    
    df = b.load('core/src/geomag/data/stormsphase2')

    df = c.geomagnetic_analysis(df)
    print(df)
    
    df['month'] = df.index.month 
    
    ds = df.groupby(['category', 'month']).size().unstack(fill_value=0)
    
    # print(df[['kp', 'category', 'sym']])
    ds = ds.T[['intense', 'moderate', 'weak', 'quiet']]
    
    fig = plot_seasonal_bars(ds)
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Suppression_stastistical\\June-2024-latex-templates\\'
    
    FigureName = 'seasonal_bars_by_storm'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 300)
    
# main()
