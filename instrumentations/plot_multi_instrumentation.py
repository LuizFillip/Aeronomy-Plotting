import os
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from skimage import io
import digisonde as dg
import imager as im
import base as b
import epbs as pb
import plotting as pl


def folder_date(date: dt.datetime) -> str:
    return date.strftime('%Y%m%d')


def plot_imager(ax, path_sky: str, filename: str, index: int) -> dt.datetime:
    """Plota imagem All-Sky processada em um eixo."""
    
    image = im.DisplayASI(path_sky)
    
    image.display_original(ax)

    dn = image.dn
    ax.set(title = dn.strftime(f'({index}) %Hh%M'))
    return dn


def plot_ionogram(
        ax, 
        path_iono: str, 
        target: dt.datetime, 
        col: int, 
        site: str
        ) -> None:
    """Plota ionograma recortado."""
    filename = target.strftime(f'{site}_%Y%m%d(%j)%H%M%S.PNG')
    filepath = os.path.join(path_iono, filename)

    img = io.imread(filepath)
    cropped = img[300:860, 188:747]
    ax.imshow(cropped)

    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set(title=target.strftime(f'({col + 1}) %Hh%M'))

    if col == 1:
        ax.text(0.6, -0.2, 'Frequency (MHz)', transform=ax.transAxes)
    if col == 0:
        ax.set(ylabel='Virtual Height (km)')
        
    return None 

    
def plot_roti_curves(
        ax, 
        dn: dt.datetime, 
        root: str = 'E:\\'
        ) -> None:
    """Plota as curvas de ROTI para o dia selecionado."""
    ds = pb.concat_files(dn, root=root)
    ds = b.sel_times(ds, dn)

    ax.plot(
        ds['roti'], 
        marker='o', 
        markersize=1, 
        linestyle='none',
        color='gray', 
        alpha=0.3
        )

    times = pb.time_range(ds)
    df1 = pb.maximum_in_time_window(ds, 'max', times)

    ax.plot(df1, color='k', marker='o', markersize=5, linestyle='none')

    ax.set(
        ylim=[0, 5],
        yticks=range(0, 6),
        ylabel='ROTI (TECU/min)',
        xlim=[df1.index[0], df1.index[-1]]
    )

    pl.legend_max_points_roti(ax, fontsize=25)
    b.format_time_axes(ax, pad=80)
    
    return None 


def plot_shades(
        ax, 
        time: dt.datetime, index: int, y: float = 4.5) -> None:
    """Destaca a região de tempo com uma barra sombreada e rótulo."""
    delta = dt.timedelta(minutes=10)

    ax.text(time, y, str(index), transform=ax.transData)
    ax.axvspan(time, time + delta, alpha=0.5, color='gray',
               edgecolor='k', lw=2)
    
    return None 

def closest_iono(path_iono: str, target: dt.datetime) -> dt.datetime:
    """Retorna o ionograma mais próximo ao tempo alvo."""
    iono_times = [
        dg.ionosonde_fname(f)
        for f in os.listdir(path_iono) if 'PNG' in f
    ]
    return b.closest_datetime(iono_times, target)


def plot_multi_instrumentation(
    image_files: list[str],
    site: str = 'SAA0K',
    letter: str = 'a'
) -> plt.Figure:
    """Gera visualização combinada de imagens All-Sky, ionogramas e ROTI."""
    
    # dn = get_datetime_from_file(image_files[0])
    dn = im.fn2dn(with_epbs[0])
    fig = plt.figure(dpi=300, figsize=(12, 16), layout="constrained")
    fig.text(0.07, 0.9, f'({letter})', fontsize=45)

    folder_img = dn.strftime('CA_%Y_%m%d')
    folder_ion = dn.strftime('%Y/%Y%m%d')
    path_sky = f'database/images/{folder_img}/'
    path_iono = f'database/ionogram/{folder_ion}{site[0]}/'

    gs = GridSpec(3, len(image_files))
    gs.update(hspace=0.1, wspace=0)
    ax_roti = plt.subplot(gs[2, :])

    plot_roti_curves(ax_roti, dn)

    for col, fn_sky in enumerate(image_files):
        ax_sky = plt.subplot(gs[0, col])
        time_sky = plot_imager(ax_sky, path_sky, fn_sky, col + 1)

        ax_iono = plt.subplot(gs[1, col])
        time_iono = closest_iono(path_iono, time_sky)
        plot_ionogram(ax_iono, path_iono, time_iono, col, site)

        plot_shades(ax_roti, time_iono, col + 1)

    return fig

non_epbs = [ 
    'O6_CA_20130610_220827.tif',
    'O6_CA_20130610_225828.tif', 
    'O6_CA_20130611_001329.tif', 
    'O6_CA_20130611_014955.tif'
    ]

with_epbs = [
    'O6_CA_20130114_224619.tif', 
    'O6_CA_20130114_231829.tif',
    'O6_CA_20130114_234329.tif', 
    'O6_CA_20130115_020958.tif'
    ]


# with_epbs = [
#     # 'O6_CA_20131224_222810.tif', 
#     'O6_CA_20131224_231957.tif',
#     'O6_CA_20131225_011602.tif',
#     'O6_CA_20131225_021645.tif',
#     'O6_CA_20131225_024146.tif'
#     ]

with_epbs = [
    'O6_CA_20181213_003415.tif',
    'O6_CA_20181213_003938.tif',
    'O6_CA_20181213_012430.tif',
    'O6_CA_20181213_020735.tif'
    ]
def main():

    figure_1  = plot_multi_instrumentation(with_epbs) 
    figure_2  = plot_multi_instrumentation(non_epbs, letter = 'b') 
    
    fig = b.join_images(figure_1, figure_2)
    
    FigureName = 'validation_roti_paper'
    
    # fig.savefig(
    #     b.LATEX(FigureName, 
    #     folder = 'products'),
    #     dpi = 400)
    
# main()

# figure_1  = plot_multi_instrumentation(with_epbs) 


