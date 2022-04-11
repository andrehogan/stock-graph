import pandas as pd
import yfinance as yf
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import warnings

warnings.filterwarnings('ignore')

def graphstock():
    # plot the open price
    x = df["ds"]
    y = df["y"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y))

    # Set title
    fig.update_layout(
        title_text='Time series plot of %s Open Price' % (stock),
    )

    fig.update_layout(
        xaxis=dict(
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
            rangeslider=dict(visible=True),
            type="date",
        )
    )
    fig.show()

pd.options.display.float_format = '${:,.2f}'.format

today = datetime.today().strftime('%Y-%m-%d')
start_date = '2016-01-01'

stockname = ["AMD", "ETH-USD", "SHIB-USD"]
for stock in stockname:
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
    graphstock()