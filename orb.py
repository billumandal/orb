from nsepython import *
#from tabulate import tabulate
import pandas as pd

#At 9:20 it will scan all fno stocks and take the first 10 and last 10.
#highest gainer and loser of the day
#from here https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES IN F%26O

#folist = fnolist()[3:8]
#scrip_values = {}

	#for scrip in folist:
    #open_price = nse_eq(scrip)['priceInfo']['open']
    #high_price = nse_eq(scrip)['priceInfo']['intraDayHighLow']['max']
    #low_price = nse_eq(scrip)['priceInfo']['intraDayHighLow']['min']
    #price_of_scrip = nse_quote_ltp(scrip)

    #trying to put max positive and negative to be sorted in table
    #high_diff_percentage = (high_price-open_price)/open_price
    #low_diff_percentage = (low_price-open_price)/open_price

    #scrip_values.update({scrip : [high_diff_percentage, low_diff_percentage]})


#df = pd.DataFrame(scrip_values)
#print(df)

    # Do the same with nsefetch.
scrip_list = []
folist = nsefetch('http://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
fo = json.dumps(f)
folist = json.loads(fo)
fodict = folist['data']