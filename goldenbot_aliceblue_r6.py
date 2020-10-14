

#from nsepython import *
from alice_blue import *
import datetime as datetime
import calendar
import time
import requests
import pandas as pd 
import pytz

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Initialize all global variables
ltp = 0
openprice = 0
highprice = 0
lowprice  = 0
closeprice = 0
ticktime = 0
positions = None
who_triggered = None
socket_opened = False
alice = None
buy_above = None
sell_below = None


# Define a function that formats the chart data from Alice historical API into OHLCV
def format_intraday(data):
    records = data['data']
    df = pd.DataFrame(records, columns=[
                      'datetime', 'open', 'high', 'low', 'close', 'volume'])  # , index=0)
    df['datetime'] = df['datetime'].apply(
        pd.Timestamp, unit='s', tzinfo=pytz.timezone("Asia/Kolkata"))
    df['open'] = df['open'].astype(float).div(100)
    df['high'] = df['high'].astype(float).div(100)
    df['low'] = df['low'].astype(float).div(100)
    df['close'] = df['close'].astype(float).div(100)
    #df.set_index('datetime', inplace=True)
    return df

# Historical function needs NSE token numbers rather than script names
# so we define a function that returns token number for script name - a csv file is used for reference here.
def get_token_from_symbol_NSE(symbol):
    global expiry_date #get the expiry date
    if symbol == 'NIFTY' or symbol == 'BANKNIFTY':
        all_scripts = alice.search_instruments('NFO', symbol)
        df = pd.DataFrame(all_scripts)
        day = int(datetime.datetime.now().strftime('%d'))
        if day < 23: #if day is more than or equal to 23 which covers all months except Feb; trade in next month futures
            month = datetime.datetime.now().strftime('%h').upper()
        else:
            month = month = datetime.datetime.now().month
            lol =['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
            month = lol[month]
        symbol = symbol + ' ' + month + ' FUT'
        #print(symbol) to check if correct
        expiry_date = df[df['symbol']==symbol]['expiry'].values[0]
        return(df[df['symbol']==symbol]['token'].values[0])
    else:
        all_scripts = alice.search_instruments('NSE', symbol)
        df = pd.DataFrame(all_scripts)
        return(df[df['symbol']==symbol]['token'].values[0])

# Define a function to fetch historical data
def historical_data(symbol):
    global starttime, endtime
    token = get_token_from_symbol_NSE(symbol)
    if symbol == 'NIFTY' or symbol == 'BANKNIFTY':
        exchange = 'NFO'
    else:
        exchange = 'NSE'
    HEADERS = {'X-Authorization-Token': open('auth_token.txt', 'r').read().strip()} #OATH toekn is read from a file
    PARAMS = {
        'candletype': 3, #1 = minutewise data, #2 = hourly, #3 = daily
        'data_duration': 1,
        'starttime': starttime,
        'endtime': endtime,
        'exchange': exchange,
        'type': 'historical',
        'token': token
    }
    try:
        r = requests.get(
            "https://ant.aliceblueonline.com/api/v1/charts", params=PARAMS, headers=HEADERS)
        data = r.json()
        data = format_intraday(data)
        #print(data)
        return data
    except:
        print(
            "Some Error occurred in getting intraday data for ticker :: {}".format(token))

#Define a funciton to get the buyabove sell below data for all the stocks in the watchlist using NSE Python
def ohlcdata():
    global pdh, pdl, pdc  #define as global valriables
    global expiry_date
    global starttime, endtime
    tday = datetime.date.today()
    print('Today is: ' + str(tday))

    #First lets get the PDH, PDL and PDC data 
    #Take 1 months data - The code may throw an error if running on 31st of a month or 29/30/31 march - will fix this later
    starttime = int(datetime.datetime(tday.year, tday.month-1, tday.day,
                                hour=9, minute=0, second=0).timestamp())
    endtime = int(datetime.datetime(tday.year, tday.month, tday.day,
                            hour=23, minute=59, second=0).timestamp())
    print('Getting Daily OHLC data from ', datetime.datetime.fromtimestamp(starttime),' To ',datetime.datetime.fromtimestamp(endtime))
    dailydata = historical_data('BANKNIFTY')
    #dailydata['Range']= dailydata['high'] - dailydata['low']
    #dailydata['change']= dailydata['open'] - dailydata['close'] 
    df = pd.DataFrame(dailydata)
    #print(df)
    pdh = float(df['high'].iloc[-1])
    pdl = float(df['low'].iloc[-1])
    pdc = float(df['close'].iloc[-1])
    print('Previous Day High = ', pdh)
    print('Previous Day Low = ', pdl)
    print('Previous Day Close = ', pdc)
    
#Functions for getting data from Alice Blue
def open_callback():
    global socket_opened
    socket_opened = True

def socket_error(error):
    print(error)

def quote_update(message):
    global ltp, openprice, highprice, lowprice, closeprice, ticktime
    #print("Quote Received")
    #print(message) #debug step to verify the message tuple formatting is correctly being received
    ticktime = datetime.datetime.fromtimestamp(message['exchange_time_stamp']).strftime("%Y-%m-%d %H:%M:%S")
    ltp = float(message['ltp'])
    openprice = float(message['open'])
    highprice = float(message['high'])
    lowprice = float(message['low'])
    closeprice = float(message['close'])
    

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
    print(alice.get_balance()) # get balance / margin limits
    #print(alice.get_profile()) # get profile
    #print(alice.get_daywise_positions()) # get daywise positions
    #print(alice.get_netwise_positions()) # get netwise positions
    #print(alice.get_holding_positions()) # get holding positions
    #login to get master contracts to get the script info from AliceBlue
 
#Start Execution
def main():
    global pdh,pdl,pdc
    global alice
    global socket_opened
    global expiry_date
    global ltp, openprice, highprice, lowprice, closeprice, ticktime
    #Lets login into Alice
    AliceBlueLogin()

    #get previous data
    ohlcdata()
    ltp = pdc # If I initialize scrip with 0; it creates an automatic sell order due to logic before the first value gets updated. So initializing with pdc
    #Get the instrument details
    
    alice.start_websocket(subscribe_callback=quote_update,
                            socket_open_callback=open_callback,
                            socket_error_callback = socket_error,
                            run_in_background=True)
    
    #Calculate ORB Data
    while True: 
        print("Current Value of BankNIFTY : " + str(ltp) + " at time : " + str(ticktime))
        #totype = pd.Series({'time':ticktime, 'ltp':ltp, 'open':openprice, 'high':highprice, 'low':lowprice, 'close':closeprice})
        #df = pd.DataFrame(columns=['time','ltp','open','high','low','close'])
        #df.append(totype, ignore_index=True)
        now = datetime.datetime.now()
        range_high = 0
        range_low = 0
        if(now.hour == 9 and now.minute==25 and now.second>=0 and now.second < 10):
            range_high = float(highprice)
            range_low = float(lowprice)
            print('ORB Range High = ', range_high)
            print('ORB Range Low = ', range_low)
            opening_range = range_high - range_low
            print('Opening Range = ', opening_range)
            break
        time.sleep(10)

    #Calculate the Golden Number
    golden_number = ((pdh - pdl) + opening_range) * .618

    #Get the trade entry values
    buy_above = int(pdc + golden_number)
    sell_below = int(pdc - golden_number)

    print("Buy Above:" + str(buy_above))
    print('Sell Below:' + str(sell_below))

    #Trade Executions 

    while True: 
        print("Current Value of BankNifty : " + str(ltp) + " at time : " + str(ticktime))
        who_triggered = "NONE"

        if(ltp>buy_above):
            print("Buy Order executed at: " + str(ltp) + " Entry Time :"+ str(datetime.datetime.now()))
            who_triggered = "BUY"
            stop_loss = ltp*(.995)
            target = ltp*(1.02)

            #Place order on Alice
            alice.place_order(transaction_type=TransactionType.Buy,
                            instrument=bn_Fut,
                            quantity = 25,  # 1 lot or should i use 25 here as 1 lot = 25 units?
                            order_type=OrderType.Limit,
                            product_type=ProductType.Intraday,
                            price=ltp,
                            trigger_price=None,
                            stop_loss=stop_loss,
                            square_off=target,
                            trailing_sl=None,
                            is_amo=False)

        elif(ltp<sell_below):
            print("Sell Order executed at: " + str(ltp)+ " Entry Time :"+ str(datetime.datetime.now()))
            who_triggered = "SELL"
            stop_loss = ltp*(1.005)
            target = ltp*(.98)

            #Place order on Alice
            #We are placing a Limit order with Target & stop loss 
            alice.place_order(transaction_type=TransactionType.Sell,
                            instrument=bn_Fut,
                            quantity = 25,  # 1 lot or should i use 25 here as 1 lot = 25 units?
                            order_type=OrderType.Limit,
                            product_type=ProductType.Intraday,
                            price=ltp,
                            trigger_price=None,
                            stop_loss=stop_loss,
                            square_off=target,
                            trailing_sl=None,
                            is_amo=False)

        if(who_triggered != "NONE"):
            entry_price = ltp
            print("Stop Loss : " + str(stop_loss))
            print("Target : " + str(target))
            break
        
        time.sleep(10)

    # Trade Management

    while True:
        print("Current Value of BankNIFTY : " + str(ltp) + " at time : " + str(ticktime))
        exit_price = ltp
        if(who_triggered == "BUY"):
            if(ltp>target):
                print("Target hit at: "+ str(ltp)+"Exit Time : "+ str(datetime.datetime.now()))
                print("Net Profit: "+str(abs(entry_price-exit_price)))
                break
            if(ltp<stop_loss):
                print("Stop Loss hit at: "+ str(ltp)+"Exit Time : "+ str(datetime.datetime.now()))
                print("Net Loss: "+str(abs(entry_price-exit_price)))
                break
        elif(who_triggered == "SELL"):
            if(ltp<target):
                print("Target hit at: "+ str(ltp)+"Exit Time : "+ str(datetime.datetime.now()))
                print("Net Profit: "+str(abs(entry_price-exit_price)))
                break

            if(ltp>stop_loss):
                print("Stop Loss hit at: "+ str(ltp)+"Exit Time : "+ str(datetime.datetime.now()))
                print("Net Loss: "+str(abs(entry_price-exit_price)))
                break
        time.sleep(10)

if(__name__ == '__main__'):
            main()
