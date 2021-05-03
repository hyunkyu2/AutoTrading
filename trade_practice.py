import numpy as np
import pyupbit
import pandas as pd
import datetime
import time
from tensorflow.keras.models import load_model
model = load_model('model.h5')

def get_target(ticker):
    df_target_price = []
    for Coin in ticker:
        df = pyupbit.get_ohlcv(Coin, interval="minute240", count=50)
        high_prices = df['high']
        low_prices = df['low']
        mid_prices = (high_prices + low_prices) / 2

        graph_data = np.array(mid_prices/mid_prices[0] - 1)
        graph_data = np.reshape(graph_data, (1, graph_data.shape[0], 1))

        pred_result = model.predict(graph_data)
        df_target = (np.reshape(pred_result, (pred_result.shape[0],))+1) * np.array(mid_prices[0:pred_result.shape[0]])
        df_target_price.append(list(df_target))
    return df_target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker[0], interval="minute240", count=1)
    start_time = df.index[0]
    return start_time

def get_current_price(ticker):
    current_price=[]
    for i in range(0,len(ticker),1):
        current_price.append(pyupbit.get_orderbook(tickers=ticker)[i]["orderbook_units"][0]["ask_price"])
    return current_price

def get_balance(balance_ticker, access, secret):
    upbit = pyupbit.Upbit(access, secret)
    """잔고 조회"""
    having_balance = []
    balances = upbit.get_balances()
    for coin_idx in range(0,len(balance_ticker),1):
        for b in balances:
                if b['currency'] == balance_ticker[coin_idx]:
                    if b['balance'] is not None:
                        having_balance.append(float(b['balance']))
    return having_balance

