import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import ta
import mplfinance as mpf
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

from flask import Flask, render_template, request
app = Flask(__name__)

# list of stock symbols
stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN','TSLA',
    'IBM',
    'NFLX',
    'NVDA',
    'SQ',
    'SNAP',
    'LYFT',
    'UBER',
    'ZM',
    'PINS',
    'TWTR',
    'ETSY',
    'MVIS',
    'PLUG',
    'SNDL',
    'AMC',
    'BB',
    'NIO',
    'RKT',
    'WKHS']

# stock data with PE ratio
def fetch_stock_data():
    stock_data = {}
    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        history = stock.history(period='1y')
        pe_ratio = stock.info.get('trailingPE')
        stock_data[symbol] = {'history': history, 'pe_ratio': pe_ratio}
    return stock_data

#  displaying stock data with PE ratio
@app.route('/stock_data', methods=['GET'])
def display_stock_data():
    stock_data = fetch_stock_data()
    return render_template('stock_data.html', stocks=stock_data)

if __name__ == '__main__':
    app.run(debug=True)
app = Flask(__name__)

# stock symbols to market cap values
stocks_market_cap = {
    'AAPL': 'Large Cap',
    'GOOGL': 'Large Cap',
    'MSFT': 'Large Cap',
    'AMZN': 'Large Cap',
    'TSLA': 'Large Cap',
    'IBM': 'Large Cap',
    'NFLX': 'Large Cap',
    'NVDA': 'Large Cap',
    'SQ': 'Mid Cap',
    'SNAP': 'Mid Cap',
    'LYFT': 'Mid Cap',
    'UBER': 'Mid Cap',
    'ZM': 'Mid Cap',
    'PINS': 'Mid Cap',
    'TWTR': 'Mid Cap',
    'ETSY': 'Mid Cap',
    'MVIS': 'Small Cap',
    'PLUG': 'Small Cap',
    'SNDL': 'Small Cap',
    'AMC': 'Small Cap',
    'BB': 'Small Cap',
    'NIO': 'Small Cap',
    'RKT': 'Small Cap',
    'WKHS': 'Small Cap'
}

# Route for displaying stock data with filters
@app.route('/stock_data', methods=['GET'])
def stock_data():
    # Get the filter values from the request parameters
    market_cap = request.args.get('market_cap')

    # Filter stocks based on market cap
    if market_cap == 'largecap':
        filtered_stocks = [symbol for symbol, cap in stocks_market_cap.items() if cap == 'Large Cap']
    elif market_cap == 'midcap':
        filtered_stocks = [symbol for symbol, cap in stocks_market_cap.items() if cap == 'Mid Cap']
    elif market_cap == 'smallcap':
        filtered_stocks = [symbol for symbol, cap in stocks_market_cap.items() if cap == 'Small Cap']
    else:
        filtered_stocks = stocks_market_cap.keys()

    # Fetch the stock data for filtered stocks
    stock_data = {}
    for symbol in filtered_stocks:
        stock = yf.Ticker(symbol)
        stock_data[symbol] = stock.history(period='1y')

    return render_template('stock_data.html', stocks=stock_data, market_cap=market_cap)


if __name__ == '__main__':
    app.run(debug=True)

import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# Fetch stock data
symbol = ['AAPL', 'GOOGL', 'MSFT', 'AMZN','TSLA',
    'IBM',
    'NFLX',
    'NVDA',
    'SQ',
    'SNAP',
    'LYFT',
    'UBER',
    'ZM',
    'PINS',
    'TWTR',
    'ETSY',
    'MVIS',
    'PLUG',
    'SNDL',
    'AMC',
    'BB',
    'NIO',
    'RKT',
    'WKHS']
stock = yf.Ticker(symbol)
history = stock.history(period='1d')

#  The candlestick chart
mpf.plot(history, type='candle', title=f'Candlestick Chart - {symbol}', ylabel='Price', show_nontrading=False)

#  moving averages
history['MA20'] = history['Close'].rolling(window=20).mean()
history['MA50'] = history['Close'].rolling(window=50).mean()
plt.plot(history['MA20'], label='MA20')
plt.plot(history['MA50'], label='MA50')

#  MACD
exp12 = history['Close'].ewm(span=12, adjust=False).mean()
exp26 = history['Close'].ewm(span=26, adjust=False).mean()
history['MACD'] = exp12 - exp26
history['MACD_Signal'] = history['MACD'].ewm(span=9, adjust=False).mean()
plt.plot(history['MACD'], label='MACD')
plt.plot(history['MACD_Signal'], label='MACD Signal')

# Bollinger Bands
history['Bollinger_Middle'] = history['Close'].rolling(window=20).mean()
history['Bollinger_Std'] = history['Close'].rolling(window=20).std()
history['Bollinger_Upper'] = history['Bollinger_Middle'] + (2 * history['Bollinger_Std'])
history['Bollinger_Lower'] = history['Bollinger_Middle'] - (2 * history['Bollinger_Std'])
plt.plot(history['Bollinger_Upper'], label='Bollinger Upper')
plt.plot(history['Bollinger_Middle'], label='Bollinger Middle')
plt.plot(history['Bollinger_Lower'], label='Bollinger Lower')

# RSI
delta = history['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
relative_strength = avg_gain / avg_loss
history['RSI'] = 100 - (100 / (1 + relative_strength))
plt.plot(history['RSI'], label='RSI')

# Set chart title and labels
plt.title(f'Candlestick Chart with Indicators - {symbol}')
plt.xlabel('Date')
plt.ylabel('Price/Indicator')

# Add legend
plt.legend()

# Display the chart
plt.show()
