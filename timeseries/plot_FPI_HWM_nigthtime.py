
import matplotlib.pyplot as plt
import settings as s
from common import plot_terminators


fig, ax = plt.subplots(
    sharey = True, sharex = True,
    nrows = 2, dpi = 400, 
    figsize = (12, 8)
    )
wd = join_hwm_fpi()

ds = wd[wd.index < dt.datetime(2013, 1, 10)].copy()

ax[0].plot(ds["mer"])
ax[1].plot(ds["zon"])

ax[0].set(ylabel = "Vento meridional (m/s)")
ax[1].set(ylabel = "Vento zonal (m/s)")

s.format_time_axes(
        ax[1], 
        hour_locator = 12, 
        day_locator = 1, 
        tz = "UTC"
        )






for ax in ax.flat:
    plot_terminators(ax, ds)