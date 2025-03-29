import matplotlib.pyplot as plt 
import digisonde as dg 
import datetime as dt 
import base as b 

sites = ['FZA0M', 'SAA0K', 'BVJ03', 'BLJ03'] #, 'CAJ2M']


def plot_height_fixes_for_multi_sites(
        sites,
        translate = True,
        cols = list(range(4, 10, 1)),
        fontsize = 35

        ):
    
    fig, ax = plt.subplots(
        nrows = len(sites),
        dpi = 300,
        sharey = True, 
        sharex = True,
        figsize = (16, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    dn = dt.datetime(2023, 10, 14)
    
    if translate:
       ylabel = 'Height (km)'
       title = 'Fixed frequencies (MHz)'
    else:
        ylabel = 'Altura (km)'
        title = 'Frequência fixas (MHz)'
        
        
    
    for i, site in enumerate(sites):
        
        # df = dg.join_iono_days(
        #         site, 
        #         dn,
        #         cols = cols,
        #         parameter = 'heights'
        #         )
        
        file =  dg.dn2fn(dn, site)
        
        df = dg.IonoChar(
            file, cols, 
            sum_from = None
            ).heights.interpolate()
        
        df = df.between_time('17:00', '21:00')
        
        # pl.plot_terminators(ax[i], df, site)
        
        
        # for x in df.columns:
        #     vls = b.filter_frequencies(
        #             df[x], 
        #             high_period = 5, 
        #             low_period = 1, 
        #             fs = 6, 
        #             order = 1
        #             )
            # print(len(vls), len(df))
            # ax[i].plot(df.index, vls)
        ax[i].plot(df)  
        delta = dt.timedelta(hours = 16)
        lim = 30
        ax[i].set(
            # ylim = [-lim, lim],
            ylim = [0, 500],
            # xlim = [
            #     df.index[0] + delta,
            #     df.index[-1] ]
            )
        
        s = b.chars()[i]
        name = dg.code_name(site)
        ax[i].text(
            0.02, 0.75, 
            f'({s}) {name}', 
            transform = ax[i].transAxes
            )
        
        # start = dt.datetime(2015, 12, 20, 21, 0)
        
        # ax[i].axvspan(
        #      start, 
        #      start + dt.timedelta(hours = 12), 
        #      ymin = 0, 
        #      ymax = 1,
        #      alpha = 0.2, 
        #      color = 'gray'
        #      )
        
    fig.text(
        0.03, 0.35, 
        ylabel, 
        fontsize = fontsize + 5, 
        rotation = 'vertical'
        )
  
    ax[0].legend(
        cols, 
        ncol = len(cols), 
        title = title,
        bbox_to_anchor = (0.5, 1.5), 
        loc = 'upper center', 
        columnspacing = 0.7
        )
    
    b.format_time_axes(
        ax[-1], 
        hour_locator = 1, 
        pad = 80, 
        translate = translate, 
         # = '%d/%m/%y'
        )
        
    return fig

def main():
    fig = plot_height_fixes_for_multi_sites(
        sites,
        translate = True
        
        )
    
    FigureName = 'fixed_heights_sites'
    
    # fig.savefig(
    #       b.LATEX(FigureName, 'Iono'),
    #       dpi = 400)

main()