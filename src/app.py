# Import packages
import pandas as pd
import numpy as np

# Visualization packages
import altair as alt
from altair_saver import save

# Save a vega-lite spec and a PNG blob for each plot in the notebook
alt.renderers.enable("mimetype")
# Handle large data sets without embedding them in the notebook
alt.data_transformers.enable("data_server")
# Dashboard packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import functions from data_wrangling script
from data_wrangling import main_plot, left_plot, right_plot

# Assign column names to a list for dropdown widget
columns = ["Guest Numbers", "Average daily rate per person", "Required parking spaces"]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server #to deploy the app. 

# Setup app layout and front-end
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("Super Hotel Management", className="display-3"),
                html.P(
                    "This is an interactive dashboard based on the data comes from the Hotel Booking Demand dataset",
                    className="lead",
                ),
            ],
        )
    ],
    fluid=True,
)

info_area = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Select Hotel Types"),
                        html.Br(),
                        dcc.RadioItems(
                            id="hotel-type-selection",
                            options=[
                                {"label": "All Hotels", "value": "All"},
                                {"label": "Resort Hotel", "value": "Resort"},
                                {"label": "City Hotel", "value": "City"},
                            ],
                            value="All",
                            labelStyle={"display": "block"},
                        ),
                        html.Br(),
                        html.Br(),
                        html.H4("Select Weeks"),
                        html.Br(),
                        dcc.RangeSlider(
                            id="week-selection",
                            min=1,
                            max=53,
                            value=[1, 53],
                            marks={
                                1: "",
                                9: "Spring",
                                22: "Summer",
                                35: "Fall",
                                48: "Winter",
                                53: "",
                            },
                        ),
                        html.Br(),
                        html.Br(),
                        html.H4("Select Features for Main Plot"),
                        html.Br(),
                        dcc.Dropdown(
                            id="y-axis-dropdown",
                            options=[
                                {"label": label, "value": label} for label in columns
                            ],
                            value=columns[0],
                            multi=False,
                            searchable=False,
                            clearable=False,
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.Iframe(
                                    id="lines",
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "500px",
                                    },
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.Iframe(
                                    id="hist1",
                                    style={
                                        "border-width": "0",
                                        "width": "50%",
                                        "height": "500px",
                                    },
                                ),
                                html.Iframe(
                                    id="hist2",
                                    style={
                                        "border-width": "0",
                                        "width": "50%",
                                        "height": "500px",
                                    },
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ],
    style={"max-width": "55%"},
)

app.layout = html.Div([jumbotron, html.Br(), info_area])

# Callbacks and back-end
@app.callback(
    Output("lines", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("week-selection", "value"),
    Input("y-axis-dropdown", "value"),
)
# Function to plot the main plot using selected hotel type and y variables
def plot_altair(hotel_type, x_col, y_col):
    df = main_plot(hotel_type, x_col)
    title_text = y_col + " for each week in the year"
    chart = (
        alt.Chart(df, title=title_text)
        .mark_line(color="orange")
        .encode(
            alt.X("Arrival week", title="Week numbers", axis=alt.Axis(grid=False)),
            alt.Y(y_col, title=y_col, scale=alt.Scale(zero=False)),
        )
        .properties(width=820, height=390)
        .configure_axis(labelFontSize=13, titleFontSize=17)
        .configure_title(fontSize=23)
    )
    return chart.to_html()


@app.callback(
    Output("hist1", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("week-selection", "value"),
)
# Function to plot the bottom left plot using selected hotel type
def histogram_1(hotel_type, weeks):
    df = left_plot(hotel_type, weeks)
    top_countries = (
        alt.Chart(df, title="Top 20 Home Countries of Guests")
        .mark_bar(color="orange")
        .encode(
            alt.X("Country of origin", sort="-y", title="Countries"),
            alt.Y("counts", title="Guests numbers"),
            alt.Tooltip("Country of origin"),
        )
        .properties(width=390, height=200)
        .configure_axis(labelFontSize=10, titleFontSize=15)
        .configure_title(fontSize=19)
    )
    return top_countries.to_html()


@app.callback(
    Output("hist2", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("week-selection", "value"),
)
# Function to plot the bottom right plot using selected hotel type
def histogram_2(hotel_type, weeks):
    df = right_plot(hotel_type, weeks)
    stay = (
        alt.Chart(df, title="Length of Guests Stay")
        .mark_bar(clip=True, color="orange")
        .encode(
            alt.X(
                "Number of Nights of Stay",
                title="Number of nights of stay",
                scale=alt.Scale(domain=(0, 15)),
                bin=alt.Bin(maxbins=75),
            ),
            alt.Y("Percent of Guests", title="Percent of guests"),
            alt.Tooltip("Percent of Guests"),
        )
        .properties(width=390, height=200)
        .configure_axis(labelFontSize=10, titleFontSize=15)
        .configure_title(fontSize=19)
    )
    return stay.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)