from nsepython import *

#At 9:20 it will scan all fno stocks and take the first 10 and last 10.
#highest gainer and loser of the day
#from here https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES IN F%26O

folist = fnolist()[3:]
value_dict = {}

for scrip in folist:
    open_price = nse_eq(scrip)['priceInfo']['open']
    high_price = nse_eq(scrip)['priceInfo']['intraDayHigh']
    low_price = nse_eq(scrip)['priceInfo']['intraDayLow']
    #price_of_scrip = nse_quote_ltp(scrip)
    high_difference = high_price-open_price
    low_difference = open_price-low_price
    
    #if price_of_scrip < float(upper_bound):
    #    if price_of_scrip > float(lower_bound):
    #        resultant_scrips.append(scrip)

print(resultant_scrips)