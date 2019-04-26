import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
import random
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 5, 3

# https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/
# http://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/
# https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/
# https://www.datasciencecentral.com/profiles/blogs/tutorial-forecasting-with-seasonal-arima

def test_decompose(timeseries):

    decomposition = seasonal_decompose(timeseries)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.subplot(411)
    plt.plot(timeseries, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal, label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show(block=True)

def test_stationarity(timeseries):
    # Determing rolling statistics
    #rolmean = pd.rolling_mean(timeseries, window=12)
    rolmean = timeseries.rolling(window=12).mean()
    #rolstd = pd.rolling_std(timeseries, window=12)
    rolstd = timeseries.rolling(window=12).std()

    # Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=True)

    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)

def get_data():
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
    data = pd.read_csv('data/AirPassengers.csv', parse_dates=['Month'], index_col='Month', date_parser=dateparse)
    print(data)
    ts = data['#Passengers']

    return ts

def main():
    ts = get_data()
    # test_stationarity(ts)
    # plt.plot(ts)
    # plt.show()

    ts_log = np.log(ts)
    ts_log_diff = ts_log - ts_log.shift()

    # test_decompose(ts_log)

    # plt.plot(ts_log_diff)
    #
    arima_order = (1, 1,1)
    arima_seasonal_order = (2, 0, 1, 12)
    model = SARIMAX(ts_log, order=arima_order, seasonal_order=arima_seasonal_order)
    #model = ARIMA(ts_log, order=arima_order)
    results_ARIMA = model.fit(disp=-1)
    print(results_ARIMA.summary())
    #print results_ARIMA.predict(dynamic= True)
    plt.plot(ts_log)
    forecast_res = results_ARIMA.forecast(120)
    print(forecast_res)
    plt.plot(forecast_res, color='red')
    # print results_ARIMA.fittedvalues
    # plt.plot(results_ARIMA.fittedvalues[1:], color='red')
    # plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))
    plt.show()


def main2():
    ts = get_data()
    # test_stationarity(ts)
    # plt.plot(ts)
    # plt.show()

    ts_log = np.log(ts)
    ts_log_diff = ts_log - ts_log.shift()

    test_decompose(ts_log)


def predict_test(scale):
    def fitting(x_1,x_2, e, e_1, e_2):
        X = 1.6293 * x_1 + -0.8946 * x_2 + e + -1.8270 * e_1 + 0.9245 * e_2
        return X

    def fitting_seasonality(x_1,x_12, e, e_1, e_2, e_12):
        X = 0.8491 * x_1 + e -1.2016 * e_1 + 0.2396 * e_2 + 0.9906 * x_12 - 0.5653 * e_12
        return X

    ts = get_data()
    ts_log = np.log(ts)
    res = []
    x_1 = ts_log[-1]
    x_12 = ts_log[-12]
    e = random.random()*scale
    e_1 = 0
    e_2 = 0
    e_12 = 0

    for i in range(12):
        x = fitting_seasonality(x_1, x_12, e, e_1, e_2, e_12)
        res.append(x)

        x_12 = ts_log[-12+i]
        x_1 = x
        e_2 = e_1
        e_1 = e
        e = random.random()*scale

    return res


main()


# plt.plot(predict_test(0.0))
# plt.plot(predict_test(0.1))
#
# plt.show()



