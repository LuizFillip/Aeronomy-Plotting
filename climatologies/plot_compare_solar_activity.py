import matplotlib.pyplot as plt 
import RayleighTaylor as rt 
import base as b 


def plot_year(df, ax, col, year = 2019):
    ds = df.loc[df.index.year == year]
    ds.index = ds.index.day_of_year
    ds[col].plot(ax = ax, label = year)
    ax.legend()
    # b.format_month_axes(ax)
    
    
def plot_compare_solar_activity(
        col = 'K', 
        site = 'saa'
        ):
    

    fig, ax = plt.subplots(
        sharey = True,
        sharex = True,
        dpi = 300, 
        nrows = 2,
        figsize = (14, 8), 
        )
    
   
    df = rt.load_grt(site)

   
    plot_year(df, ax[0], col, year = 2013)
    plot_year(df, ax[1], col, year = 2019)
    
    
    
    
plot_compare_solar_activity()


