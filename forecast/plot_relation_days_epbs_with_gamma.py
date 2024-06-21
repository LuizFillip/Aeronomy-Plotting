import matplotlib.pyplot as plt
import base as b 


b.config_labels()


# print(convert_to_latex(df))



from matplotlib.legend_handler import HandlerTuple

class HandlerTupleVertical(HandlerTuple):
    def __init__(self, **kwargs):
        HandlerTuple.__init__(self, **kwargs)

    def create_artists(
            self, 
            legend, 
            orig_handle,
            xdescent, 
            ydescent, 
            width, 
            height, 
            fontsize, 
            trans
            ):

        numlines = len(orig_handle)
        handler_map = legend.get_legend_handler_map()

        height_y = (height / numlines)

        leglines = []
        for i, handle in enumerate(orig_handle):
            handler = legend.get_legend_handler(
                handler_map, handle)

            legline = handler.create_artists(
                legend, handle,
                xdescent,
                (2*i + 1)*height_y,
                width,
                2*height,
                fontsize, trans)
            leglines.extend(legline)

        return leglines

import numpy as np 



def plot_seasonal_gamma_relation():
    

    c = ['k', 
         '#00B945', 
     '#FF9500', 
     '#FF2C00', 
     '#845B97'] 
    
    
    fig, ax = plt.subplots(
        figsize = (12, 5),
        dpi = 300)
    
    
    list_lines = []
    
    for i, season in enumerate(names):
    
        line1, = ax.plot(
            day[season], 
            color = c[i], 
            lw = 2,
            label = season, 
            marker = 's'
            )
        
        ax1 = ax.twinx()
        
        line2, = ax1.plot(
            epb[season],
            lw = 2,
            color = c[i],
            marker = 'o',
            linestyle = '--')
        
        list_lines.append((line1, line2))
    
        ax1.set(ylim = [0, 100])
        
    ax1.set(ylabel = 'Número de EPBs')
    
    ax.set(
           xticks = np.arange(-0.2, 2.6, 0.2),
           ylim = [0, 300],
           ylabel = 'Número de dias', 
           xlabel = '$\gamma_{RT}~(10^{-3}~s^{-1})$')
    
    plt.legend(
        list_lines, names,
        ncol = 4, 
        columnspacing = 0.4,
        bbox_to_anchor = (0.5, 1.2),
        loc = 'upper center',
        handler_map = {tuple : HandlerTupleVertical()}
        )
    
    return fig