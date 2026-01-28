def savefig(fig, FigureName):
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Suppression_stastistical\\June-2024-latex-templates\\'
    
    fig.savefig(path_to_save + FigureName, dpi = 300)
    
    return None 
    
    
def legend_for_sym_h(
        ax, 
        quiet = False, 
        loc = 'upper right',
        ncol = 1, par = 'Dst', 
        fontsize = 18
        ):
    
    legend_labels = {
        'weak': '-50 $<$ SYM-H $\leq$ -30 nT',
        'moderate': '-100 $<$ SYM-H $\leq$ -50 nT',
        'intense': 'SYM-H $\leq$ -100 nT'
    }
    
    if quiet:
        legend_labels['quiet'] = 'SYM-H $>$ -30 nT'
    
    handles, labels = ax.get_legend_handles_labels()
    
    ax.legend(
        handles, [legend_labels[l] for l in labels],
        loc = loc,
        fontsize = fontsize,
        title_fontsize = 20, 
        ncol = ncol
    )
    
    return None 
