import pandas as pd
import matplotlib.pyplot as plt
from common import plot_terminators
import settings as s
from utils import smooth2

def load(iono_file, alt = None):
    ds = pd.read_csv(iono_file, index_col = 0)
    ds.index = pd.to_datetime(ds.index)
    if alt is not None:
        return ds.loc[ds["alt"] == alt]
    else:
        return ds
    
def plot_grad(ax, dig, iri):
    ax.plot(dig["L"], label = "Digissonda - São Luis")
    
    ax.plot(iri["L"], label = "IRI-2016")
    ax.axhline(0, linestyle = "--")

    ax.set(xlim = [dig.index[0], dig.index[-1]],
           ylabel = "$L^{-1} ~(m^{-1})$", 
           ylim = [-7e-5, 7e-5]
           )
    
    ax.legend(ncol = 2, loc = "upper center", 
                 bbox_to_anchor = (.5, 1.4))


def plot_parameters_iri_digisonde():
    
    iri_file = "database/RayleighTaylor/gamma_parameters.txt"
    iri_file = "database/RayleighTaylor/20130316_20130320.txt"
    alt = 300
    
    iri = load(iri_file, alt = alt)
    
    dig = load("parameters_car.txt", alt = alt)
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (10, 6),
        nrows = 2)
    
    
    plot_grad(ax[0], dig, iri)
    ax[1].plot(dig["R"])
    ax[1].set(ylabel = "$R~(s^{-1})$")
    s.format_time_axes(ax[1])
    name = ["gradiente de escala", "recombinação química"]
    for i, ax in enumerate(ax.flat):
        plot_terminators(ax, dig)
        letter = s.chars()[i]
        ax.text(0.01, 0.85, f"({letter}) {name[i]}", 
                transform = ax.transAxes)
    
    plt.show()
    
    # fig.savefig('liken/src/figures/gradient_recom.png', dpi = 300)