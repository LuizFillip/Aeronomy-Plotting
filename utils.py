from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score



def func(x, a, c):
    return a * x + c


def get_fit(xdata, ydata):
    
    popt, pcov = curve_fit(func, xdata, ydata)

    y_pred = func(xdata, *popt)

    r2 = round(r2_score(ydata, y_pred), 2)
    
    return func(xdata, *popt), r2 


def get_fit2(x, y):
    
    regression_model = LinearRegression()
    # Fit the data(train the model)
    regression_model.fit(x, y)
    # Predict
    y_predicted = regression_model.predict(x)

    # model evaluation
    rmse = mean_squared_error(y, y_predicted)
    r2 = r2_score(y, y_predicted)
    return round(r2, 2), y_predicted




