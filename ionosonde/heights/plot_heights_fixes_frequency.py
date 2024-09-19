import matplotlib.pyplot as plt 
import digisonde as dg 
import datetime as dt 
import base as b 

sites = ['SAA0K', 'BVJ03', 'CAJ2M']


def plot_height_fixes_for_multi_sites(
        sites,
        translate = True,
        cols = list(range(2, 7, 1))
        ):
    
    fig, ax = plt.subplots(
        nrows = 3,
        dpi = 300,
        sharey = True, 
        sharex = True,
        figsize = (16, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    dn = dt.datetime(2015, 12, 19)
    
    if translate:
       ylabel = 'Height (km)'
       title = 'Fixed frequencies (MHz)'
    else:
        ylabel = 'Altura (km)'
        title = 'Frequência fixas (MHz)'
        
        
    fontsize = 35
    
    for i, site in enumerate(sites):
        
        df = dg.join_iono_days(
                site, 
                dn,
                cols = cols,
                parameter = 'heights'
                )
        
        
        
        ax[i].plot(df)
        
        ax[i].set(
            ylim = [50, 550],
            xlim = [df.index[0], df.index[-1]])
        
        s = b.chars()[i]
        name = dg.code_name(site)
        ax[i].text(
            0.02, 0.75, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        start = dt.datetime(2015, 12, 20, 21, 0)
        
        ax[i].axvspan(
             start, 
             start + dt.timedelta(hours = 12), 
             ymin = 0, 
             ymax = 1,
             alpha = 0.2, 
             color = 'gray'
             )
        
    ax[1].set_ylabel(ylabel, fontsize = fontsize)
  
    ax[0].legend(
        cols, 
        ncol = len(cols), 
        title = title,
        bbox_to_anchor = (0.5, 1.8), 
        loc = 'upper center', 
        columnspacing = 0.7
        )
    
    b.format_time_axes(
        ax[-1], 
        hour_locator = 12, 
        pad = 80, 
        translate = translate
        )
        
    return fig

def main():
    fig = plot_height_fixes_for_multi_sites(
        sites,
        translate = False
        
        )
    
    FigureName = 'fixed_heights_sites'
    
    fig.savefig(
          b.LATEX(FigureName, 'Iono'),
          dpi = 400)

# main()