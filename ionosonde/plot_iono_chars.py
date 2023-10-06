import base as b
import digisonde as dg 
import matplotlib.pyplot as plt
import GEO as gg


PATH_CHAR = 'database/iono/midnight/'

def site_name(fn):
    if 'BVJ' in fn:
        name = 'Boa vista'
        site = 'boa'
    elif 'SAA' in fn:
        name = 'São Luis'
        site = 'saa'
    else:
        name = 'Fortaleza'
        site = 'for'
    return name, site


def plot_hmF2(ax, df, name):
    
    ax.plot(df["hmF2"], label = name)
    
    ax.set(
        ylim = [100, 600], 
        ylabel = "hmF2 (km)",
        #xlim = [df.index[0], df.index[-1]]
        )
    
def plot_hF2(ax, df, name):
    
    ax.plot(df["hF2"], label = name)
    
    ax.set(
        ylim = [100, 600], 
        ylabel = "hF2 (km)",
        #xlim = [df.index[0], df.index[-1]]
        )
    
def plot_foF2(ax, df, name):
    
    ax.plot(df["foF2"], label = name)
    
    ax.set(
        ylim = [0, 20], 
        ylabel = "foF2 (MHz)"
        )


def plot_QF(ax, df, name):
    
    ax.bar(df.index, df["QF"],
           width = 0.01, 
           label = name)
    
    ax.set(
        ylim = [0, 40], 
        ylabel = "QF (Km)"
        )


def plot_terminators(
        ax, 
        df, 
        site = 'boa',
        color = 'k'):
    
    dn = df.index[0]
    
    glat, glon = gg.sites[site]['coords']
    
    dusk = gg.dawn_dusk(
            dn,  
            lat = glat, 
            lon = glon, 
            twilightAngle = 18
            )
    for ax in ax.flat:
        ax.axvline(
            dusk, 
            color = color
            )
        
dn = '20161003(277)'
dn = '20170423(113)'
dn = '20170403(093)'
dn = '20130327(086)'
dn = '20150409(099)'

def plot_iono_chars(dn):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (10, 8), 
        nrows = 4, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    out = []
    
    for site in [ 'BVJ03', 'FZA0M', 'SAA0K']: 
        
        fn  = f'{site}_{dn}.TXT'
        
        df = dg.pipeline_char(PATH_CHAR + fn)
        
        name, site = site_name(fn)
        
        out.append(site)
        
        plot_hmF2(ax[0], df, name)
        
        plot_hF2(ax[1], df, name)
        
        plot_foF2(ax[2], df, name)
        
        plot_QF(ax[3], df, name)
       
    
    ax[0].legend(
        ncol = 3, 
        loc = 'upper center',
        title = 'Sites',
        bbox_to_anchor = (.5, 1.7),
        )
    
    b.format_time_axes(ax[3])
    color = ['k', '#0C5DA5', '#00B945']
    
    for i, site in enumerate(out):
        plot_terminators(
            ax, df, site, color[i])


plot_iono_chars(dn)