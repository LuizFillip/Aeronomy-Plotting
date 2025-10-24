import matplotlib.pyplot as plt
import core as c
import base as b

b.sci_format(fontsize = 25)


def plot_count_events_by_symh(df):
    
    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        'quiet': '#32CD32'      # verde
    }

    
    # Ordenar as colunas conforme severidade
    df = df[['intense', 'moderate', 'weak', 'quiet']]
    
    fig, ax = plt.subplots(dpi = 300, figsize = (12, 6))
    df.plot(
        kind='bar',
        stacked=True,
        color=[colors[c] for c in df.columns], 
        ax = ax
    )
    
    # Adicionar rótulos no centro de cada bloco
    for i, idx in enumerate(df.index):
        y_offset = 0
        for col in df.columns:
            value = df.loc[idx, col]
            if value > 0:
                ax.text(i, y_offset + value / 2, 
                        f"{int(value)}",
                        ha='center', va='center', color='k', 
                        fontsize=10, weight='bold'
                        )
            y_offset += value
    
 
    ax.set(
        xlabel = "Phase", 
        ylabel = "Number of occurrences", 
        title = "EPB occurrences by phase and geomagnetic category"
        )


    legend_labels = {
        'quiet': 'SYM-H $>$ -30 nT',
        'weak': '-50 $<$ SYM-H $\leq$ -30 nT',
        'moderate': '-100 $<$ SYM-H $\leq$ -50 nT',
        'intense': 'SYM-H $\leq$ -100 nT'
    }
    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles, [legend_labels[l] for l in labels],
        title = "Geomagnetic Condition (SYM-H)",
        loc = 'upper left',
        fontsize = 20,
        title_fontsize = 20
    )
    
    ax.set_xticklabels(df.index, rotation=0, ha='center')
    
    plt.tight_layout()
    plt.show()
    return fig 


df = c.geomagnetic_analysis()

df = c.count_events(df)

fig = plot_count_events_by_symh(df)