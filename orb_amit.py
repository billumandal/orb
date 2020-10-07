from alice_blue import *
import datetime as datetime
import calendar
import time
import requests 
from nsepython import *
import pandas as pd
import logging

#Adding the code to disable debut logging which is there in nsepython by default
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_gainers():
    gainers = nsefetch("https://www.nseindia.com/api/live-analysis-variations?index=gainers")
    gainers=pd.DataFrame.from_records(gainers["NIFTY"]["data"])
    gainers=gainers.head(5)
    gainers.drop(gainers.columns.difference(["symbol","high_price","low_price","ltp"]), 1, inplace=True)
    return gainers

def get_losers():
    losers = nsefetch("https://www.nseindia.com/api/live-analysis-variations?index=losers")
    losers=pd.DataFrame.from_records(losers["NIFTY"]["data"])
    losers=losers.head(5)
    losers.drop(losers.columns.difference(["symbol","high_price","low_price","ltp"]), 1, inplace=True)
    return losers

#Functions for getting data from Alice Blue
def open_callback():
    global socket_opened
    socket_opened = True

def socket_error(error):
    print(error)

def AliceBlueLogin():
    global alice
    #get token
    username = 'AB072170'
    password = 'somamandal2'
    twoFA='q'
    client_id = 'UNOFFICED'
    client_secret = 'AYBTHY25UFEDJ6EZY6ZISK1K0LBEUX18XGKB038P8RJF2660WHAZNWP07025XXL6'
    redirect_url= 'https://www.unofficed.com/alice/fallback/'

    access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=twoFA,  api_secret=client_secret, redirect_url=redirect_url, app_id=client_id)

    alice = AliceBlue(username=username, password=password, access_token=access_token, master_contracts_to_download=['NSE','NFO'])

def main():
	now = datetime.datetime.now()
	alice.start_websocket(subscribe_callback=quote_update,
	                        socket_open_callback=open_callback,
	                        socket_error_callback = socket_error,
	                        run_in_background=True)
    AliceBlueLogin()
	gainers = get_gainers()
	losers = get_losers()

	if(now.hour == 9 and now.minute==25 and now.second>=0 and now.second < 10):
		for i in range(0,5):
		    symbol = gainers.symbol.iloc[i]
		    current_ltp = nse_quote_ltp(symbol)
		    day_high = gainers.high_price.iloc[i]
		    day_low = gainers.low_price.iloc[i]
		    quantity = int(100000/current_ltp)
				    if(current_ltp>day_high):
				    	who_triggered = "BUY"
						alice.place_order(transaction_type=TransactionType.Buy, instrument=symbol,quantity=quantity, order_type=OrderType.Market, product_type=ProductType.Intraday)
			time.sleep(100)



if(__name__ == '__main__'):
			main()