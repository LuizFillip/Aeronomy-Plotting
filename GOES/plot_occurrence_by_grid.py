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

