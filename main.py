import yfinance as yf
import pandas as pd

# Define the trading strategy
def moving_average_crossover(symbol):
    # Download historical stock data
    data = yf.download(symbol, start='2021-01-01', end='2021-12-31')

    # Calculate moving averages
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # Generate trading signals
    data['Signal'] = 0
    data.loc[data['MA50'] > data['MA200'], 'Signal'] = 1
    data.loc[data['MA50'] < data['MA200'], 'Signal'] = -1

    # Calculate daily returns
    data['Return'] = data['Close'].pct_change()

    # Calculate position
    data['Position'] = data['Signal'].shift()

    # Simulate trades and calculate strategy returns
    data['StrategyReturn'] = data['Position'] * data['Return']

    # Calculate cumulative returns
    data['CumulativeReturn'] = (1 + data['StrategyReturn']).cumprod()

    return data

# Execute the trading strategy
symbol = 'AAPL'  # Replace with the desired stock symbol
strategy_data = moving_average_crossover(symbol)

# Print the strategy performance
print(strategy_data[['Close', 'MA50', 'MA200', 'Signal', 'Return', 'StrategyReturn', 'CumulativeReturn']])
