import base as b
import digisonde as dg 
import matplotlib.pyplot as plt
import GEO as gg


PATH_CHAR = 'digisonde/data/chars/midnight/'

def site_name(fn):
    if 'BVJ' in fn:
        name = 'Boa vista'
        site = 'boa'
    elif 'CAJ' in fn:
        name = 'Cachoeira Paulista'
        site = 'caj'
    elif 'SAA' in fn:
        name = 'São Luis'
        site = 'saa'
    else:
        name = 'Fortaleza'
        site = 'fza'
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
    
    line, = ax.plot(df["foF2"], label = name)
    
    ax.set(
        ylim = [0, 20], 
        ylabel = "foF2 (MHz)"
        )
    
    return line.get_color()


def plot_fhF2(ax, df, name):
    
    ax.plot(df["fhF2"], label = name)
    
    ax.set(
        ylim = [0, 20], 
        ylabel = "f(hF2) (MHz)"
        )




def plot_terminators(
        ax, 
        df, 
        site = 'boa',
        color = 'k'
        ):
    
    dn = df.index[0]
    
    glat, glon = gg.sites[site]['coords']
    
    dusk = gg.dusk_from_site(
            dn, 
            site,
            twilight_angle = 18
            )
    
    for ax in ax.flat:
        ax.axvline(
            dusk, 
            lw = 2,
            color = color
            )
        


def plot_iono_chars(dn):
    
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 10), 
        nrows = 4, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    out = {}
    
    for site in [ 'FZA0M', 'SAA0K', 'CAJ2M']: 
        
        fn  = f'{site}_{dn}.TXT'
        
        df = dg.chars(PATH_CHAR + fn)
      
        name, site = site_name(fn)
        
        plot_hmF2(ax[0], df, name)
        
        plot_hF2(ax[1], df, name)
        
        color = plot_foF2(ax[2], df, name)
     
        # plot_QF(ax[3], df, name, color)
        
        out[site] = color
        
    
    ax[0].legend(
        ncol = 3, 
        columnspacing=0.3,
        loc = 'upper center',
        bbox_to_anchor = (.5, 1.4),
        )
    
    b.format_time_axes(ax[-1])
    
    for site, color in out.items():
        plot_terminators(ax, df, site, color)
        
    b.plot_letters(ax, y = 0.79, x = 0.02)
    return fig

dn = '20161003(277)'
dn = '20170423(113)'
dn = '20170403(093)'
dn = '20130327(086)'
dn = '20150409(099)'
dn = '20220724(205)'

fig = plot_iono_chars(dn)