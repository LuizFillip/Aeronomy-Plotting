import matplotlib.pyplot as plt
import digisonde as dg
import base as s
import GEO as gg 
import datetime as dt


s.config_labels(fontsize = 25)

def plot_terminators(ax, dn):
         
     dusk = gg.dusk_from_site(
             dn, 
             site = 'jic',
             twilight_angle = 18
             )
     
     delta = dt.timedelta(minutes = 30)
     
     for row in range(2):
         
         ax[row].axvspan(
             dusk - delta,
             dusk + delta,
             alpha = 0.2, 
             color = 'gray',
             edgecolor = 'k', 
             lw = 2
         )
             
         ax[row].axvline(
             dusk, 
             linestyle = '--',
             color = 'k'
             )
 

     return dusk

def plot_infos(ax, vz, dn):
    
    idx, vmax = dg.time_between_terminator(vz, dn)
    idx = idx.strftime('%Hh%M')
    vmax = round(vmax, 2)
    ax.text(0.5, 0.8,
            f'Vp = {vmax} m/s ({idx} UT)',
            transform = ax.transAxes)
    
def plot_vz_and_frequencies(df, vz, dn):
    
    df = df.iloc[1:]
    vz = vz.iloc[1:]
    
    fig, ax = plt.subplots(
        figsize = (12, 8), 
        nrows = 2, 
        sharex = True, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    
    
    for num, col in enumerate(df.columns):
        
        if col != 'time':
            
            ax[0].plot(df[col], label = f'{col}')
            
            ax[1].plot(vz[col], label = f'{col}')


    ax[0].set(ylabel = "Altitude (km)", 
              ylim = [100, 700])
    
    vmax = 70
    
    ax[1].set(
              ylabel = "Deriva vertical (m/s)", 
              ylim = [-vmax, vmax], 
              xlim = [df.index[0], df.index[-1]]
              )
     
    s.format_time_axes(ax[1], translate = True)
    
    ax[0].legend(
        bbox_to_anchor = (.5, 1.45), 
        ncol = 5, 
        loc = "upper center", 
        title = "Frequências fixas"
        )
    
    plot_terminators(ax, dn)
    
    ax[1].axhline(0, linestyle = '--')
    
    s.plot_letters(ax, y = 0.85, x = 0.03)
    
    plot_infos(ax[1], vz, dn)

    return fig



   

        
def main():
        
    year = 2015
    infile =  f'database/jic/freq/{year}'
    df = dg.freq_fixed(infile)
    
    dn = dt.datetime(year, 1, 10, 20)
    
    ds = s.sel_times(df, dn, hours = 7) 
    
    vz = dg.vertical_drift(ds)
    
    
    fig = plot_vz_and_frequencies(ds, vz, dn)
    
# main()