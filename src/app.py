import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from vega_datasets import data
import pandas as pd
import numpy as np

hotels = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv")
hotel_trim = hotels[:4000].drop(columns=['agent', 'company'])
# have left categorical columns in for now, to remove add this to line below: select_dtypes(include=np.number)
data = hotel_trim.columns.tolist()


def plot_altair(x_col, y_col):
    title_text = x_col + " vs. " + y_col
    chart = alt.Chart(hotel_trim, title=title_text).mark_point().encode(
        x=x_col,
        y=y_col)
    line = alt.Chart()
    return chart.to_html()

def plot_histograms(x_col):
    histo1_title = x_col + " Histogram"
    histo = alt.Chart(hotel_trim, title=histo1_title).mark_bar().encode(
        x=alt.X(x_col, bin=alt.Bin(maxbins=20)),
        y='count()')
    return histo.to_html()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Super-Hotels-Happy-Manager-Info'),
    html.P('by Sakshi Jain, Trevor Kinsey, Cameron Harris, Chen Zhao'), 

    html.Iframe(
        id='scatter',
        srcDoc=plot_altair(x_col=data[5], y_col=data[2]),
        style={
            'border-width': '0',
            'width': '100%',
            'height': '500px'
            }),
        # dcc.Slider(id='xslider', min=0, max=240),
        html.Div([
            html.H4('Select variable 1 (x-axis)'),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options = [{'label': label, 'value': label} for label in data],
                value=data[5],
                multi=False,
                searchable=False)],    
        ),
        html.Div([
            html.H4('Select variable 2 (y-axis)'),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options = [{'label': label, 'value': label} for label in data],
                value=data[2],
                multi=False,
                searchable=False)]),
    html.Iframe(
        id='histogram',
        srcDoc=plot_histograms(x_col=data[5]),
        style={'border-width': '0', 'width': '100%', 'height': '300px'})
        ], style = {'margin':'auto','width': "50%"})

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('x-axis-dropdown', 'value'),
    Input('y-axis-dropdown', 'value')
    )
    # Slider was giving me errors because the dtype is defined as an int here but the x-axis dtype changes
    # Input('xslider', 'value'))
def update_crossplot(x_col, y_col):
    return plot_altair(x_col, y_col)

@app.callback(
    Output('histogram', 'srcDoc'),
    Input('x-axis-dropdown', 'value')
    )
def update_histogram(x_col):
    return plot_histograms(x_col)

if __name__ == '__main__':
    app.run_server(debug=True)