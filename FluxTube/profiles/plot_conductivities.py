import matplotlib.pyplot as plt
import pandas as pd 
import base as b 
from matplotlib.gridspec import GridSpec


b.config_labels(fontsize = 25)

def plot_profiles(ax, df, col):
    ax.plot(df[f"{col}_E"], df.index, label = "$\Sigma_P^E$")
    ax.plot(df[f"{col}_F"], df.index, label = "$\Sigma_P^F$")
    
    ax.plot(df[f"total_{col}"], 
            df.index, 
            label = "$\Sigma_P^F + \Sigma_P^E$")
    
    # name =  translate(col)
    ax.set(xlabel = "$\Sigma_P$ (ohms)", )
    
    return ax


def plot_total(ax, df):
    
    region_E = df[["south_E", "north_E"]].sum(axis = 1)
    region_F = df[["south_F", "north_F"]].sum(axis = 1)
    
    ax.plot(region_E, df.index, label = "$\Sigma_P^E$")
    ax.plot(region_F, df.index, label = "$\Sigma_P^F$")
    
    ax.plot(region_E + region_F, 
            df.index, 
            label = "$\Sigma_P^F + \Sigma_P^E$")
    
    ax.set(xlabel = "$\Sigma_P$ (ohms)", 
           title = "Total")
    
    return ax


def plot_conductivities(df):
    
    fig, ax = plt.subplots(
        figsize = (8, 5), 
        sharey = True,
        sharex = True,
        dpi = 300, 
        ncols = 3
        )    
    
    plt.subplots_adjust(wspace = 0.1)
    
   
    ax[1].legend(bbox_to_anchor = [1.5, 1.18],
                 ncol = 3)
    
    ax[0].set(ylim = [100, 700], 
              xlim = [0, 120])
    
    for ax in ax.flat:
        
        ax.axhline(150, color = "k")
        
        ax.axhline(300, color = "k")
    


def smooth_from_heigth(df):
    df[df.index >= 200] = df[df.index >= 200].rolling(
        10, min_periods = 3).mean()
    
    return df.interpolate()

#df = smooth_from_heigth(df)

#plot_conductivities(df)


lbs = b.Labels()

infile = "20131224sep.txt"

df = pd.read_csv(infile, index_col = 0)

dn = '2013-12-24 22:00:00'

ds = df.loc[df['dn'] == dn]

fig = plt.figure(dpi = 300, figsize = (15, 6))


plt.subplots_adjust(wspace = 0.4, hspace = 0.1)

gs = GridSpec(1, 3)


def plot_height_prf(ds):
    ax1 = fig.add_subplot(gs[0, 0])

    ax1.plot(ds.index, ds['E'])
    
    ax1.set(ylabel = 'Altura de Apex (km)', 
            xlabel = '$\Sigma_P$')
    return

def plot_time_prf(ds):
    
    ax2 = fig.add_subplot(gs[0, 1:])
    ax2.set(
        xlabel = 'Hora universal',
        ylabel = '$\Sigma_P$'
        )
    return 

plot_height_prf(ds)
plot_time_prf(ds)