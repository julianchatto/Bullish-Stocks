import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

ema_params = [
    ('21-day EMA', 'orange', 21),
    # ('33-day EMA', 'green', 33),
    ('55-day EMA', 'yellow', 50),
    # ('100-day EMA', 'red', 100)
]

# calculate Exponential Moving Average
def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=True).mean()

# plot closing price with EMAs
def plotData(data, ticker):
    fig = plt.figure(figsize=(12,6))
    ax1 = fig.add_subplot(111, ylabel='Price in $')

    data['Close'].plot(ax=ax1, color='b', lw=2.)
    data['21-day EMA'].plot(ax=ax1, color='green', lw=2.)
    data['55-day EMA'].plot(ax=ax1, color='red', lw=2.)

    ax1.plot(data.loc[data.crossover == 1.0].index, 
            data.Close[data.crossover == 1.0],
            '^', markersize=10, color='g')
    ax1.plot(data.loc[data.crossover == -1.0].index, 
            data.Close[data.crossover == -1.0],
            'v', markersize=10, color='r')
    plt.legend(['Close', '21-day EMA', '55-day EMA', 'Buy', 'Sell'])
    plt.title(f'{ticker} Exponential Moving Average Crossover')
    plt.show()

# Scrape S&P 500 tickers
def get_sp500():
    url = 'https://www.slickcharts.com/sp500'
    request = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs(request.text, "lxml")
    stats = soup.find('table',class_='table table-hover table-borderless table-sm')
    df = pd.read_html(str(stats))[0]
    df['% Chg'] = df['% Chg'].str.strip('()-%')
    df['% Chg'] = pd.to_numeric(df['% Chg'])
    df['Chg'] = pd.to_numeric(df['Chg'])
    return df['Symbol'].tolist()

def main():
    tickers = get_sp500()
    bullish = []
    bearish = []
    for ticker in tickers:
        try: 
            stock = yf.Ticker(ticker)
            data = stock.history(period="1y")
            
            for ema_label, _, window in ema_params:
                data[ema_label] = calculate_ema(data, window)

            data['bullish'] = 0.0
            data['bullish'] = np.where(data['21-day EMA'] > data['55-day EMA'], 1.0, 0.0)
            data['crossover'] = data['bullish'].diff()
            
            if (data['21-day EMA'].iloc[-1] > data['55-day EMA'].iloc[-1]):
                bullish.append(ticker)
            else:
                bearish.append(ticker)
        except: 
            print("Error: ", ticker)
            continue
        

        # plotData(data, ticker)
        
    with open("bullish.txt", 'w') as f:
        for stock in bullish:
            f.write(f"{stock}\n")
        f.close()
            
    with open("bearish.txt", 'w') as f:
        for stock in bearish:
            f.write(f"{stock}\n")
        f.close()
    
main()