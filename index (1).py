import pyupbit #터미널에 pip pyupbit 로 다운해야 실행됨
import time
import datetime
import pandas as pd
import os
import schedule

access = "Mx7GdxxulfojBwPH8ULX45RN9f6tXuKUraBvVeJD"          # 본인 값으로 변경
secret = "OXuNQOTeOMLtGwdhrDHxJSQF5TigZFTPT7AzpdZr"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
KRWbalance = upbit.get_balance("KRW")
buy_price = 100000
coinlist = pyupbit.get_tickers('KRW')
STARTLIST = []
RSILIST = []
ORDERLIST = []
PRICELIST = []

def MAKELIST():
    while True:
        for KRWcoin in coinlist:
            df = pyupbit.get_ohlcv(KRWcoin, interval="minute1")
            print(KRWcoin)
            #KRWbalance = upbit.get_balance("KRW")
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
            STARTLIST.append(KRWcoin)
            RSILIST.append(rsi)
            print(STARTLIST)     
            
        if KRWcoin == "KRW-XEC":
            break

def MAKEORDER():
    while True:
        for KRWcoin in coinlist:
            if KRWcoin in ORDERLIST:
                NULL=0
            else:
                coinnum = coinlist.index(KRWcoin)
                df = pyupbit.get_ohlcv(KRWcoin, interval="minute1")
                print(KRWcoin)
                #KRWbalance = upbit.get_balance("KRW")
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
                if RSILIST[coinnum] + 10 <= rsi:
                    print(upbit.buy_market_order(KRWcoin, buy_price))
                    ORDERLIST.append(KRWcoin)
                    PRICELIST.append(pyupbit.get_current_price(KRWcoin))
                
        if KRWcoin == "KRW-XEC":
            break

            
                
def DEL():
    STARTLIST.clear()
    RSILIST.clear()
                
# 매일 특정 HH:MM 및 다음 HH:MM:SS에 작업 실행
schedule.every().day.at("06:55:40").do(MAKELIST)
schedule.every().day.at("06:56:40").do(MAKEORDER)
schedule.every().day.at("06:57:40").do(MAKEORDER)
schedule.every().day.at("06:58:40").do(MAKEORDER)
schedule.every().day.at("06:59:40").do(DEL)
        



while True:
    schedule.run_pending()
    now = datetime.datetime.now()
    nowTime = now.strftime('%H:%M:%S')
    print(nowTime) # 12:11:32
    print(ORDERLIST)
    for BUYcoin in ORDERLIST:
            buynum = ORDERLIST.index(BUYcoin)
            if PRICELIST[buynum] - (PRICELIST[buynum]*0.03) >= pyupbit.get_current_price(BUYcoin):
                print(upbit.sell_market_order(BUYcoin, upbit.get_balance(BUYcoin.replace('KRW-',""))))
                ORDERLIST.remove(BUYcoin)
                del PRICELIST[buynum]
            
            if PRICELIST[buynum] + (PRICELIST[buynum]*0.05) <= pyupbit.get_current_price(BUYcoin):
                print(upbit.sell_market_order(BUYcoin, upbit.get_balance(BUYcoin.replace('KRW-',""))))
                ORDERLIST.remove(BUYcoin)
                del PRICELIST[buynum]
    time.sleep(1)
    os.system('clear')