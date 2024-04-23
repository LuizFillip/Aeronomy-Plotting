import matplotlib.pyplot as plt
import base as s
import numpy as np
import pandas as pd
import datetime as dt
from models import altrange_iri    

def change_color_background(ax, color = "black"):
    
    ax.spines['bottom'].set_color(color)
    ax.spines['top'].set_color(color)
    ax.spines['left'].set_color(color)
    ax.spines['right'].set_color(color)
    
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.zaxis.label.set_color(color)
    ax.title.set_color(color)
    
    for axes in ["x", "y", "z"]:
        ax.tick_params(axis = axes, colors=color)

def config_plot(ax):

    ax.grid(False)
    
    ax.view_init(azim = -80, elev = 25)
    
    ax.set(ylabel = "Latitude (°)", 
           xticks = np.arange(-50, -38, 1),
           zlim = [75, 500],
           xlim = [-50, -40], 
           ylim = [-12, 20], 
           xlabel = "Longitude (°)", 
           zlabel = "Altura de apex (km)")

    ax.xaxis.set_pane_color((1.0, 0.0, 1.0, .0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, .0))
    
    
def plot_scatter_fluxtube(ax, df, 
                          parameter = "Ne", 
                          color = "black"):

    lons, lats, alts = df.lon.values, df.lat.values, df.zeq.values
    vls = np.log10(df[parameter])
    
    ax.plot3D(lons, lats, alts, 'gray')
    
    img = ax.scatter3D(lons, lats, alts, 
                       c = vls, 
                       cmap = "rainbow")
    
    vmin, vmax = round(min(vls)), round(max(vls)) + 1
    
    ticks = np.arange(vmin, vmax, 1)
    
    s.colorbar(
        img, ax,
        ticks, 
        height = "100%", 
        width = "3%", 
        # loc = "upper right",
        label = "log10 Ne ($cm^{-3}$)", 
        # color='k',
        anchor = (0.2, 0.05, 0.4, 0.8)
        )
    middle = len(lons) // 2 
    ax.text(lons[middle - 10], lats[middle], 320, 
            "Tubo de\nFluxo", color = color)
    
def plot_local_profile(ax,
        dn = dt.datetime(2013, 1, 1, 21), 
        glon = -44, 
        glat = -4, 
        color = "black"):


    ds = altrange_iri(dn, glat, glon, 
                      hmin = 75, 
                      hmax = 500,
                      step = 30)
    
    b = np.zeros(len(ds))
    ax.scatter3D(
        b + glon, 
        b + glat, 
        ds.index, 
        c = np.log10(ds["ne"]*1e-6),
        cmap = "rainbow"
        )
    
    ax.text(glon + 0.5, glat, 400, 
            "Perfil local", color = color)
        
def plot_meridian(
        ax, df, color = "black", 
                  translate = True):
    
    base = np.zeros(len(df)) + 80
    ax.plot3D(df.lon, df.lat, base)
    if translate:
        label = "Meridiano\nmagnético"
    else:
        label = 'Magnetic meridian'
    
    ax.text(
        -45, -12, 75, 
          label , 
          color = color)
   
   
def plot_surface_region(ax, df):
        
    
    X, Y = np.meshgrid(df.lon, df.lat)
     
    Z = X * 0 + 150
    
    ax.plot_surface(X, Y, Z, color = "b", alpha = 0.6)
    
    ax.text(-42, -2, 150, "Região E", 
            color = "b", alpha = 0.8)

def plot_vertical_line(ax, df):
    
    lons = df.lon.values
    lats = df.lat.values
    
    b = np.zeros(len(lons))
    
    z = np.linspace(75, 500, len(lons))
    
    middle = len(lons) // 2
    
    
    ax.plot3D(b + lons[middle], 
              b + lats[middle], 
              z, color = "k")
    
    
def load_data(infile, apex = 300):
    df1 =  pd.read_csv(infile, index_col = 0)
    
    df1.rename(columns = {"alt": "zeq",
                          "glon": "lon", 
                          "glat": "lat"}, 
               inplace = True)
    
    
    return df1.loc[df1["apex"] == apex]


def plot_3D_fluxtube(color = "k"):
    fig = plt.figure(figsize= (12, 8), dpi = 300)
    ax = plt.axes(projection = "3d")
    
    infile = "FluxTube/data/20131224.txt"
    
    
    df = load_data(infile, apex = 300)
    df = df.iloc[::3, :]
    
    plot_scatter_fluxtube(ax, df, color = color)
    
    plot_meridian(ax, df, color = color)
    
    plot_local_profile(ax, color = color)
    
    plot_surface_region(ax, df)
    
    plot_vertical_line(ax, df)
    
    config_plot(ax)
    
    change_color_background(ax, color = color)

    return fig


    
fig = plot_3D_fluxtube()


# fig.savefig("name.png", transparent=True)
