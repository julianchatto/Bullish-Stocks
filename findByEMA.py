import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  

ema_params = [
    ('21-day EMA', 'orange', 21),
    # ('33-day EMA', 'green', 33),
    ('55-day EMA', 'yellow', 50),
    # ('100-day EMA', 'red', 100)
]

def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=True).mean()

def plotData(data, ticker):
    fig = plt.figure(figsize=(12,6))
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    data['Close'].plot(ax=ax1, color='b', lw=2.)
    data['21-day EMA'].plot(ax=ax1, color='r', lw=2.)
    data['55-day EMA'].plot(ax=ax1, color='g', lw=2.)

    ax1.plot(data.loc[data.crossover == 1.0].index, 
            data.Close[data.crossover == 1.0],
            '^', markersize=10, color='g')
    ax1.plot(data.loc[data.crossover == -1.0].index, 
            data.Close[data.crossover == -1.0],
            'v', markersize=10, color='r')
    plt.legend(['Close', '21-day EMA', '55-day EMA', 'Buy', 'Sell'])
    plt.title(f'{ticker} Exponential Moving Average Crossover')
    plt.show()

for ticker in tickers:
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    
    for ema_label, _, window in ema_params:
        data[ema_label] = calculate_ema(data, window)

    data['bullish'] = 0.0
    data['bullish'] = np.where(data['21-day EMA'] > data['55-day EMA'], 1.0, 0.0)
    data['crossover'] = data['bullish'].diff()
    

    plotData(data, ticker)