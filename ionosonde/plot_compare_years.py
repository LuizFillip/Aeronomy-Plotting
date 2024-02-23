import base as b
import pandas as pd
import matplotlib.pyplot as plt



def plot_compare_years(df, years = [2015, 2019]):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 8)
        )
    plt.subplots_adjust(hspace = 0.05)
    for yr in years:
        
        df1 = df.loc[df.index.year == yr]
        df1.index = df1.index.day_of_year
        ax[0].plot(df1['vp'], label = yr)
        
        ax[1].plot(df1['dusk'], lw = 2,
                   label = yr)
       
        
        ax[1].scatter(df1.index, df1['time'], label = yr)
        
    ax[1].set(ylim = [23, 26], 
            ylabel = 'Hora universal', 
                   xlabel = 'Dia do ano') 

    ax[0].set(ylabel = '$V_P$ (m/s)')
    ax[0].legend(ncol = 2)
    ax[1].legend(['', 2015, '', 2019, ], ncol = 4, 
                 labelspacing = 0)
    plt.show()

def main():
    
    infile = 'jic_freqs2'
    
    df = b.load(infile)
    df['dusk'] = pd.to_datetime(df['dusk']).apply(b.dn2float)
    df['time'] = pd.to_datetime(df['time']).apply(b.dn2float)
    
    plot_compare_years(df, years = [2015, 2019])