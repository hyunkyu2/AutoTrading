import numpy as np
import pyupbit
import pandas as pd
import datetime
import time
from tensorflow.keras.models import load_model
from trade_practice import *
model = load_model('model.h5')

access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)

ticker = ["KRW-BTC", "KRW-XRP"]
balance_ticker = []
for idx in range(0,len(ticker),1):
    balance_ticker.append(ticker[idx][4:])
start_time = get_start_time(ticker)
target_price = get_target(ticker)
target_price = sum(target_price, [])

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ticker)
        end_time = start_time + datetime.timedelta(hours=4)
        current_price = get_current_price(ticker)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target(ticker)
            target_price = sum(target_price, [])
            
            if target_price < current_price:
                krw = get_balance(["KRW"], access, secret)
                
                if krw[0] > 5000*len(ticker):
                    for num_coin in range(0, len(ticker), 1):
                        print(upbit.buy_market_order(ticker[num_coin], (krw[0]-200)/2))
        else:
            balance = get_balance(balance_ticker, access, secret)
            bal_mul_price = np.multiply(balance, current_price)
            for num_coin in range(0, len(ticker), 1):
                if bal_mul_price[num_coin] > 5000:
                    print(upbit.sell_market_order(ticker[num_coin], balance[0]))
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)