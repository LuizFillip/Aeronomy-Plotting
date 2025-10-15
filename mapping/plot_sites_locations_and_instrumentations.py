import cartopy.crs as ccrs
import GEO as gg
import matplotlib.pyplot as plt
import base as b 
import numpy as np 

b.sci_format(fontsize = 30)


def place_ocean_labels(
    ax, stations, side="east",
    margin=1.0, min_dy=0.8,
    line_kw=None, text_kw=None, crs=None
):
    """
    Coloca rótulos das estações no lado do oceano e liga com uma linha reta.

    Parâmetros
    ----------
    ax : matplotlib Axes (ou GeoAxes do Cartopy)
    stations : list[dict]  cada item: {"name": str, "lon": float, "lat": float}
    side : {"east","west"} lado onde os rótulos ficam
    margin : float         margem em graus do limite do mapa para posicionar textos
    min_dy : float         separação mínima em latitude entre rótulos (evita overlap)
    line_kw : dict         kwargs para a linha (cor, lw, etc.)
    text_kw : dict         kwargs para o texto (fontsize, ha, va, etc.)
    crs : cartopy.crs ou None  passe PlateCarree() se estiver com Cartopy
    """
    line_kw = {"color": "k", "lw": 2} | (line_kw or {})
    text_kw = {"fontsize": 12, "ha": "left", "va": "center"
               } | (text_kw or {})

    # limites do mapa (em graus) já definidos pelo set_extent / set_xlim,set_ylim
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()

    # coordenada x onde os rótulos ficam
    if side == "east":
        x_lab = (x1 - margin)
        text_kw["ha"] = "left"
    else:
        x_lab = (x0 + margin)
        text_kw["ha"] = "right"

    # Ordena por latitude para distribuir sem sobrepor
    sts = sorted(stations, key = lambda s: s["lat"])
    
    # posição desejada (lat) e ajustada (para evitar overlap)
    target_lats = np.array([s["lat"] for s in sts], dtype = float)
    placed_lats = target_lats.copy()

    # “espalhador” simples: garante distância mínima min_dy entre rótulos
    for i in range(1, len(placed_lats)):
        if placed_lats[i] - placed_lats[i-1] < min_dy:
            placed_lats[i] = placed_lats[i-1] + min_dy
    
    # clip dentro do mapa
    
    placed_lats = np.clip(
        placed_lats, 
        y0 + 0.5 * min_dy, 
        y1 - 0.5 * min_dy
        )

    # Desenha textos e linhas
    for s, y_txt in zip(sts, placed_lats):
        lon, lat, name = s["lon"], s["lat"], s["name"]
        
    
        ax.text(x_lab, y_txt, name, transform=crs, **text_kw)
        xs = [lon, x_lab]
        ys = ([lat, y_txt] if abs(y_txt - lat) > 0
              else [lat, lat] )
        ax.plot(xs, ys, transform=crs, **line_kw)
            
    return None 


def plot_sites(ax, year):
        
    sites  = ['jic', 'saa', 'bvj', 'ca', 'cp', 'bjl']
    sites = ['saa', 'fza', 'ca', 'caj', 'cgk', 'bvj']
    for i, s in enumerate(sites):
        
        site = gg.sites[s]
        
        name = site['name']
        glat, glon = site['coords']
        

        if s == 'ca':
            marker = 'o'
            gg.plot_circle(
                    ax, 
                    glon, 
                    glat, 
                    radius = 250, 
                    edgecolor = "green",
                    lw = 3
                    )
        else:
            marker = 's'
        
        ax.scatter(
            glon, glat, 
            s = 150,
            marker = marker, 
            label = name
            )
        
        ax.text(glon + 3, glat + 1, name)
  
    
    return None

