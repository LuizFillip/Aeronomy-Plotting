import base as b
    
def fmt(index, value):
    return f'({index}) {value} '

def plot_infos(
        ax, 
        values, 
        x = 0.75, 
        y = 0.25,
        translate = False,
        epb_title = True
        ):
    
    if isinstance(translate, str):
        title = translate
        event = 'eventos'
    
    if epb_title:
        if translate:
            title = 'Ocorrência de EPBs'
            event = 'eventos'
        else:
            title = 'EPB occurrence'
            event = 'events'
    else:
        title = '$\gamma_{RT}$ total'
        event = 'events'
    
    out = []
    for i, val in enumerate(values):
        out.append(fmt(i + 1, val) + event)
        
    infos = (f'{title}\n' + '\n'.join(out))
        
    ax.text(x, y, infos, transform = ax.transAxes)


    return None 

def legend(ax):
    
    ax.legend(
        ncol = 2, 
        bbox_to_anchor = (0.5, 1.3),
        loc = "upper center"
        )
def plot_events_infos(ax, row, LIST):
    

    for col, total in enumerate(LIST):    
        
        plot_infos(
            ax[row, col], 
            total, 
            x = 0.55, y = 0.2,
            translate = True
            )
        
        legend(ax[0, col])
        l = b.chars()[col]
        
        ax[0, col].text(
            -0.1, 1.2, f'({l})', 
            fontsize = 35,
            transform = ax[0, col].transAxes
            )
        