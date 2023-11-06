import matplotlib.pyplot as plt
import base as b 
import RayleighTaylor as rt 


b.config_labels()

lbs = b.Labels().infos


def plot_gamma(ax, df):
    
    df = df * 1e3
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    avg = b.smooth2(df, 20)
    ax.plot(
        df.index, 
        avg, 
        lw = 2
        )
    
    ax.set(
        ylim = [-1, 4], 
        ylabel = b.y_label('gamma'),
        xlabel = 'years',
        xlim = [df.index[0], df.index[-1]]
        )
    
    ax.axhline(avg.max(), linestyle = '--')
    ax.axhline(avg.min(), linestyle = '--')
    
    return df


def plot_grad(ax, df):
    
    df = df * 1e5

    ax.plot(
        df, 
        lw = 2
        )

    ax.set(
        ylim = [-1, 7], 
        ylabel = b.y_label('K')
        )
    
    ax.axhline(df.max(), linestyle = '--')
    ax.axhline(df.min(), linestyle = '--')
    
    
def plot_ratio(ax, df):
    
    ax.plot(
        df, 
        lw = 2
        )
    
    ax.axhline(1, linestyle = '--')
    
    ax.set(
        ylim = [0.9, 1.05], 
        ylabel = b.y_label('ratio')
        )
    
def plot_gravity(ax, df):
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    ax.plot(
        df.index, 
        b.smooth2(df, 20), 
        lw = 2
        )
    
    ax.set(
        ylim = [0, 30], 
        ylabel = b.y_label('gravity_L')
        )
     
    
def plot_vzp(ax, df):
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    ax.plot(
        df.index, 
        b.smooth2(df, 20), 
        lw = 2
        )
    
    ax.set(
        ylim = [-10, 90], 
        ylabel = b.y_label('vp')
        )
    
    ax.axhline(df.max(), linestyle = '--')
    ax.axhline(df.min(), linestyle = '--')
    
def plot_wind(ax, df):
    
    ax.scatter(
        df.index, df, 
        s = 30,
        alpha = 0.4, 
        color = 'gray'
        )
    
    ax.plot(
        df.index, 
        b.smooth2(df, 20), 
        lw = 2
        )
    
    ax.set(
        ylim = [-10, 15], 
        ylabel = b.y_label('mer_perp')
        )
    
    
    ax.axhline(df.max(), linestyle = '--')
    ax.axhline(df.min(), linestyle = '--')


def plot_annual_GRT(
        site = 'saa', 
        col = 'e_f'
        ):

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 6, 
        figsize = (12, 16), 
        )
    
    plt.subplots_adjust(hspace = 0.1)
      
    df = rt.load_grt(site)

    plot_ratio(ax[0], df['ratio'])
    plot_vzp(ax[1], df['vp'])
    plot_wind(ax[2], df['mer_perp'])
    plot_grad(ax[3], df['K'])
    
    plot_gravity(ax[4], df['ge'] / df['nui'])
    
    plot_gamma(ax[5], df['gamma'])
    
    ax[0].set(title = df.columns.name)
    
    for i, ax in enumerate(ax.flat):
        
        l = b.chars()[i]
        ax.text(
            0.02, 0.8, f'({l})', 
            transform = ax.transAxes
            )
    
    return fig


fig = plot_annual_GRT(site = 'saa')


FigureName = 'annual_grt_parameters'

# fig.savefig(b.LATEX(FigureName), dpi = 400)

# df = rt.load_grt()

# df.columns