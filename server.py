from dash import Dash, dcc, html, Input, Output
import pandas
import plotly.express as px
from catch_data import *

app = Dash(__name__)

animals = {}



app.layout = html.Div([
    dcc.Interval(id='interval1', interval=5 * 1000, n_intervals=0),
    dcc.Interval(id='interval-update-graph', interval=5 * 1000, n_intervals=0),
    html.Div([],id='dummy-interval-div'),
    html.H4('Tracker Movement'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select stock:"),
])


@app.callback(
    Output("time-series-chart", "figure"), 
    Input('interval-update-graph', "n_intervals"))
def display_time_series(n_intervals):
    try :
        for element in animals.items() :
            element[1].exportAsCSV(str(element[0])+'_data.csv')            
        a = animals[2103]
        a = pandas.DataFrame({'time' : a.getTime(),'Latitude' : a.getLatitude()})
        fig = px.line(a, x='time', y='Latitude')

        return fig
    except KeyError :
        return PreventUpdate


@app.callback(
    Output('dummy-interval-div', 'children'),
    Input('interval1', 'n_intervals')
    )
def update_interval(n):
    gatherInfo(animals)
    return 'Intervals Passed: ' + str(n)


if __name__ == '__main__':
    gatherInfo(animals)
    a = animals[2102]
    animals[2102].addPositionFromJSON({"lat" : a.getLatitude()[0]+10., "lng" : a.getLongitude(), "altitude" : a.getAltitude(), "timestamp" : '2022-05-21T17:10:10.077000+02:00', "satellites" : 12})
    app.run_server(debug=True)