def plot_GNSS(ax, year, translate = False):

    lon, lat = gg.stations_coordinates(year, distance = 100)
    if translate:
        label = 'Receptores GNSS'
    else:
        label = 'GNSS receivers'
    
    args = dict( 
        s = 50, 
        marker = '^',
        color = 'red', 
        transform = ccrs.PlateCarree()
        )


    sits, lon, lat = gg.arr_coords(year = 2021)
    ax.scatter(lon, lat, **args)
    
    # ax.annotate(
    #     'Receptores GNSS', xy=(lon[1], lat[1]), 
    #     xytext=(lon[1] - 5, lat[1] + 15),
    #     arrowprops=dict(lw = 2, arrowstyle='->'), 
    #     transform = ax.transData, 
    #     fontsize = 25
    #     )
    return None 

lat_lims = dict(min = -30, max = 10, stp = 10)
lon_lims = dict(min = -65, max = -30, stp = 10)

def legend_dummy():
    
    kwargs = dict(
        edgecolors = 'none',
        s = 200
        )
    
    l1 = plt.scatter(
        [], [], color = 'black', marker = 's', 
        **kwargs)
    l2 = plt.scatter(
        [], [], color = 'green', marker = 'o', 
        **kwargs)
    l3 = plt.scatter(
        [], [], color = 'red', marker = '^', 
        **kwargs)

    labels = ["Ionosonde", "FPI", 'GNSS receivers']

    plt.legend(
        [l1, l2, l3], 
        labels, 
        ncol = 3, 
        fontsize = 25,
        handlelength = 2,
        bbox_to_anchor = (1, 1.1),
        labelspacing = 0,
        columnspacing = 0.3 
        # scatterpoints = 1
        )
    
    return None 

def plot_regions_over_map(year = 2013):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        figsize = (15, 10),
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )
    
    gg.map_attrs(
        ax, year,
        degress = None, 
        grid = False, 
        lat_lims = lat_lims,
        lon_lims = lon_lims
        )
    stations = [
        {"name": "Boa Vista",           "lon": -60.7, "lat":  2.8},
        {"name": "São Luís",            "lon": -44.2, "lat": -2.6},
        {"name": "Fortaleza",           "lon": -38.5, "lat": -3.7},
        {"name": "São João \ndo Cariri",  "lon": -36.5, "lat": -7.4},
       
    ]

    plot_GNSS(ax, year, translate = False)
    

    place_ocean_labels(
        ax, stations,
        side = "east", margin = 9, min_dy=1.6,
        line_kw = {"color":"0.2","lw":2},
        text_kw = {"fontsize":25},
        crs = ccrs.PlateCarree()
    )
    
    # stations = [
    #     {"name": "Campo Grande",        "lon": -54.6, "lat": -20.4},
    #     {"name": "Cachoeira Paulista",  "lon": -45.0, "lat": -22.7},
    #     ]
    
    # place_ocean_labels(
    #     ax, stations,
    #     side = "east", margin = 14, min_dy=1.,
    #     line_kw = {"color":"0.2","lw":2},
    #     text_kw = {"fontsize":25},
    #     crs = ccrs.PlateCarree()
    # )
    
    # for s in stations:
        
    #     marker = 's'
    #     color = "k"
            
    #     ax.plot(
    #         s["lon"], s["lat"], 
    #         marker, 
    #         color = color, 
    #         markersize = 15,
    #         transform = ccrs.PlateCarree()
    #         )
    legend_dummy()
    
    for s in stations:
        if s['name'] == "São João \ndo Cariri":
            marker = 'o'
            color = 'green'
            
            gg.plot_circle(
                    ax, 
                    s["lon"], s["lat"], 
                    radius = 250, 
                    edgecolor = color,
                    lw = 3
                    )
            
        else:
            marker = 's'
            color = "k"
            
        ax.plot(
            s["lon"], s["lat"], 
            marker, 
            color = color, 
            markersize = 15,
            transform = ccrs.PlateCarree()
            )

    return fig

def main():
    fig = plot_regions_over_map(year = 2015)
    
    FigureName = 'sites_locations'
    
    save_in = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'

    # fig.savefig(save_in + FigureName, dpi = 300
    #             )
    
main()