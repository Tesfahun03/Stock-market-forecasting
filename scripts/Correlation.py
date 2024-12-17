import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Example datasets: stock_data (retrieved earlier) and news_data (to be provided)

# Step 1: Prepare News Data
def process_news_data(news_data):
    # Normalize column names to lowercase for consistency
    news_data.columns = news_data.columns.str.lower()

    # Convert the 'date' column to datetime and normalize
    news_data['date'] = pd.to_datetime(
        news_data['date'], errors='coerce', utc=True
    ).dt.date  # Normalize to date only

    # Drop rows with invalid or missing dates
    news_data.dropna(subset=['date'], inplace=True)

    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Calculate sentiment score for each headline
    news_data['sentiment score'] = news_data['headline'].apply(
        lambda x: sia.polarity_scores(str(x))['compound']
    )

    # Group by Date and calculate mean sentiment score
    daily_sentiment = news_data.groupby('date')['sentiment score'].mean().reset_index()

    return daily_sentiment


# Step 2: Compute Daily Stock Returns
def compute_daily_returns(stock_data):
    # Reset the multi-index
    stock_data = stock_data.reset_index()

    # Check the columns to confirm the structure
    

    # If 'AAPL' appears multiple times, select the relevant column (e.g., 'Adj Close' or 'Close')
    # Use the correct column name for stock prices. Here I assume 'Adj Close' or 'AAPL' columns.
    stock_data['Daily Return'] = stock_data['AAPL'].pct_change() * 100  # Adjust 'AAPL' to your correct column name

    # Convert 'Date' column to datetime (if needed)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    # Return the relevant columns: Date and Daily Return
    daily_returns = stock_data[['Date', 'Daily Return']].dropna()
    return daily_returns


# Step 3: Merge Datasets
def merge_datasets(stock_returns, daily_sentiment):
    merged_data = pd.merge(stock_returns, daily_sentiment, on='Date', how='inner')
    return merged_data

# Step 4: Perform Correlation Analysis
def correlation_analysis(merged_data):
    correlation, p_value = pearsonr(merged_data['Daily Return'], merged_data['Sentiment Score'])
    print(f"Correlation Coefficient: {correlation}")
    print(f"P-Value: {p_value}")

        # Visualization
    plt.scatter(merged_data['Sentiment Score'], merged_data['Daily Return'])
    plt.title("Correlation Between Sentiment Score and Daily Returns")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Daily Return (%)")
    plt.grid(True)
    plt.show()