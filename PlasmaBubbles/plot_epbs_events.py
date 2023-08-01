import pandas as pd
import datetime as dt
from PlasmaBubbles import find


def shade(
        ax, 
        df: pd.DataFrame, 
        start: dt.datetime, 
        label: bool = True
        ):
    
    end = start + dt.timedelta(minutes = 10)
    
    ax.axvspan(start, end, alpha = 0.3, color = "gray")
    
    if label:
        
        bubble = find(
            df, 
            start, 
            end, 
            col = "roti"
            )
        delta = dt.timedelta(minutes = 2.5)
        ax.text(start + delta, 7.5, 
                bubble, 
                transform = ax.transData)