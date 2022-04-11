import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import warnings
from bs4 import BeautifulSoup
import requests

warnings.filterwarnings('ignore')

pd.options.display.float_format = '${:,.2f}'.format

today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'

def get500():
    URL = 'https://topforeignstocks.com/indices/components-of-the-sp-500-index/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    results = soup.find(id="tablepress-3968")
    txt = open("stocks.txt", "w")
    for i, stocks in enumerate(results.find_all("td", class_="column-3")):
        stock = stocks.text
        txt.write(stock + '\n')
    txt.close

txt = open("stocks.txt", "r")
#plotlen = len(txt.readlines())
for i, symbol in enumerate(txt):
    print(symbol)
    symbol_df = yf.download(symbol,start_date, today)

    symbol_df.tail()

    symbol_df.info()

    symbol_df.isnull().sum()

    symbol_df.columns

    symbol_df.reset_index(inplace=True)
    symbol_df.columns

    df = symbol_df[["Date", "Open"]]

    new_names = {
        "Date": "ds", 
        "Open": "y",
    }

    df.rename(columns=new_names, inplace=True)

    df.tail()

    fig = make_subplots(
        rows=505, cols=1,
        subplot_titles=(symbol)
    )

    # plot the open price
    x = df["ds"]
    y = df["y"]

    fig.append_trace(go.Scatter(
        x = x, 
        y = y,
    ),  row = i + 1, col = 1)

    fig.update_xaxes(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )

fig.show()

def ml_forecast():

    m = Prophet(
        seasonality_mode="multiplicative",
        yearly_seasonality=True,
        daily_seasonality=True
    )

    m.fit(df)

    future = m.make_future_dataframe(periods = 365)
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    next_day = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    forecast[forecast['ds'] == next_day]['yhat'].item()

    plot_plotly(m, forecast)
    plot_components_plotly(m, forecast)

# get500()