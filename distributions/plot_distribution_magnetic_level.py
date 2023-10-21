
    
     # letter = b.chars()[i]
     
     # ax[i].text(
     #     0.02, 0.87, 
     #     f"({letter}) {titles[i]} ({c} events)", 
     #     transform = ax[i].transAxes
     #     )
     

def plot_single_distribution(
        ax,
        df, 
        step = 0.2, 
        gamma = 'night',
        quiet_level = 4
        ):
    

    vmin, vmax = df[gamma].min(), df[gamma].max()
    
    vmin, vmax = floor(vmin), ceil(vmax)
    
        
    labels = [f'$Kp \\leq$ {quiet_level}', 
              f'$Kp >$ {quiet_level}']
    
    datasets = ev.kp_levels(
        df, 
        level = quiet_level
        )
    
    
    count = []
    nums = []
    for i, ds in enumerate(datasets):
                
        index = i + 1

        c = plot_distribution(
            ax, 
            ds,
            label = f'({index}) {labels[i]}',
            step = step, 
            col_gamma = 'night',
            col_epbs = 'epb'
            )
        
        nums.append(c)
        
        count.append(f'({index}) {c} events')
        
    
    infos = ('EPB occurrence\n' +
             '\n'.join(count))
        
    ax.text(
        0.79, 0.2, infos, 
        transform = ax.transAxes
        )
        
    ax.set(
        xlim = [vmin - step, vmax],
        xticks = np.arange(vmin, vmax, step * 2),
        ylim = [-0.2, 1.3],
        yticks = np.arange(0, 1.25, 0.25),
        )

    return sum(nums)