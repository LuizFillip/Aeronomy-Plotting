# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:03:29 2024

@author: Luiz
"""

def solar_minimum():
    
    site =  'SAA0K'
    
    dn = dt.datetime(2019, 12, 28, 21)
    
    files = [
        'O6_CA_20191228_230604.tif',
        'O6_CA_20191229_001044.tif',
        'O6_CA_20191229_013322.tif', 
        'O6_CA_20191229_023803.tif'
        ]
    
    
    figure_1 = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 10,
        letter = '(a)')
    
    dn = dt.datetime(2019, 6, 24, 21)
    
    files = [
        'O6_CA_20190624_220934.tif',
        'O6_CA_20190624_231934.tif', 
        'O6_CA_20190625_003457.tif', 
        'O6_CA_20190625_010152.tif'
        ]
    
    
    
    figure_2  = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 10,
        letter = '(b)')
    
    
    fig = b.join_images(figure_1, figure_2)
    
    FigureName = dn.strftime('validation_solar_min')
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'products'),
        dpi = 400
        )
    
    return None


def solar_maximum(site =  'SAA0K'):
    dn = dt.datetime(2013, 12, 24, 20)
    
    files = [
        # 'O6_CA_20131224_222810.tif', 
        'O6_CA_20131224_231957.tif',
        'O6_CA_20131225_011602.tif',
        'O6_CA_20131225_021645.tif',
        'O6_CA_20131225_024146.tif'
        ]
    
    
    
    figure_2 = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 60)
    
    dn = dt.datetime(2013, 6, 10, 20)
    
    files = [ 
            
        'O6_CA_20130610_220827.tif',
        'O6_CA_20130610_225828.tif', 
        'O6_CA_20130611_001329.tif', 
        'O6_CA_20130611_023100.tif',
        ]
    
    figure_1 = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 60, letter = '(b)')
    
    fig = b.join_images(figure_2, figure_1)

    FigureName = dn.strftime('validation')
    
    fig.savefig(
        b.LATEX(FigureName, folder = 'products'),
        dpi = 400
        )
# solar_maximum(site =  'SAA0K')


# dn = dt.datetime(2019, 5, 2, 20)

# files = [
#     'O6_CA_20190502_222618.tif',
#     'O6_CA_20190503_010603.tif',
#     'O6_CA_20190503_014157.tif',
#     'O6_CA_20190503_023548.tif'
#     ]


def bubble_valid_2():
    

    dn = dt.datetime(2016, 10, 3, 20)
    
    site = 'FZA0M'
    site = 'SAA0K'
    
    files = [
        'O6_CA_20161003_232538.tif', 
        'O6_CA_20161004_022602.tif',
        'O6_CA_20161004_031109.tif',
        'O6_CA_20161004_042903.tif'
        
        ]
    fig = TEC_6300_IONOGRAM_ROTI(
        files, dn, site, tec_max = 30,
        letter = '')
    
    FigureName = dn.strftime('%Y%m%d_validation')
     
    # fig.savefig(
    #       b.LATEX(FigureName, folder = 'products'),
    #       dpi = 400
    #       )
    
    
    
def test_database():
    dirs = im.get_first_file()

    out = []

    for folder in list(dirs.keys()):
    
        dn = get_datetime(folder)
        
        file = dirs[folder]
        
        df =  pb.concat_files(
              dn, 
              root = 'D:\\'
              )
         
        ds = b.sel_times(df, dn, hours = 11)
        try:
            
            plot_time_evolution(file, dn, ds, vmax = 40)
        except:
            print(folder)
            out.append(folder)
            continue
        
    return out