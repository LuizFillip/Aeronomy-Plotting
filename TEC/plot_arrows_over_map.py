import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches

def add_red_arrows_on_panels(
        axes, arrows_by_panel, *,
        crs= ccrs.PlateCarree(),         # normais
        dy=3,                
        color="crimson",
        lw=2.0,
        arrowstyle="-|>"
    ):

    for (r, c), items in arrows_by_panel.items():
        ax = axes[r][c]
        for item in items:
            x, y = item

            # ann_kw = dict(
            #     xy=(x, y),
            #     xytext=(x, y + 4), 
            #     arrowprops=dict( color = color,
            #      lw = 4,
            #      arrowstyle='->'), 
            #      transform = ax.transData, 
            #      fontsize = 40, 
            #      color = 'r'
            #  )
            
            arrow1 = mpatches.FancyArrowPatch(
                (x, y + 10), (x, y),
                mutation_scale=40,
                color="red",
                transform=ax.transData
                )
            
            ax.add_patch(arrow1)
            
    
def plot_test():
    fig, axes = plt.subplots(
        3, 4, 
        figsize=(9, 7),
        subplot_kw = {'projection': ccrs.PlateCarree()},
        constrained_layout = True
        )
   
    # (Exemplo) configurar mapas rapidamente
    for ax in axes.ravel():
        ax.set_extent([-80, -30, -40, 10])
        ax.coastlines(linewidth=0.5)
    
    # Diga onde colocar as setas: (linha, coluna) -> lista de (lon, lat)
    arrows = {
        (0, 2): [(-50, -5), (-44, -5)], 
        (0, 3): [(-50, -5), (-40, -8), (-55, -7)],# duas setas no painel (a3)
        (2, 2): [(-60, -5), (-50, -5)],             # (c3)
        (2, 3): [(-63, -8), (-57, -5), (-45, -5)]  # seta com dy customizado
    }
    
    # add_red_arrows_on_panels(axes, arrows, crs=ccrs.PlateCarree(), dy=3, color="red")
    
    x_tail, y_tail = -50, -5 + 10
    x_head, y_head = -50, -5 
    
    # no primeiro eixo (coordenadas normalizadas do eixo)
    arrow1 = mpatches.FancyArrowPatch(
        (x_tail, y_tail), (x_head, y_head),
        mutation_scale=30,
        color="red",
        transform=axes[0, 0].transData
        )
    
    axes[0, 0].add_patch(arrow1)
    
    plt.show()

