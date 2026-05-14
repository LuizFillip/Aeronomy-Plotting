import numpy as np
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
from mpl_toolkits.mplot3d import Axes3D

# -------------------------
# grade
# -------------------------
lon = np.linspace(40, 120, 150)
lat = np.linspace(-30, 40, 120)

LON, LAT = np.meshgrid(lon, lat)

# superfície exemplo
Z = 450 * np.exp(
    -((LON - 70)**2 / 180 + (LAT - 5)**2 / 120)
)

# -------------------------
# figura
# -------------------------
fig = plt.figure(figsize=(10, 8), dpi=300)
ax = fig.add_subplot(111, projection='3d')

# -------------------------
# superfície
# # -------------------------
# surf = ax.plot_surface(
#     LON,
#     LAT,
#     Z,
#     cmap='jet',
#     edgecolor='k',
#     linewidth=0.25,
#     antialiased=True
# )

# -------------------------
# contornos no plano
# -------------------------
ax.contour(
    LON,
    LAT,
    Z,
    zdir='z',
    offset=0,
    levels=10,
    cmap='jet',
    linewidths=1.2
)

# # -------------------------
# # plano inferior
# # -------------------------
# ax.plot_surface(
#     LON,
#     LAT,
#     np.zeros_like(Z),
#     color='lightcyan',
#     alpha=0.4,
#     linewidth=0
# )

# -------------------------
# mapa no plano z=0
# -------------------------
shpfilename = shpreader.natural_earth(
    resolution='110m',
    category='physical',
    name='coastline'
)

reader = shpreader.Reader(shpfilename)

# limites
lon_min, lon_max = -90, -30
lat_min, lat_max = -70, 10

for geom in reader.geometries():

    if geom.geom_type == 'LineString':

        coords = np.array(geom.coords)

        x = coords[:, 0]
        y = coords[:, 1]

        mask = (
            (x >= lon_min) & (x <= lon_max) &
            (y >= lat_min) & (y <= lat_max)
        )

        if np.any(mask):

            ax.plot(
                x[mask],
                y[mask],
                zs=0,
                zdir='z',
                color='darkgreen',
                linewidth=0.7
            )

    elif geom.geom_type == 'MultiLineString':

        for line in geom.geoms:

            coords = np.array(line.coords)

            x = coords[:, 0]
            y = coords[:, 1]

            mask = (
                (x >= lon_min) & (x <= lon_max) &
                (y >= lat_min) & (y <= lat_max)
            )

            if np.any(mask):

                ax.plot(
                    x[mask],
                    y[mask],
                    zs=0,
                    zdir='z',
                    color='darkgreen',
                    linewidth=0.7
                )
# -------------------------
# eixos
# -------------------------
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.set_zlim(0, 600)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude (km)')

ax.view_init(elev=30, azim=-135)

plt.tight_layout()
plt.show()