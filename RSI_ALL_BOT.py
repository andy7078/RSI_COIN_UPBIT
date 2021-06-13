#Guri_Rsi_Beta_1.0
#

import pyupbit #터미널에 pip pyupbit 로 다운해야 실행됨
import time
import pandas as pd
import os

access = "UwYm4gZhXiwwExhGgDmnrVPDapAroVWuXLA1xKJx"          # 본인 값으로 변경
secret = "ERsFJFGC8A8jt5BMBjGpENi7oq6F2RnCpTxVxCUf"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
KRWbalance = upbit.get_balance("KRW")
buy_price = 9000
first_buy_coin_list = []
second_buy_coin_list = []
Third_buy_coin_list = []
fourth_buy_coin_list = []
WOW = []
coinlist = pyupbit.get_tickers('KRW')

while True:
    for KRWcoin in coinlist:
        df = pyupbit.get_ohlcv(KRWcoin, interval="minute3")
        print(KRWcoin)
        KRWbalance = upbit.get_balance("KRW")
        def rsi(ohlc: df, period: int = 14):
            ohlc["close"] = ohlc["close"]
            delta = ohlc["close"].diff()

            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0

            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")

        rsi = rsi(df, 14).iloc[-1]
        if KRWcoin in first_buy_coin_list or KRWcoin in second_buy_coin_list or KRWcoin in Third_buy_coin_list or KRWcoin in fourth_buy_coin_list or KRWcoin in WOW:
            D = 0
        else:
            if rsi <= 30:
                print(upbit.buy_market_order(KRWcoin, buy_price))
                first_buy_coin_list.append(KRWcoin)
                globals()['price_{}'.format(KRWcoin)] = pyupbit.get_current_price(KRWcoin)

        if KRWcoin in first_buy_coin_list and rsi <= 25:
            print(upbit.buy_market_order(KRWcoin, buy_price*2))
            second_buy_coin_list.append(KRWcoin)
            first_buy_coin_list.remove(KRWcoin)
            globals()['price_{}'.format(KRWcoin)] = pyupbit.get_current_price(KRWcoin)

        if KRWcoin in second_buy_coin_list and rsi <= 20:
            print(upbit.buy_market_order(KRWcoin, buy_price*3))
            Third_buy_coin_list.append(KRWcoin)
            second_buy_coin_list.remove(KRWcoin)
            globals()['price_{}'.format(KRWcoin)] = pyupbit.get_current_price(KRWcoin)

        if KRWcoin in Third_buy_coin_list and rsi <= 15:
            print(upbit.buy_market_order(KRWcoin, buy_price*4))
            fourth_buy_coin_list.append(KRWcoin)
            Third_buy_coin_list.remove(KRWcoin)
            globals()['price_{}'.format(KRWcoin)] = pyupbit.get_current_price(KRWcoin)

        if rsi >= 67 and KRWcoin in first_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)
            
        if rsi >= 67 and KRWcoin in second_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)
            
        if rsi >= 67 and KRWcoin in Third_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)
            
        if rsi >= 67 and KRWcoin in fourth_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)

        if rsi <= 62 and KRWcoin in WOW and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            print(upbit.sell_limit_order(KRWcoin, pyupbit.get_current_price(KRWcoin), upbit.get_balance(KRWcoin.replace('KRW-',""))))
            if KRWcoin in first_buy_coin_list:
                first_buy_coin_list.remove(KRWcoin)
            if KRWcoin in second_buy_coin_list:
                second_buy_coin_list.remove(KRWcoin)
            if KRWcoin in Third_buy_coin_list:
                Third_buy_coin_list.remove(KRWcoin)
            if KRWcoin in fourth_buy_coin_list:
                fourth_buy_coin_list.remove(KRWcoin)
            if KRWcoin in WOW:
                WOW.remove(KRWcoin)

        print('WOW:', WOW)
        print('first:', first_buy_coin_list)
        print('second:', second_buy_coin_list)
        print('third:', Third_buy_coin_list)
        print('fourth:', fourth_buy_coin_list)
        time.sleep(0.2)
        os.system('clear')
        if KRWbalance > buy_price:
            continue
        else:
            break

    for KRWcoin in coinlist:
        df = pyupbit.get_ohlcv(KRWcoin, interval="minute1")
        print(KRWcoin)
        print('less money')
        KRWbalance = upbit.get_balance("KRW")
        def rsi(ohlc: df, period: int = 14):
            ohlc["close"] = ohlc["close"]
            delta = ohlc["close"].diff()

            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0

            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")

        rsi = rsi(df, 14).iloc[-1]

        if rsi >= 67 and KRWcoin in first_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)

        if rsi >= 67 and KRWcoin in second_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)

        if rsi >= 67 and KRWcoin in Third_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)

        if rsi >= 67 and KRWcoin in fourth_buy_coin_list and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            WOW.append(KRWcoin)

        if rsi <= 62 and KRWcoin in WOW and globals()['price_{}'.format(KRWcoin)] < pyupbit.get_current_price(KRWcoin):
            print(upbit.sell_limit_order(KRWcoin, pyupbit.get_current_price(KRWcoin), upbit.get_balance(KRWcoin.replace('KRW-',""))))
            if KRWcoin in first_buy_coin_list:
                first_buy_coin_list.remove(KRWcoin)
            if KRWcoin in second_buy_coin_list:
                second_buy_coin_list.remove(KRWcoin)
            if KRWcoin in Third_buy_coin_list:
                Third_buy_coin_list.remove(KRWcoin)
            if KRWcoin in fourth_buy_coin_list:
                fourth_buy_coin_list.remove(KRWcoin)
            if KRWcoin in WOW:
                WOW.remove(KRWcoin)

        print('WOW:', WOW)
        print('first:', first_buy_coin_list)
        print('second:', second_buy_coin_list)
        print('third:', Third_buy_coin_list)
        print('fourth:', fourth_buy_coin_list)
        time.sleep(0.2)
        os.system('clear')

        if KRWbalance < buy_price:
            continue
        else:
            break
    