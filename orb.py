from nsepython import *
#from tabulate import tabulate
import pandas as pd

#At 9:20 it will scan all fno stocks and take the first 10 and last 10.
#highest gainer and loser of the day

# Do the same with nsefetch.
scrip_list = []
folist = nsefetch('http://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
fo = json.dumps(f)
fodict = json.loads(fo)
fnolist = fodict['data']

#print(fnolist[3]['symbol'])

df = pd.DataFrame(fnolist).reindex(columns=['symbol','pChange'])
print(df)