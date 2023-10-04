import PlasmaBubbles as pb
import matplotlib.pyplot as plt 
import numpy as np 
import base as b 
import datetime as dt 
import os

b.config_labels()

args = dict(
    marker = 'o', 
    markersize = 3,
    linestyle = 'none', 
    alpha = 0.5,
    color = 'k'
    )



def plot_roti_avg(ax, df):
    
    vmax = round(df['avg'].max(), 2)
    ax.plot(df['roti'], **args, label = 'ROTI')
    
    ax.plot(df['avg'], lw = 3, color = 'r')
    ax.axhline(
        vmax, 
        lw = 2, 
        linestyle = '--', 
        color = 'r', 
        label = '$\mu_{max}$'
        )
    
    return vmax


def plot_std_shade(ax, df, i = 3):
    
    ax.fill_between(
        df.index, 
        df['avg'] + i * df['std'], 
        df['avg'] - i * df['std'], 
        alpha = 0.3, 
        color = 'r'
        )
    

def plot_base(ax, df):
    
    base = round(df['roti'].mean(), 2)
    ax.axhline(
        base, 
        lw = 2, 
        color = 'b', 
        label = 'Base (mean)'
        )
    
    return base


def plot_threshold(ax, dn, lon = -60):
    
    if lon is not None:
        threshold = pb.threshold(dn, lon)
    else:
        threshold = dn
    
    # value = f'{threshold} TECU/min'
    ax.axhline(
        threshold, 
        lw = 2, 
        color = 'magenta'
        )

def plot_solar_flux(ax, dn):
    
    flux = b.get_flux(dn) / 100
    
    ax.axhline(
        flux, 
        lw = 2, 
        color = 'g', 
        label = '$F_{10.7} / 100$'
        )
    
    return flux



def load_data(dn, long, N = 60):
    
    df = pb.longitude_sector(
        pb.concat_files(dn), long
        )
    
    df = b.sel_times(df, dn, hours = 11)
    
    df['avg'] =  b.smooth2(
        b.running(df['roti'], N), N * 4
        )
    df['std'] =  b.smooth2(
        b.running_std(df['roti'], N), N * 4
        )
    
    cond = (df['roti'] > df['avg'] + df['std'] * 2)

    return df.loc[~cond]
    # return df


def plot_demo_get_threshold(dn, lon):
    
    fig, ax = plt.subplots(
        dpi = 300,
        sharex = True, 
        sharey = True,
        figsize = (12, 4)
        )
    
    infile = os.path.join(
            pb.PATH_LONG, 
            f'{dn.year}.txt'
        )
     
    ds = b.sel_times(
            b.load(infile), 
            dn, 
            hours = 11
        )
    
    # ax.plot(df[lon])
    # ax.plot(ds[str(lon)], **args)
    df = load_data(dn, lon)
    
    # plot_std_shade(ax, df, i = 2)
    
    
    avg = plot_roti_avg(ax, df)
    flux = plot_solar_flux(ax, dn)
    base = plot_base(ax, df)
    
    
    the = round((avg + flux + base) / 3, 2)
    
    # plot_threshold(ax, the, None)
    
    b.format_time_axes(ax)
    
    ax.set(
        yticks = np.arange(0, 5, 1), 
        ylabel = 'ROTI (TECU/min)',
        ylim = [0, 3], 
        )
    
    ax.legend(
        ncol = 4, 
        bbox_to_anchor = (.5, 1.2), 
        loc = "upper center", 
        columnspacing = 0.6
        )

    return fig


dn = dt.datetime(2013, 1, 1, 21)

lon = -60

f = plot_demo_get_threshold(dn, lon)

def save_from_figure(FigureName = None):
    func = plot_demo_get_threshold
    if FigureName is None:
        FigureName = func.__name__.replace("plot_", "") + ".png"
    save_in = os.path.join(b.LATEX, FigureName)
    
    b.save_img(f, save_in)