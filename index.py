import pyupbit #터미널에 pip pyupbit 로 다운해야 실행됨
import time
import datetime
import pandas as pd
import os
import schedule

access = "i08DtXroTBITfJX0hxV8487SxG3L6lrl26NzFv0F"          # 본인 값으로 변경
secret = "7Io54DCTFOyL8aBcDMhUxwS3NBeqIWUb23b9nlZ0"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
KRWbalance = upbit.get_balance("KRW")
buy_price = 100000
coinlist = pyupbit.get_tickers('KRW')

TIMEPRICE = []
ORDERLIST = []
PRICELIST = []
PASTPRICE = []

def MAKELIST():
    while True:
        for KRWcoin in coinlist:
            print(KRWcoin)
            TIMEPRICE.append(pyupbit.get_current_price(KRWcoin))
            time.sleep(0.2)
        if KRWcoin == "KRW-XEC":
            break

def MAKEORDER():
    while True:
        for KRWcoin in coinlist:
            if KRWcoin in ORDERLIST:
                continue
            else:
                if KRWbalance > buy_price:
                    coinnum = coinlist.index(KRWcoin)
                    print(KRWcoin)
                    if TIMEPRICE[coinnum] + (TIMEPRICE[coinnum]*0.015) <= pyupbit.get_current_price(KRWcoin):
                        print(upbit.buy_market_order(KRWcoin, buy_price))
                        ORDERLIST.append(KRWcoin)
                        PRICELIST.append(pyupbit.get_current_price(KRWcoin))
                        PASTPRICE.append(pyupbit.get_current_price(KRWcoin))

            time.sleep(0.2)
        if KRWcoin == "KRW-XEC":
            break


def DEL():
    TIMEPRICE.clear()

# 매일 특정 HH:MM 및 다음 HH:MM:SS에 작업 실행
schedule.every().hour.at(":59").do(MAKELIST)
schedule.every().hour.at(":00").do(MAKEORDER)
schedule.every().hour.at(":01").do(MAKEORDER)
schedule.every().hour.at(":02").do(MAKEORDER)
schedule.every().hour.at(":03").do(MAKEORDER)
schedule.every().hour.at(":04").do(MAKEORDER)
schedule.every().hour.at(":05").do(MAKEORDER)
schedule.every().hour.at(":06").do(DEL)




while True:
    schedule.run_pending()
    now = datetime.datetime.now()
    nowTime = now.strftime('%H:%M:%S')
    print(nowTime) # 12:11:32
    print(ORDERLIST)
    print(PASTPRICE)
    time.sleep(1)
    os.system('clear')
    for BUYcoin in ORDERLIST:

        buynum = ORDERLIST.index(BUYcoin)
        print("TEST")
        print(BUYcoin)
        print(buynum)
        print(PASTPRICE[buynum])
        print(PRICELIST[buynum]*0.03)
        print(pyupbit.get_current_price(BUYcoin))
        print("TEST")

        if PRICELIST[buynum] - (PRICELIST[buynum]*0.03) >= pyupbit.get_current_price(BUYcoin):
            print(upbit.sell_market_order(BUYcoin, upbit.get_balance(BUYcoin.replace('KRW-',""))))
            ORDERLIST.remove(BUYcoin)
            del PRICELIST[buynum]
            del PASTPRICE[buynum]
        else:
            if PASTPRICE[buynum] - (PASTPRICE[buynum]*0.03) >= pyupbit.get_current_price(BUYcoin):
                print(upbit.sell_market_order(BUYcoin, upbit.get_balance(BUYcoin.replace('KRW-',""))))
                ORDERLIST.remove(BUYcoin)
                del PASTPRICE[buynum]
                del PRICELIST[buynum]
            else:
                PASTPRICE[buynum] = pyupbit.get_current_price(BUYcoin)
        time.sleep(0.2)
