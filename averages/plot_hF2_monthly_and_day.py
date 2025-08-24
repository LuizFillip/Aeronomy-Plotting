import base as b
import pandas as pd
import digisonde as dg
import matplotlib.pyplot as plt
import numpy as np

b.config_labels()
PATH_IONO = "digisonde/data/chars/"


def average(ax, infile):

    df = dg.chars(PATH_IONO + infile)

    df = df.between_time("20:00", "08:00")

    df["time"] = b.time2float(df.index, sum_from=18)

    df["day"] = df.index.day
    df["hF2"] = b.smooth2(df["hF2"], 3)
    ds = pd.pivot_table(df, values="hF2", columns="day", index="time")

    avg = ds.mean(axis=1)

    std = ds.std(axis=1)

    ax.errorbar(
        avg.index,
        avg,
        yerr=std,
        linestyle="none",
        marker="o",
        capsize=5,
        color="k",
        lw=2,
    )

    return None


def day_target(ax, file):

    cols = list(range(3, 8, 1))
    ds = dg.IonoChar(file, cols)
    df = ds.chars
    dn = ds.date.strftime("%d %B %Y")
    dn = "24 - 25 July 2022"
    df.index = b.time2float(df.index, sum_from=18)

    df["hF2"] = b.smooth2(df["hF2"], 3)

    ax.plot(df["hF2"], lw=2, color="red", label=dn)

    ax1 = ax.twinx()

    ax1.bar(df.index, df["QF"], width=0.15, alpha=0.7, edgecolor="k", color="gray")

    ax1.set(ylim=[0, 60], ylabel="QF (km)")

    ax.set(
        xlim=[21, 31],
        ylim=[100, 500],
        yticks=np.arange(100, 600, 100),
        xticks=np.arange(21, 34, 1),
        ylabel="h`F2 (km)",
    )

    xticks = ax.get_xticks()
    new_ticks = np.where(xticks >= 24, xticks - 24, xticks)

    ax.set(xticklabels=new_ticks)


def plot_hF2_monthly_and_target():

    fig, ax = plt.subplots(dpi=300, figsize=(12, 8), nrows=2, sharey=True, sharex=True)

    plt.subplots_adjust(hspace=0.1)

    # average(ax[0], 'SAA0K_20220701(182).TXT')

    infile = "SAA0K_20151202(336).TXT"

    ds = dg.IonoAverage(infile, parameter="hF2")
    # digisonde/data/chars/midnight/
    ax[0].plot(ds["hF2"], lw=2)
    day_target(ax[0], "SAA0K_20151220(354).TXT")

    # average(ax[1], 'CAJ2M_20220701(182).TXT')

    # day_target(ax[1], 'CAJ2M_20220724(205).TXT')

    ax[-1].set(xlabel="Universal time")

    ax[0].legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.3),
    )

    names = ["São Luís", "Cachoeira Paulista"]
    b.add_lines_and_letters(
        ax, names=names, fontsize=25, x=0.03, y=0.82, num2white=None
    )

    return fig


fig = plot_hF2_monthly_and_target()

# FigureName = 'averages_of_hF2'

# fig.savefig(b.LATEX(FigureName, 'paper2'), dpi = 400)
