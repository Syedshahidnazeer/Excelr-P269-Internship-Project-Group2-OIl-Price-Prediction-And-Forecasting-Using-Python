import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pickle
import pandas as pd

app = dash.Dash(__name__)

# Load the saved Prophet model
with open('/Dataset/prophet_model_11k', 'rb') as model_file:
    model = pickle.load(model_file)

app.layout = html.Div(
    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'height': '100vh',
           'background-image': 'url("/assets/background.jpg")', 'background-size': '100% 100%'},
    children=[
        html.Div(
            style={'flex': 1, 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
            children=[
                html.Div(
                    style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center',
                           'background-color': 'rgba(255, 255, 255, 0.8)', 'padding': '20px', 'border-radius': '10px'},
                    children=[
                        dcc.DatePickerSingle(
                            id='date-picker',
                            date=pd.to_datetime('2023-08-10').date(),  # Set a default date
                            style={'border': '1px solid #ccc', 'border-radius': '5px', 'padding': '5px'}
                        ),
                        html.Button('Predict Price', id='predict-button', n_clicks=0,
                                    style={'margin-top': '10px', 'background-color': '#0074D9', 'color': 'white'}),
                        html.Div(id='output-div', style={'margin-top': '10px'}),
                    ]
                )
            ]
        ),
        html.Div(
            id='previous-prices',
            style={'flex': 1, 'padding': '20px', 'text-align': 'left'}
        ),
        html.Div(
            id='next-prices',
            style={'flex': 1, 'padding': '20px', 'text-align': 'right'}
        )
    ]
)

@app.callback(
    Output('output-div', 'children'),
    [Input('predict-button', 'n_clicks')],
    [Input('date-picker', 'date')]
)
def predict_price(n_clicks, selected_date):
    if n_clicks > 0:
        selected_date = pd.to_datetime(selected_date)
        future = pd.DataFrame({'ds': [selected_date]})
        forecast = model.predict(future)
        predicted_price = forecast.loc[0, 'yhat']
        return f"Predicted Price: {predicted_price:.2f}"
    return ""

@app.callback(
    [Output('previous-prices', 'children'), Output('next-prices', 'children')],
    [Input('date-picker', 'date')]
)
def display_previous_next_prices(selected_date):
    selected_date = pd.to_datetime(selected_date)
    previous_dates = [selected_date - pd.DateOffset(days=i) for i in range(5, 0, -1)]
    next_dates = [selected_date + pd.DateOffset(days=i) for i in range(1, 6)]
    
    previous_prices = []
    next_prices = []

    for date in previous_dates:
        future = pd.DataFrame({'ds': [date]})
        forecast = model.predict(future)
        predicted_price = forecast.loc[0, 'yhat']
        previous_prices.append(f"{date.date()}: {predicted_price:.2f}")

    for date in next_dates:
        future = pd.DataFrame({'ds': [date]})
        forecast = model.predict(future)
        predicted_price = forecast.loc[0, 'yhat']
        next_prices.append(f"{date.date()}: {predicted_price:.2f}")

    previous_prices_div = html.Div([html.P(price) for price in previous_prices])
    next_prices_div = html.Div([html.P(price) for price in next_prices])

    return previous_prices_div, next_prices_div

if __name__ == '__main__':
    app.run_server(debug=True)
