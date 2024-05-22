


def plot_separe_in_solar_activity():

    fig, ax = plt.subplots(
        figsize = (14, 12),
        dpi = 300,
        sharex = True,
        sharey = True,
        nrows = 2, 
        ncols = 2
        )
    
    plt.subplots_adjust(wspace = 0.05, hspace = 0.15)
    
    df = c.load_results('saa', eyear = 2022)
    
    level = c.limits_on_parts(df['f107a'], parts = 2)
    
    df_index = c.DisturbedLevels(df)
    
    F107_labels = df_index.solar_labels(level)
     
    total_epb = []
    total_day = []
    colors = ['k', 'b']
    
    for i, ds in enumerate(df_index.F107(level)):
        
        label =  f'{F107_labels[i]}'
        
        plot_seasonal_gamma_vs_pre(
            ax, ds, 
            col = 'gamma', 
            color = colors[i], 
            index = i * 0.1, 
            label = label
            )
    
    plot_labels(fig, fontsize = 30)
    
    return fig