import plotting as pl 
import matplotlib.pyplot as plt 

lon = 20
df = run_in_days(lon = lon) 

dn = dt.datetime(2015, 12, 20, 22)

ds = sel_lon(load_madrigal(dn), lon = lon).set_index('mlat')



def plot_magnetic_tec(df, ds):
    b.sci_format(fontsize = 25)
    fig, ax = plt.subplots(
        dpi = 300, 
        figsize = (12, 6)
        )
    
    ax.plot(ds['tec'], lw = 2, label = 'Storm-time')
    
    avg = df.mean(axis = 1)
    std = df.std(axis = 1)
    
    ax.plot(avg, lw = 2, color = 'purple', label = 'Quiet-time')
    ax.fill_between(
        avg.index, 
        avg - std, 
        avg + std, 
        color = "purple", 
        alpha = 0.3
        )
    
    ax.set(
           xlabel = 'Magnetic latitude (°)',
           ylabel = 'TEC (TECU)',
           xlim = [-30, 30], 
           ylim = [0, 100],
           xticks = np.arange(-30, 30, 5)
           )
    
    ax.legend(loc = 'upper center', 
              ncol = 2)
    
    ax.axvline(0, linestyle = ':')
    
    return fig 
    
   

fig =  plot_magnetic_tec(df, ds)


def main():
    
    FigureName = 'latitude_tec_profile'
    
    path_to_save = 'G:\\Meu Drive\\Papers\\Case study - 21 december 2015\\June-2024-latex-templates\\'
    
    
    fig.savefig(path_to_save + FigureName, dpi = 400)
# import apexpy 

# apex = apexpy.Apex(date = 2015)

# apex.convert(
#     -2, -50, 
#     'geo', 'qd', height = 350
#     )
