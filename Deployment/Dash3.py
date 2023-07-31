import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Load data
data = pd.read_csv('E:\Excelr-P269-Internship-Project-Group2-OIl-Price-Prediction-And-Forecasting-Using-Python\oil_prices_yahoo1.csv')
# covertnig the date column to datetime using pandas
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# creating a data frame using pandas
df=pd.DataFrame(data)

# renaming the column to price
df.rename(columns = {'Close':'Price'}, inplace = True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1('Home'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    ),
    html.Br(),
    dcc.Link('Go to Time Series Map', href='/time-series-map'),
    html.Br(),
    dcc.Link('Go to Bar Chart', href='/bar-chart'),
])

time_series_map_page = html.Div([
    html.H1('Time Series Map'),
    dcc.Graph(id='time-series-map'),
    html.P(id='time-series-map-explanation'),
    html.Br(),
    dcc.Link('Go to Bar Chart', href='/bar-chart'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])
# Define the callback to update the time series map
@app.callback(
    Output('time-series-map', 'figure'),
    Input('time-series-map', 'id')
)
@app.callback(
    Output('bar-chart', 'figure'),
    Input('bar-chart', 'id')
)
def update_graph(id):
    # Create the interactive time series map
    fig = px.line(df, x='Date', y='Price', title='Time Series Map')

    # Add maximum price label
    max_price = df['Price'].max()
    max_date = df.loc[df['Price'] == max_price, 'Date'].iloc[0]
    fig.add_annotation(x=max_date, y=max_price, text=f'Max Price: {max_price} on {max_date}', showarrow=True, arrowhead=1 ,font=dict(color='red'))

    # Add minimum price label
    min_price = df['Price'].min()
    min_date = df.loc[df['Price'] == min_price, 'Date'].iloc[0]
    fig.add_annotation(x=min_date, y=min_price, text=f'Min Price: {min_price} on {min_date}', showarrow=True, arrowhead=1 ,font=dict(color='red'))

    return fig
def update_time_series_map_explanation(id):
    return 'This is an explanation of the time series map.'

bar_chart_page = html.Div([
    html.H1('Bar Chart'),
    dcc.Graph(id='bar-chart'),
    html.P(id='bar-chart-explanation'),
    html.Br(),
    dcc.Link('Go to Time Series Map', href='/time-series-map'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])
def update_bar_chart(id):
# Convert the Date column to a datetime object
    df['Date'] = pd.to_datetime(df['Date'])

# Group the data by month and calculate the mean price for each month
    monthly_data = df.groupby(pd.Grouper(key='Date', freq='M')).mean().reset_index()

# Create the interactive bar chart
    fig = px.bar(monthly_data, x='Date', y='Price', title='Monthly Bar Chart')  

# Add maximum price label
    max_price = monthly_data['Price'].max()
    max_date = monthly_data.loc[monthly_data['Price'] == max_price, 'Date'].iloc[0]
    fig.add_annotation(x=max_date, y=max_price, text=f'Max Oil Price: {max_price} on {max_date.strftime("%Y-%m")}', showarrow=True, arrowhead=1, font=dict(color='red'))

# Add minimum price label
    min_price = monthly_data['Price'].min()
    min_date = monthly_data.loc[monthly_data['Price'] == min_price, 'Date'].iloc[0]
    fig.add_annotation(x=min_date, y=min_price, text=f'Min Oil Price: {min_price} on {min_date.strftime("%Y-%m")}', showarrow=True, arrowhead=1, font=dict(color='black'))

    return fig
def update_time_series_map_explanation(id):
    return 'This is an explanation of the time series map.'

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/time-series-map':
        return time_series_map_page
    elif pathname == '/bar-chart':
        return bar_chart_page
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)
