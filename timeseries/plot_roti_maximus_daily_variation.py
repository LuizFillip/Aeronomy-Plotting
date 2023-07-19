


infile = "database/RayleighTaylor/reduced/300.txt"
df = rt.load(infile)

ds = rt.split_by_freq(df, freq_per_split = "10D")[0]