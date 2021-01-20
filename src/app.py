# Import required packages
import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from vega_datasets import data
import pandas as pd
import numpy as np

# Read in global data, once processed data is ready -> change URL path to load in processed data
hotels = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv")
# Trimmed hotel data to <5000 rows to avoid Altair max data error
# Dropped agent and company variables due to missing values
hotel_trim = hotels[:4000].drop(columns=['agent', 'company'])
# Assign column names to a list for dropdown widget
data = hotel_trim.columns.tolist()

app = dash.Dash(__name__)

## Setup app layout and front-end ##
app.layout = html.Div([
    html.H1('Super-Hotels-Happy-Manager-Info'),
    html.P('by Sakshi Jain, Trevor Kinsey, Cameron Harris, Chen Zhao'), 

    html.Iframe(
        id='scatter',
        style={
            'border-width': '0',
            'width': '100%',
            'height': '500px'
            }),
        html.Div([
            html.H4('Select variable 1 (x-axis)'),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options = [{'label': label, 'value': label} for label in data],
                value=data[13],
                multi=False,
                searchable=False)],    
        ),
        html.Div([
            html.H4('Select variable 2 (y-axis)'),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options = [{'label': label, 'value': label} for label in data],
                value=data[8],
                multi=False,
                searchable=False)]),
    html.Iframe(
        id='x-histogram',
        style={
            'border-width': '0',
            'width': '100%',
            'height': '500px'}),
    html.Iframe(
        id='y-histogram',
        style={
            'border-width': '0',
            'width': '100%',
            'height': '500px'})
        ],    
        style = {'margin':'auto','width': "50%"})


## Callbacks and back-end functions ##
# Scatter plot decorator
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('x-axis-dropdown', 'value'),
    Input('y-axis-dropdown', 'value')
    )
# Function to plot cross-plot using dropdown x and y variables
def plot_altair(x_col, y_col, ):
    title_text = x_col + " vs. " + y_col
    chart = alt.Chart(hotel_trim, title=title_text).mark_point().encode(
        x=x_col,
        y=y_col,
        tooltip=y_col).interactive()
    line = alt.Chart()
    return chart.to_html()

# Histogram x-variable decorator
@app.callback(
    Output('x-histogram', 'srcDoc'),
    Input('x-axis-dropdown', 'value')
    )
# Function to plot histogram for x variable
def plot_x_histogram(x_col):
    histo1_title = x_col + " Histogram"
    x_histo = alt.Chart(hotel_trim, title=histo1_title).mark_bar().encode(
        x=x_col,
        y='count()')
    return x_histo.to_html()

# Histogram y-variable decorator
@app.callback(
    Output('y-histogram', 'srcDoc'),
    Input('y-axis-dropdown', 'value')
    )
# Function to plot histogram for y variable
def plot_y_histogram(y_col):
    histo2_title = y_col + " Histogram"
    y_histo = alt.Chart(hotel_trim, title=histo2_title).mark_bar().encode(
        x=alt.X(y_col, bin=alt.Bin(maxbins=20)),
        y='count()')
    return y_histo.to_html()    

if __name__ == '__main__':
    app.run_server(debug=True)