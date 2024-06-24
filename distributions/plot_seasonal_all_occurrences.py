# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:40:08 2024

@author: Luiz
"""

import base as b 
import matplotlib.pyplot as plt 
import core as c
import plotting as pl 



b.config_labels(fontsize = 25)

def plot_distributions_seasons(
        df, 
        parameter = 'gamma',
        solar_level = 86, 
        translate = False,
        outliner = 10,
        limit = None
        ):
    
    fig, ax = pl.axes_for_seasonal_plot()

    names = ['march', 'june', 'september', 'december']
    
    for row, name in enumerate(names):
        
        total_epb = []
        total_day = []
        
        df_season = c.SeasonsSplit(
            df, 
            name, 
            translate = translate
            )
        
        data, epb = pl.plot_distribution(
                ax[row, 0], 
                df_season.sel_season, 
                parameter,
                label = '',
                outliner = outliner, 
                translate = translate,
                limit = limit
                )
        
        total_epb.append(epb)
        
        days = pl.plot_histogram(
                ax[row, 1], 
                data, 
                row,
                parameter = parameter,
                label = ''
                )
        
        total_day.append(days)
        
        ax[row, 1].set(
            ylim = [0, 350], 
            yticks = list(range(0, 400, 100))
            )
                
        ax[row, 0].text(
            0.35, 0.82,
            f'{df_season.name}',
            transform = ax[row, 0].transAxes
            )
            

        TOTAL = [total_epb, total_day]
       
        pl.plot_events_infos(
            ax, row, TOTAL, 
            x = 0.58,
            y = 0.3,
            parameter = parameter,
            translate = translate
            )
            
        
    pl.FigureLabels(
        fig, 
        translate = translate, 
        parameter = parameter,
        fontsize = 30
        )
    
    return fig


def main():
    
    translate = True
    parameter = 'gamma'
    df = c.load_results('saa', eyear = 2022)
    solar_limit = c.limits_on_parts(df['f107a'])
    
    fig = plot_distributions_seasons(
            df, 
            parameter = parameter,
            solar_level = solar_limit,
            translate = translate,
            outliner = 10,
            limit = True
            )
    
    FigureName = f'seasonal_{parameter}_all'
    
    if translate:
        folder = 'distributions/pt/'
    else:
        folder = 'distributions/en/'
        
        
    # fig.savefig(
    #     b.LATEX(FigureName, folder),
    #     dpi = 400
    #     )
    

    plt.show()
main()
# 
