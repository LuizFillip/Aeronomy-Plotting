import RayleighTaylor as rt
from common import load, split_by_freq

infile = "database/FluxTube/IGRF/300_2013.txt"
df = load(infile)

ds = split_by_freq(df, freq_per_split = "10D")[0]

# rt.gammas_integrated(ds)

ds.columns