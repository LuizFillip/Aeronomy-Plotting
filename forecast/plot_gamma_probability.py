# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:02:51 2024

@author: Luiz
"""

import matplotlib.pyplot as plt 
import core as c 
import base as b 

b.config_labels()

parameter = 'gamma'

df = c.load_results('saa', eyear = 2023)
obs = df.loc[df.index.year == 2023, ['gamma', 'epb']]
pred = c.forecast_epbs(
    year_threshold = 2023, 
    parameter= 'gamma')
pred = pred.data['predict']

def plot_gamma_predict_epbs(obs, pred):
    
    fig, ax = plt.subplots(
        nrows = 2,
        sharex=True,
        figsize = (12, 10)
        )
    
    ax[0].plot(obs, label = ['$\gamma_{RT}$','EPBs'])
    
    ax[0].set(ylabel = '$\gamma_{RT}$')
    ax[0].legend()
    
    ax[1].plot(pred *100, color = 'g')
    
    ax[1].set(ylabel = 'Probability (\%)')
    
    b.format_month_axes(ax[1])
