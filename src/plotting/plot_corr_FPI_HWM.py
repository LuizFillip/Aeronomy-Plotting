import matplotlib.pyplot as plt
from FabryPerot.src.core import load_FPI
from liken.src.utils import get_fit, rename_cols
import datetime as dt
from common import load

def join_data():
    
    mod = load().HWM(infile = "database/HWM/car_250_2013.txt")
    obs = load_FPI()
    
    mod = rename_cols(mod, name = "HWM")
    obs = rename_cols(obs, name = "FPI")
    
    return mod.join(obs).dropna()


def plot_corr_FPI_HWM(time = None):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        figsize = (7, 5), 
        sharex = True, 
        sharey = True
        )      

    df = join_data()
    
    if time is not None:
        df = df.loc[df.index.time == time]
        title = time
    else:
        title = "Todos os horários"
       
    names = ["zonal", "meridional"]
     
     
    for n, ax in enumerate(ax.flat):
        
        col = names[n][:3]
        
        x = df[f"{col}_HWM"].values
        y = df[f"{col}_FPI"].values
        
        ax.scatter(x, y)
        
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)
    
        r2, fit = get_fit(x, y)
        
        ax.plot(x, fit, 
                color = "r", 
                lw = 2, 
                label = f"$R^2$ = {r2}")
    
        ax.legend(loc = "lower right")
        
        ax.text(0.04, 0.8, 
                names[n].capitalize(), 
                transform = ax.transAxes)
        
        ax.set(xlabel = "HWM", 
               ylabel = "FPI", 
               ylim = [-200, 200], 
               xlim = [-200, 200])
        
        
    fig.suptitle(f"Cariri - {title}")

    
    return fig
        

time = dt.time(22, 0, 0)

plot_corr_FPI_HWM()

