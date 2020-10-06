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
highest_change = df['symbol'][:5]
lowest_change = df['symbol'][-5:]

#print(highest_three[0:1]['symbol'].to_string()," | ", highest_three[0:1]['open'].to_string())

print("Highest Changes in                 ", highest_change)
print("===================================================")
print("Lowest Changes in                   ", lowest_change)
