# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 08:30:48 2026

@author: Luiz
"""

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

