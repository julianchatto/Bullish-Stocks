import yfinance as yf
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  

def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=False).mean()

def plotData(data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Closing Price')
    plt.plot(data.index, data['12-day EMA'], label='12-day EMA', color='orange')
    plt.plot(data.index, data['26-day EMA'], label='26-day EMA', color='green')
    plt.plot(data.index, data['55-day EMA'], label='55-day EMA', color='yellow')
    plt.plot(data.index, data['100-day EMA'], label='100-day EMA', color='red')
    plt.title(f'{ticker} Exponential Moving Average (EMA)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

for ticker in tickers:
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    data['12-day EMA'] = calculate_ema(data, 12)
    data['26-day EMA'] = calculate_ema(data, 26)
    data['55-day EMA'] = calculate_ema(data, 55)
    data['100-day EMA'] = calculate_ema(data, 100)
    plotData(data, ticker)