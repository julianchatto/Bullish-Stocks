import yfinance as yf
import matplotlib.pyplot as plt

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  

ema_params = [
    ('12-day EMA', 'orange', 12),
    ('26-day EMA', 'green', 26),
    ('55-day EMA', 'yellow', 55),
    ('100-day EMA', 'red', 100)
]

def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=False).mean()

def plotData(data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Closing Price')
    
    for ema_label, color, _ in ema_params:
        plt.plot(data.index, data[ema_label], label=ema_label, color=color)

    plt.title(f'{ticker} Exponential Moving Average (EMA)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

for ticker in tickers:
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    
    for ema_label, _, window in ema_params:
        data[ema_label] = calculate_ema(data, window)

    plotData(data, ticker)