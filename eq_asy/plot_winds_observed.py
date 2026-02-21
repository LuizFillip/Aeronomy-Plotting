from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import  Literal, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import base as b
import core as c


Direction = Literal["zonal", "meridional", "east", "west", "north", "south"]
Season = Literal["march", "june", "september", "december"]


@dataclass(frozen=True)
class SeasonSpec:
    name: Season
    months: tuple[int, int]  # two-month season bins (e.g. Mar–Apr)


SEASONS: tuple[SeasonSpec, ...] = (
    SeasonSpec("march", (3, 4)),
    # SeasonSpec("june", (6, 7)),  # uncomment if needed
    SeasonSpec("september", (9, 10)),
    # SeasonSpec("december", (12, 1)),  # DJF proxy: Dec–Jan 
)

LOS_MAP: dict[str, tuple[str, str]] = {
    "meridional": ("north", "south"),
    "zonal": ("east", "west"),
}


def set_data(file: str) -> pd.DataFrame:
    """
    Load database file and compute derived components.
    Assumes the index is datetime-like.
    """
    df = b.load(f"database/FabryPerot/{file}").copy()

    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    # Derived components
    df["zonal"] = df[["west", "east"]].mean(axis=1)
    df["meridional"] = df[["north", "south"]].mean(axis=1)

    # Features used by the compositor
    df["time"] = df.index.to_series().apply(b.dn2float)  # your existing time conversion
    df["doy"] = df.index.dayofyear  # robust grouping key for compositing

    return df


def sel_season(df: pd.DataFrame, season: SeasonSpec) -> pd.DataFrame:
    """Select rows belonging to a 2-month season window."""
    m1, m2 = season.months
    if m1 == 12 and m2 == 1:
        # DJF-like: Dec OR Jan
        mask = (df.index.month == 12) | (df.index.month == 1)
    else:
        mask = (df.index.month == m1) | (df.index.month == m2)
    return df.loc[mask]


def mean_compose(
    ds: pd.DataFrame,
    direction: Direction = "zonal",
    group_key: str = "doy",
    ref: Optional[dt.datetime] = dt.datetime(2014, 1, 1),
) -> pd.DataFrame:


    table = pd.pivot_table(
        ds,
        values=direction,
        index="time",
        columns=group_key,
        aggfunc="mean",
    )

    out = pd.DataFrame(
        {
            "mean": table.mean(axis=1),
            "std": table.std(axis=1),
        },
        index=table.index,
    )
    
    if ref is not None:
        out.index = b.new_index_by_ref(ref, out.index)

    return out.sort_index()


def _set_axis_limits(ax: plt.Axes, direction: str):
    """Set default y-limits and ticks based on component."""
    if direction == "meridional":
        ax.set(ylim=(-50, 100), yticks=[-50, 0, 50, 100])
    else:
        ax.set(ylim=(-10, 150), yticks=[0, 50, 100, 150])


def plot_seasonal_winds(
    ax: np.ndarray,
    df: pd.DataFrame,
    direction: Literal["zonal", "meridional"] = "zonal",
    plot_los: bool = False,
    resample_rule: str = "1H",
):
    """
    Plot seasonal composites on a column of a (n_seasons x n_cols) axes array.
    """
    marker = ['s', 'd']
   
    for i, season in enumerate(SEASONS):
        
        df_season = sel_season(df, season)
        ds_season = c.SeasonsSplit(df, season.name) 

        stats = mean_compose(df_season, direction=direction, group_key="doy")

        df_stats = stats.resample(resample_rule).mean()
        
        label = season.name.capitalize() + ' Eq.'

        ax.errorbar(
            df_stats.index,
            df_stats["mean"].values,
            yerr=df_stats["std"].values,
            capsize=4,
            lw=1.5,
            marker=marker[i],
            markersize = 14,
            fillstyle='none',
            label= label,
        )

        if plot_los:
            for v in LOS_MAP[direction]:
                los_stats = mean_compose(
                    df_season, 
                    direction=v, group_key="doy"
                    ).resample(resample_rule).mean()
                ax.errorbar(
                    los_stats.index,
                    los_stats["mean"].values,
                    yerr=los_stats["std"].values,
                    capsize=4,
                    lw=1.5,
                    marker=marker[i],
                    markersize=7,
                    fillstyle='none',
                    label= label,
                )

    ax.legend()
    
    ax.axhline(0, linestyle=":", linewidth=1)
    b.axes_hour_format(ax, hour_locator=1)
    
    return None 


b.sci_format()
def plot_FPI_seasonal_winds(
    direction: Literal["zonal", "meridional"] = "zonal"
) -> plt.Figure:


    fig, ax = plt.subplots(
        dpi= 300,
        figsize= (12, 6),
    )

    plt.subplots_adjust(hspace=0.05, wspace=0.05)

    df = set_data("mean")

    plot_seasonal_winds(
        ax,
        df=df,
        direction=direction,
        plot_los=False,
    )
    
    ylabel = direction.capitalize()
    ax.set(
        title= "São João do Cariri", 
        xlabel = 'Universal time', 
        ylabel = f'{ylabel} velocity (m/s)'
        )
    
    return fig


fig = plot_FPI_seasonal_winds(direction = "zonal")
    # fig.savefig("seasonal_analysis.png", bbox_inches="tight")
