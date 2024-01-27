
    
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


seasons_keys = {
      0: 'March equinox',
      1: 'June solstice',
      2: 'September equinox',
      3: 'December solstice'
      }

# seasons_keys = {
#       'March equinox': 3,
#       'June solstice': 6,
#       'September equinox': 9,
#       'December solstice': 12
#       }
