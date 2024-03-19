import matplotlib.pyplot as plt 
import base as b 
import plotting as pl 
import core as c 



def plot_roti_solar_magnetic_activity():
    
    df = b.load('all_maximus')


    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 3,
        figsize = (16, 12), 
        )

    plt.subplots_adjust(hspace = 0.1)


    ds = df.resample('1D').mean()

    idx = c.geo_index(
            cols = ['f107a', 'f107', 'kp', 'dst'],
            syear = 2013, 
            eyear = 2023
            )

    pl.plot_F107(ax[1], idx, solar_level = None)
    pl.plot_Kp(ax[0], idx, kp_level = None)
    ax[2].plot(ds['-50'])

    ax[2].set(
        xlim = [ds.index[0], ds.index[-1]], 
        xlabel = 'Anos', ylabel = 'ROTI (TECU/min)')

    b.plot_letters(ax, y = 0.8, x = 0.02)
    
    return fig
    
    
fig = plot_roti_solar_magnetic_activity()


# FigureName = 'annual_variation_roti_and_indices'
# fig.savefig(b.LATEX(FigureName, folder = 'climatology'))
