import matplotlib.pyplot as plt
from FabryPerot.core import load_FPI
from liken.utils import get_fit, rename_cols
from liken.core import load_HWM
import datetime as dt


def join_data():
    
    mod = load_HWM()
    obs = load_FPI()
    
    mod = rename_cols(mod, name = "HWM")
    obs = rename_cols(obs, name = "FPI")
    
    return mod.join(obs).dropna()


def plot_corr_FPI_HWM(fig, ax, time = None):

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
                color = "k", 
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

    
    
        
        
fig, ax = plt.subplots(nrows = 2, 
                       figsize = (7, 5), 
                       sharex = True, 
                       sharey = True)       

time = dt.time(22, 0, 0)

plot_corr_FPI_HWM(fig, ax, time)

