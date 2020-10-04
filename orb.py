from nsepython import *
import pandas as pd

#At 9:20 it will scan all fno stocks and take the first 10 and last 10.
#highest gainer and loser of the day

# Do the same with nsefetch.
scrip_list = []
f = nsefetch('http://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
fo = json.dumps(f)
fodict = json.loads(fo)
fnolist = fodict['data']
#print(fnolist[3]['symbol'])

df = pd.DataFrame(fnolist).reindex(columns=['symbol','pChange'])

df.sort_values(by=['pChange'])
highest_change = df['symbol'][:3]
lowest_change = df['symbol'][-3:]

import time 
import logging
from alice_blue import *
logging.basicConfig(level=logging.DEBUG)

###################################################
#Alice API 
username = 'AB072170'
password = 'somamandal2'
twoFA = 'q'
client_id = 'UNOFFICED'
client_secret = 'AYBTHY25UFEDJ6EZY6ZISK1K0LBEUX18XGKB038P8RJF2660WHAZNWP07025XXL6'
redirect_url = 'https://www.unofficed.com/alice/fallback/'
access_token = AliceBlue.login_and_get_access_token(username=username, password=password, twoFA=twoFA,  api_secret=client_secret, redirect_url=redirect_url, app_id=client_id)
alice = AliceBlue(username=username, password=password, access_token=access_token,master_contracts_to_download=['NSE', 'BSE', 'MCX', 'NFO'])
#bn_fut= alice.get_instrument_for_fno(symbol=symbol, expiry_date=expiry_date, is_fut=True, strike=None, is_CE=False)
###################################################

#alice.place_order(transaction_type=TransactionType.Buy, instrument=scrip1,quantity=1, order_type=OrderType.Market, product_type=ProductType.Intraday)

#print(highest_change[1])
#return lowest_change

alldata = pd.DataFrame(fnolist)

highest_three = alldata[:3]
print(highest_three[0:1]['symbol']," | ", highest_three[0:1]['open'])