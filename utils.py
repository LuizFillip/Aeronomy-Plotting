from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression


def get_fit(x, y):
    
    regression_model = LinearRegression()
    # Fit the data(train the model)
    regression_model.fit(x, y)
    # Predict
    y_predicted = regression_model.predict(x)

    r2 = r2_score(y, y_predicted)
    return round(r2, 2), y_predicted




