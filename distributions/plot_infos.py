
    
def fmt(index, value):
    return f'({index}) {value} '

def plot_infos(
        ax, 
        values, 
        x = 0.75, 
        y = 0.25,
        translate = False
        ):
    
    if isinstance(translate, str):
        title = translate
        event = 'eventos'
        
    if translate:
        title = 'Ocorrência de EPBs'
        event = 'eventos'
    else:
        title = 'EPB occurrence'
        event = 'events'
    
    out = []
    for i, val in enumerate(values):
        out.append(fmt(i + 1, val) + event)
        
    infos = (f'{title}\n' + '\n'.join(out))
        
    ax.text(
            x, y, 
            infos, 
            transform = ax.transAxes
            )


