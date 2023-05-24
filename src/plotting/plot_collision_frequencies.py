import FluxTube as ft
import ionosphere as io
from GEO import load_meridian
import datetime as dt
import matplotlib.pyplot as plt



dn = dt.datetime(2013, 1, 1, 21, 0) 

mlon, mlat, _, _, = load_meridian()

kwargs = dict(
    dn = dn, 
    glat = mlat, 
    glon = mlon,
    hmin = 90,
    step = 5,
    hmax = 1000
    
    )

ds = io.test_data(**kwargs)


def plot_collision_frequency(ax):

   
    #ax.plot(nu_eff, apex)
    
    ax.set(xlabel = "$\nu_{eff}^F$", 
           ylabel = "Altura de apex (km)")


infile = "database/FluxTube/201301012100.txt"

ds = io.load_calculate(infile)
ne = ft.IntegratedParameters(ds)

ds