# convert time series into supervised learning problem
from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
#from sklearn.metrics import mean_squared_error
#from sklearn.preprocessing import MinMaxScaler
from numpy import array

def parser(x):
    return datetime.strptime('190'+x, '%Y-%m')

series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

raw_values = series.values
raw_values = raw_values.reshape(len(raw_values), 1)


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('vari%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        print(n_vars,'Input sequence')
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('varo%d(t)' % (j+1)) for j in range(n_vars)]
            print(n_vars,'Output sequence1')
        else:
            names += [('varo%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
            print(n_vars,'Output sequence2')
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

#supervised = series_to_supervised(raw_values, 1, 3)
#print(supervised)
#print(series, '\n', len(series))

'''data = raw_values
if type(data) is list:
    print(" list ")
else:
    a = data.shape[1]
    print(f' the value of a is {a}')'''


n_in = 1
n_vars = 1

'''def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1
    if type(data) is list:
        print('yes')
     else:
        data.shape[1]
        print('not a list')
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('vari%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        #print(n_vars)
s = series_to_supervised(series, 1, 3)'''

#print([names])'''

from pandas import DataFrame
from pandas import concat
from pandas import read_csv
from pandas import datetime

# date-time parsing function for loading the dataset
def parser(x):
    return datetime.strptime('190'+x, '%Y-%m')

# convert time series into supervised learning problem
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

# transform series into train and test sets for supervised learning
def prepare_data(series, n_test, n_lag, n_seq):
    # extract raw values
    raw_values = series.values
    raw_values = raw_values.reshape(len(raw_values), 1)
    # transform into supervised learning problem X, y
    supervised = series_to_supervised(raw_values, n_lag, n_seq)
    supervised_values = supervised.values
    # split into train and test sets
    train, test = supervised_values[0:-n_test], supervised_values[-n_test:]
    return train, test

# load dataset
series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
# configure
n_lag = 1
n_seq = 3
n_test = 10
# prepare data
train, test = prepare_data(series, n_test, n_lag, n_seq)
#print(test)
#print('Train: %s, Test: %s' % (train.shape, test.shape))

# make a persistence forecast
def persistence(last_ob, n_seq):
    return [last_ob for i in range(n_seq)]

# evaluate the persistence model
def make_forecasts(train, test, n_lag, n_seq):
    forecasts = list()
    for i in range(len(test)):
        X, y = test[i, 0:n_lag], test[i, n_lag:]
        #print(y.shape[:])
        # make forecast
        forecast = persistence(X[-1], n_seq)
        #print(X)
        #print(X[-1],"This is X[-1]\n")
        # store the forecast
        forecasts.append(forecast)
        print("This is the new",'\n',forecasts)
    return forecasts

#forecasts = make_forecasts(train, test, 1, 3)
#print(test)




