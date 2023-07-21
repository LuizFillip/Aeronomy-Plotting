import matplotlib.pyplot as plt
import RayleighTaylor as rt
from common import plot_roti, plot_terminators



def plot_drift(
        ax, 
        ds, 
        recom = False,
        effect = "vz"
        ):
    
    gamma = rt.effects_due_to_drift(
                    ds, 
                    recom = recom, 
                    col = effect
                    )
    
    eq = rt.EquationsFT()
    
    label = eq.drift(recom = recom)
    
    ax.plot(gamma * 1e4, 
            label = label)
                
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], ds.index[-1]]
           )
    
    ax.axhline(0, linestyle = "--")

def plot_drift_effect(df, station = "salu"):
    
    fig, ax = plt.subplots(
        figsize = (12, 13), 
        sharex = True,
        sharey = "row",
        ncols = 1, 
        nrows = 5, 
        dpi = 300
        )

    plt.subplots_adjust(hspace = 0.1)

    cols = [("north", "vz"), 
            ("north", "vzp"),
            ("south", "vz"),
            ("south", "vzp")]

    for row, col in enumerate(cols):
        
        hem, drift = col
        
        ds = df.loc[df["hem"] == hem]
        
        if hem == "north":
            title = "Norte"
        else:
            title = "Sul"
        
        ax[row].text(
            0.01, 0.8, 
            f"$V_P = ${drift.title()} ({title})", 
            transform = ax[row].transAxes
            )
        
        ax[row].set_ylabel(rt.EquationsFT().label)
        
        plot_drift(ax[row], ds, effect = drift)

        plot_drift(ax[row], ds, effect = drift, recom = True)
        
    ax[0].legend(
        loc = "upper center", 
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.45)
        )

    plot_roti(ax[4], ds, station = station)
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    fig.suptitle(
        "Efeitos devido à deriva vertical: constante (Vzp) e variando no tempo (Vz)"
        )
    
    return fig


def main():
    infile = "database/RayleighTaylor/reduced/300.txt"
    df = rt.load_process(infile, apex = 300)
    ds = rt.split_by_freq(df, freq_per_split = "10D")[0]
    fig = plot_drift_effect(ds)
        


