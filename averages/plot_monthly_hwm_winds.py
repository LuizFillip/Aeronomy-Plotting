import pandas as pd 
import matplotlib.pyplot as plt 
import base as b 
import datetime as dt

files = ['202110', '202203', '202209']

def set_data(file, values = 'zon'):
    infile = 'database/HWM/winds_bjl_' + file
    
    df = b.load(infile)
    
    df['day'] = df.index.day 
    df['time'] = b.dn2float(df.index, sum_from = None)
    
    return pd.pivot_table(
        df, 
        columns = 'day', 
        index = 'time', 
        values = values
        )

b.config_labels(fontsize = 25)

def plot_monthly_hwm_winds(files):
    
    fig, ax = plt.subplots(
        nrows = 3,
        dpi= 300,
        sharex = True, 
        sharey=True, 
        figsize = (12, 10)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    for i, file in enumerate(files):
        ds = set_data(file)
    
        ax[i].plot(ds, color = 'gray', alpha = 0.4)
        ax[i].plot(ds.mean(axis = 1), lw = 3, 
                   color = 'k', label = 'Zonal')
        
        ax[i].set(ylim = [-150, 150], 
                  xlim = [ds.index[0], ds.index[-1]]
                  )
        
        date = dt.datetime.strptime(file, '%Y%m').strftime('%B-%Y')
        ax[i].text(0.4, 0.8, date, transform = ax[i].transAxes)
        
        ds = set_data(file, values = 'mer')
    
        ax[i].plot(ds, color = 'gray', alpha = 0.4)
        ax[i].plot(ds.mean(axis = 1), lw = 3,
                   color = 'b', label = 'Meridional')
        
        ax[i].axhline(0, linestyle = '--')
        
    ax[0].legend(
        bbox_to_anchor = (.5, 1.4),
        ncol = 2, 
        loc = 'upper center'
        )
    
    ax[2].set(xlabel = 'Universal time')
    
    fig.text(
        0.03, 0.38, 
        'Velocity (m/s)', 
        fontsize = 25, 
        rotation = 'vertical'
        )
    
    return fig

# fig = plot_monthly_hwm_winds(files)



delta = dt.timedelta(days = 221)

dn = dt.datetime(2013, 1, 1, ) + delta

dn