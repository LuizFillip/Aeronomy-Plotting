import matplotlib.pyplot as plt 

def plot_compare_solar_activity():
    

    fig, ax = plt.subplots(
        sharex = True,
        dpi = 300, 
        figsize = (14, 8), 
        )
    
    
    site = 'jic'
    path = os.path.join(
       PATH_GAMMA,
       f't_{site}.txt'
       )
    
    df = b.load(path)
    df = df.loc[df.index.year == 2019]
    
    df['night'].plot(ax = ax)
    
    site = 'saa'
    path = os.path.join(
       PATH_GAMMA,
       f't_{site}.txt'
       )
    
    df = b.load(path)
    df = df.loc[df.index.year == 2019]
    
    df['night'].plot(ax = ax)