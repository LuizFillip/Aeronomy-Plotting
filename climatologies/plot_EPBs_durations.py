import base as b 
import matplotlib.pyplot as plt

df = b.load('events_2013_2023_2')



fig, ax = plt.subplots(
    nrows = 4,
    sharex = True, 
    sharey = True,
    figsize = (12, 10),
    dpi = 300
    )

fontsize = 30
plt.subplots_adjust(hspace = 0.1)

lons = df['lon'].unique()[::-1]

for i, lon in enumerate(lons):
    ds = df.loc[df['lon'] == lon, 'duration']
    ax[i].plot(ds)
    l = b.chars()[i]
    ax[i].text(0.02, 0.75, f'({l}) {lon}°', 
               transform = ax[i].transAxes)

fig.text( 
    0.4, 0.05,
    'Anos', 
    fontsize = fontsize)

fig.text(
    0.03, .32, 'Tempo somado (horas)', 
    rotation = 'vertical', 
    fontsize = fontsize
    )