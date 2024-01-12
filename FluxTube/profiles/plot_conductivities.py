import matplotlib.pyplot as plt
from utils import translate

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
    
    plot_profiles(ax[0], df, "south")
    
    plot_profiles(ax[1], df, "north")
    
    
    plot_total(ax[2], df)


    ax[1].legend(bbox_to_anchor = [1.5, 1.18],
                 ncol = 3)
    
    ax[0].set(ylim = [100, 700], 
              xlim = [0, 120])
    
    for ax in ax.flat:
        
        ax.axhline(150, color = "k")
        
        ax.axhline(300, color = "k")
    
infile = "database/FluxTube/201301012100.txt"


def smooth_from_heigth(df):
    df[df.index >= 200] = df[df.index >= 200].rolling(
        10, min_periods = 3).mean()
    
    return df.interpolate()

#df = smooth_from_heigth(df)



#plot_conductivities(df)




