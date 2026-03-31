
import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 

b.sci_format()

lat_lims = dict(min = -30, max = 10, stp = 10)
lon_lims = dict(min = -65, max = -30, stp = 10)



fig, ax = plt.subplots(
    dpi = 300,
    sharex = True, 
    figsize = (15, 10),
    subplot_kw = {'projection': ccrs.PlateCarree()}
)

gg.map_attrs(
    ax, year = None,
    degress = None, 
    grid = False, 
    lat_lims = lat_lims,
    lon_lims = lon_lims
    )

for year in [2013, 2023]:
    gg.mag_equator(
        ax,
        year,
        degress = None, 
        color = 'red'
        )
