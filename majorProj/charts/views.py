from django.shortcuts import render, redirect

#most dependencies and imports made in functions.py to avoid clutter
from .functions import *
import os
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
from talib import MACD, RSI
import talib
import numpy as np
from itertools import compress
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from talib import BBANDS
from plotly.subplots import make_subplots

# Create your views here.

def homeView(request):


    api_key = 'YX9741BHQFXIYA0B'

    stock = 'PLTR'

    api_key = 'YX9741BHQFXIYA0B'
    period= 60

    ts = TimeSeries(key=api_key, output_format='pandas',)
    data_ts, meta_data_ts = ts.get_intraday(stock, interval='1min', outputsize='compact')

    ti = TechIndicators(key=api_key, output_format='pandas')
    data_ti, meta_data_ti  = ti.get_rsi(stock, interval='1min', time_period=period, series_type='close')

    ts_df = data_ts
    ti_df = data_ti

    #Fundamentals
    payload = {'function': 'OVERVIEW', 'symbol': 'PLTR', 'apikey': 'YX9741BHQFXIYA0B'}
    r = requests.get('https://www.alphavantage.co/query', params=payload)
    r = r.json()


    #plotly graph
    def candlestick():
        figure = go.Figure(
            data = [
                    go.Candlestick(
                      x = ts_df.index,
                      high = ts_df['2. high'],
                      low = ts_df['3. low'],
                      open = ts_df['1. open'],
                      close = ts_df['4. close'],
                    )
                  ]
        )

        candlestick_div = plot(figure, output_type='div')
        return candlestick_div


    sector = r['Sector']
    marketcap = r['MarketCapitalization']
    peratio = r['PERatio']
    yearhigh = r['52WeekHigh']
    yearlow = r['52WeekLow']
    eps = r['EPS']



    timeseries = ts_df.to_dict(orient='records')

    closingprice = []
    for k in timeseries:
      closingprice.append(k['4. close'])

    lowprice = []
    for k in timeseries:
      closingprice.append(k['3. low'])

    highprice = []
    for k in timeseries:
      closingprice.append(k['2. high'])

    openprice = []
    for k in timeseries:
      closingprice.append(k['1. open'])

    pricedata = {
        'close': [closingprice],
        'open': [openprice],
        'high': [highprice],
        'low': [lowprice],
    }

    #miscellaneous stuff
    day = datetime.datetime.now()
    day = day.strftime("%A")

    def human_format(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    marketcap = int(marketcap)
    marketcap = human_format(marketcap)

    closingprice = closingprice[0:15]


    context = {
        'sector': sector,
        'marketcap': marketcap,
        'peratio': peratio,
        'yearhigh': yearhigh,
        'yearlow': yearlow,
        'eps': eps,
        'closingprice': closingprice,
        'openprice': openprice,
        'highprice': highprice,
        'lowprice': lowprice,
        'pricedata': pricedata,
        'timeseries': timeseries,
        'stock': stock,
        'day': day,
        'candlestick': candlestick(),
    }

    context={}
    return render(request, 'dashboard/index.html', context)
    


# def homeView(request):
#     if request.method == 'POST':
#         symbol = request.POST.get('symbol')
#         return redirect('crypto/')

#     context={

#     }
#     return render(request, 'dashboard/index.html', context)



def cryptoView(request, company_tech):

    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        symbol = symbol.upper()
    else:
        symbol = 'HDFCBANK.BSE'
        # symbol = 'BTCUSD'

    data = spotquote(symbol)
    pricedata = pricechange(symbol)
    moredata = pricechange(symbol)
    # print(f'''
    # moredata: {moredata},
    # pricedata: {pricedata}
    # ''')

    dirname = os.path.dirname(__file__)
    dirname = dirname[:-7]
    filename = os.path.join(dirname, 'combined_imputed_HDFC_Bank_withDate.csv')
    filename_replaced = filename.replace("\\", "/")
    # print(f'{filename_replaced}')

    ts_df = pd.read_csv(f'{filename_replaced}')
    company = "HDFC Bank"
    # C:\Users\ojasa\Documents\BE\Major Project\Proj\majorProj\combined_imputed_HDFC_Bank_withDate.csv
    actual_df = pd.read_csv((os.path.join(dirname, 'combined_imputed_HDFC_Bank_withDate.csv')).replace("\\","/"))
    actual_df['Date']= pd.to_datetime(actual_df['Date'])
    actual_df = actual_df.iloc[900:, :]
    
    pred_df = pd.read_csv(os.path.join(dirname, f'{company}.csv').replace("\\","/"))

    # print(actual_df)
    # print(pred_df)

    # extract OHLC 
    # op = actual_df['Open']
    # hi = actual_df['High']
    # lo = actual_df['Low']
    # cl = actual_df['Close']
    # # create columns for each pattern

    # candle_names = talib.get_function_groups()['Pattern Recognition']
    # print(len(candle_names))
    # remove = [
    #           'CounterAttack', 
    #           'Longline', 
    #           'Shortline', 
    #           'Stalledpattern', 
    #           'Kickingbylength'
    #           ]
    # remove = ['CDL'+x.upper() for x in remove]
    # for item in remove:
    #   print(item in candle_names)
    #   candle_names.remove(item)

    # print(len(candle_names))

    # for candle in candle_names:
    #   actual_df[candle] = getattr(talib, candle)(op, hi, lo, cl)


    # candle_rankings = {
    #         "CDL3LINESTRIKE_Bull": 1,
    #         "CDL3LINESTRIKE_Bear": 2,
    #         "CDL3BLACKCROWS_Bull": 3,
    #         "CDL3BLACKCROWS_Bear": 3,
    #         "CDLEVENINGSTAR_Bull": 4,
    #         "CDLEVENINGSTAR_Bear": 4,
    #         "CDLTASUKIGAP_Bull": 5,
    #         "CDLTASUKIGAP_Bear": 5,
    #         "CDLINVERTEDHAMMER_Bull": 6,
    #         "CDLINVERTEDHAMMER_Bear": 6,
    #         "CDLMATCHINGLOW_Bull": 7,
    #         "CDLMATCHINGLOW_Bear": 7,
    #         "CDLABANDONEDBABY_Bull": 8,
    #         "CDLABANDONEDBABY_Bear": 8,
    #         "CDLBREAKAWAY_Bull": 10,
    #         "CDLBREAKAWAY_Bear": 10,
    #         "CDLMORNINGSTAR_Bull": 12,
    #         "CDLMORNINGSTAR_Bear": 12,
    #         "CDLPIERCING_Bull": 13,
    #         "CDLPIERCING_Bear": 13,
    #         "CDLSTICKSANDWICH_Bull": 14,
    #         "CDLSTICKSANDWICH_Bear": 14,
    #         "CDLTHRUSTING_Bull": 15,
    #         "CDLTHRUSTING_Bear": 15,
    #         "CDLINNECK_Bull": 17,
    #         "CDLINNECK_Bear": 17,
    #         "CDL3INSIDE_Bull": 20,
    #         "CDL3INSIDE_Bear": 56,
    #         "CDLHOMINGPIGEON_Bull": 21,
    #         "CDLHOMINGPIGEON_Bear": 21,
    #         "CDLDARKCLOUDCOVER_Bull": 22,
    #         "CDLDARKCLOUDCOVER_Bear": 22,
    #         "CDLIDENTICAL3CROWS_Bull": 24,
    #         "CDLIDENTICAL3CROWS_Bear": 24,
    #         "CDLMORNINGDOJISTAR_Bull": 25,
    #         "CDLMORNINGDOJISTAR_Bear": 25,
    #         "CDLXSIDEGAP3METHODS_Bull": 27,
    #         "CDLXSIDEGAP3METHODS_Bear": 26,
    #         "CDLTRISTAR_Bull": 28,
    #         "CDLTRISTAR_Bear": 76,
    #         "CDLGAPSIDESIDEWHITE_Bull": 46,
    #         "CDLGAPSIDESIDEWHITE_Bear": 29,
    #         "CDLEVENINGDOJISTAR_Bull": 30,
    #         "CDLEVENINGDOJISTAR_Bear": 30,
    #         "CDL3WHITESOLDIERS_Bull": 32,
    #         "CDL3WHITESOLDIERS_Bear": 32,
    #         "CDLONNECK_Bull": 33,
    #         "CDLONNECK_Bear": 33,
    #         "CDL3OUTSIDE_Bull": 34,
    #         "CDL3OUTSIDE_Bear": 39,
    #         "CDLRICKSHAWMAN_Bull": 35,
    #         "CDLRICKSHAWMAN_Bear": 35,
    #         "CDLSEPARATINGLINES_Bull": 36,
    #         "CDLSEPARATINGLINES_Bear": 40,
    #         "CDLLONGLEGGEDDOJI_Bull": 37,
    #         "CDLLONGLEGGEDDOJI_Bear": 37,
    #         "CDLHARAMI_Bull": 38,
    #         "CDLHARAMI_Bear": 72,
    #         "CDLLADDERBOTTOM_Bull": 41,
    #         "CDLLADDERBOTTOM_Bear": 41,
    #         "CDLCLOSINGMARUBOZU_Bull": 70,
    #         "CDLCLOSINGMARUBOZU_Bear": 43,
    #         "CDLTAKURI_Bull": 47,
    #         "CDLTAKURI_Bear": 47,
    #         "CDLDOJISTAR_Bull": 49,
    #         "CDLDOJISTAR_Bear": 51,
    #         "CDLHARAMICROSS_Bull": 50,
    #         "CDLHARAMICROSS_Bear": 80,
    #         "CDLADVANCEBLOCK_Bull": 54,
    #         "CDLADVANCEBLOCK_Bear": 54,
    #         "CDLSHOOTINGSTAR_Bull": 55,
    #         "CDLSHOOTINGSTAR_Bear": 55,
    #         "CDLMARUBOZU_Bull": 71,
    #         "CDLMARUBOZU_Bear": 57,
    #         "CDLUNIQUE3RIVER_Bull": 60,
    #         "CDLUNIQUE3RIVER_Bear": 60,
    #         "CDL2CROWS_Bull": 61,
    #         "CDL2CROWS_Bear": 61,
    #         "CDLBELTHOLD_Bull": 62,
    #         "CDLBELTHOLD_Bear": 63,
    #         "CDLHAMMER_Bull": 65,
    #         "CDLHAMMER_Bear": 65,
    #         "CDLHIGHWAVE_Bull": 67,
    #         "CDLHIGHWAVE_Bear": 67,
    #         "CDLSPINNINGTOP_Bull": 69,
    #         "CDLSPINNINGTOP_Bear": 73,
    #         "CDLUPSIDEGAP2CROWS_Bull": 74,
    #         "CDLUPSIDEGAP2CROWS_Bear": 74,
    #         "CDLGRAVESTONEDOJI_Bull": 77,
    #         "CDLGRAVESTONEDOJI_Bear": 77,
    #         "CDLHIKKAKEMOD_Bull": 82,
    #         "CDLHIKKAKEMOD_Bear": 81,
    #         "CDLHIKKAKE_Bull": 85,
    #         "CDLHIKKAKE_Bear": 83,
    #         "CDLENGULFING_Bull": 84,
    #         "CDLENGULFING_Bear": 91,
    #         "CDLMATHOLD_Bull": 86,
    #         "CDLMATHOLD_Bear": 86,
    #         "CDLHANGINGMAN_Bull": 87,
    #         "CDLHANGINGMAN_Bear": 87,
    #         "CDLRISEFALL3METHODS_Bull": 94,
    #         "CDLRISEFALL3METHODS_Bear": 89,
    #         "CDLKICKING_Bull": 96,
    #         "CDLKICKING_Bear": 102,
    #         "CDLDRAGONFLYDOJI_Bull": 98,
    #         "CDLDRAGONFLYDOJI_Bear": 98,
    #         "CDLCONCEALBABYSWALL_Bull": 101,
    #         "CDLCONCEALBABYSWALL_Bear": 101,
    #         "CDL3STARSINSOUTH_Bull": 103,
    #         "CDL3STARSINSOUTH_Bear": 103,
    #         "CDLDOJI_Bull": 104,
    #         "CDLDOJI_Bear": 104
    #     }

    # actual_df['candlestick_pattern'] = np.nan
    # actual_df['candlestick_match_count'] = np.nan
    # for index, row in actual_df.iterrows():

    #     # no pattern found
    #     if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
    #         actual_df.loc[index,'candlestick_pattern'] = "NO_PATTERN"
    #         actual_df.loc[index, 'candlestick_match_count'] = 0
    #     # single pattern found
    #     elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
    #         # bull pattern 100 or 200
    #         if any(row[candle_names].values > 0):
    #             pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bull'
    #             actual_df.loc[index, 'candlestick_pattern'] = pattern
    #             actual_df.loc[index, 'candlestick_match_count'] = 1
    #         # bear pattern -100 or -200
    #         else:
    #             pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bear'
    #             actual_df.loc[index, 'candlestick_pattern'] = pattern
    #             actual_df.loc[index, 'candlestick_match_count'] = 1
    #     # multiple patterns matched -- select best performance
    #     else:
    #         # filter out pattern names from bool list of values
    #         patterns = list(compress(row[candle_names].keys(), row[candle_names].values != 0))
    #         container = []
    #         for pattern in patterns:
    #             if row[pattern] > 0:
    #                 container.append(pattern + '_Bull')
    #             else:
    #                 container.append(pattern + '_Bear')
    #         rank_list = [candle_rankings[p] for p in container]
    #         if len(rank_list) == len(container):
    #             rank_index_best = rank_list.index(min(rank_list))
    #             actual_df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
    #             actual_df.loc[index, 'candlestick_match_count'] = len(container)
    # # clean up candle columns
    # actual_df.drop(candle_names, axis = 1, inplace = True)

    # o = actual_df['Open'].astype(float)
    # h = actual_df['High'].astype(float)
    # l = actual_df['Low'].astype(float)
    # c = actual_df['Close'].astype(float)

    # # Formatting the Title column
    # title_list = []
    # print(actual_df.columns)
    # # for title in actual_df['Title']:
    # #   # print(repr(title))
    # #   # print(title[1:-1].replace("\n ","<br>"))
    # #   # print(title[1:-1].replace("\n ","<br>").count("\""),title[1:-1].replace("\n ","<br>").count("'"))
    # #   # print()
    # #   title_list.append(title[1:-1].replace("\n ","<br>"))


    # trace = go.Candlestick(
    #             x = actual_df['Date'],
    #             open=o,
    #             high=h,
    #             low=l,
    #             close=c,
    #             name='candles',
    #             # text="Pattern: "
    #             # +actual_df['candlestick_pattern']+"<br>Recent News:<br>"+title_list
    #           )
    # data = [trace]
    # fig = go.Figure(data)

    # fig.update_layout(
    #     title=f"{company} Candlestick Chart",
    #     # xaxis_title="Time",
    #     yaxis_title="Stock Price",
    #     legend_title="Legend",
    #     font=dict(
    #         family="Arial",
    #         size=18,
    #         color="black"
    #     )
    # )

    # # Remove range slider; (short time frame)
    # fig.update(layout_xaxis_rangeslider_visible=False)
    # # fig.show()

    # # Create subplots with 2 rows; top for candlestick price, and bottom for bar volume
    # fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ('Price', 'Volume'), vertical_spacing = 0.1, row_width = [0.2, 0.7])

    # o = actual_df['Open'].astype(float)
    # h = actual_df['High'].astype(float)
    # l = actual_df['Low'].astype(float)
    # c = actual_df['Close'].astype(float)

    # upperband, middleband, lowerband = BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    # trace = go.Candlestick(
    #             x = actual_df['Date'],
    #             open=o,
    #             high=h,
    #             low=l,
    #             close=c,
    #             name='candles',
    #             # text="Pattern: "+actual_df['candlestick_pattern']+"<br>Recent News:<br>"+title_list
    #           )
    # data = [trace]
    # # fig = go.Figure(data)
    # fig.add_trace(go.Scatter(y=middleband,
    #                         x = actual_df['Date'],
    #                     mode='lines',
    #                     name='middleband',
    #                     line_color='black'
    #                     ), row=1, col=1)
    # fig.add_trace(go.Scatter(y=upperband,
    #                     x = actual_df['Date'],
    #                     mode='lines',
    #                     line_color = 'gray',
    #                     line = {'dash': 'dash'},
    #                     name='upperband'
    #                     ), row=1, col=1)
    # fig.add_trace(go.Scatter(y=lowerband,
    #                         x = actual_df['Date'],
    #                     mode='lines',
    #                     line_color = 'gray',
    #                     line = {'dash': 'dash'},
    #                     name='lowerband',
    #                     fill = 'tonexty',
    #                     # fillcolor = 'violet',
    #                     opacity=0.5), row=1, col=1)
    # fig.add_trace(go.Candlestick(
    #             x = actual_df['Date'],
    #             open=o,
    #             high=h,
    #             low=l,
    #             close=c,
    #             name='candles',
    #             # text=actual_df['candlestick_pattern']
    #           ), row=1, col=1)

    # # ----------------
    # # Volume Plot
    # fig.add_trace(go.Bar(x = actual_df['Date'], y = actual_df['Volume'], showlegend=False), 
    #               row = 2, col = 1)

    # fig.update_yaxes(title_text="Price", row=1, col=1)
    # fig.update_yaxes(title_text="Volume", row=2, col=1)
    # fig.update_layout(
    #     title="ONGC Candlestick Chart with Bollinger Band",
    #     legend_title="Legend",
    #     font=dict(
    #         family="Arial",
    #         size=14,
    #         color="black"
    #     )
    # )

    # # Remove range slider; (short time frame)
    # fig.update(layout_xaxis_rangeslider_visible=False)
    # # fig.show()
    # plot(data, filename='go_candle1.html')
    # ts_df = candles(symbol)
    #PlotlyGraph
    def candlestick():
          op = actual_df['Open']
          hi = actual_df['High']
          lo = actual_df['Low']
          cl = actual_df['Close']
          # create columns for each pattern

          candle_names = talib.get_function_groups()['Pattern Recognition']
          print(len(candle_names))
          remove = [
                    'CounterAttack', 
                    'Longline', 
                    'Shortline', 
                    'Stalledpattern', 
                    'Kickingbylength'
                    ]
          remove = ['CDL'+x.upper() for x in remove]
          if len(candle_names) > 56 :
            for item in remove:
              # print(item in candle_names)
              candle_names.remove(item)

          # print(len(candle_names))

          for candle in candle_names:
            actual_df[candle] = getattr(talib, candle)(op, hi, lo, cl)


          candle_rankings = {
                  "CDL3LINESTRIKE_Bull": 1,
                  "CDL3LINESTRIKE_Bear": 2,
                  "CDL3BLACKCROWS_Bull": 3,
                  "CDL3BLACKCROWS_Bear": 3,
                  "CDLEVENINGSTAR_Bull": 4,
                  "CDLEVENINGSTAR_Bear": 4,
                  "CDLTASUKIGAP_Bull": 5,
                  "CDLTASUKIGAP_Bear": 5,
                  "CDLINVERTEDHAMMER_Bull": 6,
                  "CDLINVERTEDHAMMER_Bear": 6,
                  "CDLMATCHINGLOW_Bull": 7,
                  "CDLMATCHINGLOW_Bear": 7,
                  "CDLABANDONEDBABY_Bull": 8,
                  "CDLABANDONEDBABY_Bear": 8,
                  "CDLBREAKAWAY_Bull": 10,
                  "CDLBREAKAWAY_Bear": 10,
                  "CDLMORNINGSTAR_Bull": 12,
                  "CDLMORNINGSTAR_Bear": 12,
                  "CDLPIERCING_Bull": 13,
                  "CDLPIERCING_Bear": 13,
                  "CDLSTICKSANDWICH_Bull": 14,
                  "CDLSTICKSANDWICH_Bear": 14,
                  "CDLTHRUSTING_Bull": 15,
                  "CDLTHRUSTING_Bear": 15,
                  "CDLINNECK_Bull": 17,
                  "CDLINNECK_Bear": 17,
                  "CDL3INSIDE_Bull": 20,
                  "CDL3INSIDE_Bear": 56,
                  "CDLHOMINGPIGEON_Bull": 21,
                  "CDLHOMINGPIGEON_Bear": 21,
                  "CDLDARKCLOUDCOVER_Bull": 22,
                  "CDLDARKCLOUDCOVER_Bear": 22,
                  "CDLIDENTICAL3CROWS_Bull": 24,
                  "CDLIDENTICAL3CROWS_Bear": 24,
                  "CDLMORNINGDOJISTAR_Bull": 25,
                  "CDLMORNINGDOJISTAR_Bear": 25,
                  "CDLXSIDEGAP3METHODS_Bull": 27,
                  "CDLXSIDEGAP3METHODS_Bear": 26,
                  "CDLTRISTAR_Bull": 28,
                  "CDLTRISTAR_Bear": 76,
                  "CDLGAPSIDESIDEWHITE_Bull": 46,
                  "CDLGAPSIDESIDEWHITE_Bear": 29,
                  "CDLEVENINGDOJISTAR_Bull": 30,
                  "CDLEVENINGDOJISTAR_Bear": 30,
                  "CDL3WHITESOLDIERS_Bull": 32,
                  "CDL3WHITESOLDIERS_Bear": 32,
                  "CDLONNECK_Bull": 33,
                  "CDLONNECK_Bear": 33,
                  "CDL3OUTSIDE_Bull": 34,
                  "CDL3OUTSIDE_Bear": 39,
                  "CDLRICKSHAWMAN_Bull": 35,
                  "CDLRICKSHAWMAN_Bear": 35,
                  "CDLSEPARATINGLINES_Bull": 36,
                  "CDLSEPARATINGLINES_Bear": 40,
                  "CDLLONGLEGGEDDOJI_Bull": 37,
                  "CDLLONGLEGGEDDOJI_Bear": 37,
                  "CDLHARAMI_Bull": 38,
                  "CDLHARAMI_Bear": 72,
                  "CDLLADDERBOTTOM_Bull": 41,
                  "CDLLADDERBOTTOM_Bear": 41,
                  "CDLCLOSINGMARUBOZU_Bull": 70,
                  "CDLCLOSINGMARUBOZU_Bear": 43,
                  "CDLTAKURI_Bull": 47,
                  "CDLTAKURI_Bear": 47,
                  "CDLDOJISTAR_Bull": 49,
                  "CDLDOJISTAR_Bear": 51,
                  "CDLHARAMICROSS_Bull": 50,
                  "CDLHARAMICROSS_Bear": 80,
                  "CDLADVANCEBLOCK_Bull": 54,
                  "CDLADVANCEBLOCK_Bear": 54,
                  "CDLSHOOTINGSTAR_Bull": 55,
                  "CDLSHOOTINGSTAR_Bear": 55,
                  "CDLMARUBOZU_Bull": 71,
                  "CDLMARUBOZU_Bear": 57,
                  "CDLUNIQUE3RIVER_Bull": 60,
                  "CDLUNIQUE3RIVER_Bear": 60,
                  "CDL2CROWS_Bull": 61,
                  "CDL2CROWS_Bear": 61,
                  "CDLBELTHOLD_Bull": 62,
                  "CDLBELTHOLD_Bear": 63,
                  "CDLHAMMER_Bull": 65,
                  "CDLHAMMER_Bear": 65,
                  "CDLHIGHWAVE_Bull": 67,
                  "CDLHIGHWAVE_Bear": 67,
                  "CDLSPINNINGTOP_Bull": 69,
                  "CDLSPINNINGTOP_Bear": 73,
                  "CDLUPSIDEGAP2CROWS_Bull": 74,
                  "CDLUPSIDEGAP2CROWS_Bear": 74,
                  "CDLGRAVESTONEDOJI_Bull": 77,
                  "CDLGRAVESTONEDOJI_Bear": 77,
                  "CDLHIKKAKEMOD_Bull": 82,
                  "CDLHIKKAKEMOD_Bear": 81,
                  "CDLHIKKAKE_Bull": 85,
                  "CDLHIKKAKE_Bear": 83,
                  "CDLENGULFING_Bull": 84,
                  "CDLENGULFING_Bear": 91,
                  "CDLMATHOLD_Bull": 86,
                  "CDLMATHOLD_Bear": 86,
                  "CDLHANGINGMAN_Bull": 87,
                  "CDLHANGINGMAN_Bear": 87,
                  "CDLRISEFALL3METHODS_Bull": 94,
                  "CDLRISEFALL3METHODS_Bear": 89,
                  "CDLKICKING_Bull": 96,
                  "CDLKICKING_Bear": 102,
                  "CDLDRAGONFLYDOJI_Bull": 98,
                  "CDLDRAGONFLYDOJI_Bear": 98,
                  "CDLCONCEALBABYSWALL_Bull": 101,
                  "CDLCONCEALBABYSWALL_Bear": 101,
                  "CDL3STARSINSOUTH_Bull": 103,
                  "CDL3STARSINSOUTH_Bear": 103,
                  "CDLDOJI_Bull": 104,
                  "CDLDOJI_Bear": 104
              }

          actual_df['candlestick_pattern'] = np.nan
          actual_df['candlestick_match_count'] = np.nan
          for index, row in actual_df.iterrows():

              # no pattern found
              if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
                  actual_df.loc[index,'candlestick_pattern'] = "NO_PATTERN"
                  actual_df.loc[index, 'candlestick_match_count'] = 0
              # single pattern found
              elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
                  # bull pattern 100 or 200
                  if any(row[candle_names].values > 0):
                      pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bull'
                      actual_df.loc[index, 'candlestick_pattern'] = pattern
                      actual_df.loc[index, 'candlestick_match_count'] = 1
                  # bear pattern -100 or -200
                  else:
                      pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bear'
                      actual_df.loc[index, 'candlestick_pattern'] = pattern
                      actual_df.loc[index, 'candlestick_match_count'] = 1
              # multiple patterns matched -- select best performance
              else:
                  # filter out pattern names from bool list of values
                  patterns = list(compress(row[candle_names].keys(), row[candle_names].values != 0))
                  container = []
                  for pattern in patterns:
                      if row[pattern] > 0:
                          container.append(pattern + '_Bull')
                      else:
                          container.append(pattern + '_Bear')
                  rank_list = [candle_rankings[p] for p in container]
                  if len(rank_list) == len(container):
                      rank_index_best = rank_list.index(min(rank_list))
                      actual_df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
                      actual_df.loc[index, 'candlestick_match_count'] = len(container)
          # clean up candle columns
          actual_df.drop(candle_names, axis = 1, inplace = True)

          o = actual_df['Open'].astype(float)
          h = actual_df['High'].astype(float)
          l = actual_df['Low'].astype(float)
          c = actual_df['Close'].astype(float)

          # Formatting the Title column
          title_list = []
          # print(actual_df.columns)
          # for title in actual_df['Title']:
          #   # print(repr(title))
          #   # print(title[1:-1].replace("\n ","<br>"))
          #   # print(title[1:-1].replace("\n ","<br>").count("\""),title[1:-1].replace("\n ","<br>").count("'"))
          #   # print()
          #   title_list.append(title[1:-1].replace("\n ","<br>"))


          trace = go.Candlestick(
                      x = actual_df['Date'],
                      open=o,
                      high=h,
                      low=l,
                      close=c,
                      name='candles',
                      # text="Pattern: "
                      # +actual_df['candlestick_pattern']+"<br>Recent News:<br>"+title_list
                    )
          data = [trace]
          fig = go.Figure(data)

          fig.update_layout(
              title=f"{company} Candlestick Chart",
              # xaxis_title="Time",
              yaxis_title="Stock Price",
              legend_title="Legend",
              font=dict(
                  family="Arial",
                  size=18,
                  color="black"
              )
          )

          # Remove range slider; (short time frame)
          fig.update(layout_xaxis_rangeslider_visible=False)
          # fig.show()

          # Create subplots with 2 rows; top for candlestick price, and bottom for bar volume
          fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ('Price', 'Volume'), vertical_spacing = 0.1, row_width = [0.2, 0.7])

          o = actual_df['Open'].astype(float)
          h = actual_df['High'].astype(float)
          l = actual_df['Low'].astype(float)
          c = actual_df['Close'].astype(float)

          upperband, middleband, lowerband = BBANDS(c, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

          trace = go.Candlestick(
                      x = actual_df['Date'],
                      open=o,
                      high=h,
                      low=l,
                      close=c,
                      name='candles',
                      # text="Pattern: "+actual_df['candlestick_pattern']+"<br>Recent News:<br>"+title_list
                    )
          data = [trace]
          # fig = go.Figure(data)
          fig.add_trace(go.Scatter(y=middleband,
                                  x = actual_df['Date'],
                              mode='lines',
                              name='middleband',
                              line_color='black'
                              ), row=1, col=1)
          fig.add_trace(go.Scatter(y=upperband,
                              x = actual_df['Date'],
                              mode='lines',
                              line_color = 'gray',
                              line = {'dash': 'dash'},
                              name='upperband'
                              ), row=1, col=1)
          fig.add_trace(go.Scatter(y=lowerband,
                                  x = actual_df['Date'],
                              mode='lines',
                              line_color = 'gray',
                              line = {'dash': 'dash'},
                              name='lowerband',
                              fill = 'tonexty',
                              # fillcolor = 'violet',
                              opacity=0.5), row=1, col=1)
          fig.add_trace(go.Candlestick(
                      x = actual_df['Date'],
                      open=o,
                      high=h,
                      low=l,
                      close=c,
                      name='candles',
                      # text=actual_df['candlestick_pattern']
                    ), row=1, col=1)

          # ----------------
          # Volume Plot
          fig.add_trace(go.Bar(x = actual_df['Date'], y = actual_df['Volume'], showlegend=False), 
                        row = 2, col = 1)

          fig.update_yaxes(title_text="Price", row=1, col=1)
          fig.update_yaxes(title_text="Volume", row=2, col=1)
          fig.update_layout(
              title="HDFC Candlestick Chart with Bollinger Band",
              legend_title="Legend",
              font=dict(
                  family="Arial",
                  size=14,
                  color="black"
              )
          )

          # Remove range slider; (short time frame)
          fig.update(layout_xaxis_rangeslider_visible=False)
          # fig.show()
          # fig1 = (
          #   go.Figure(
          #     data = [
          #             go.Candlestick(
          #               # x = ts_df.index,
          #               x = ts_df['Date'],
          #               high = ts_df['High'],
          #               low = ts_df['Low'],
          #               open = ts_df['Open'],
          #               close = ts_df['Close'],
          #             )
          #           ]
          # )
          # )

          o = actual_df['Open'].astype(float)
          h = actual_df['High'].astype(float)
          l = actual_df['Low'].astype(float)
          c = actual_df['Close'].astype(float)

          # Formatting the Title column
          title_list = []
          # for title in actual_df['Title']:
          #   # print(repr(title))
          #   # print(title[1:-1].replace("\n ","<br>"))
          #   # print(title[1:-1].replace("\n ","<br>").count("\""),title[1:-1].replace("\n ","<br>").count("'"))
          #   # print()
          #   title_list.append(title[1:-1].replace("\n ","<br>"))


          trace = go.Candlestick(
                      x = actual_df['Date'],
                      open=o,
                      high=h,
                      low=l,
                      close=c,
                      name='candles',
                      # text="Pattern: "+actual_df['candlestick_pattern']+"<br>Recent News:<br>"+title_list
                    )
          data = [trace]
          fig1 = go.Figure(data)

          fig1.update_layout(
              title=f"{company} Candlestick Chart",
              # xaxis_title="Time",
              yaxis_title="Stock Price",
              legend_title="Legend",
              font=dict(
                  family="Arial",
                  size=18,
                  color="black"
              )
          )

          # Remove range slider; (short time frame)
          fig1.update(layout_xaxis_rangeslider_visible=False)

          actual_close = actual_df[['Date','Close']]
          pred_close = pred_df[['Date','Close']]

          combined_close = pd.concat([actual_close,pred_close])

          fig2 = make_subplots(rows = 2, cols = 1, shared_xaxes = True, subplot_titles = ('MACD', 'RSI'), vertical_spacing = 0.1, row_width = [0.2, 0.7])

          c = combined_close['Close'].astype(float)
          macd, macdsignal, macdhist = MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)

          color = ['green' if x>=0 else 'red' for x in macdhist]

          fig2.add_trace(go.Scatter(y=macd,
                                    x=combined_close['Date'],
                              mode='lines',
                              name='MACD'), row=1, col=1)
          fig2.add_trace(go.Scatter(y=macdsignal,
                                    x=combined_close['Date'],
                              mode='lines',
                              name='Signal'), row=1, col=1)
          fig2.add_trace(go.Bar(y=macdhist,
                              x=combined_close['Date'],
                              name='MACD Hist',
                              marker_color = color,
                              showlegend=False,
                              ), row=1, col=1)
          fig2.add_vline(x=pred_close['Date'][0], line_dash="dash", row=1, col=1)

          # RSI Plot
          real = RSI(c, timeperiod=14)
          fig2.add_trace(go.Scatter(y=real,
                                    x=combined_close['Date'],
                              mode='lines',
                              name='RSI'), row=2, col=1)
          fig2.add_hline(y=30, line_dash="dot", row=2, col=1)
          fig2.add_hline(y=70, line_dash="dot", row=2, col=1)
          fig2.add_vline(x=pred_close['Date'][0], line_dash="dash", row=2, col=1)


          fig2.update_yaxes(title_text="MACD", row=1, col=1)
          fig2.update_yaxes(title_text="RSI", row=2, col=1)

          fig2.update_layout(
              title="MACD AND RSI for HDFC Bank ",
              legend_title="Legend",
              font=dict(
                  family="Arial",
                  size=14,
                  color="black"
              )
          )

          # Remove range slider; (short time frame)
          fig2.update(layout_xaxis_rangeslider_visible=False)

          candlestick_div = []

          candlestick_div.append(plot(fig, output_type='div'))
          candlestick_div.append(plot(fig1, output_type='div'))
          candlestick_div.append(plot(fig2, output_type='div'))
          return candlestick_div
    #endPlotlyGraph
    # percentchange = pricedata['priceChangePercent']
    # buyers = pricedata['askQty']
    # sellers = pricedata['bidQty']

    # print(f'''
    # pricedata : {pricedata}
    # buyers: {buyers}
    # sellers: {sellers}
    # ''')

    fav1 = spotquote(symbol='HDFCBANK.BSE')
    fav2 = spotquote(symbol="AXISBANK.BSE")
    fav3 = spotquote(symbol="ICICIBANK.BSE")

    candlestick_div = candlestick()

    technical_analysis_context = technical_analysis(company_tech)
    
    charts_context={
    'moredata': moredata,
    'fav1': fav1,
    'fav2': fav2,
    'fav3': fav3,
    # 'percentchange': percentchange,
    # 'buyers': buyers,
    # 'sellers': sellers,
    'data': data,
    'candlestick0': candlestick_div[0],
    'candlestick1': candlestick_div[1],
    'candlestick2': candlestick_div[2],
    }
    context = dict(charts_context, **technical_analysis_context)
    return render(request, 'dashboard/crypto.html', context)








