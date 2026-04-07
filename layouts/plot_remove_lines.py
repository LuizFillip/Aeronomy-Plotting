import numpy as np
import matplotlib.pyplot as plt


def remove_inner_spines(ax, nrows, ncols, hide_inner_y=True):
    """
    Remove spines internas de uma grade de subplots, preservando apenas
    a borda externa do conjunto.

    Regras:
    - primeira linha: mantém spine superior
    - última linha: mantém spine inferior
    - linhas internas: remove top e bottom
    - primeira coluna: mantém spine esquerda
    - última coluna: mantém spine direita
    - colunas internas: remove left e right

    Parameters
    ----------
    ax : matplotlib Axes, array-like de Axes
        Retornado por plt.subplots().
    nrows : int
        Número de linhas.
    ncols : int
        Número de colunas.
    hide_inner_y : bool, default=True
        Se True, remove eixo y das colunas que não são a primeira.
    """
    ax = np.array(ax, dtype=object).reshape(nrows, ncols)

    for i in range(nrows):
        for j in range(ncols):
            a = ax[i, j]

            # Spines horizontais
            a.spines['top'].set_visible(i == 0)
            a.spines['bottom'].set_visible(i == nrows - 1)

            # Spines verticais
            a.spines['left'].set_visible(j == 0)
            a.spines['right'].set_visible(j == ncols - 1)

            # Controle do eixo Y
            if hide_inner_y and j != 0:
                a.yaxis.set_visible(False)
                a.set_yticks([])

    return ax


def main():
    scopes = [(3, 1), (1, 3), (3, 3)]

    for nrows, ncols in scopes:
        fig, ax = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(6, 6),
            sharex=True,
            sharey=True
        )

        fig.subplots_adjust(hspace=0, wspace=0)

        ax = remove_inner_spines(ax, nrows=nrows, ncols=ncols)

        plt.show()

 
main()