import matplotlib.pyplot as plt
import ionosphere as io
import datetime as dt
from GEO import sites
import pandas as pd

import pandas as pd
import ionosphere as io
from models import altrange_models

def test_data(**kwargs):
    
    df = altrange_models(**kwargs)

    nu = io.collision_frequencies()

    nui = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
        
    nue = nu.electrons_neutrals(
        df["O"], df["O2"], df["N2"],
        df["He"], df["H"], df["Te"]
    )    
    return pd.DataFrame({"ne": df["ne"].copy(), 
                         "nui": nui, 
                         "nue": nue})

def plot_pedersen_in_different_alts():
    
    glat, glon = sites["saa"]["coords"]

    kwargs = dict(
        dn = dt.datetime(2013, 1, 1, 12), 
        glat = glat, 
        glon = glon,
        hmin = 75,
        hmax = 150
        )

    ds = test_data(**kwargs)

    c = io.conductivity()

    ds_lower = ds.loc[ds.index <= 100].copy()
        
    ds_lower["perd"] = c.electron_term(ds["ne"], ds["nue"])
        
    ds_upper = ds.loc[(ds.index >= 100)].copy()
    
    ds_upper["perd"] = c.ion_term(ds["ne"], ds["nui"])
    
    region_E = pd.concat([ds_lower, ds_upper])
    
    lower_F = ds.loc[(ds.index >= 130)].copy()
    
    lower_F["perd"] = c.pedersen_F(lower_F["ne"], lower_F["nui"])
    
    ds["perd"] = c.pedersen(ds["ne"], ds["nui"], ds["nue"])
    
    fig, ax = plt.subplots(dpi = 300)
        
    ax.plot(ds["perd"], ds.index, label = "total")
    #ax.plot(lower_F["perd"], lower_F.index, label = "$> 130$")
    ax.plot(ds_lower["perd"], ds_lower.index, label = "$< 100$")
    ax.plot(ds_upper["perd"], ds_upper.index, label = " $>100$")
    #ax.plot(region_E["perd"], region_E.index, linestyle = "--")
    
    
    #print(pd.concat([ds_lower, ds], axis = 1)["perd"].dropna())

    
    ax.set(xscale = "log", 
           xlabel = "$\sigma_P$ (mho)", 
           ylabel = "Altitude (km)")
    
    ax.legend()
    
plot_pedersen_in_different_alts()
