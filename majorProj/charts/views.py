from django.shortcuts import render, redirect

#most dependencies and imports made in functions.py to avoid clutter
from .functions import *

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
    


def homeView(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        return redirect('crypto/')

    context={

    }
    return render(request, 'dashboard/index.html', context)



def cryptoView(request):

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

    actual_df = pd.read_csv(f'C:/Users/MONA/Desktop/Major Project/Performance-Analyzer/majorProj/combined_0imputed_HDFC_Bank_withDate.csv')
    ts_df = actual_df

    #get a fricken df
    # ts_df = candles(symbol)
    #PlotlyGraph
    def candlestick():
        figure = go.Figure(
            data = [
                    go.Candlestick(
                      # x = ts_df.index,
                      x = ts_df['Date'],
                      high = ts_df['High'],
                      low = ts_df['Low'],
                      open = ts_df['Open'],
                      close = ts_df['Close'],
                    )
                  ]
        )

        candlestick_div = plot(figure, output_type='div')
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

    print(f'''
    fav1: {fav1}''')

    context={
    'moredata': moredata,
    'fav1': fav1,
    'fav2': fav2,
    'fav3': fav3,
    # 'percentchange': percentchange,
    # 'buyers': buyers,
    # 'sellers': sellers,
    'data': data,
    'candlestick': candlestick(),
    }
    return render(request, 'dashboard/crypto.html', context)

def technical_analysis(request, company):

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
        # value = latest_rsi,
        # number = {'suffix': "<br>"+advice+"<br>", "prefix": "Rs."},
        # mode = "gauge+number",
        mode = "gauge",
        title = {'text': f"<span style=font-size:22px>RSI<br><b>{advice}</b></span>"},
        # delta = {'reference': 380},        
        gauge = {'axis': {'range': [None, 180], "visible": False},
                  'borderwidth': 20,
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
        value = crossover_macd,
        number = {'prefix': f"MACD: Rs.{crossover_macd:.2f} | Signal: Rs.", "suffix": f'<br>{macd_advice}'},
        mode = "gauge+number+delta",
        title = {'text': "MACD"},
        # delta = {'reference': crossover_macd, 'position': 'top'},        
        gauge = {'axis': {'range': [None, 180], "visible": False},
                  'borderwidth': 20,
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
  

  return render(request, 'dashboard/technicalanalysis.html', context)