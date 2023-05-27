import matplotlib.pyplot as plt
from models import altrange_iri
from GEO import sites
import digisonde as dg


infile = "database/Digisonde/SAA0K_20130316(075).TXT"

df = dg.load_profilogram(infile)

times = df.index.unique()
dn = times[130]



ds = df.loc[df.index == dn]



plt.plot(ds["ne"], ds["alt"])




lat, lon = sites["saa"]["coords"]

iri = altrange_iri(dn = dn, glat = lat, glon = lon, hmin = 75, 
                   hmax = 800)

plt.plot(iri["ne"], iri.index)

plt.show()

dn