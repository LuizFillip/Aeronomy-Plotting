import matplotlib.pyplot as plt
import core as c



def plot_count_events_by_symh(df):
    
    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        'quiet': '#32CD32'      # verde
    }

    
    # Ordenar as colunas conforme severidade
    df = df[['intense', 'moderate', 'weak', 'quiet']]
    
    fig, ax = plt.subplots(figsize = (6, 6))
    ax = df.plot(
        kind='bar',
        stacked=True,
        figsize=(7, 4),
        color=[colors[c] for c in df.columns]
    )
    
    # Adicionar rótulos no centro de cada bloco
    for i, idx in enumerate(df.index):
        y_offset = 0
        for col in df.columns:
            value = df.loc[idx, col]
            if value > 0:
                ax.text(i, y_offset + value / 2, f"{int(value)}",
                        ha='center', va='center', color='white', fontsize=10, weight='bold')
            y_offset += value
    
    # Personalização dos eixos e título
    ax.set_ylabel("Number of occurrences", fontsize=11)
    ax.set_xlabel("Phase", fontsize=11)
    ax.set_title("EPB occurrences by phase and geomagnetic category", fontsize=13, pad=12)
    
    # Legenda com base em condições do SYM
    legend_labels = {
        'quiet': 'SYM-H > -30 nT',
        'weak': '-50 < SYM-H ≤ -30 nT',
        'moderate': '-100 < SYM-H ≤ -50 nT',
        'intense': 'SYM-H ≤ -100 nT'
    }
    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles, [legend_labels[l] for l in labels],
        title="Geomagnetic Condition (SYM-H)",
        bbox_to_anchor=(1.05, 1), loc='upper left',
        fontsize=9, title_fontsize=10
    )
    
    ax.set_xticklabels(df.index, rotation=0, ha='center')
    
    plt.tight_layout()
    plt.show()
    return fig 


df = c.geomagnetic_analysis()

df = c.count_events(df)

plot_count_events_by_symh(df)