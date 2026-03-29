import datetime as dt
import numpy as np 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 
import GEO as gg
from FluxTube import Apex

 
def plot_meridian_range(ax, x, y, nx, ny, rlat=12, color="magenta", lw=3, hemisphere = 'both'):
    """Plota apenas o trecho (ex.: hemisfério norte) do meridiano."""
    x1, y1 = gg.limit_hemisphere(x, y, nx, ny, rlat, hemisphere=hemisphere)
    ax.plot(x1, y1, linestyle="--", lw=lw, color=color)
    return ax


def plot_all_meridians(ax, year, *, delta=5, lmin=-120, lmax=-30, color="k", lw=1):
    """Plota o conjunto de meridianos (linhas finas) para referência."""
    dn = dt.datetime(year, 1, 1)
    mer = gg.meridians(dn, delta=delta)
    meridian_set = mer.range_meridians(lmin=lmin, lmax=lmax)

    for i in range(meridian_set.shape[0]):
        x, y = meridian_set[i][0], meridian_set[i][1]
        ax.plot(np.asarray(x) - 0.1, np.asarray(y) - 1.8, lw=lw, color=color)

    return ax







def plot_site_meridian(
        ax, year, site="saa", 
        marker = '*',
        meridian_color="k", meridian_lw=2):
    """Plota o site (estrela) e o meridiano carregado do JSON."""
    st = gg.sites[site]
    glat, glon = st["coords"]

    ax.scatter(
        glon, glat,
        s=100, marker= marker, c="r",
        transform=ccrs.PlateCarree(),
        label=st['name'],
        zorder=6,
    )

    nx, ny, x, y = gg.load_meridian(year, site)
 
    x, y = gg.interpolate_path(x, y, points=50)
   
    ax.plot(
        x, y,
        color=meridian_color,
        lw=meridian_lw,
        transform=ccrs.PlateCarree(), 
    )
    
    mlat = Apex(300).apex_lat_base(base = 75)

 
    plot_meridian_range(ax, x, y, nx, ny, rlat=np.degrees(mlat), color="magenta", lw=3)

    return nx, ny, x, y




 
def plot_mag_meridians(year=2024, site="saa"):
    fig, ax = plt.subplots(
        dpi=300,
        figsize=(12, 10),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )

    lat_lims = dict(min=-40, max=10, stp=5)
    lon_lims = dict(min=-90, max=-35, stp=5)

    gg.map_attrs(
        ax, year,
        lon_lims=lon_lims,
        lat_lims=lat_lims,
        grid=False,
        degress=None,
    )

    # referência: todos meridianos
    plot_all_meridians(ax, year, delta=5)

 
    # meridiano do site
    plot_site_meridian(ax, year, site=site)
    plot_site_meridian(ax, year, site='jic', marker = 's')
    # equador magnético
    gg.mag_equator(ax, year, degress=None)

    # legenda
    ax.legend(
        ncol=2,
        loc="upper center",
        columnspacing=0.6,
        bbox_to_anchor=(0.5, 1.15),
        frameon=False,
    )

    return fig, ax


 
fig, ax = plot_mag_meridians(year=2024, site="saa")
 
nx, ny, x, y = gg.load_meridian(2024, 'jic')


plt.plot(x, y)