import matplotlib.pyplot as plt 
import core as c


# count_events(df)

# df = df[['field', 'by', 'bz', 'speed', 'electric',
#        'ae', 'sym', 'divtime', 'occ']]
# ds = seasonal_average(df)

# 

# plt.scatter(ds.occ, ds.electric)

def plot_seasonal_bars(df):

    df['month'] = df.index.month 
    
    ds = df.groupby(['category', 'month']).size().unstack(fill_value=0)
    ds = ds.T
    # print(ds)
    colors = {
        'intense': '#8B0000',   # vermelho escuro
        'moderate': '#FF4500',  # laranja forte
        'weak': '#FFD700',      # dourado
        'quiet': '#32CD32'      # verde
    }
    ds = ds.reindex(range(1, 13), fill_value = 0)
    
    ds.plot(
        kind='bar',
        stacked=True,
        figsize=(7, 4),
        color=[colors[c] for c in ds.columns]
    )

df = c.geomagnetic_analysis()


ds = df[['divtime', 'category', 'phase']] 

ds 