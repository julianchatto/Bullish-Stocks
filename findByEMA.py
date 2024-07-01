import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  

# calculate EMA
def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

# Function to determine if stock is above EMAs
def is_above_ema(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    y_axis = []
    for i in range(1, 52):
        y_axis.append(calculate_ema(hist['Close'], i * 7).iloc[-1])
    df = pd.DataFrame({'x_axis': range(1, 52), 'y_axis': y_axis})
    plt.plot('x_axis', 'y_axis', data=df, linestyle='-', marker='o')
    plt.show()
    latest_price = hist['Close'].iloc[-1]

for ticker in tickers:
    is_above_ema(ticker)


