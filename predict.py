import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from stocknews import StockNews
from alpha_vantage.fundamentaldata import FundamentalData

def get_stock_market(ticker):
    ticker_info = yf.Ticker(ticker).info
    if 'exchange' in ticker_info:
        exchange = ticker_info['exchange']
        if exchange == 'NMS':
            return "NASDAQ"
        elif exchange == 'SNP':
            return "S&P 500"
        else:
            return "Other"
    else:
        return "Unknown"

def app():
    # Page title
    st.title('📈 Stock Market / Investment Dashboard')
    st.write("""
    Welcome to the Stock Market / Investment Dashboard! This dashboard helps you explore stock data, news, and predictions.
    
    **Instructions for Beginners:**
    - Enter a stock symbol (e.g., AAPL for Apple).
    - Choose a start and end date to fetch historical data.
    - Explore different tabs for pricing data, fundamental data, news, and predictions.
    """)
    st.markdown("---")

    # Query Parameters - Horizontal layout
    col1, col2, col3 = st.columns([1, 1, 1])  # Create three equal columns

    with col1:
        st.header('Query Parameters')
    col4, col5, col6 = st.columns([1, 1, 1])
    with col4:
        ticker = st.text_input('Ticker (Stock Symbol)', value='AAPL')
    with col5:
        start_date = st.date_input('Start Date', pd.to_datetime('2020-01-01'))
    with col6:
        end_date = st.date_input('End Date', pd.to_datetime('today'))

    # Fetch data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    # Display market information at the top
    st.header(f"**{stock_info['shortName']} ({ticker})**")
    st.write(f"**Exchange:** {get_stock_market(ticker)}")
    st.write(f"**Current Price:** ${stock_info['currentPrice']:.2f}")
    st.write(f"**Market Cap:** ${stock_info['marketCap']:,}")
    st.write(f"**P/E Ratio:** {stock_info['trailingPE']:.2f}")
    st.write(f"**Dividend Yield:** {stock_info['dividendYield']:.2%}")

    # Plot stock price data
    fig = px.line(data, x=data.index, y='Adj Close', title=f'{ticker} Adjusted Close Price')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # Tips for beginners
    st.subheader('Tips for Beginners')
    st.markdown("""
    - **Pricing Data:** Explore historical prices and analyze trends over time.
    - **Fundamental Data:** Understand a company's financial health with balance sheets, income statements, and cash flow.
    - **News:** Stay informed with top news related to your stock of interest.
    - **Prediction:** Get insights into future stock price movements based on historical data.
    """)

    # Create tabs for different types of data
    pricing_data, fundamental_data, news, prediction = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News", "Prediction"])

    # News Tab
    with news:
        st.subheader(f'Top 10 News for {ticker}')
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()
        
        for i in range(10):
            st.markdown(f"### News {i + 1}: {df_news['title'][i]}")
            st.markdown(f"**Published on:** {df_news['published'][i]}")
            st.markdown(f"**Summary:** {df_news['summary'][i]}")
            title_sentiment = df_news['sentiment_title'][i]
            news_sentiment = df_news['sentiment_summary'][i]
            
            sentiment_colors = {
                'Positive': 'green',
                'Neutral': 'gray',
                'Negative': 'red'
            }
            
            title_color = sentiment_colors.get(title_sentiment, 'black')
            news_color = sentiment_colors.get(news_sentiment, 'black')
            
            st.markdown(f"**Title Sentiment:** <span style='color:{title_color}'>{title_sentiment}</span>", unsafe_allow_html=True)
            st.markdown(f"**News Sentiment:** <span style='color:{news_color}'>{news_sentiment}</span>", unsafe_allow_html=True)
            st.markdown('---')

    # Pricing Data Tab
    with pricing_data:
        st.subheader('Pricing Data')
        data['% Change'] = data['Adj Close'].pct_change()
        data.dropna(inplace=True)
        st.write(data)
        
        annual_return = data['% Change'].mean() * 252 * 100
        stdev = data['% Change'].std() * np.sqrt(252)

        col7, col8 ,col9 = st.columns([1,1,1])
        
        with col7:
            st.metric("Annual Return", f"{annual_return:.2f}%")

        with col8:
            st.metric("Standard Deviation", f"{stdev:.2f}%")

        with col9:
            st.metric("Risk Adjusted Return", f"{annual_return/stdev:.2f}")

    # Fundamental Data Tab
    with fundamental_data:
        key = '1VZ9G6S9P6TTKQLF'
        fd = FundamentalData(key, output_format='pandas')
        st.subheader('Balance Sheet')
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        st.write(bs)
        st.subheader('Income Statement')
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        st.write(is1)
        st.subheader('Cash Flow Statement')
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        st.write(cf)

    # Prediction Tab
    with prediction:
        st.subheader(f'{ticker} Stock Price Prediction')

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
        st.plotly_chart(fig_pred, use_container_width=True)

        # Future predictions
        days_to_predict = st.slider('Days to Predict', 1, 365, 30)
        future_days = pd.DataFrame({'Days': np.arange(data['Days'].max() + 1, data['Days'].max() + 1 + days_to_predict)})
        future_dates = pd.date_range(start=data['Date'].max() + pd.Timedelta(days=1), periods=days_to_predict, freq='D')
        future_predictions = model.predict(future_days)

        # Create a dataframe for future predictions
        future_data = pd.DataFrame({'Date': future_dates, 'Predicted': future_predictions})
        
        # Plot future predictions
        fig_future_pred = px.line(future_data, x='Date', y='Predicted', labels={'Predicted': 'Price'}, title=f'{ticker} Future Stock Price Prediction')
        st.plotly_chart(fig_future_pred, use_container_width=True)
    
    # FAQ Section
    st.markdown("---")
    st.subheader('Frequently Asked Questions (FAQ)')
    st.markdown("""
    **Q: How do I use this dashboard?**
    A: Enter a stock symbol, select a date range, and explore different tabs to analyze stock data.

    **Q: Can I trust the predictions shown here?**
    A: Predictions are based on historical data and should be used for informational purposes only.

    **Q: What if I encounter issues or have feedback?**
    A: Contact us through the provided form below or reach out to [A187996@siswa.ukm.edu.my].
    """)

if __name__ == "__main__":
    app()
