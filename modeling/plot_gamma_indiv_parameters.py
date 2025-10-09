import base as b
import GEO as gg
import datetime as dt
import matplotlib.pyplot as plt
import RayleighTaylor as rt 
import numpy as np 
import pandas as pd 

b.sci_format(fontsize = 30)

def plot_shade_around_terminator(ax, dn, site, translate = True):
    
    if translate:
        
        label = 'Solar terminator'
        
    else:
        label = 'Terminadouro solar'
    
    dusk = gg.dusk_from_site(
            dn, 
            site[:3].lower(),
            twilight_angle = 18
            )
    
    ax.axvline(dusk, lw = 2, linestyle = '--', 
               )
    delta = dt.timedelta(minutes = 30)
    
    ax.text(
        dusk + delta, 1.6,
        label
        , transform = ax.transData
        )
    
    
    ax.axvspan(
         dusk - delta, 
         dusk + delta, 
         ymin = 0, 
         ymax = 1,
         alpha = 0.2, 
         color = 'red'
     )
    
    
    return dusk

def junk_smooth(ds):
    # ds = ds.resample('10min').mean()

    dn = dt.datetime(2015, 12, 21)
    
    delta = dt.timedelta(hours = 12)
    
    end = dn + delta
    
    ds.loc[dn: end] = ds.loc[dn: end].rolling(
        window = 5, 
        center = True
        ).mean()
    return ds.interpolate()


def get_results(ds, ref_dn, col = 'wind'):
    # ref_dn = dt.datetime(2015, 12, 20, 22, 0)
    delta = dt.timedelta(minutes=30)
    
    sel = ds.loc[
        ((ds.index > ref_dn - delta) & 
        (ds.index < ref_dn))
        ].copy()
    
    date = sel[col].idxmax()
    # print(date)
    value =  sel.loc[date][col]
    return pd.DataFrame({col: value}, index = [date])

    
    
def plot_winds_effects_on_gamma(site = 'FZA0M', translate = True):
    
    if translate:
        b_label = '(b) Without meridional winds'
        a_label = '(a) With meridional winds'
        labels = ['Storm-time', 'Quiet-time']
    else:
        b_label = '(b) Sem ventos meridionais'
        a_label = '(a) Com ventos meridionais'
        labels = ['Periodo perturbado', 'Período calmo']
    fig, ax = plt.subplots(
        figsize = (16, 10), 
        dpi = 300, 
        nrows = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    dn = dt.datetime(2015, 12, 20, 12)
   
    storm =  b.sel_times(rt.stormtime_gamma(site), dn, hours = 24)
    quiet =  b.sel_times(rt.quiettime_gamma(site), dn, hours = 24)
    
    
    frames = [storm, quiet]
    lws = ['-', '--']
    colors = ['k', 'purple']
    lw = 3
    out = []
    for i, ds in enumerate(frames):
        
        ds = junk_smooth(ds)
        
        ax[0].plot(
            ds['wind'], 
            label = labels[i], 
            lw = lw, 
            linestyle = lws[i],
            color = colors[i]
            )
    
        ax[1].plot(
            ds['no_wind'], 
            label = labels[i], 
            lw = lw, 
            linestyle = lws[i],
            color = colors[i]
            )
        
        
        lim = 2.2
        ax[i].set(
            ylim = [-lim, lim],
            yticks = np.arange(-2, 3, 1),
            xlim = [storm.index[0], storm.index[-1]],
            ylabel = '$\\gamma_{RT}~ (\\times 10^{-3} ~s^{-1})$'
            )
        
        ax[i].axhline(0, lw = 0.5)
        
        dn = dt.datetime(2015, 12, 20, 21, 40)
        dusk = plot_shade_around_terminator(ax[i], dn, site, translate = translate)
        
        out1 = []
        for col in ['wind', 'no_wind']:
            res = get_results(ds, dusk, col)
            res.index = [labels[i]]
            out1.append(res)
    
        out.append(pd.concat(out1, axis=1))
        
        
        
        
    
    b.format_time_axes(
            ax[-1], 
            hour_locator = 2, 
            tz = 'UTC',
            translate = translate, 
            pad = 85
            )
    
    # print(pd.concat(out))
    
    
    ax[0].legend(
        ncol = 2, 
        loc = 'upper center', 
        bbox_to_anchor = (0.5, 1.2), 
    
        )
     
    ax[0].text(
        0.01, 0.85, 
        a_label, 
        transform = ax[0].transAxes
        )
    
    ax[1].text(
        0.01, 0.85, 
        b_label, 
        transform = ax[1].transAxes
        )
    
    return fig 
    
def main():
    
    site = 'FZA0M'
    # site = 'SAA0K'
    fig = plot_winds_effects_on_gamma(site, translate=False)
    
    
    FigureName = 'fortaleza_gamma_pt'
    
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    
    fig.savefig(path_to_save + FigureName, dpi = 400)



# main()

