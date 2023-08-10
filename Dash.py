import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pickle
import pandas as pd

app = dash.Dash(__name__)

# Load the saved Prophet model
with open('E:\Excelr-P269-Internship-Project-Group2-OIl-Price-Prediction-And-Forecasting-Using-Python\Dataset\prophet_model_11k.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

app.layout = html.Div(
    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100vh'},
    children=[
        html.Div(
            style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
            children=[
                dcc.DatePickerSingle(
                    id='date-picker',
                    date=pd.to_datetime('2023-08-10').date(),  # Set a default date
                ),
                html.Button('Predict Price', id='predict-button', n_clicks=0),
                html.Div(id='output-div', style={'margin-top': '10px'})
            ]
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
        return f"The Predicted Price On The {selected_date} is {predicted_price:.2f}$"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
