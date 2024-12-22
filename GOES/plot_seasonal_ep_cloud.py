import pandas as pd 
import matplotlib.pyplot as plt
import base as b 
from scipy.ndimage import gaussian_filter
# import core as c

def limits(df, 
           x0 = -80, x1 = -40, 
           y0 = -10, y1 = 0):
    return  df.loc[
        ((df['Lon'] > x0) & (df['Lon'] < x1)) |
        ((df['Lat'] > y0) & (df['Lat'] < y1))
        ]

x0 = -80
x1 = -40
y0 = -10
y1 = 0


def load_nucleos(year = 2019, sample = '15D'):
    infile = f'GOES/data/nucleos/{year}'
    
    df = b.load(infile)
    
    df['Lon'] = (df['x1'] + df['x0']) / 2
    df['Lat'] = (df['y1'] + df['y0']) / 2
    
    df = limits(df, x0, x1, y0, y1)
    
    df = df.resample(sample).size()
    
    df = (df / df.values.max()) *100
    
    return df 


def plot_seasonal(df, ds, title):

    fig, ax = plt.subplots(
          dpi = 300, 
          figsize = (16, 8 )
          )
        
    sdf = gaussian_filter(df, sigma=1)

    ax.plot(
        df.index,
        sdf, 
        lw = 3, color = 'blue')
    ax.set(
        ylim = [30, 100], 
        ylabel = 'Convective activity (\%)',
        xlabel = 'Years'
        )
    
    b.change_axes_color(
            ax, 
            color = 'blue',
            axis = "y", 
            position = "left"
            )
    
    ax1 = ax.twinx()
    sds = gaussian_filter(ds, sigma=1)
    
    ax1.plot(ds.index, sds,  lw = 3, color = 'red')
    
    io = f' Lat = {y0} - {y1}, Lon = {x0} - {x1}'
    
    ax1.set(
        title = title.title() + io,
        ylabel = 'GW potential energy (J/Kg)', 
        xlabel = 'Years'
        )
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )
    
    return fig


def potential_energy(year = 2019):
    
    infile = f'GOES/data/Ep/Select_ep_data_lat_lon_{year}.txt'
    
    df = pd.read_csv(infile, delim_whitespace=True)
    
    df.index = pd.to_datetime(
        df['Date'] + ' ' + 
        df[['Hour', 'Minute', 'Second']
           ].astype(str).agg(':'.join, axis=1))
    
    df = df.drop(
        columns = [
        'Year', 'DOY', 'Date', 
        'Hour', 'Minute', 'Second']
        )
    
    
    return limits(df, x0, x1 , y0, y1)


def get_couples(title):
    
    out_1 = []
    out_2 = []
    
    for year in range(2013, 2023, 1):
        out_1.append(load_nucleos(year , sample = '1M'))
        
        df = potential_energy(year)
        
        out_2.append(df[title].resample('1M').mean())
        
    df = pd.concat(out_1)
    ds = pd.concat(out_2)
    
    return df, ds

def main():
    cols = ['mean_20_60', 'mean_60_90', 'mean_90_110']
    
    for title in cols:
        df, ds = get_couples(title)
        plot_seasonal(df, ds, title = title)