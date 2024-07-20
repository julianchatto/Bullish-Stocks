import yfinance as yf
import mplfinance as mpf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=False).mean()

def plotData(data, ticker):
    # Calculate the Exponential Moving Averages (EMAs)
    data['21-day EMA'] = calculate_ema(data, 21)
    data['33-day EMA'] = calculate_ema(data, 33)
    data['55-day EMA'] = calculate_ema(data, 55)
    data['100-day EMA'] = calculate_ema(data, 100)

    # Plotting the data using mplfinance
    emaplot = [
        mpf.make_addplot(data['21-day EMA'], color='orange', width=1),
        mpf.make_addplot(data['33-day EMA'], color='green', width=1),
        mpf.make_addplot(data['55-day EMA'], color='yellow', width=1),
        mpf.make_addplot(data['100-day EMA'], color='red', width=1)
    ]

    mpf.plot(data, type='candle', style='charles', title=f'{ticker} Exponential Moving Average (EMA)',
             ylabel='Price', addplot=emaplot, volume=True)

for ticker in tickers:
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    plotData(data, ticker)