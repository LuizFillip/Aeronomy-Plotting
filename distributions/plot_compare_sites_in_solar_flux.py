import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 
 




    

def plot_compare_sites_in_solar_flux(df):
    fig, ax = plt.subplots(
        dpi = 300, 
        nrows = 2,
        sharex = True,
        figsize = (12, 12)
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    df_index = c.DisturbedLevels(df)
    
    limit = c.limits_on_parts(df['f107a'], parts = 2)
    
    F107_labels = df_index.solar_labels(limit)
    
    datasets = [sep_data(df, 'saa'), sep_data(df, 'jic')]

    titles = [ 'São Luís', 'Jicamarca']
    
    total_epb = []
    total_day = []
    
    
    for i, ds in enumerate(datasets):
        index = i + 1
        label = f'({index}) {titles[i]}'
        data, epbs = pl.plot_distribution(
                ax[0], 
                ds,
                parameter = 'gamma',
                label = label,
                axis_label = True,
                drop_ones = True
            )
        
        days = pl.plot_histogram(
                ax[1], 
                data, 
                index, 
                label =  label,
                parameter = 'gamma',
                axis_label = True
            )
        
        total_epb.append(epbs)
        total_day.append(days)
        
        ax[1].set(ylim = [0, 600])
        ax[0].set(xlabel = '')
        
        
    ax[0].legend(loc = 'upper center', ncol = 2)
    ax[1].legend(loc = 'upper center', ncol = 2)
    
    pl.plot_infos(ax[0], total_epb)
    pl.plot_infos(ax[1], total_day, epb_title = False)
        
    return fig 

df = c.concat_sites()

# df = df.loc[~df.index.year.isin([2014, 2015, 2020])]

fig = plot_compare_sites_in_solar_flux(df)