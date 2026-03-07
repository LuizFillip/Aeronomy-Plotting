import matplotlib.pyplot as plt
import base as b 
import plotting as pl 
import core as c 

PATH_INDEX =  'database/indices/omni_pro2.txt'

b.sci_format()




def plot_long_term(start, end):
    
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 6), 
        nrows = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    df = c.low_omni()
    
    df = b.sel_dates(df, start, end)
    
        
    pl.plot_kp(ax[1], df)
    pl.plot_dst(ax[0], df['dst']) 
    ax[-1].set(xlim= [df.index[0], df.index[-1]])
    
    b.format_days_axes(ax[-1])
  
    b.plot_letters(ax, y = 0.83, x = 0.02, fontsize = 25)
        
    fig.align_ylabels()
    return fig
    

def main():
    fig = plot_long_term(2022, 2024)
    
    FigureName = 'geomagnetic_indexes_2023'
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'indices'),
        dpi = 400
        )

