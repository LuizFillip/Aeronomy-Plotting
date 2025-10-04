import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as dates
import pytz


def midnight_points(times):
    midnight = times[times.time == dt.time(0, 0)]
    return [midnight[0], midnight[-1]]

def points_to_axes(ax1, points):
        
    trans_points = [ax1.transData.transform(
        (dates.date2num(date), 0)) 
                    for date in points]
    
    return [ax1.transAxes.inverted().transform(trans_point) 
                        for trans_point in trans_points]


def text_midnight(ax1, times, h = 0.5):
    midpoints =  midnight_points(times)
    
    transAxes_points = points_to_axes(ax1, midpoints)
    
    for date, point in zip(midpoints, transAxes_points):
        
        str_dt = date.strftime("%d/%m/%Y")
        ax1.text(point[0] - 0.05, 
                 point[1] - h, 
                 str_dt, 
                 transform = ax1.transAxes)
    
    
def secondary_axis(ax):
    """
    Adding an secondary axes bellow of the main with the 
    time difference
    """
    ax1 = ax.twiny()
    
    ax1.set(xticks = ax.get_xticks(), xlim = ax.get_xlim())
    
    ax1.xaxis.set_major_formatter(dates.DateFormatter('%H'))
    ax1.xaxis.set_major_locator(dates.AutoDateLocator())
    
    ax1.xaxis.set_ticks_position('bottom') 
    ax1.xaxis.set_label_position('bottom') 
    ax1.spines['bottom'].set_position(('outward', 40))
    
    return ax1


def local_and_universal_axis(
        ax, times, h = 0.5, time_zone = 'America/Fortaleza'
        ):
    brasil_tz = pytz.timezone(time_zone)
    3
    ax.xaxis.set_major_formatter(dates.DateFormatter(
        '%H', tz = brasil_tz))
    ax.xaxis.set_major_locator(dates.AutoDateLocator())
    
    ax.set(xlabel = "Hora local")
    
    ax1 = secondary_axis(ax)

    #text_midnight(ax1, times, h = h)
    
    ax1.set_xlabel("Hora universal")

def main():
    fig, ax = plt.subplots(
        figsize = (8, 3), 
        dpi = 300, constrained_layout=True)
    
    times = pd.date_range("2013-01-01", "2013-01-03", freq = "10min")
    x = np.arange(len(times))**2
    ax.plot(times, x)
   
    #local_and_universal_axis(ax, times)
