import datetime as dt 
import matplotlib.pyplot as plt
import base as b 
import core as c 
import RayleighTaylor as rt 
b.config_labels()


def plot_percent_gamma_weigths():
    
    return 

cols = ['gamma', 'gravity', 'drift', 'winds']

df  = c.gamma(
        site = 'saa', 
        time = dt.time(22, 0), 
        el_upper = True,
        file = 'p2',
        gamma_cols = cols
        )

fig, ax = plt.subplots(figsize = (12, 6), dpi = 300)
lb = rt.EquationsFT()

df = df.resample('1M').mean()

# df = df.loc[(df.index.year == 2013) & 
#             (df.index.month == 7)]
names = [lb.gravity, lb.drift, lb.winds]
out = []
for i, col in enumerate(cols[1:]):
    val = (df[col] / df['gamma'])
    print(col, val.values[130], )
    out.append(val.values[130])
    ax.plot((df[col] / df['gamma']), label = names[i])
print('total', sum(out))
ax.legend(
    ncol = 3, 
    bbox_to_anchor = (0.5, 1.5),
    loc = "upper center"      
          )
ax.set(ylim = [-0.5, 1],
       ylabel = 'Contribution in $\gamma_{RT}$', 
       xlabel = 'Years')


plt.show()


