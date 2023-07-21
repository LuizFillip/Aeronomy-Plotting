import matplotlib.pyplot as plt
import RayleighTaylor as rt
from common import plot_roti, plot_terminators




def plot_gamma(
        ax, 
        ds, 
        cols, 
        sign = -1, 
        recom = False,
        hem = "north",
        drift = "vz"
        ):
    
    if hem == "north":
        hem = "Norte"
    else:
        hem = "Sul"
        


    for wd in cols:
                    
        gamma = rt.all_effects(
                ds, 
                wind = wd,
                drift = drift, 
                sign_wd = sign, 
                recom = recom)
      
        if "ef" in wd:
            label = f"Efetivo ({hem})"
        else:
            label = f"Geográfico ({hem})"
        
        ax.plot(gamma * 1e4, label = label)
        
    
    ax.axhline(0, linestyle = "--")
        
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], 
                   ds.index[-1]]
           )
    return ax


def plot_all_effects(df, recom, drift = "vz", station = "salu"):


    fig, ax = plt.subplots(
           figsize = (14, 12), 
           sharex = True,
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
            
            ax[row].set(title =eq.complete(
                wind_sign = sign, 
                recom = recom ))
        
        
            plot_gamma(ax[row], ds, cols, 
                          sign = sign, 
                          recom = recom, 
                          drift = drift,
                          hem = hem)
            
            if "zon" in cols:
                coord =  "Zonal"
            else:
                coord = "Meridional"
                
                
            ax[row].text(0.01, 0.8, coord, 
                         transform = ax[row].transAxes)

    plot_roti(ax[4], ds, station = station)
    
    ax[0].legend(
        ncol = 4, 
        bbox_to_anchor = (0.5, 1.7),
        loc = "upper center")
    
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    if recom:
        r = "com"
    else:
        r = "sem"
        
    fig.suptitle(f"Efeitos devido aos ventos neutros, $V_P = ${drift} e {r} recombinação")

    return fig

def main():
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    
    ds = rt.split_by_freq(df, freq_per_split = "10D")[0]
    recom  = False
    plot_all_effects(ds, recom, drift = "vzp")
    
    
# 