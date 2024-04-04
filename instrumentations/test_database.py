# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:03:29 2024

@author: Luiz
"""

def test_database():
    dirs = im.get_first_file()

    out = []

    for folder in list(dirs.keys()):
    
        dn = get_datetime(folder)
        
        file = dirs[folder]
        
        df =  pb.concat_files(
              dn, 
              root = 'D:\\'
              )
         
        ds = b.sel_times(df, dn, hours = 11)
        try:
            
            plot_time_evolution(file, dn, ds, vmax = 40)
        except:
            print(folder)
            out.append(folder)
            continue
        
    return out