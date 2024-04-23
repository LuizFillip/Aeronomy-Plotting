import core as c
import matplotlib.pyplot as plt
import base as b 


b.config_labels()

def plot_steam_occurrences(
        df, 
        parameter = 'gamma', 
        translate = True, 
        percent = 100
        ):
        
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (16, 8)
        )
    
    ds = df.loc[df['observed'] == df['pred1']]

    ax.stem(ds.index, 
            ds['predict'] * percent, 
            linefmt='k-',
            label = 'True'
            )
    
    ds = df.loc[df['observed'] != df['pred1']]

    ax.stem(ds.index, 
            ds['predict'] * percent,
            linefmt='r-',
            label = 'False', 
            )
    
    
    ax.legend(
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.1),
        loc = "upper center"
        )
    
    ax.axhline(percent * 0.5, color = 'k', lw = 2, linestyle = '--')
    
    
    if translate:
        ylabel = 'Occurrence/probability (\%)'
        with_epb = 'With EPB'
        witout_epb = 'Without EPB'
    else:
        ylabel = 'Ocorrência/probabilida (\%)'
        with_epb = 'Com EPB'
        witout_epb = 'Without EPB'
        
    ax.set(
            xlim = [df.index[0], df.index[-1]],
           ylabel = ylabel
           )
    
    ax.text(1.01, 0.25, with_epb, transform = ax.transAxes)
    ax.text(1.01, 0.75, witout_epb, transform = ax.transAxes)
    
    if parameter == 'gamma':
        fig.suptitle('Prediction for 2023', y = 1.05)
    else:
        fig.suptitle('$V_p$', y = 1.05)
        
    b.format_month_axes(ax, translate = translate)
    return fig


def main():
    
    parameter = 'gamma'
    
    df  = c.forecast_epbs(parameter= parameter).data 
    
    fig = plot_steam_occurrences(df, parameter)
    
    plt.show()





main()