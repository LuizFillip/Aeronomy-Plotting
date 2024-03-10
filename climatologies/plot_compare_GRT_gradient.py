# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:27:11 2024

@author: Luiz
"""

import matplotlib.pyplot as plt 
import base as b 
import datetime as dt
import RayleighTaylor as rt

def compare_gradient_on_gamma(year):
    

    fig, ax = plt.subplots(
         dpi = 300, 
         nrows = 3,
         sharex = True,
         figsize = (12, 10)
         )
    
    plt.subplots_adjust(hspace = 0.05)
     
    names = [ 'ionossonde', 'IRI-2016']
    b.config_labels()
    
    for i, col_grad in enumerate(['L', 'L1']):
        
        df = rt.local_results(
            year, 
            col_grad, 
            time = dt.time(1, 0)
            )
        
        
        ax[1].plot(df['gamma'], label = names[i])
        ax[1].text(0.1, 0.8, '$(g / \\nu_{in}) L^{-1}$', 
                   transform = ax[1].transAxes)
        
        
        ax[2].plot(df['gamma2'], label = names[i])
        ax[2].text(0.1, 0.8, '$(V_p + g / \\nu_{in}) L^{-1}$', 
                   transform = ax[2].transAxes)
        
    ax[0].plot(df[['L', 'L1']], label = names)
    
    b.format_month_axes(ax[-1])
    
    ylabels = ['$L^{-1}~m^{-2}$', 
               '$\\gamma_{RT}~(10^{-3}~s^{-1})$', 
               '$\\gamma_{RT}~(10^{-3}~s^{-1})$']
    
    vmin, vmax = -2, 4
    
    ylim = [[vmin - 2, vmax + 2], [vmin, vmax], [vmin, vmax]]
    
    for i, ax in enumerate(ax.flat):
        ax.legend(ncol = 2, loc = 'upper right')
        ax.set(ylabel = ylabels[i],
               ylim = ylim[i])
        
        
    return fig