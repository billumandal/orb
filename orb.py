from nsepython import *
#from tabulate import tabulate
import pandas as pd

#At 9:20 it will scan all fno stocks and take the first 10 and last 10.
#highest gainer and loser of the day
#from here https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES IN F%26O

folist = fnolist()[3:8]
scrip_values = {}

for scrip in folist:
    open_price = nse_eq(scrip)['priceInfo']['open']
    high_price = nse_eq(scrip)['priceInfo']['intraDayHighLow']['max']
    low_price = nse_eq(scrip)['priceInfo']['intraDayHighLow']['min']
    #price_of_scrip = nse_quote_ltp(scrip)

    #trying to put max positive and negative to be sorted in table
    high_diff_percentage = (high_price-open_price)/open_price
    low_diff_percentage = (low_price-open_price)/open_price

    scrip_values.update({scrip : [high_diff_percentage, low_diff_percentage]})

    #if price_of_scrip < float(upper_bound):
    #    if price_of_scrip > float(lower_bound):
    #        resultant_scrips.append(scrip)

df = pd.DataFrame(scrip_values)
print(df)