import plotly.express as px
import talib as ta
import yfinance as yf


class FinanacialAnalyzer:
    def __init__(self, ticker, start_date, end_date):
        ticker = self.ticker
        start_date = self.start_date
        end_date = self.end_date
        
    def retrieve_stock_data(self):
        return yf.download(self.ticker, start =self.start_date, end = self.end_date)
    
    def calculate_technical_indicators(self, data):
        # Calculate various technical indicators
        data['Moving-average'] = ta.SMA(data['Close'], 20)
        data['Relative-strength-index'] = ta.RSI(data['Close'], timeperiod=14)
        data['Exponential-moving-average'] = ta.EMA(data['Close'], timeperiod=20) # calculating the Exponential moving average  
        data['Momuntum'] = ta.MOM(data['Close'], timeperiod=5)# calculating momuntum of closed prices
        macd, macd_signal, _ = ta.MACD(data['Close'])
        data['MACD'] = macd
        data['MACD_Signal'] = macd_signal
        # Add more indicators as needed
        return data
    def visualize_stock_data(self, data):
        fig = px.line(data, x=data.index, y=['Close', 'Moving-average'], title='Stock Price with Moving Average')
        fig.show()

    #visualizng stock price with momentum
    def visualize_stock_data(self ,data):
        fig = px.line(data, x= data.index, y = ['Close', 'Momuntum'], title= ' stock price with momentum')

    def visualize_MACD(self, data):
        fig = px.line(data, x=data.index, y=['MACD', 'MACD_Signal'], title='Moving Average Convergence Divergence (MACD)')
        fig.show()
