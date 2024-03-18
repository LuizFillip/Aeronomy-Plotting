import matplotlib.pyplot as plt 
import base as b
import core as c

b.config_labels(fontsize = 25)

def plot_annualy_kp_level(
        df,
        kp_level = 3,
        translate = True
        ):
    
    if translate:
        ylabel = 'Número de casos'
    else:
        ylabel = 'Number of nights'
        
    
    fig, ax = plt.subplots(
        nrows = 2, 
        dpi = 300, 
        sharex = True,
        figsize = (12, 8)
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    levels = c.kp_levels(
            df, 
            level =  kp_level, 
            kp_col = 'kp'
            )

    names = [
        f'$Kp \\leq$ {kp_level}', 
        f'$Kp >$ {kp_level}'
        ]
    
    for i, dataset in enumerate(levels):
        
        ds = c.count_occurences(dataset).year
     
        ds.plot(
            kind = 'bar',
            ax = ax[i], 
            legend = False, 
            edgecolor = 'k'
            )
    
        ax[i].set(
            ylim = [0, 200],
            ylabel =  ylabel,
            xlabel = 'Years'
            )
        
        epb_count = int(dataset['epb'].sum())
        
        l = b.chars()[i]
        n = names[i]
        info = f'({l}) {n} ({epb_count} EPBs events)'
        
        ax[i].text(
            0.02, 0.85, info, 
            transform = ax[i].transAxes
            )
        
    plt.xticks(rotation = 0)
#
    return fig

df = c.concat_results('saa')
# fig = plot_annualy_kp_level(df)


# fig.savefig(b.LATEX('kp_annual_variation', folder = 'bars'))

ds = c.non_and_occurrences(df).yearly()

ds