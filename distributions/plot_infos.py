
    
def fmt(index, value):
    return f'({index}) {value} events'
def plot_infos(
        ax, 
        values, 
        title = 'EPB occurrence',
        x = 0.75, 
        y = 0.25
        ):
    
    out = []
    for i, val in enumerate(values):
        out.append(fmt(i + 1, val))
        
    infos = (f'{title}\n' + '\n'.join(out))
        
    ax.text(
            x, y, 
            infos, 
            transform = ax.transAxes
            )


def streval(index, values):
    return [fmt(index, value) for value in values]