import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import GOES as gs
import base as b 

def join_wave_nucleos(
    year=2013,
    freq="1M",
    ep_vls="Ep_max",
    area=30,
    lon_min=-70,
    lon_max=-50,
    lat_min=-10,
    lat_max=0,
):
    s1 = gs.nucleos_by_time(
        year=year,
        freq=freq,
        area=area,
        lon_min=lon_min,
        lon_max=lon_max,
        lat_min=lat_min,
        lat_max=lat_max,
    )

    s2 = gs.wave_avg_heights(
        year=year,
        freq=freq,
        values=ep_vls,
        lon_min=lon_min,
        lon_max=lon_max,
        lat_min=lat_min,
        lat_max=lat_max,
    )

    df = pd.concat([s1, s2], axis = 1).dropna()
 
    df["month"] = df.index.month
    df = df.groupby("month", as_index = True).mean()

    return df

def join_all_years(
        start, end,
        area = 0,
        freq = "1M",
        lon_min=-70,
        lon_max=-40,
        lat_min=-10,
        lat_max=0,
        ):

    out = []
    for year in range(start, end + 1):
        df = gs.join_wave_nucleos(
            year=year,
            freq = freq,
            ep_vls = "Ep_max",
            area = area,
            lon_min=lon_min,
            lon_max=lon_max,
            lat_min=lat_min,
            lat_max=lat_max,
        )
        
        df.index = year + (df.index - 1) / 12
        
        out.append(df)
        
        
    return pd.concat(out)



def plot_heights_correlations(
        year = 2013,
        freq = "1M",
        ep_vls = "Ep_max",
        area = 30,
        lon_min = -70,
        lon_max = -60,
        lat_min = -10,
        lat_max = 0,
    ):
    fig, ax = plt.subplots(
        figsize = (10, 8),
        dpi = 300)
 
    ds = gs.join_wave_nucleos(
         year=year,
         freq = "1M",
         ep_vls = "Ep_max",
         area = area,
         lon_min=lon_min,
         lon_max=lon_max,
         lat_min=lat_min,
         lat_max=lat_max,
     )
    df1 = compute_corr_by_altitude(ds)

    plot_altitude_corr(ax, df1, area)

    # ax.set(title= f'Profiles in {lat_min} to {lat_min + 10} by area')


    df1 


 
 
def compute_corr_by_altitude(df):    
    x = df["nucleos"].values

    alts = []
    corrs = []

    for col in df.columns:
        if col == "nucleos":
            continue
        if not isinstance(
                col, (int, float, np.integer, np.floating)):
            continue

        y = df[col].values
        mask = np.isfinite(x) & np.isfinite(y)

        if mask.sum() < 3:
            continue

        corrs.append(np.corrcoef(x[mask], y[mask])[1, 0])
        alts.append(col)

  
    ds = pd.DataFrame(
        {"alt": alts, "corr": corrs}
        ).sort_values("alt")
    
    return ds



def plot_altitude_corr(ax, df, label = 'All years'):
 
    ax.plot(
        df['corr'], 
        df['alt'], 
        marker="o", 
        fillstyle = 'none',
        markersize = 15,
        label = label
        )
    ax.axvline(0, linestyle="--", color="k", lw=1)
    
    ax.set(
        ylim = [0, 120],
        ylabel="Altitude (km)",
        xlabel="Pearson correlation",
        xlim=(-1, 1),
        xticks = np.arange(-1, 1.5, 0.5)
    )
    
    corr_max = df['corr'].max()
    
    ax.axvline(corr_max, linestyle = ':')
     
    ax.legend()

def plot_seasonal_timeseries(ax, df, alt = 100):
    
    ax.plot(df['nucleos'], lw = 3, color = 'blue')
    
    ax1 = ax.twinx()
    
    ax.set(ylabel = 'Number of nucleos',
           xlabel = 'Years')
    
    ax1.plot(df[alt], lw = 3, color = 'red')
    
    ax1.set(
        ylabel = f'Ep (J/kg) at {alt} km', 
        ylim = [50, 100], 
        xlabel = 'Years'
        )
    
    b.change_axes_color(
            ax1, 
            color = 'red',
            axis = "y", 
            position = "right"
            )



lat_min = -10
lon_min = -70
lon_max = -60
lat_max = 0
 
df = join_all_years(
        2014, 2017,
        area = 0,
        freq = '1M',
        lon_min = lon_min,
        lon_max = lon_max,
        lat_min = lat_min ,
        lat_max = lat_max,
        )
 
def plot_timeseries_and_corr_heights():
    
    
    fig, ax = plt.subplots(
        figsize = (12, 5), 
        ncols = 2,
        dpi = 300, 
        width_ratios= [2, 1]
        )
    
    plt.subplots_adjust(wspace = 0.5)
    
    
    plot_seasonal_timeseries(ax[0], df)
    
    ds = compute_corr_by_altitude(df)
    
    plot_altitude_corr(ax[1], ds)
    
    title = (f'Latitudes {lat_min}° to {lat_max}°, ' + 
             f'Longitudes {lon_min}° to {lon_max}°, ')
    
    fig.suptitle(title, )
    
    return fig 