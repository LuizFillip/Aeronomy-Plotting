
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

import GOES as gs
import base as b


def load_convection_data(year):
    """Carrega os dados de núcleos convectivos para um ano."""
    df = b.load(f"GOES/data/nucleos_40/{year}").copy()
    df.index = pd.to_datetime(df.index)
    return df


def prepare_convection_dataframe(df):
    """Adiciona coordenadas centrais dos núcleos."""
    df = df.copy()
    df["lon_center"] = (df["lon_min"] + df["lon_max"]) / 2
    df["lat_center"] = (df["lat_min"] + df["lat_max"]) / 2
    return df


def select_fixed_longitude(
        df, 
        lon_fixed, 
        use_bbox_intersection = True, 
        lon_tol = 0.5
        ):
    """
    Seleciona núcleos associados a uma longitude fixa.

    Parameters
    ----------
    use_bbox_intersection : bool
        Se True, seleciona bbox que cruza lon_fixed.
        Se False, usa o centro do núcleo com tolerância lon_tol.
    """
    if use_bbox_intersection:
        mask = (
            df["lon_min"] <= lon_fixed
                ) & (df["lon_max"] >= lon_fixed)
    else:
        mask = np.abs(
            df["lon_center"] - lon_fixed) <= lon_tol

    return df.loc[mask].copy()


def count_convection_lat_bins_fixed_lon(
    year=2013,
    freq="15D",
    lon_fixed=-60,
    lat_bins=None,
    area_min=0,
    use_bbox_intersection=True,
    lon_tol=0.5,
):
    """
    Conta o número de núcleos de convecção por bin latitudinal
    em uma longitude fixa, ao longo do tempo.
    """
    if lat_bins is None:
        lat_bins = np.arange(-40, 15, 2)

    df = load_convection_data(year)
    df = prepare_convection_dataframe(df)

    if area_min > 0:
        df = df.loc[df["area"] > area_min].copy()

    df = select_fixed_longitude(
        df,
        lon_fixed=lon_fixed,
        use_bbox_intersection=use_bbox_intersection,
        lon_tol=lon_tol,
    )

    if df.empty:
        out = pd.DataFrame(
            0,
            index=pd.DatetimeIndex([], name="time"),
            columns=lat_bins[:-1],
            dtype=float,
        )
        return out

    df["lat_bin"] = pd.cut(
        df["lat_center"],
        bins=lat_bins,
        right=False,
        include_lowest=True,
    )

    counts = (
        df.groupby([pd.Grouper(freq=freq), 
                    "lat_bin"], observed=False)
        .size()
        .unstack(fill_value=0)
        .sort_index(axis=1)
    )

    # renomeia colunas para o limite inferior de cada bin
    counts.columns = lat_bins[:-1]
    return counts


def join_years(
    years=range(2012, 2018),
    lon_fixed=-70,
    freq="15D",
    step=5,
    area_min=0,
    lat_min=-40,
    lat_max=15,
    use_bbox_intersection=True,
    lon_tol=0.5,
    show_progress=True,
):
    """
    Junta vários anos em uma única série tempo-latitude.
    """
    lat_bins = np.arange(lat_min, lat_max, step)
    iterator = tqdm(years, desc="Joining years") if show_progress else years

    out = []
    for year in iterator:
        ds = count_convection_lat_bins_fixed_lon(
            year=year,
            freq=freq,
            lon_fixed=lon_fixed,
            lat_bins=lat_bins,
            area_min=area_min,
            use_bbox_intersection=use_bbox_intersection,
            lon_tol=lon_tol,
        )
        out.append(ds)

    if not out:
        return pd.DataFrame(columns=lat_bins[:-1], dtype=float)

    return pd.concat(out).sort_index()


def smooth_time_lat_grid(ds, sigma=1):
    """Suaviza a grade tempo-latitude."""
    grid = ds.T.to_numpy(dtype=float)
    return gs.smooth_grid(grid, sigma=sigma)


def plot_time_lat_convection(
    ax,
    ds,
    title=None,
    sigma=1,
    levels=30,
    cmap="jet",
    add_colorbar=True,
    cbar_label="Number of convective nuclei",
    vmin=None,
    vmax=None,
):
    """
    Plota um diagrama tempo-latitude da contagem de convecção.
    """
    if ds.empty:
        ax.set_title(title or "No data")
        ax.set_ylabel("Latitude (deg)")
        return None

    grid = smooth_time_lat_grid(ds, sigma=sigma)

    mesh = ax.contourf(
        ds.index,
        ds.columns,
        grid,
        levels=levels,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
    )

    if add_colorbar:
        plt.colorbar(mesh, ax=ax, label=cbar_label)

    ax.set_ylabel("Latitude (deg)")
    ax.set_title(title or "Convection count by latitude bin")

    return mesh


def plot_multiple_longitudes(
    longitudes=range(-80, -30, 10),
    years=range(2012, 2018),
    freq="1MS",
    step=2,
    area_min=0,
    lat_min=-40,
    lat_max=15,
    sigma=1,
    use_bbox_intersection=True,
    lon_tol=0.5,
    figsize=(16, 12),
    dpi=300,
):
    """
    Plota painéis tempo-latitude para várias longitudes fixas.
    """
    longitudes = list(longitudes)

    fig, axes = plt.subplots(
        nrows=len(longitudes),
        figsize=figsize,
        sharex=True,
        sharey=True,
        dpi=dpi,
        constrained_layout=True,
    )

    if len(longitudes) == 1:
        axes = [axes]

    all_data = []
    for lon_fixed in longitudes:
        ds = join_years(
            years=years,
            lon_fixed=lon_fixed,
            freq=freq,
            step=step,
            area_min=area_min,
            lat_min=lat_min,
            lat_max=lat_max,
            use_bbox_intersection=use_bbox_intersection,
            lon_tol=lon_tol,
        )
        all_data.append(ds)

    # mesma escala em todos os painéis
    all_max = max((ds.to_numpy().max() for ds in 
                   all_data if not ds.empty), default=None)

    last_mesh = None
    for ax, lon_fixed, ds in zip(axes, longitudes, all_data):
        last_mesh = plot_time_lat_convection(
            ax=ax,
            ds=ds,
            title=f"Longitude {abs(lon_fixed):.0f}°{'W' if lon_fixed < 0 else 'E'}",
            sigma=sigma,
            levels=30,
            cmap="jet",
            add_colorbar=False,
            vmin=0,
            vmax=all_max,
        )

    axes[-1].set_xlabel("Time")

    if last_mesh is not None:
        fig.colorbar(
            last_mesh,
            ax=axes,
            orientation="vertical",
            label="Number of convective nuclei",
            shrink=0.95,
            pad=0.02,
        )

    return fig, axes

fig, axes = plot_multiple_longitudes(
    longitudes=range(-80, -30, 10),
    years=range(2012, 2018),
    freq="1MS",
    step=2,
    area_min=0,
    lat_min=-40,
    lat_max=15,
    sigma=1,
)