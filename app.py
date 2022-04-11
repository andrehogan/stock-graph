import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import warnings

warnings.filterwarnings('ignore')

pd.options.display.float_format = '${:,.2f}'.format

today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'

stockname = ["AMD", "ETH-USD", "SHIB-USD"]

fig = make_subplots(
    rows=len(stockname), cols=1,
    subplot_titles=(stockname))

for i, stock in enumerate(stockname):
    print(stock)
    stock_df = yf.download(stock,start_date, today)

    stock_df.tail()

    stock_df.info()

    stock_df.isnull().sum()

    stock_df.columns

    stock_df.reset_index(inplace=True)
    stock_df.columns

    df = stock_df[["Date", "Open"]]

    new_names = {
        "Date": "ds", 
        "Open": "y",
    }

    df.rename(columns=new_names, inplace=True)

    df.tail()

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