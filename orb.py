from nsepython import *

#At 9:20 it will scan all fno stocks and take the first 10 and last 10.
#highest gainer and loser of the day
#from here https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES IN F%26O

folist = fnolist()[3:]

for scrip in folist:
    #price_of_scrip = nse_eq(scrip)['priceInfo']['close']
    price_of_scrip = nse_quote_ltp(scrip) 
    
    if price_of_scrip < float(upper_bound):
        if price_of_scrip > float(lower_bound):
            resultant_scrips.append(scrip)

print(resultant_scrips)