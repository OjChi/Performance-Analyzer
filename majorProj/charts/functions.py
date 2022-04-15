import requests
import pandas as pd
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import datetime
import time
from pandas import Timestamp
import requests
from bs4 import BeautifulSoup

def spotquote(symbol):
    import requests
    import json
    # symbol='BTCUSD'
    # payload = {
    #   'symbol': symbol,
    # }
    # url = 'https://api.binance.us/api/v3/ticker/price'
    # r = requests.get(url, params = payload)
    # data = r.json()
    # print(f'''data:{data}''')
    
    url1 = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+symbol+'&apikey=2LDC13KUVCTN5W49'
    r1 = requests.get(url1)
    data1 = r1.json()

    # print(list(data1.items())[0][1])

    # print(data)
    # {'symbol': 'BTCUSD', 'price': '40191.1000'}

    data_dict = {}
    data_dict['symbol'] = symbol
    data_dict['price'] = list(data1.items())[0][1]['05. price']
    data_dict['percentchange'] = list(data1.items())[0][1]['10. change percent']

    return data_dict



#returns a pandas dataframe with candlestick data
def candles(symbol):
  symbol=symbol
  interval = '1m'
  limit = '500'

  payload = {
      'symbol': symbol,
      'interval': interval,
      'limit': limit,
  }

  url= 'https://api.binance.us/api/v3/klines'
  r = requests.get(url, params = payload)
  r = r.json()
  # print(len(r))

  index = []
  open = []
  high = []
  low = []
  close = []
  volume = []
  for i in r:
    index.append(i[:][0])
    open.append(i[:][1])
    high.append(i[:][2])
    low.append(i[:][3])
    close.append(i[:][4])
    volume.append(i[:][5])

  newindex=[]
  for n in index:
      newindex.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(n/1000)))

  ts_df = pd.DataFrame(open,
                       index = newindex,
                       columns=['open'],
                       )
  ts_df['high'] = high
  ts_df['low'] = low
  ts_df['close'] = close
  ts_df['volume'] = volume



  df = ts_df.reindex(index=ts_df.index[::-1])


  return df



 #PRICE CHANGE DATA
def pricechange(symbol):
    symbol=symbol
    payload = {
        'symbol': symbol,
    }
    # url= 'https://api.binance.us/api/v3/ticker/24hr'
    # r = requests.get(url, params = payload)
    # r = r.json()
    # pricechange = r

    url1 = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RELIANCE.BSE&outputsize=full&apikey=demo'
    r1 = requests.get(url1)
    data1 = r1.json()

    # print(list(data1['Time Series (Daily)'].items())[0][1])
    #{'1. open': '2577.0000', '2. high': '2592.8999', '3. low': '2546.0000', '4. close': '2552.4500', '5. volume': '156923'}
    data_dict = {}
    data_dict['highPrice'] = list(data1['Time Series (Daily)'].items())[0][1]['2. high']
    data_dict['lowPrice'] = list(data1['Time Series (Daily)'].items())[0][1]['3. low']
    data_dict['volume'] = list(data1['Time Series (Daily)'].items())[0][1]['5. volume']

    # print(data_dict)
    return data_dict