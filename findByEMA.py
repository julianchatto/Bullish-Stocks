import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  

# calculate EMA
def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

# Function to determine if stock is above EMAs
def is_above_ema(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")
    
    hist['EMA21'] = calculate_ema(hist['Close'], 21)
    hist['EMA33'] = calculate_ema(hist['Close'], 33)
    hist['EMA55'] = calculate_ema(hist['Close'], 55)

    latest_price = hist['Close'].iloc[-1]
    ema21 = hist['EMA21'].iloc[-1]
    ema33 = hist['EMA33'].iloc[-1]
    ema55 = hist['EMA55'].iloc[-1]
    print(ticker, ema21, ema33, ema55)

for ticker in tickers:
    is_above_ema(ticker)

