# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 06:49:28 2025

@author: Luiz
"""

def plot_with_and_without_epb(
        with_epb, 
        without_epb, 
        delta
        ):
    
    file = im.get_closest(
        with_epb + delta, 
        file_like = True
        )
    figure_1 = plot_ion_tec_img(
            file, 
            with_epb, 
            kind = 'With EPB', 
            title_dn = True)
    
    
    file = im.get_closest(
        without_epb + delta, 
        file_like = True
        )
    figure_2 = plot_ion_tec_img(
            file, 
            without_epb, 
            kind = 'Without EPB', 
            title_dn = True
            )
    
    fig = b.join_images(figure_1, figure_2)
    
    dn = with_epb + delta
    
    fn = dn.strftime('%Y%m%d%H%M%S')
    fig.savefig('temp/' + fn)
    return fig

def run():
    with_epb = dt.datetime(2014, 1, 2, 21)
    without_epb = dt.datetime(2014, 6, 21, 21)

    for minute in tqdm(range(2 * 60, 12 * 60, 2)):
        
        delta = dt.timedelta(minutes = minute)
        
        plt.ioff()
    
        fig = plot_with_and_without_epb(
                with_epb, 
                without_epb, 
                delta
                )
        
        plt.clf()   
        plt.close()   

# run()

# with_epb = dt.datetime(2014, 1, 2, 21)
# without_epb = dt.datetime(2014, 6, 21, 21)

# delta = dt.timedelta(hours = 3)
# fig =  plot_with_and_without_epb(
#         with_epb, 
#         without_epb, 
#         delta
#         )

dn = dt.datetime(2014, 1, 2, 21)

file = im.get_closest(
    dn, 
    file_like = True
    )
plot_ion_tec_img(
        file, 
        dn, 
        kind = 'With EPB', 
        title_dn = None, 
        root = 'E:\\'
        )