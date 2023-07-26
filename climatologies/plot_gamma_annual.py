import matplotlib.pyplot as plt
from common import load_by_time
import RayleighTaylor as rt


fig, ax = plt.subplots(
    sharex = True,
    dpi = 300, 
    nrows = 1, 
    figsize = (12, 6), 
    )

# plt.subplots_adjust(hspace = 0.5)

infile = 'database/Results/maximus/local_2013_dusk.txt'

df = load_by_time(infile, dn = None)

ax.plot(df['all_perp'], label = 'Local quantities')

# infile = 'database/Results/maximus/integrated_2013_dusk.txt'
infile = 'integrated_2013_dusk.txt'

df = load_by_time(infile, dn = None)

ax.plot(df['all_perp'], label = 'Integraded quantities')
import settings as s 

lbs = rt.EquationsRT(r = False)

s.axes_month_format(ax)

ax.set(ylabel = lbs.label)
ax.legend()