def homeView(request):
  if request.method == 'POST':
      symbol = request.POST.get('symbol')
      return redirect('crypto/')

  context={}
  return render(request, 'dashboard/home_page.html', context)

def aboutView(request):
  if request.method == 'POST':
      symbol = request.POST.get('symbol')
      return redirect('crypto/')

  context={}
  return render(request, 'dashboard/about_us.html', context)


def contactView(request):
  if request.method == 'POST':
      symbol = request.POST.get('symbol')
      return redirect('crypto/')

  context={}
  return render(request, 'dashboard/contact_us.html', context)


# def technical_analysis(request, company):
def technical_analysis(company):
  file_path = f"indicators_{company}.csv"
  indicators_csv = pd.read_csv(file_path)

  def rsi_gauge(latest_rsi):

    rsi_degrees, advice = 90, 'neutral'
    if latest_rsi < 30:
      rsi_degrees, advice = 30, 'buy'
    elif latest_rsi > 70:
      rsi_degrees, advice = 150, 'sell'
      
    fig = go.Figure(
      go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = latest_rsi,
        number = {'suffix': "<br>"+advice+"<br>", "prefix": ""},
        mode = "gauge+number",
        # mode = "gauge",
        # title = {'text': f"<span style=font-size:22px>RSI<br><b>{advice}</b></span>"},
        title = {'text': f"<span style=font-size:22px>RSI</span>"},
        # delta = {'reference': 380},        
        gauge = {'axis': {'range': [None, 180], "visible": False},
                  'borderwidth': 15,
                  'bordercolor': "white",  
                  'steps' : [
                      {'range': [0, 60], 'color': "red", 'name':"buy"},
                      {'range': [60, 120], 'color': "lightgray"},
                      {'range': [120, 180], 'color': "green"}
                  ],
                  'threshold' : {
                    'line': {'color': "black", 'width': 10}, 
                    'thickness': 1, 
                    'value': rsi_degrees
                  },
                  'bar' : {
                      'thickness': 0,
                      # 'color': 'blue'
                  }
        }
        
      )
    )

    rsi_gauge_div = plot(fig, output_type='div')
    return rsi_gauge_div, advice
  
  
  # MACD crosses above signal line then buy
  # MACD crosses below MACD signal line then sell
  def macd_gauge():
    # finding the next predicted crossover

    # number of predictions
    no_pred = 60
    pred_df = indicators_csv.iloc[-1*no_pred:]
    macd, signal = pred_df['macd'].tolist(), pred_df['macdsignal'].tolist()
    gr = 0
    if macd[0] >= signal[0]:
      gr = 1 #macd is greater
    else:
      gr = 2 #signal is greater

    crossover_dict = {'buy': [], 'sell': []}
    for i in range(1,60):
      if gr == 1 and macd[i] < signal[i]:
          crossover_dict['sell'].append(i)
          gr = 2
      elif gr == 2 and macd[i] > signal[i]:
          crossover_dict['buy'].append(i)
          gr = 1

    crossover_pts =  sum(crossover_dict.values(), [])
    if len(crossover_pts) == 0:
      macd_advice, macd_degrees = 'neutral', 90
      crossover_macd, crossover_macdsignal = None, None
    else:
      upcoming_crossover = min(crossover_pts)
      macd_advice = 'buy' if upcoming_crossover in crossover_dict['buy'] else 'sell'
      crossover_macd, crossover_macdsignal = macd[upcoming_crossover], signal[upcoming_crossover]
      if macd_advice == 'buy':
        macd_degrees = 30
      elif macd_advice == 'sell':
        macd_degrees = 150

    fig = go.Figure(
      go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = crossover_macdsignal,
        number = {'prefix': f"MACD: {crossover_macd:.2f}<br>Signal: ", 
          "suffix": f'<br>{macd_advice}',
          # "font":{
          #   "size": 16
          # }
        },
        mode = "gauge+number+delta",
        title = {'text': "MACD"},
        # delta = {'reference': crossover_macd, 'position': 'top'},        
        gauge = {'axis': {'range': [None, 180], "visible": False},
                  'borderwidth': 15,
                  'bordercolor': "white",  
                  'steps' : [
                      {'range': [0, 60], 'color': "red", 'name':"buy"},
                      {'range': [60, 120], 'color': "lightgray"},
                      {'range': [120, 180], 'color': "green"}
                  ],
                  'threshold' : {
                    'line': {'color': "black", 'width': 10}, 
                    'thickness': 1, 
                    'value': macd_degrees
                  },
                  'bar' : {
                      'thickness': 0,
                  }
        }
        
      )
    )

    macd_gauge_div = plot(fig, output_type='div')
    return macd_gauge_div, macd_advice

  latest_rsi = indicators_csv.iloc[-1]['rsi']
  rsi_gauge_div, rsi_advice = rsi_gauge(latest_rsi)
  macd_gauge_div, macd_advice = macd_gauge()

  context = {
    'gauges': [
      {'indicator':'rsi', 'chart_div': rsi_gauge_div, 'advice': rsi_advice}, 
      {'indicator':' macd', 'chart_div': macd_gauge_div,'advice': macd_advice}
    ],
    'advice': [
      {'indicator':'rsi', 'advice': rsi_advice}, 
      {'indicator':' macd', 'advice': macd_advice}
    ]
  }
  
  return context
  # return render(request, 'dashboard/technicalanalysis.html', context)
