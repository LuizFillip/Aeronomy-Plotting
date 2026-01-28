import matplotlib.pyplot as plt
import core as c
import base as b
import plotting as pl 
import numpy as np 

from scipy.stats import norm

def plot_stats(
        ax,
        arr,
        unit="m/s",
        fontsize=14,
        loc=(0.05, 0.95),
        box=True,
        robust=False,
        precision=2
    ):

    arr = np.asarray(arr)
    arr = arr[~np.isnan(arr)]
    center = arr.mean()
    spread = arr.std()
    label_center = r"\mu"
    label_spread = r"\sigma"

    vmax = arr.max()
    vmin = arr.min()

    fmt = f"{{:.{precision}f}}"

    text = (
        f"${label_center}$ = {fmt.format(center)} {unit}\n"
        f"${label_spread}$ = {fmt.format(spread)} {unit}\n"
        f"max = {fmt.format(vmax)} {unit}\n"
        f"min = {fmt.format(vmin)} {unit}"
    )

    bbox = dict(
        boxstyle="round,pad=0.3",
        fc="white", alpha=0.8) if box else None

    ax.text(
        loc[0],
        loc[1],
        text,
        fontsize=fontsize,
        transform=ax.transAxes,
        verticalalignment="top",
        bbox=bbox
    )



b.sci_format(fontsize = 25)

def start_vs_duration(df):
    for ss in ['end', 'start']:
        df[ss] = pd.to_datetime(df[ss])
    
    df['duration'] = (df['end'] - df['start']).dt.total_seconds() / 3600 
    
    # df['duration'].plot(kind = 'hist')

    plt.scatter(df['duration'], df['div_initial'])
    
    

def plot_count_events_by_symh(ax, df):
    
    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        # 'quiet': '#32CD32'      # verde
    }

    df = df[['intense', 'moderate', 'weak']]
    

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
                ax.text(
                    i, y_offset + value / 2, 
                        f"{int(value)}",
                        ha = 'center', va='center',
                        color='k', 
                        fontsize=fontsize, weight='bold'
                        )
            y_offset += value
    
 
    ax.set(
        xlabel = "Storm phase", 
        ylabel = "Number of events", 
        )

    pl.legend_for_sym_h(ax, loc = 'upper right')
      
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
    
    

def plot_histogram_time_shift():
    
    args = dict(
         facecolor = 'lightgrey', 
         alpha = 1, 
         edgecolor = 'black', 
         hatch = '////', 
         color = 'gray', 
         linewidth = 2
        )
    fig, ax = plt.subplots(dpi = 300, figsize = (12, 6))
    
    arr = df['div_initial'].values
    
    mu, sigma = norm.fit(arr)
    
    bins = np.arange(0, 300, 25)
    count, bins, _ = ax.hist(arr, bins=bins, **args)
    
    bin_width = bins[1] - bins[0]
    
    x = np.linspace(bins[0], bins[-1], 300)
    y = norm.pdf(x, mu, sigma) * len(arr) * bin_width
    
    # Plot da curva
    ax.plot(x, y, 'r-', linewidth=2)
    
    # Rótulos
    ax.set(xlabel = "Time from storm begging (hours)", 
           ylabe = "Frequency")
 
    plot_stats(
        ax,
        arr,
        unit="hrs",
        fontsize=14,
        loc=(0.05, 0.95),
        box=True,
        robust=False,
        precision=2
    )
    
import pandas as pd 

def set_data():
    df = b.load('core/src/geomag/data/stormsphase')
    
    df_source = c.category_and_low_indices()
    
    for col in df_source.columns:
        
        df[col] = df.index.map(df_source[col])
        
    df = df.replace(('weak+', 'weak-'), 'weak')
    
    ds = df.groupby(
        ['phase', 'cate']
        ).size().unstack(fill_value=0)
    
    ds = ds.rename(index={
        "main": "Main",
        "recovery": "Recovery",
        "after": "To quiet"
        })
    
    order = ["Main", "Recovery", "To quiet"]
    
    ds = ds.reindex(order)
    return ds 

    

def main():
    df = set_data()
    
    fig = plot_count_events_by_symh(df)
    
    
    fig, ax = plt.subplots(dpi = 300, figsize = (12, 6))
      