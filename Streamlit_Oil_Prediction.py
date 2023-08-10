import dash
from dash import dcc, html
from datetime import date
import pandas as pd
from prophet import Prophet

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2023, 9, 19),
            initial_visible_month=date(2023, 8, 5),
            date=date(2023, 8, 25)
        ),
        html.Div(id='output-container-date-picker'),
        html.Button('Refresh', id='refresh-button', n_clicks=0),
        html.Button('Next Page', id='next-page-button', n_clicks=0)
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
], style={'height': '100vh', 'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})

@app.callback(
    dash.dependencies.Output('output-container-date-picker', 'children'),
    [dash.dependencies.Input('date-picker', 'date')])
def update_output(date_value):
    if date_value is not None:
        # Load and preprocess the data
        df = pd.read_csv('E:\Excelr-P269-Internship-Project-Group2-OIl-Price-Prediction-And-Forecasting-Using-Python\Dataset\Cleaned_Oil_Price.csv')
        df = df.rename(columns={'Date': 'ds', 'Price': 'y'})

        # Create and fit a Prophet model
        model = Prophet()
        model.fit(df)

        # Create a dataframe for the future date to predict
        future = pd.DataFrame({'ds': [date_value]})

        # Make predictions for the future date
        forecast = model.predict(future)

        # Get the predicted price for the specified date
        price = forecast.loc[0, 'yhat']

        return f'The predicted price on {date_value} is {price}'

if __name__ == '__main__':
    app.run_server(debug=True)

