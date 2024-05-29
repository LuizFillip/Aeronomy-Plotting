# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:04:26 2024

@author: Luiz
"""

import plotting as pl
import core as c 
import matplotlib.pyplot as plt 
import base as b


b.config_labels()

def plot_seasonal_RTI_contribution(
        df, fontsize = 35):
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols = 2, 
        sharey = 'row',
        sharex = 'col',
        dpi = 300,
        figsize = (18, 16)
        )
    
    plt.subplots_adjust(
        hspace = 0.25,
        wspace = 0.02
        )
    
    
    # names = ['march', 'june', 'september', 'december']
     
    # b.plot_letters(ax, y = 1.04, x = 0.01)
    
    cols = ['vp', 'K', 'gr', 'mer_perp']
    for i ,a in enumerate(ax.flat):
                            
        pl.plot_single_correlation(
            df, 
            ax = a, 
            color = 'k', 
            col = cols[i],
            index = 0, 
            label = ''
            )
        
    
    # ax[-1, 0].set(xlabel = b.y_label('vp'))
    # ax[-1, 1].set(xlabel = b.y_label('K'), xlim = [1, 4.2])
    # ax[-1, 2].set(xlabel = b.y_label('g_nui_eff'), xlim = [0, 30])
    
    
    
    fig.text(
          0.06, 0.4, 
          b.y_label('gamma'), 
          fontsize = fontsize, 
          rotation = 'vertical'
          )
    
    plt.show()
    return fig


def main():
    
    df = c.load_results('saa', eyear = 2022, 
    gamma_cols = ['vp', 'gamma', 'K', 'gr', 'mer_perp'])
    
    df['K']  = df['K'] *  1e5
    
    fig = plot_seasonal_RTI_contribution(df)
    
    FigureName = 'correlation_vp_K_nui'
    
    fig.savefig(b.LATEX(
        FigureName, 
        folder = 'correlations'), dpi = 400)
    
