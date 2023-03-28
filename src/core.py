import pandas as pd

def load_HWM():
    f3 = "database/HWM/car_250_2013.txt"
    
    df = pd.read_csv(f3, index_col = "time")
    df.index = pd.to_datetime(df.index)
    del df["Unnamed: 0"]
    return df

def load_EPB(infile, lat = -5):
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    if lat is None:
        return df
    else:
        return  df.loc[df["lat"] == lat]

def main():
   infile = 'EPBs_DRIFT.txt'

   df = load_EPB(infile, lat = -5)

   print(df)
    
