import matplotlib.pyplot as plt
from common import load_by_time
import RayleighTaylor as rt
import settings as s


def plot_annual_variation(df, integrated = True):

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        nrows = 2, 
        figsize = (14, 8), 
        )
    
    plt.subplots_adjust(hspace = 0.5)
    
    cols = [
            ['vz', 'g', 'u_perp', 'u_parl'],
            ['all_perp', 'all_parl']
            ]
    
    if integrated:
        lbs = rt.EquationsFT(r = False)
        names = [
            [lbs.drift, lbs.gravity, 
              lbs.winds + ' ($U_L^P \\perp$ to B)', 
              lbs.winds + ' ($U_L^P \\parallel$ to B)'], 
            ['$U_L^P \\perp$ to B', '$ U_L^P \\parallel$ to B']

                  ]
    else:
        lbs = rt.EquationsRT(r = False)
        names = [
            [lbs.drift, lbs.gravity, 
              lbs.winds + ' ($u_n \\perp$ to B)', 
              lbs.winds + ' ($u_n \\parallel$ to B)'], 
            ['$u_n \\perp$ to B', '$u_n \\parallel$ to B']

                  ]
    

    for i, col in enumerate(cols):
    
        ax[i].plot(df[col], label = names[i])
        ax[i].set(
            #ylim = [-5, 25], 
            xlim = [df.index[0], df.index[-1]], 
            ylabel = lbs.label
            )
        
        if i == 1:
            title = lbs.complete
        else:
            title = ''
        
        
    s.axes_month_format(ax[1])
    
    ax[0].legend(loc = 'upper center',
        bbox_to_anchor = (.5, 1.9),
        title = title, ncol = 2)
    ax[1].legend(title = title, ncol = 2, 
                 loc = 'upper center',
                     bbox_to_anchor = (.5, 1.5),)
        
    ax[1].set(xlabel = "Months (2013)")
    
    s.add_lines_and_letters(ax)
    return fig
def main():
    import datetime as dt
    infile = 'database/Results/maximus/integrated_2013_dusk.txt'
    
    df = load_by_time(infile, dn = None)
    
    df = df.loc[df['all_perp'] < 20]
    fig = plot_annual_variation(df, integrated = True)
    
    # df.loc[(df.index >= dt.datetime(2013, 3, 12)) &
    #        (df.index <= dt.datetime(2013, 3, 22))].plot()
    
    # df