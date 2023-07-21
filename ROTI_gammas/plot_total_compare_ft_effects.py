import RayleighTaylor as rt
import settings as s 
import matplotlib.pyplot as plt


def plot_ft_nighttime(ds):

    lb = rt.EquationsFT()
    
    
    fig, ax = plt.subplots(
        figsize = (12, 8), 
        sharey = True, 
        sharex = True,
        nrows = 2
        )
    
    plt.subplots_adjust(hspace = 0.05)
    
    
    labels= [lb.drift, lb.gravity, 
             lb.winds + ' ($\\parallel$ to B)', 
             lb.complete]
    
    
    ax[0].plot(rt.gammas_integrated(ds), 
               label = labels)
    
    ax[0].legend(ncol = 2, loc = 'upper center', 
                 bbox_to_anchor = (.5, 1.5))
    
    ax[1].plot(rt.gammas_integrated(ds, rc = True))
    
    names = ['$R_T = 0$', '$R_T \\neq  0$']
    
    s.add_lines_and_letters(ax, names = names)
    
    s.format_time_axes(ax[1])
    
    for ax in ax.flat:
        ax.set(ylabel = lb.label, 
               ylim = [-40, 40])

def plot_interval_integrated(ds):

    fig, ax = plt.subplots(
        figsize = (12, 4), 
        dpi = 300)
    
    lbs = rt.EquationsFT(r = False)
    names = [lbs.drift, lbs.gravity, 
             lbs.winds + ' ($U_L^P \\perp$ to B)', 
             lbs.complete]
    
    cols = ['vz', 'g', 'u_perp', 'all_perp']
    ax.plot(ds[cols],
            label = names)
    
    
    ax.legend(
        bbox_to_anchor = (.5, 1.5),
        loc = 'upper center', 
        ncol = 2)
    
    ax.set(ylabel = lbs.label, 
           ylim = [-2, 6]
           )
    
    for col in cols:
        ax.scatter(ds[col].idxmax(), 
                   ds[col].max(), 
                   label = 'maximum value'
                   )
        
    s.format_time_axes(ax)
    
    E = sun_terminator(dn, twilight_angle = 12)
    F = sun_terminator(dn, twilight_angle = 18)
    ax.axvline(F)
    ax.axvline(E, color = 'blue')
    ax.axvspan(F, 
               F + dt.timedelta(minutes = 30),
               alpha = 0.5, color = "gray")