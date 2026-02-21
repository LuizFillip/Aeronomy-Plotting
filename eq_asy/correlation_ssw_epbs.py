from merra import load_merra 
import pandas as pd 
import numpy as np
import datetime as dt 
import base as b 
import core as c 
import matplotlib.pyplot as plt 
 



def plot_correlation(df):
    fig, ax = plt.subplots(
         dpi = 300
         )
 
    x = df.iloc[:, 0].values
    y = df.iloc[:, 1].values
    
    ax.scatter(x, y, s = 30)
    
    fit = b.linear_fit(x, y)
    
    corr = np.corrcoef(x, y)[1, 0]
    
    ax.plot(
        x, fit.y_pred, 
        lw = 2, 
        color = 'red', 
        label = round(corr, 2)
        )
    
    ax.legend()



def join_data(data_1, data_2, col):
    names = [col, 'epb']
    
    df_new =  pd.DataFrame()
    for i, da in enumerate([data_1, data_2]):
    
        df_new[names[i]] = (
            da['september'] - da['march']) /  da['march']
        
        
    
    plot_correlation(df_new) 
    
    return df_new


start, end = 2015, 2023

def data_1(start, end):
    # ds = b.load('database/epbs/north/north_epbs')
    df = b.load('database/epbs/epbs_2013_2023')
    
 
    df = c.add_geo(df, start, end)

    df = df.loc[df['kp'] <= 3]
    ds = c.pivot_epb_by_type(df, total = False, sel_lon = -50)
    
    ds = c.count_epbs_by_season(ds, start, end, percent = False)
            
    ds['dev_pb'] = (ds['september'] - 
                    ds['march']) /  ds['march']
      
    return ds 


def data_2(start, end, col = 'T_60_90_S'):
    df = load_merra()
    
    ds = c.average_equinox(df[col], start, end) 
    
    ds['dev_' + col[0]] = (
        ds['september'] -  ds['march']) /  ds['march']
    
    return ds

df = pd.concat(
    [data_1(start, end).iloc[:, -1], 
      data_2(start, end).iloc[:, -1]], axis = 1) #.dropna()

plot_correlation(df)

# df 


# data_1()
