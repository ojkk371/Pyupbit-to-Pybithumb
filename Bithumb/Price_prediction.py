import os
import pandas as pd
import numpy as np
import talib
import os
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
from keras.models import load_model
import lightgbm as lgb
#import xgboost

coinname = 'C:\\Users\\happy\\model\\XRP'
xs_xrp = joblib.load(coinname + 'Xscale.pkl')
ys_xrp = joblib.load(coinname + 'Yscale.pkl')
LSTM_xrp = load_model(coinname + 'LSTM.h5')
lgb1_xrp = joblib.load(coinname + 'lgb1.pkl')
lgb2_xrp = joblib.load(coinname + 'lgb2.pkl')
#xgb_xrp = joblib.load(coinname + 'xgb.pkl')

coinname = 'C:\\Users\\happy\\model\\COSM'
xs_cosm = joblib.load(coinname + 'Xscale.pkl')
ys_cosm = joblib.load(coinname + 'Yscale.pkl')
LSTM_cosm = load_model(coinname + 'LSTM.h5')
lgb1_cosm = joblib.load(coinname + 'lgb1.pkl')
lgb2_cosm = joblib.load(coinname + 'lgb2.pkl')
#xgb_cosm = joblib.load(coinname + 'xgb.pkl')

coinname = 'C:\\Users\\happy\\model\\ETH'
xs_eth = joblib.load(coinname + 'Xscale.pkl')
ys_eth = joblib.load(coinname + 'Yscale.pkl')
LSTM_eth = load_model(coinname + 'LSTM.h5')
lgb1_eth = joblib.load(coinname + 'lgb1.pkl')
lgb2_eth = joblib.load(coinname + 'lgb2.pkl')
#xgb_eth = joblib.load(coinname + 'xgb.pkl')

coinname = 'C:\\Users\\happy\\model\\KNC'
xs_knc = joblib.load(coinname + 'Xscale.pkl')
ys_knc = joblib.load(coinname + 'Yscale.pkl')
LSTM_knc = load_model(coinname + 'LSTM.h5')
lgb1_knc = joblib.load(coinname + 'lgb1.pkl')
lgb2_knc = joblib.load(coinname + 'lgb2.pkl')
#xgb_knc = joblib.load(coinname + 'xgb.pkl')

coinname = 'C:\\Users\\happy\\model\\POWR'
xs_powr = joblib.load(coinname + 'Xscale.pkl')
ys_powr = joblib.load(coinname + 'Yscale.pkl')
LSTM_powr = load_model(coinname + 'LSTM.h5')
lgb1_powr = joblib.load(coinname + 'lgb1.pkl')
lgb2_powr = joblib.load(coinname + 'lgb2.pkl')
#xgb_powr = joblib.load(coinname + 'xgb.pkl')


def Indicators(df):  # date close open high low volume 컬럼순
    # 결측치 33줄 생김 0~32 까지
    df['sma5'] = talib.SMA(np.asarray(df['close']), 5)
    df['sma20'] = talib.SMA(np.asarray(df['close']), 20)
    # df['sma120'] = talib.SMA(np.asarray(df['close']), 120)
    df['ema12'] = talib.SMA(np.asarray(df['close']), 12)
    df['ema26'] = talib.SMA(np.asarray(df['close']), 26)
    upper, middle, lower = talib.BBANDS(np.asarray(df['close']), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df['dn'] = lower
    df['mavg'] = middle
    df['up'] = upper
    df['pctB'] = (df.close - df.dn) / (df.up - df.dn)
    rsi14 = talib.RSI(np.asarray(df['close']), 14)
    df['rsi14'] = rsi14
    macd, macdsignal, macdhist = talib.MACD(np.asarray(df['close']), 12, 26, 9)
    df['macd'] = macd
    df['macdsignal'] = macdsignal
    df['obv'] = talib.OBV(df['close'], df['volume'])
    df['ad'] = talib.AD(df['high'], df['low'], df['close'], df['volume'])
    df['ADOSC'] = talib.ADOSC(df['high'], df['low'], df['close'], df['volume'], fastperiod=3, slowperiod=10)
    df = df.iloc[33:]
    df = df.fillna(0)
    df = df.drop(columns=['date'])

    return df


def NLP_Coinpan_News(df):
    return df


def predcoin(coinname, dataset):
    result = []
    global xs_xrp, ys_xrp, LSTM_xrp, lgb1_xrp, lgb2_xrp, xgb_xrp
    global xs_cosm, ys_cosm, LSTM_cosm, lgb1_cosm, lgb2_cosm, xgb_cosm
    global xs_eth, ys_eth, LSTM_eth, lgb1_eth, lgb2_eth, xgb_eth
    global xs_knc, ys_knc, LSTM_knc, lgb1_knc, lgb2_knc, xgb_knc
    global xs_powr, ys_powr, LSTM_powr, lgb1_powr, lgb2_powr, xgb_powr

    if coinname == 'XRP':
        xs, ys, LSTM, lgb1, lgb2 = xs_xrp, ys_xrp, LSTM_xrp, lgb1_xrp, lgb2_xrp#, xgb_xrp
    elif coinname == 'COSM':
        xs, ys, LSTM, lgb1, lgb2= xs_cosm, ys_cosm, LSTM_cosm, lgb1_cosm, lgb2_cosm#, xgb_cosm
    elif coinname == 'ETH':
        xs, ys, LSTM, lgb1, lgb2 = xs_eth, ys_eth, LSTM_eth, lgb1_eth, lgb2_eth#, xgb_eth
    elif coinname == 'KNC':
        xs, ys, LSTM, lgb1, lgb2 = xs_knc, ys_knc, LSTM_knc, lgb1_knc, lgb2_knc#, xgb_knc
    elif coinname == 'POWR':
        xs, ys, LSTM, lgb1, lgb2= xs_powr, ys_powr, LSTM_powr, lgb1_powr, lgb2_powr#, xgb_powr

    data = Indicators(dataset)

    nptf = np.array(data[-50:])
    nptf = pd.DataFrame(xs.transform(nptf), columns=data.columns)
    nptf = np.array(nptf)
    nptf = nptf.reshape(1, 50, -1)

    result.append(ys.inverse_transform(LSTM.predict(nptf)))

    nptf = np.array(data.iloc[-1])
    nptf = nptf.reshape(1, -1)

    result.append(lgb1.predict(nptf))
    result.append(lgb2.predict(nptf))
    #result.append(xgb.predict(nptf))

    return result
