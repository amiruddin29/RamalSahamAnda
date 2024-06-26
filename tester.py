import streamlit as bt
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

def app():
    # Page title
    bt.title('📈 Stock Market / Investment Dashboard')

    # Sidebar for input fields
    bt.header('Query Parameters')
    ticker = bt.text_input('Ticker', value='AAPL')
    start_date = bt.date_input('Start Date', pd.to_datetime('2020-01-01'))
    end_date = bt.date_input('End Date', pd.to_datetime('today'))

    # Fetch data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)

    # Plot stock price data
    bt.subheader(f'{ticker} Stock Price')
    fig = px.line(data, x=data.index, y='Adj Close', title=f'{ticker} Adjusted Close Price')
    bt.plotly_chart(fig, use_container_width=True)

    # Create tabs for different types of data
    pricing_data, fundamental_data, news, prediction = bt.tabs(["Pricing Data", "Fundamental Data", "Top 10 News", "Prediction"])

    # News Tab
    with news:
        bt.subheader(f'Top 10 News for {ticker}')
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()
        
        for i in range(10):
            bt.markdown(f"### News {i + 1}: {df_news['title'][i]}")
            bt.markdown(f"**Published on:** {df_news['published'][i]}")
            bt.markdown(f"**Summary:** {df_news['summary'][i]}")
            title_sentiment = df_news['sentiment_title'][i]
            news_sentiment = df_news['sentiment_summary'][i]
            
            sentiment_colors = {
                'Positive': 'green',
                'Neutral': 'gray',
                'Negative': 'red'
            }
            
            title_color = sentiment_colors.get(title_sentiment, 'black')
            news_color = sentiment_colors.get(news_sentiment, 'black')
            
            bt.markdown(f"**Title Sentiment:** <span style='color:{title_color}'>{title_sentiment}</span>", unsafe_allow_html=True)
            bt.markdown(f"**News Sentiment:** <span style='color:{news_color}'>{news_sentiment}</span>", unsafe_allow_html=True)
            bt.markdown('---')


    # Pricing Data Tab
    with pricing_data:
        bt.subheader('Pricing Data')
        data['% Change'] = data['Adj Close'].pct_change()
        data.dropna(inplace=True)
        bt.write(data)
        
        annual_return = data['% Change'].mean() * 252 * 100
        stdev = data['% Change'].std() * np.sqrt(252)
        
        bt.metric("Annual Return", f"{annual_return:.2f}%")
        bt.metric("Standard Deviation", f"{stdev:.2f}%")
        bt.metric("Risk Adjusted Return", f"{annual_return/stdev:.2f}")

    # Fundamental Data Tab
    from alpha_vantage.fundamentaldata import FundamentalData
    with fundamental_data:
        key = '1VZ9G6S9P6TTKQLF'
        fd = FundamentalData(key,output_format = 'pandas')
        bt.subheader('Balance Sheet')
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        bt.write(bs)
        bt.subheader('Income Statement')
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        bt.write(is1)
        bt.subheader('Cash Flow Statement')
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        bt.write(cf)

    # Prediction Tab
    with prediction:
        bt.subheader(f'{ticker} Stock Price Prediction')

        # Prepare the data for prediction
        data['Date'] = data.index
        data.reset_index(drop=True, inplace=True)
        data['Days'] = (data['Date'] - data['Date'].min()).dt.days

        # Select features and target
        X = data[['Days']]
        y = data['Adj Close']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Create and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        data['Predicted'] = model.predict(X)

        # Plot the actual and predicted prices
        fig_pred = px.line(data, x='Date', y=['Adj Close', 'Predicted'], labels={'value': 'Price', 'variable': 'Legend'}, title=f'{ticker} Stock Price Prediction')
        bt.plotly_chart(fig_pred, use_container_width=True)

        # Future predictions
        days_to_predict = bt.slider('Days to Predict', 1, 365, 30)
        future_days = pd.DataFrame({'Days': np.arange(data['Days'].max() + 1, data['Days'].max() + 1 + days_to_predict)})
        future_dates = pd.date_range(start=data['Date'].max() + pd.Timedelta(days=1), periods=days_to_predict, freq='D')
        future_predictions = model.predict(future_days)

        # Create a dataframe for future predictions
        future_data = pd.DataFrame({'Date': future_dates, 'Predicted': future_predictions})
        
        # Plot future predictions
        fig_future_pred = px.line(future_data, x='Date', y='Predicted', labels={'Predicted': 'Price'}, title=f'{ticker} Future Stock Price Prediction')
        bt.plotly_chart(fig_future_pred, use_container_width=True)

    # Run the application
    if __name__ == "__main__":
        app()
