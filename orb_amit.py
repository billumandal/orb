from nsepython import *
import pandas as pd

gainers = nsefetch("https://www.nseindia.com/api/live-analysis-variations?index=gainers")

gainers=pd.DataFrame.from_records(gainers["NIFTY"]["data"])
gainers=gainers.head(5)
gainers.drop(gainers.columns.difference(["symbol","high_price","low_price","ltp"]), 1, inplace=True)
print(gainers)