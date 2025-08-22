import pandas as pd 
import matplotlib.pyplot as plt
import base as b 
import numpy as np 
from matplotlib.ticker import MultipleLocator

b.sci_format(fontsize = 25)


def add_LT_axis(ax, offset_hours=-3, position=-0.18, fmt="%02d"):
    """
    Adiciona um eixo LT (hrs) abaixo do eixo x (UT) de `ax`.

    - LT = (UT + offset_hours) % 24
    - position < 0 coloca o eixo abaixo (ex.: -0.18)
    - fmt controla o formato do rótulo (default: 2 dígitos)
    """
    # eixo secundário com transformação identidade
    secax = ax.secondary_xaxis(position, functions=(lambda x: x, lambda x: x))
    secax.set_xlabel("LT (hrs)")

    
    def _update(_=None):
        ut_ticks = ax.get_xticks()
        lt_vals = (ut_ticks + offset_hours) % 24
        secax.set_xticks(ut_ticks)
        # aqui usamos f-string com :02d para garantir 2 dígitos
        secax.set_xticklabels([f"{int(v)%24:02d}" for v in lt_vals])

    # atualiza agora e sempre que xlim mudar
    _update()
    ax.callbacks.connect('xlim_changed', _update)
    
    # major ticks de 1h
    ax.xaxis.set_major_locator(MultipleLocator(1))
    # minor ticks: 4 subdivisões por intervalo → 1/4 = 0.25
    ax.xaxis.set_minor_locator(MultipleLocator(0.25))
    
    return secax

def set_zonal_drift(infile):
    
    f = open(infile)
    
    lines = f.readlines()
    
    out1 = []
    for ln in lines:
       
        out = []
        for el in ln.split('\t'):
            out.append(
                el.replace('\n', '').strip()
                )
        
        if len(out) > 1:
            out1.append(out)
    
    df = pd.DataFrame(
        out1[1:], 
        columns = out1[0]
        )
    
    df = df.set_index('')
    
    df = df.replace('', float('nan'))
    
    df.index = pd.to_numeric(df.index)
    
   
    return df.astype(float)  

def plot_zonal_drift():
    infile = 'plotting/Taka/zonal_drift.txt'
    df = set_zonal_drift(infile)
    df = df.iloc[:-1, :]
    fig, ax = plt.subplots( 
        dpi = 300, 
        figsize = (14, 7)
        )
    
    df = df.drop(columns = ['2022_09_26', '2022_09_27'])
    
    
    for i, col in enumerate(df.columns, 1):
        
        name = col.replace('_', '-')
      
        ax.errorbar(
            df.index, 
            df[col], 
            yerr = df[col]/10, 
            marker = 'o', 
            capsize = 7, 
            lw = 4, 
            label = f'({i}) {name}'
            )
    
    ax.legend(ncol = 3, bbox_to_anchor = (0.5, 1.35), 
              loc = 'upper center')
    
    ax.set(
            xlim = [23, 31], 
           ylim = [-5, 160], 
           yticks = np.arange(0, 180, 20),
           xlabel = 'UT (hrs)', 
           ylabel = 'Zonal speed (m/s)'
           )
    
    ax.axvline(27, color = 'k', linestyle = '--', lw = 3)
    
    add_LT_axis(ax, offset_hours=-3, position=-0.18)
    
   
    return fig


def plot_heights():
    
    infile = 'plotting/Taka/iono_parameters.txt'
    df = set_zonal_drift(infile)
    
    fig, ax = plt.subplots( 
        dpi = 300, 
        figsize = (14, 7)
        )
    
    for i, col in enumerate(df.columns, 1):
        
        name = col.replace('_', '-')
      
        ax.plot(
            df.index, 
            df[col], 
            lw = 4, 
            label = f'({i}) {name}'
            )
    
    ax.legend(
        ncol = 3, 
              bbox_to_anchor = (0.5, 1.35), 
              loc = 'upper center')
    
    ax.set(
            xlim = [25, 31], 
           ylim = [160, 340], 
           yticks = np.arange(160, 360, 20),
           xlabel = 'UT (hrs)', 
           ylabel = 'h`F (km)'
           )
    
    ax.axvline(27, color = 'k', linestyle = '--', lw = 3)
    
    add_LT_axis(ax, offset_hours=-3, position=-0.18)
    
    return fig 

def main():
    fig = plot_heights()
    
    # fig.savefig('heights', dpi = 300)
    
    fig = plot_zonal_drift()
    
    # fig.savefig('zonal_drift', dpi = 300)
    
main()