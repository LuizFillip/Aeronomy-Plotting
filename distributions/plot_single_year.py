import matplotlib.pyplot as plt
import base as b
import core as c 
import plotting as pl 
 
b.config_labels()


def plot_single_year(ds, col = 'gamma2'):

    fig, ax = plt.subplots(
        figsize = (12, 12),
        dpi = 300,
        nrows = 2,
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.1)
        
    # for index, year in enumerate([2015, 2019]):
    
    index = 0

    data, epbs = pl.plot_distribution(
            ax[0], 
            ds,
            parameter = col,
            label = year,
            axis_label = True,
            drop_ones = False,
            translate = True
        )
    
   
    # print(data)
    days = pl.plot_histogram(
            ax[1], 
            data, 
            index, 
            label = year, 
            parameter = col,
            axis_label = True,
            translate = True
        )
    
    ax[index].legend()
    ax[0].set(xlabel = '', ylim = [-10, 110])
            
# plot_single_year(2019,  col = 'gamma2')

# year = 2019
# ds = c.local_results(year)


# site = 'jic'
# df = c.concat_results(site)
# df = df.loc[df.index.year == 2019]
# # plot_single_year(df, col = 'vp')


# # 

# df['gamma'].plot()