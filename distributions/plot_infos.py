import base as b
import matplotlib.pyplot as plt 


def fmt(index, value):
    return f'({index}) {value} '


def titles_infos(parameter):
    if parameter == 'gamma':
        return ['EPBs occurrence', '$\gamma_{RT}$ total']
    else:
        return ['EPBs occurrence', '$V_P$ total']
      

def plot_infos_in_distribution(
        ax, 
        values, 
        x = 0.70, 
        y = 0.20,
        translate = False,
        title = '$V_P$', 
        offset_y = 0.15, 
        fontsize = 30
        ):
    
    if title == 'gamma':
        title_p = '$\gamma_{RT}$ total'
    elif title == 'vp':
        title_p = '$V_P$ total'
    else:
        if translate:
            title_p = 'Ocorrência de BPEs'
        else:
            title_p = 'EPBs occurrence'
        
    
    if translate:
        event = 'eventos'
    else:
        event = 'events'
    
    colors = ['k', 'b', '#00B945']
    for i, val in enumerate(values):
        
        info = fmt(i + 1, val) + event
        
        if i == 0:
            
            ax.text(
                x, y, f'{title_p}\n{info}', 
                transform = ax.transAxes, 
                color = colors[i], 
                fontsize = fontsize
                ) 
        else:
            ax.text(
                x, y - offset_y * i,
                f'{info}', 
                transform = ax.transAxes, 
                color = colors[i], 
                fontsize = fontsize
                ) 
    return None 

    

def plot_events_infos(
        ax, row, LIST, 
        translate = True, 
        parameter = 'gamma',
        x = 0.68, 
        y = 0.2, 
        fontsize = 30
        ):
    
    titles = ['epb', parameter]
    for col, total in enumerate(LIST):  
                
        if col == 0:
            if translate:
                f = 0
            else:
                f = 0.07
        else:
            f =  0.1
            
        plot_infos_in_distribution(
            ax[row, col], 
            total, 
            x = x + f, 
            y = y,
            translate = translate,
            title = titles[col], 
            fontsize = fontsize
            )
                
        ax[0, col].legend(
            ncol = 3, 
            bbox_to_anchor = (0.5, 1.3),
            loc = "upper center", 
            columnspacing = 0.2,
            labelcolor = 'linecolor'
            )
        
        l = b.chars()[col]
        
        ax[0, col].text(
            -0.1, 1.25, f'({l})', 
            fontsize = 35,
            transform = ax[0, col].transAxes
            )
        
    return None 

def FigureLabels(
        fig, 
        translate = False, 
        parameter = 'gamma',
        fontsize = 30
        ):
    
    if parameter == 'vp':
        xlabel = b.y_label('vp')
        x = 0.47
    else:
        xlabel = b.y_label('gamma')
        x = 0.45
        
    if translate:
        ylabel1 = "Probabilidade de ocorrência (\%)"
        ylabel2 = "Número de eventos"
       
    else:
        ylabel1 = "EPB occurrence probability (\%)"
        ylabel2 = "Number of events"
        
    fig.text(
        0.07, 0.31, 
        ylabel1, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.49, 0.39, 
        ylabel2, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        x, 0.07, 
        xlabel, 
        fontsize = fontsize
        )
    return None 

def plot_epbs_number(ax, data, color = 'k'):
    if color == 'k':
        offset = -12
        
    else:
        offset = 5
    for x, y, z in data[['start', 'rate', 'epbs']].values:
        
        ax.text(x - 0.05, (y *100) + offset, 
                int(z),
                transform = ax.transData, 
                color = color)
        
    return None 
        
        
def axes_for_seasonal_plot(
        nrows = 4, 
        figsize = (20, 14)):
    
    fig, ax = plt.subplots(
          ncols = nrows // 2, 
          nrows = nrows,
          figsize = figsize, 
          dpi = 300, 
          sharex = True, 
          sharey = 'col'
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.2
        )
    
    return fig, ax 