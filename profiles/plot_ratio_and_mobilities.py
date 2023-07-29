import matplotlib.pyplot as plt
from Models.src.core import neutral_iono_parameters


def plot_electron_ration(ax, df):
    
    args = dict(lw = 2)
    
    ax.plot(df["ke"].abs(), df.index, 
               label = "$|\kappa_e|$", 
               **args)
    
    ax.plot(df["ki"], df.index, 
               label = "$\kappa_i$", 
               **args)
    
    ax.set(
        xlabel = "Razão entre as frequências\n de giro e de colisão ",
        xscale = "log",
        title = r"$\kappa_j = \frac{q_j B}{m_j \nu_{jk}}$", 
        xlim = [1e-6, 1e10]
        )
    
    ax.legend()
    return ax


def plot_electron_mobility(ax, df):
    
    args = dict(lw = 2)
    
    ax.plot(df["be"].abs(), df.index, 
               label = "$|b_e|$", 
               **args)
    
    ax.plot(df["bi"], df.index, 
               label = "$b_i$", 
               **args)
   
    ax.set(
        xlabel = "Mobilidade elétrica",
        xscale = "log",
        title = r"$b_j = \frac{q_j}{m_j \nu_{jk}}$", 
        xlim = [1e-2, 1e14]
        )
    
    ax.legend()
    
    return ax

def plot_electron_mobility_ratio():
    
    fig, ax = plt.subplots(
         dpi = 300, 
         figsize = (8, 6), 
         ncols = 2,
         sharey = True
         )
    
    df = neutral_iono_parameters(hmin = 50, hmax = 400)
    
    plt.subplots_adjust(wspace = 0.1)
    
    plot_electron_ration(ax[0], df)
    plot_electron_mobility(ax[1], df)
    
    return fig

plot_electron_mobility_ratio()