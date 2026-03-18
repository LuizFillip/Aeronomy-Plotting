import matplotlib.pyplot as plt
import base as b 
import plotting as pl 
import core as c 
import datetime as dt 
import matplotlib.dates as mdates

b.sci_format()




def plot_long_term(df):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 8), 
        nrows = 3, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    pl.plot_kp(ax[1], df)
    pl.plot_dst(ax[0], df['dst']) 
    pl.plot_f107(ax[-1],  df,  color = 'k' )
    
    ax[-1].set(xlim = [df.index[0], df.index[-1]])
     
    b.plot_letters(ax, y = 0.83, x = 0.02, fontsize = 25)
        
    fig.align_ylabels()
    
    major_locator = mdates.MonthLocator()
    major_formatter = mdates.DateFormatter('%b/%y')
    minor_locator = mdates.MonthLocator(interval=1)
    
    for ax in ax:
        
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
        # ax.xaxis.set_minor_locator(minor_locator)
        
        ax.xaxis.set_minor_formatter(major_formatter)
        ax.xaxis.set_minor_locator(minor_locator)
        
    return fig
    

def main():
    fig = plot_long_term(2022, 2024)
    
    FigureName = 'geomagnetic_indexes_2023'
    
    # fig.savefig(
    #     b.LATEX(FigureName, folder = 'indices'),
    #     dpi = 400
    #     )

start = dt.datetime(2024, 11, 1)
end = dt.datetime(2025, 5, 1)

df = c.low_omni()

df = b.sel_dates(df, start, end)

fig = plot_long_term(df)