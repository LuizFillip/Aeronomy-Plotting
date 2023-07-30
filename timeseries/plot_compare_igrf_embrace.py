from GEO import sites, year_fraction
import pyIGRF
import matplotlib.pyplot as plt
import settings as s
import pandas as pd
import magnetometers as mm




    

df = pd.read_csv("mag.txt", index_col=0)
df.index = pd.to_datetime(df.index)


igr = mm.load_igrf(df, site = "saa")




def plot_comparece_igrf_embrace(df, igr):

    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 2, 
        figsize = (16, 10),
        dpi = 300,
        sharex = True
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.3)
    
    cols = ['D', 'I', 'H', 'F']
    name = ["Declinação", 'Inclinação', 
            'Horizonal', 'Total']
    
    lims = [[-21.3, -20.7],
            [-7.8, -7.3],
            [25900, 26200], 
            [26100, 26400]]
    c = s.chars()
    s.config_labels(fontsize = 20)
    for i, ax in enumerate(ax.flat):
        
        ax.text(0.05, 0.85, f'({c[i]}) {name[i]}', 
                transform = ax.transAxes)
        ax.plot(df[cols[i]], label = "Magnetômetro - São Luis")
        ax.plot(igr[cols[i]], label = "IGRF-12", lw = 2)
        
        
        ax.set(ylim = lims[i])
        if i >= 2:
            s.format_time_axes(ax)
            ax.set(ylabel = f"{cols[i]} (nT)")
        else:
            ax.set(ylabel = f"{cols[i]} (°)")
            
        if i == 0:
            ax.legend(ncol = 2, 
                      bbox_to_anchor = (1.1, 1.25),
                      loc = "upper center")
    return fig
            
f = plot_comparece_igrf_embrace(df, igr)

f.savefig("magnetometers/figures/comparation_igrf_embrace.png", 
          dpi = 300)