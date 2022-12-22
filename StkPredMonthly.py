import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
st.title("Jack's Stock Predictions")

i = 1

START = st.text_input("Enter the start date, formatted as 'YYYY-mm-dd':", key=i)
TODAY = date.today().strftime("%Y-%m-%d")
cname = ""

i = 2
while i == 2:
    selected_stock = st.text_input("Enter a stock symbol  # ", key=i)
    i += 1
########################################################################
cname = "Stock not found"
ticker = yf.Ticker(selected_stock)
cname = ticker.info.get('longName')
st.write(cname)
########################################################################
n_months = st.slider("Number of months to predict:", 1, 6)
period = n_months * 30

while selected_stock != '':
    ticker = yf.Ticker(selected_stock)
    cname = ticker.info.get('longName')
    if cname == "Stock Not found":
        break

    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.index = data.index.tz_localize(None)
        data.reset_index(inplace=True,)
        return data

    st.subheader('Raw Data for ' + selected_stock)
    data_load_state = st.text("Load data...")
    data = load_data(selected_stock)
    data_load_state.text = ("Loading data...done!")
#
    st.write(data.tail())


    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    plot_raw_data()
#
    #   FORCASTING
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    st.subheader('Forecast Data for ' + selected_stock)
    st.write(forecast.tail())
    st.write('forecast data')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)
    st.write('forecast components')
    fig2 = m.plot_components(forecast)
    st.write(fig2)
    break

print(START)
print(TODAY)
