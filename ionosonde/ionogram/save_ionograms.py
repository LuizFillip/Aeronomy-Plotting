# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:24:11 2024

@author: Luiz
"""


infile = 'database/ionogram/20130114S/'

def run():
    import os 
    
    for file in os.listdir(infile):
        if 'PNG' in file:
            dn = dg.ionosonde_fname(file)
            
            plt.ioff()
            
            fig = plot_single_ionogram(
                os.path.join(infile, file), 
                label = True, 
                title = True
                )
            
            FigureName = dn.strftime('%Y%m%d%H%M')
            
            fig.savefig('temp/' + FigureName)
            plt.close()
    
    
    # plt.show()