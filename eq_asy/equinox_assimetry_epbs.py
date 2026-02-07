import base as b
import pandas as pd 
import core as c 
import matplotlib.pyplot as plt 
import numpy as np 

SEASON_MONTHS = {
    "march": [3, 4],
    "september": [9, 10],
    "december": [11, 12],  # se você quiser usar depois
}

def sel_season(x, season):
    months = SEASON_MONTHS.get(season)
    if months is None:
        raise ValueError(f"Season inválida: {season}. Opções: {list(SEASON_MONTHS)}")
    return x[x.index.month.isin(months)]

def count_epbs_by_year(
        df, 
        seasons=("march", "september"),
        years=range(2013, 2024)
        ):

    years = list(years)
    out = {}

    for season in seasons:
        months = SEASON_MONTHS[season]
        mask = df.index.month.isin(months) & df.index.year.isin(years)

        # xs = df.loc[mask].groupby(df.loc[mask].index.year).sum()

        # out[season] = s
        
        xs = df.loc[mask]

        n_events = xs.groupby(xs.index.year).sum()
        
        n_total = xs.groupby(xs.index.year).count()

        rate = (n_events / n_total) * 100
        out[season] = rate

    result = pd.concat(out, axis=1)
    result.index.name = "year"
    result = result.reindex(years).fillna(0)

    return result

def average_equinox(x):

    years = range(2013, 2024)
    years = list(years)
    out = {}
    seasons=("march", "september")
    for season in seasons:
        months = SEASON_MONTHS[season]
        mask = x.index.month.isin(months) & x.index.year.isin(years)
    
        s = x.loc[mask].groupby(x.loc[mask].index.year).mean()
        out[season] = s
        
    df = pd.concat(out, axis=1)
    df.index.name = "year"
    return df.reindex(years).fillna(0)

# ds = count_epbs_by_year(df)

path = 'database/epbs/epbs_2013_2023'

df = b.load(path)

df = c.pivot_epb_by_type(
    df, total = False, sel_lon = -50)

df = c.add_geo(df)

df = df.loc[df['kp'] <= 3]

ds = count_epbs_by_year(df['epb'])
df = average_equinox(df['f107a'])

def plot_equinox_asymetry(ds, df):
        
    fig, ax = plt.subplots(
        figsize = (12, 4),
        dpi = 300
        )
 
    bar_width = 0.25
    
    lbs = {'march': "black", 'september':  "#0b4ea2"}
    
    for idx, (name, color) in enumerate(lbs.items()):
        
        data = ds[name]
        if idx == 0:
            offset = 0
        else:
            offset = bar_width / idx
            
        ax.bar(
               ds.index - offset,
               data,
               width=bar_width,
               color= color,
               label= name.capitalize(),
               edgecolor = 'white'
           )
            
    ds['div'] = (ds['september'] - 
                 ds['march']) /  ds['march']
    
    ax.legend(ncol = 2)
    
    ax.set(
           xlabel = 'Years',
           ylim = [0, 110],
           ylabel = 'Occurrence rate (\%)'
           )
    ax1 = ax.twinx()
    
    
    ax1.plot(df, lw = 2, marker = 's', 
             markeredgecolor = 'white',
             markersize = 8)
    
    ax1.set(
            ylabel = 'F10.7 (sfu)',
            ylim = [50, 200], 
            xlim = [2012.5, 2023.5],
            xticks = np.arange(2013, 2024)
            )
    
    return fig 

fig = plot_equinox_asymetry(ds, df)