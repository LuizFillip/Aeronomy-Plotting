from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import datetime as dt
import matplotlib.pyplot as plt


def get_datetime_fpi(filename):
    s = filename.split('_')
    obs_list = s[-1].split('.') 
    date_str = obs_list[0]
    return dt.datetime.strptime(
        date_str, "%Y%m%d")

def get_datetime_epb(filename):
    year, mon_day, lat = tuple(filename.replace(".txt", "").split("_"))
    month = int(mon_day[:2])
    day = int(mon_day[2:])
    year = int(year)
    
    if lat == "":
        lat = 0
    else:
        lat = int(lat)
    return dt.datetime(year, month, day), lat



def save_img(fig, 
             save_in):
    
    plt.ioff()
    fig.savefig(save_in, 
                dpi = 100, 
                pad_inches = 0, 
                bbox_inches = "tight")
    plt.clf()   
    plt.close()



def get_fit(x, y):
    
    regression_model = LinearRegression()
    # Fit the data(train the model)
    regression_model.fit(x, y)
    # Predict
    y_predicted = regression_model.predict(x)

    r2 = r2_score(y, y_predicted)
    return round(r2, 3), y_predicted




