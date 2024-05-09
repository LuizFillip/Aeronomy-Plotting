import base as b
    
def fmt(index, value):
    return f'({index}) {value} '

def plot_infos(
        ax, 
        values, 
        x = 0.70, 
        y = 0.20,
        translate = False,
        epb_title = True, 
        offset_y = 0.15
        ):
    
    if isinstance(translate, str):
        title = translate
        
    if translate:
        title = 'Ocorrência de EPBs'
        event = 'eventos'
    else:
        title = 'EPB occurrence'
        event = 'events'
        
        
    if not epb_title:       
        title = '$\gamma_{RT}$ total'
    

    for i, val in enumerate(values):
        
        info = fmt(i + 1, val) + event
        
        if i == 0:
            
            ax.text(
                x, y, f'{title}\n{info}', 
                transform = ax.transAxes, 
                color = 'k'
                ) 
        else:
            ax.text(
                x, y - offset_y, f'{info}', 
                transform = ax.transAxes, 
                color = 'b') #'#0C5DA5'

    return None 

    

def plot_events_infos(
        ax, row, LIST, 
        translate = True, 
        epb_title = True,
        x = 0.68, 
        y = 0.2
        ):
    

    for col, total in enumerate(LIST):    
        
        if col == 0:
            epb_title = True
            f = 0
        else:
            epb_title = False
            f =  0.1
            
        plot_infos(
            ax[row, col], 
            total, 
            x = x + f, 
            y = y,
            translate = translate,
            epb_title = epb_title
            )
                
        ax[0, col].legend(
            ncol = 2, 
            bbox_to_anchor = (0.5, 1.3),
            loc = "upper center", 
            labelcolor = 'linecolor'
            )
        l = b.chars()[col]
        
        ax[0, col].text(
            -0.1, 1.2, f'({l})', 
            fontsize = 35,
            transform = ax[0, col].transAxes
            )

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
        ylabel2 = "Frequência de ocorrência"
       
    else:
        ylabel1 = "EPB occurrence probability (\%)"
        ylabel2 = "Frequency of occurrence"
        
    fig.text(
        0.07, 0.33, 
        ylabel1, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        0.49, 0.37, 
        ylabel2, 
        fontsize = fontsize, 
        rotation = 'vertical'
        )
    
    fig.text(
        x, 0.07, 
        xlabel, 
        fontsize = fontsize
        )