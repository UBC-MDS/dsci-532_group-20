import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from vega_datasets import data
import pandas as pd
import numpy as np

hotels = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv")
hotel_trim = hotels[:1000]

def plot_altair(xmax):
    chart = alt.Chart(hotel_trim[hotel_trim['lead_time'] < xmax], title='Super useful cross plots').mark_point().encode(
        x='lead_time',
        y='adr')
    return chart.to_html()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Super-Hotels-Happy-Manager-Info'),
    html.P('Sakshi Jain, Trevor Kinsey, Cameron Harris, Chen Zhao'), 

    html.Iframe(
        id='scatter',
        srcDoc=plot_altair(xmax=0),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Slider(id='xslider', min=0, max=240),
        # TBD add two dropdowns to select x and y vars
        # dcc.Dropdown(
        #     id='Var1',
        #     options=[
        #         {'label': 'New York City', 'value': 'NYC'},
        #         {'label': 'Montreal', 'value': 'MTL'},
        #         {'label': 'San Francisco', 'value': 'SF'}
        #     ],
        #     value='NYC'    
        # )
    html.P('This dashboard is going to make you lots of $$$')    
])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value'))
def update_output(xmax):
    return plot_altair(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)