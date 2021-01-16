import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from vega_datasets import data
import pandas as pd
import numpy as np

cars = data.cars()

def plot_altair(xmax):
    chart = alt.Chart(cars[cars['Horsepower'] < xmax]).mark_point().encode(
        x='Horsepower',
        y='Weight_in_lbs')
    return chart.to_html()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('*****'),
    html.H1('5-star Insights '),

    html.Iframe(
        id='scatter',
        srcDoc=plot_altair(xmax=0),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Slider(id='xslider', min=0, max=240)
])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value'))
def update_output(xmax):
    return plot_altair(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)