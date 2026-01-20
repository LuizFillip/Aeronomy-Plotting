import matplotlib.pyplot as plt
import core as c
import base as b
import plotting as pl 

b.sci_format(fontsize = 25)



def plot_count_events_by_symh(df):
    
    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        # 'quiet': '#32CD32'      # verde
    }

    df = df[['intense', 'moderate', 'weak']]
    
    fig, ax = plt.subplots(dpi = 300, figsize = (12, 6))
    df.plot(
        kind='bar',
        stacked = True,
        color = [colors[c] for c in df.columns], 
        ax = ax
    )
    
    fontsize = 35
    
    for i, idx in enumerate(df.index):
        y_offset = 0
        for col in df.columns:
            value = df.loc[idx, col]
            if value > 0:
                ax.text(i, y_offset + value / 2, 
                        f"{int(value)}",
                        ha = 'center', va='center', color='k', 
                        fontsize=fontsize, weight='bold'
                        )
            y_offset += value
    
 
    ax.set(
        xlabel = "Storm phase", 
        ylabel = "Number of occurrences", 
        title = "Storm-time events"
        )

    pl.legend_for_sym_h(ax)
      
    ax.set_xticklabels(
        df.index,
        rotation = 0, 
        ha = 'center'
        )
    
    plt.tight_layout()
    plt.show()
    return fig 


def main(df):


    df = c.geomagnetic_analysis(df)
    
    df = c.count_events(df)
    
    fig = plot_count_events_by_symh(df)
    
    path_to_save = 'G:\\Meu Drive\\Papers\\SuppressionAnalysis\\June-2024-latex-templates\\'
    
    FigureName = 'count_by_phases'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 300)
    
    
# main()

df = b.load('core/src/geomag/data/stormsphase')

df_source = b.load('core/src/geomag/data/4hours_low_res')

for col in df_source.columns:
    df[col] = df.index.map(df_source[col])
    
    
df = df.iloc[:, 3:] 