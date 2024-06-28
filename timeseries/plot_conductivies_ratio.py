import matplotlib.pyplot as plt
import settings as s
import pandas as pd
import datetime as dt
import astral 
from astral.sun import sun

def plot_timeseries_cond_ratio():
    
    df = pd.read_csv("ratio.txt", index_col=0)

    df.index = pd.to_datetime(df.index)

    fig, ax = plt.subplots(
        figsize = (8, 4), 
        dpi = 300)
    
    sigma_E = (df["EN"] + df["ES"])
    sigma_F = (df["FN"] + df["FS"])
    df["total"] =  sigma_F / (sigma_F + sigma_E)
    ax.plot(df["Sul"], label = "Sul")
    ax.plot(df["Norte"], label = "Norte")
    ax.plot(df["total"], label = "Total")
    
    s.format_axes_date(ax, time_scale = "hour", interval = 2)
    ax.set(ylim = [0, 1.5], 
           xlabel = "Tempo (UT)", 
           ylabel = "$\Sigma_P^F / (\Sigma_P^F + \Sigma_P^E)$")
    
    observer = astral.Observer(latitude = -2.1, 
                                longitude = -44.0)
    sun_phase = sun(observer, 
                     df.index[0], 
                     dawn_dusk_depression = 18)
    
    names = ["Amanhecer", "Pôr do Sol"]
    
    ax.axhline(1, color = "r")
    for i, j in enumerate(["dawn", "dusk"]):
   
        ax.axvline(sun_phase[j])
        ax.text(sun_phase[j] - dt.timedelta(hours = 2.5), 
                1.55, names[i], transform = ax.transData)
    
    
        
    
    return fig
    
        
    
