import matplotlib.pyplot as plt
import datetime as dt
from common import load_by_time, plot_roti, sun_terminator
import RayleighTaylor as rt
import settings as s
from GEO import dawn_dusk




fig, ax = plt.subplots(
    sharex = True,
    dpi = 300, 
    nrows = 3, 
    figsize = (12, 10), 
    )

plt.subplots_adjust(hspace = .0)



infile = "database/Results/local_gammas/2013.txt"
dn = dt.datetime(2013, 1, 1, 20)

df = load_by_time(infile, dn)

cols = ['all_perp', 'all_parl']

seps = ['vz', 'g', 'u_perp', 'u_parl']

lbs = rt.EquationsRT(r = True)
names1 = [lbs.drift, lbs.gravity, 
         lbs.winds + ' ($\\perp$ to B)', 
         lbs.winds + ' ($\\parallel$ to B)']


for i, col in enumerate(seps):
    ax[0].plot(df[col], label = names1[i])

ax[0].set(ylabel = lbs.label, 
          ylim = [-5, 20])
ax[0].legend(
    loc = 'upper right', 
    ncol = 2
    )

names = ['$\\perp$ to B', 
         '$\\parallel$ to B']

for j, row in enumerate(cols):
    ax[1].plot(df[row], label = names[j])
    
ax[1].set(ylabel = lbs.label, 
          ylim = [-5, 20])
ax[1].legend(
    title = lbs.complete, 
    loc = 'upper right', 
    ncol = 2
    )

plot_roti(ax[2], df)
    
da, du = dawn_dusk(dn)


for i, ax in enumerate(ax.flat):

    
    
    ax.axvline(du)
    ax.axvline(sun_terminator(dn), color = 'blue')
    ax.axvspan(du, 
               du + dt.timedelta(minutes = 30),
               alpha = 0.5, color = "gray")
    ax.axhline(0, linestyle = '--')
    letter = s.chars()[i]
    ax.text(0.03, 0.82, f"({letter})", 
            transform = ax.transAxes)
    
    
    
    
plt.show()
