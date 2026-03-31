import pandas as pd


def plot_electron_density(ax, path="models/temp/map_iri.txt"):
    """Plota densidade eletrônica (se você quiser sobrepor ao mapa)."""
    df = pd.read_csv(path, index_col=0)

    df = pd.pivot_table(df, columns="0", index="1", values="2")
    vls = df.values * 1e-12

    img = ax.contourf(df.columns, df.index, vls, 50, cmap="rainbow", transform=ccrs.PlateCarree())

    ticks = np.arange(0, 2, 0.1)
    b.colorbar(img, ax, ticks, label=r"$N_e (\times 10^{12}\, m^{-3})$")
    return img

def plot_gnss_receivers(ax, year, *, lon_window=(-50, -40), marker_kwargs=None):
    """Plota estações GNSS dentro de uma janela de longitude."""
    if marker_kwargs is None:
        marker_kwargs = dict(s=150, marker="^", color="k", transform=ccrs.PlateCarree())

    lons, lats = gg.stations_coordinates(year, distance=10)

    # recorte por janela
    mask = (lons > lon_window[0]) & (lons < lon_window[1])
    ax.scatter(lons[mask], lats[mask], label="GNSS receivers", **marker_kwargs)

    return ax
 