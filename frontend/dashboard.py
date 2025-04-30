import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd

app = dash.Dash(__name__)
app.title = "Real-time IoT Dashboard"

history_df = pd.DataFrame(columns=['timestamp', 'temperature', 'humidity'])

app.layout = html.Div([
    html.H2("Smart Facility – Real-time IoT Monitoring"),
    dcc.Interval(id='interval', interval=3000, n_intervals=0),
    dcc.Graph(id='temp-graph'),
    dcc.Graph(id='humidity-graph')
])

@app.callback(
    Output('temp-graph', 'figure'),
    Output('humidity-graph', 'figure'),
    Input('interval', 'n_intervals')
)
def update_graph(n):
    global history_df
    response = requests.get("http://localhost:5050/iot-data")
    if response.status_code == 200:
        data = response.json()
        new_df = pd.DataFrame([data])
        history_df = pd.concat([history_df, new_df], ignore_index=True)
        
        normal_temp = history_df[history_df['temperature'] <= 30]
        alert_temp = history_df[history_df['temperature'] > 30]
        normal_humidity = history_df[history_df['humidity'] <= 60]
        alert_humidity = history_df[history_df['humidity'] > 60]

    temp_fig = {
    'data': [
        {
            'x': normal_temp['timestamp'],
            'y': normal_temp['temperature'],
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Normal Temp',
            'marker': {'color': 'blue'}
        },
        {
            'x': alert_temp['timestamp'],
            'y': alert_temp['temperature'],
            'type': 'scatter',
            'mode': 'markers',
            'name': 'High Temp Alert',
            'marker': {'color': 'red', 'size': 10, 'symbol': 'circle'}
        }
    ],
    'layout': {'title': 'Temperature Over Time'}
}

    humidity_fig = {
    'data': [
        {
            'x': normal_humidity['timestamp'],
            'y': normal_humidity['humidity'],
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Normal Humidity',
            'marker': {'color': 'green'}
        },
        {
            'x': alert_humidity['timestamp'],
            'y': alert_humidity['humidity'],
            'type': 'scatter',
            'mode': 'markers',
            'name': 'High Humidity Alert',
            'marker': {'color': 'orange', 'size': 10, 'symbol': 'square'}
        }
    ],
    'layout': {'title': 'Humidity Over Time'}
}

    return temp_fig, humidity_fig


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
