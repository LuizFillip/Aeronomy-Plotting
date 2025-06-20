import PlasmaBubbles as pb 
import pandas as pd 

def sel_season(df, season):
    
    if season == 'march':
        num = [3, 4]
    elif season == 'september':
        num = [9, 10]
    else:
        num = [12, 11]
        
        
    return df.loc[
        (df.index.month == num[0]) |
        (df.index.month == num[1])
        ]

names = ['march',  'september', 'december']

p = pb.BubblesPipe(
    'events_5', 
    drop_lim = 0.3, 
    storm = 'quiet'
    )

df = p.sel_type('sunset')

df.columns 

df = df.loc[df.lon == -50]
year = 2013

def count_epbs_by_year():
    
    out_df = []
    for year in range(2013, 2023):
        
        sel_year = df.loc[df.index.year == year]
        
        out = {name: [] for name in names}
        
        for season in names:
            ds = sel_season(df, season)
            
            out[season].append(len(ds))
            
        out_df.append(
            pd.DataFrame(
                out, index = [year])
            ) 
    return pd.concat(out_df)