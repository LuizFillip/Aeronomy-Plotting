import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import base as b
import GEO as gg

 

def occurrence_percent_grid(nl_season, lon_bins, lat_bins):
    
    # Se não houver eventos na estação
    if nl_season.empty:
        return pd.DataFrame(
            0.0,
            index=lat_bins[:-1],
            columns=lon_bins[:-1],
        )

    df = nl_season.copy()

    # centro do núcleo
    df["lon"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat"] = (df["lat_min"] + df["lat_max"]) / 2

    df["lon_bin"] = pd.cut(df["lon"], lon_bins,
                           labels=lon_bins[:-1], include_lowest=True)
    df["lat_bin"] = pd.cut(df["lat"], lat_bins,
                           labels=lat_bins[:-1], include_lowest=True)

    df = df.dropna(subset=["lon_bin", "lat_bin"])

    # total de imagens na estação
    n_total = nl_season.index.unique().size

    if n_total == 0:
        return pd.DataFrame(
            0.0,
            index=lat_bins[:-1],
            columns=lon_bins[:-1],
        )

    # conta no máximo 1 ocorrência por célula por timestamp
    hits = (
        df.reset_index(names="time")
          .drop_duplicates(subset=["time", "lon_bin", "lat_bin"])
          .groupby(["lat_bin", "lon_bin"])
          .size()
          .rename("n_hits")
          .reset_index()
    )

    hits["occ_pct"] = 100.0 * (hits["n_hits"] / n_total)

    grid = hits.pivot(
        index="lat_bin", 
        columns="lon_bin", values="occ_pct")
    
    # print(grid)
    # garante grade completa 0–100
    grid = grid.reindex(
        index=lat_bins[:-1],
        columns=lon_bins[:-1]
        ).fillna(0.0)

    grid.index = grid.index.astype(float)
    grid.columns = grid.columns.astype(float)

    return grid

def occurrence_percent_grid_bbox(nl_season, lon_bins, lat_bins):
    grid = np.zeros((len(lat_bins)-1, len(lon_bins)-1), dtype=float)
  
    
    n_total = nl_season.index.unique().size

    # acumula por frame (para não contar 2x mesma célula no mesmo timestamp)
    for t, g in nl_season.groupby(level=0):
        marked = set()

        for _, r in g.iterrows():
            x0, x1 = sorted([r.lon_min, r.lon_max])
            y0, y1 = sorted([r.lat_min, r.lat_max])

            # bins cobertos (interseção)
            j0 = np.searchsorted(lon_bins, x0, side="right") - 1
            j1 = np.searchsorted(lon_bins, x1, side="left")
            i0 = np.searchsorted(lat_bins, y0, side="right") - 1
            i1 = np.searchsorted(lat_bins, y1, side="left")

            j0 = max(j0, 0); i0 = max(i0, 0)
            j1 = min(j1, len(lon_bins)-1); i1 = min(i1, len(lat_bins)-1)

            for i in range(i0, i1):
                for j in range(j0, j1):
                    marked.add((i, j))

        for (i, j) in marked:
            grid[i, j] += 1  # conta 1 por frame

    grid = 100.0 * grid / n_total
    return pd.DataFrame(grid, index=lat_bins[:-1], columns=lon_bins[:-1])


def occurrence_by_grid(
    nl,
    step=2.0,
    rounding=0,
    lon_col=("lon_min", "lon_max"),
    lat_col=("lat_min", "lat_max"),
):
    """
    nl: DataFrame indexado por time, com lon_min/lon_max/lat_min/lat_max.
    Retorna DataFrame com lon_bin, lat_bin e occ_pct (taxa %).
    """

    df = nl.copy()

    # centro do núcleo (ou use outra proxy se preferir)
    df["lon"] = (df[lon_col[0]] + df[lon_col[1]]) / 2.0
    df["lat"] = (df[lat_col[0]] + df[lat_col[1]]) / 2.0

    # bins (use extent fixo se quiser consistência entre estações)
    lon_bins = np.arange(-90, -30 + step, step)
    lat_bins = np.arange(-40, 20 + step, step)


    df["lon_bin"] = pd.cut(
        df["lon"], bins=lon_bins, 
        labels=lon_bins[:-1], include_lowest=True
        )
    df["lat_bin"] = pd.cut(
        df["lat"], bins=lat_bins, 
        labels=lat_bins[:-1], include_lowest=True
        )

    df["lon_bin"] = df["lon_bin"].astype(float).round(rounding)
    df["lat_bin"] = df["lat_bin"].astype(float).round(rounding)

    # total de imagens/instantes (normalização)
    n_times = df.index.unique().size
    if n_times == 0:
        return pd.DataFrame(
            columns=["lon_bin", "lat_bin",
                     "occ_pct", "n_times", "n_hits"])

    # Dedup: conta no máximo 1 ocorrência por (time, cell)
    unique_hits = df.reset_index(names="time")[
        ["time", "lon_bin", "lat_bin"]].dropna()
    unique_hits = unique_hits.drop_duplicates(
        subset=["time", "lon_bin", "lat_bin"])

    # hits por célula = nº de timestamps com evento naquela célula
    hits = (unique_hits
            .groupby(["lon_bin", "lat_bin"])
            .size()
            .rename("n_hits")
            .reset_index())

    hits["n_times"] = n_times
    hits["occ_pct"] = 100.0 * hits["n_hits"] / n_times
    return hits


def plot_map_occ(ax, grid, vmax=30):
    
    
  
    lat_lims = dict(min=-40, max=20, stp=10)
    lon_lims = dict(min=-90, max=-30, stp=15)
    gg.map_attrs(
        ax, None, 
        lat_lims = lat_lims, 
        lon_lims = lon_lims, 
        grid = False, 
        degress = None
        )
    
    levels = np.linspace(0, np.max(grid.values)
, 50)
    
    img = ax.contourf(
        grid.columns,
        grid.index,
        grid.values,
        levels=levels,
        cmap="jet", 
    )
    return img


def set_occurrence_data(
        nl_season, 
        step=2.0, 
        rounding=0
        ):
    df = occurrence_by_grid(nl_season, step=step, rounding=rounding)
    grid = pd.pivot_table(
        df,
        columns="lon_bin",
        index="lat_bin",
        values="occ_pct",
        aggfunc="mean"   # aqui já é único por célula; mean ok
    ).sort_index()
    
    return grid

seasons = {
    "December": [12, 1, 2],
    "March": [3, 4, 5],
    "June": [6, 7, 8],
    "September": [9, 10, 11],
}

def plot_seasonal_occurrence_from_nl(
        nl, step=2.0, vmax=30, year=None):
    

    if year is None:
        year = int(nl.index[0].year)

    fig, ax = plt.subplots(
        dpi=300, ncols=2, nrows=2, figsize=(16, 16),
        subplot_kw={"projection": ccrs.PlateCarree()},
    )
    plt.subplots_adjust(wspace=0.02, hspace=0.12)

    axes = ax.flat 
    lon_bins = np.arange(-90, -30 + step, step)
    lat_bins = np.arange(-40,  20 + step, step)

    for i, (name, months) in enumerate(seasons.items()):
        nl_season = nl.loc[nl.index.month.isin(months)]
        grid =  occurrence_percent_grid(
            nl_season, lon_bins, lat_bins)
        img = plot_map_occ(
            axes[i], grid, 
            year=year, vmax=vmax)

        l = b.chars()[i]
        axes[i].set_title(f"({l}) {name}", fontsize=28)

        if i != 0:
            axes[i].set(
                xticklabels=[], 
                xlabel="", 
                ylabel="", 
                yticklabels=[])

    # colorbar única (se você preferir usar a sua b.fig_colorbar, ok também)
    cbar = fig.colorbar(
        img, ax=ax.ravel().tolist(), orientation="horizontal", fraction=0.035, pad=0.05)
    cbar.set_label("Occurrence rate of convective nucleos (%)", fontsize=22)

    fig.suptitle(str(year), y=0.98, fontsize=28)
    return fig

# fig = plot_seasonal_occurrence_from_nl(df, step=2, vmax=20, year=2023)
# plt.show()
nl = b.load("GOES/data/nucleos3/2023/1")  # seu df indexado por time

months = seasons['December'] 

fig, ax = plt.subplots(
    dpi = 300,  
    figsize = (8, 8),
    subplot_kw={"projection": ccrs.PlateCarree()},
)
 
nl_s = nl.loc[nl.index.month.isin(months)]

step = 0.5
lon_bins = np.arange(-90, -30 + step, step)
lat_bins = np.arange(-40,  20 + step, step)


# grid =  occurrence_percent_grid(
#     nl_s, lon_bins, lat_bins
#     )

grid = occurrence_percent_grid_bbox(nl_s, lon_bins, lat_bins)
img = plot_map_occ(
    ax, grid,   vmax=10
    )
 