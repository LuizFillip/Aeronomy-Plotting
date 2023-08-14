# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 14:11:35 2023

@author: Luiz
"""


def plot_instrumention(ax):
    markers = ['s', '^', 'o']
    
    instrs = ['All-Sky imager and FPI', 
              'Digisonde and GNSS receiver', 
              'FPI']
    
    radius = [500, 215, 0]
    colors = ['red',  'blue', 'white']
    
    
    for i, site in enumerate(["car", "saa", 'caj']):
        s = sites[site]
        clat, clon = s["coords"]
        ax.scatter(
            clon, clat, s = 50, 
            marker = markers[i], 
            label = f'{s["name"]} ({instrs[i]})'
            )
       
            
        circle_range(
            ax, 
            clon, 
            clat, 
            radius = radius[i], 
            color = colors[i]
            )
    ax.text(-37, -13, 'All-Sky range', color = 'red')
    ax.text(-42.5, -2, 'Digisonde range', color = 'blue')
    ax.legend(bbox_to_anchor = (.5, 1.2), 
              ncol = 1,
              loc = 'upper center')