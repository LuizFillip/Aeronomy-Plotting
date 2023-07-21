import matplotlib.pyplot as plt
import RayleighTaylor as rt
from common import plot_roti, plot_terminators


def plot_gravity_effect(df, station = "salu"):
    
    fig, ax = plt.subplots(
       figsize = (12, 8), 
       sharex = True,
       nrows = 3, 
       dpi = 300
       )

    plt.subplots_adjust(hspace = 0.1)
    
    eq = rt.EquationsFT()
    
    for row, hem in enumerate(["north", "south"]):
        
        ds = df.loc[df["hem"] == hem]        
       
        for recom in [True, False]:
            
            gamma = rt.effects_due_to_gravity(
                ds, recom = recom)
            
            ax[row].plot(
                gamma * 1e4, label = eq.gravity(recom = recom)
                )
        
        ax[row].axhline(0, linestyle = "--")
        
        if hem == "north":
            title = "Norte"
        else:
            title = "Sul"
            
        ax[row].text(0.05, 0.8, title, transform = ax[row].transAxes)
        ax[row].set(ylim = [-20, 20], ylabel = eq.label) 
                  
    ax[0].legend(
        loc = "upper center",
        ncol = 2, 
        bbox_to_anchor = (.5, 1.4)
        )
    
    plot_roti(ax[2], df, station = station)
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    
    fig.suptitle("Efeitos devido apenas à gravidade com e sem recombinação")
        
    return fig
    
def main():
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    #df = df[df.index.month == 8]
    ds = rt.split_by_freq(df, freq_per_split = "10D")[0]
    fig = plot_gravity_effect(ds)
        
# main()

