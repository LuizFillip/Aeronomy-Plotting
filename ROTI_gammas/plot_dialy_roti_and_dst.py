import matplotlib.pyplot as plt
import RayleighTaylor as rt
from common import plot_roti, plot_terminators

def plot_winds_ts(
        ax, 
        ds, 
        cols, 
        sign = -1, 
        recom = False,
        hem = "north"
        ):
    
    if hem == "north":
        title = "Norte"
    else:
        title = "Sul"
    
    for wd in cols:
            
        gamma = rt.effects_due_to_winds(
                ds, 
                wind = wd,
                sign_wd = sign, 
                recom = recom)
      
        if "ef" in wd:
            label = f"Efetivo ({title})"
        else:
            label = f"Geográfico ({title})"
        
        ax.plot(gamma * 1e4, label = label)
        
    ax.axhline(0, linestyle = "--")
        
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], ds.index[-1]]
           )
    return ax

def plot_winds_effect(
        df, recom = False, alt = 300, station = "salu"
        ):
    
    fig, ax = plt.subplots(
        figsize = (14, 11), 
        sharex = True,
        sharey = "row", 
        nrows = 5, 
        dpi = 300
        )
        
    plt.subplots_adjust(hspace = 0.4)

    eq = rt.EquationsFT()

    for hem in ["north", "south"]:
        
        ds = df.loc[df["hem"] == hem]
        
        cols = [("zon", 1), ("zon", -1),
                ("mer", 1), ("mer", -1)]
           
        for row, col in enumerate(cols):
            
            wd, sign = col
        
            cols = [wd, f"{wd}_ef"]
            
            title = eq.winds(wind_sign = sign, recom = recom)
            
            ax[row].set(title = title, ylabel = eq.label)
        
            plot_winds_ts(ax[row], ds, cols, 
                          sign = sign, 
                          recom = recom, 
                          hem = hem)
            
            if "zon" in cols:
                coord =  "Zonal"
            else:
                coord = "Meridional"
                
                
            ax[row].text(0.01, 0.8, coord, 
                         transform = ax[row].transAxes)
        
    ax[0].legend(
        ncol= 4, 
        bbox_to_anchor = (.5, 1.7),
        loc = "upper center")

    plot_roti(ax[4], ds, station = station)
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    if recom:
        w = "com"
    else:
        w = "sem"
        
    fig.suptitle(f"Efeitos devido aos ventos neutros {w} recombinação")
    return fig

            


def main():
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    
    ds = rt.split_by_freq(df, freq_per_split = "10D")[0]
    fig = plot_winds_effect(ds, recom = False)
    
    
# main()


