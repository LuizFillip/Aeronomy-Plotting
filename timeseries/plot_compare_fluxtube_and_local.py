import pandas as pd
import matplotlib.pyplot as plt
import digisonde as dg
import numpy as np
from GEO import sites
import models as m
import ionosphere as io
import RayleighTaylor as rt
import settings as s


def add_growth_rate(df, dn):
    
    vz = dg.add_vzp()
    
    vzp = vz[vz.index == dn.date()]["vzp"].item()
    
    df["g"] = df["L"] * (
        (9.81 / df["nui"]) - df["mer"] + vzp)
    return df


def local(dn):
    
    glat, glon = sites['saa']['coords']
    
    wargs = dict(
         dn = dn, 
         glat = glat, 
         glon = glon,
         hmin = 200,
         hmax = 500,
         step = 10
         )
    
    infile = "database/Digisonde/SAA0K_20130319(078)_pro"
    df = dg.load_profilogram(infile)
    
    df = df.loc[(df.index == dn) & 
                (df['alt'] > 200) &
                (df['alt'] < 500)]
    
    msis = m.altrange_msis(**wargs)
    nu = io.collision_frequencies()
    msis['nui'] = nu.ion_neutrals(
        msis["Tn"], msis["O"], 
        msis["O2"], msis["N2"]
        )
        
    msis.index = [dn] * len(msis)
    infile = "database/HWM/winds_all_sites.txt"
    
    wd = pd.read_csv(infile, 
                     index_col = 0)
    wd.index = pd.to_datetime(wd.index)
    
    wd = wd.loc[(wd['site'] == 'saa') & 
                (wd.index == dn) ]
    
    D = np.radians(-19.62)
    I = np.radians(-6.02)
    df['mer'] = (wd['mer'] * np.cos(D) + 
                 wd['zon'] * np.cos(D)) * np.sin(I)
    
    
    df['nui'] = msis['nui'].copy()
    return df




def plot_int_profiles():
    
    fig, ax = plt.subplots(
        ncols = 2, 
        figsize = (10, 8),
        sharey = True,
        dpi = 300
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    dates = pd.date_range(
        "2013-3-16 22:00", 
        freq = "1D", 
        periods = 3
        )
    
    for dn in dates:
        
        south = comp_gamma(dn, hem = 'north')
        north = comp_gamma(dn, hem = 'south')
        
        alt = np.linspace(200, 500, len(north))
        
        label = dn.strftime('%d/%m %H:%M (UT)')
        ax[0].plot((south + north)* 1e4, alt, 
                   label = label)
        
        df = add_growth_rate(local(dn), dn)
        
        ax[1].plot(df['g'] * 1e4, df['alt'], 
                   label = label)

    ax[0].legend(   
        bbox_to_anchor = (1., 1.1), 
        ncol = 3, 
        loc = 'upper center'
        )
    
    ax[0].set(
        xlabel = '$\gamma_{FT} ~(10^{-4}~s^{-1})$', 
        ylabel = 'Altura de apex (km)'
        )
    
    ax[1].set(
        ylabel = 'Altura local (km)',
        xlabel = '$\gamma_{RT} ~(10^{-4}~s^{-1})$'
        )
    
    integrated = rt.EquationsFT().complete()
    local_l = rt.EquationsRT().complete()
    
    names = [integrated, local_l]
    for i, ax in enumerate(ax.flat):
        ax.axhline(300)
        ax.axvline(0)
        ax.set(ylim = [200, 550], 
               xlim = [-30, 30])
    
        letter = s.chars()[i]
        ax.text(
            0.04, 0.95, f"({letter}) {names[i]}", 
            transform = ax.transAxes
            )
    
    fig.suptitle('Comparação entre os perfis locais e integrados')

    return fig


# fig = plot_int_profiles()

# fig.savefig('RayleighTaylor/figures/compare_local_fluxtube.png', dpi = 300)