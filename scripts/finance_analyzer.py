import plotly.express as px
import talib as ta
import yfinance as yf
import pandas as pd

class FinancialAnalyzer:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        
    def retrieve_stock_data(self):
        stock_data = yf.download(self.ticker, start=self.start_date, end=self.end_date, group_by='ticker')
        if stock_data.empty:
            raise ValueError(f"No data retrieved for {self.ticker} from {self.start_date} to {self.end_date}.")
        
        # Flatten MultiIndex    
        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = stock_data.columns.get_level_values(0)
        
        return stock_data
        

    
    def calculate_returns(self):
        stock_data = self.retrieve_stock_data()
        stock_data['Daily Return'] = stock_data['Adj Close'].pct_change()
        return stock_data['Daily Return']
    
    def calculate_moving_average(self, data, window_size):
        # Drop missing values to avoid dimension issues
        clean_data = data.dropna()
        # Ensure the array is 1D and pass to ta.SMA
        return ta.SMA(clean_data.to_numpy(), timeperiod=window_size)
    
    def technical_indicators(self, data):
        data = data.dropna(subset=['Close'])
        # Calculate various technical indicators
        data['Moving-average'] = self.calculate_moving_average(data['Close'], 20)
        data['Relative-strength-index'] = ta.RSI(data['Close'].to_numpy(), timeperiod=14)  # Convert to ndarray
        data['Exponential-moving-average'] = ta.EMA(data['Close'].to_numpy(), timeperiod=20)  # Convert to ndarray
        data['Momentum'] = ta.MOM(data['Close'].to_numpy(), timeperiod=5)  # Convert to ndarray
        macd, macd_signal, _ = ta.MACD(data['Close'].to_numpy())
        data['MACD'] = macd
        data['MACD_Signal'] = macd_signal
        # Add more indicators as needed
        return data


    def visualize_stock_data(self, data):
        fig = px.line(data, x=data.index, y=['Close', 'Moving-average'], title='Stock Price with Moving Average')
        fig.show()

    #visualizng stock price with momentum
    def visualize_momuntum(self ,data):
        fig = px.line(data, x= data.index, y = ['Close', 'Momentum'], title= ' stock price with momentum')
        fig.show()
    
    def visualize_daily_returns(self ,data):
        fig = px.line(data, x= data.index, y = 'Daily Return' , title= ' stock price with momentum')
        fig.show()

    def visualize_MACD(self, data):
        fig = px.line(data, x=data.index, y=['MACD', 'MACD_Signal'], title='Moving Average Convergence Divergence (MACD)')
        fig.show()
