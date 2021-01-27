# Import packages
import pandas as pd
import numpy as np

# Visualization packages
import altair as alt

# Dashboard packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import functions from data_wrangling script
from data_wrangling import get_year_data, get_month_data, left_plot, right_plot

# Columns for drop-down menus
columns = ["Reservations", "Average daily rate", 'Adults', 
'Children','Babies', 'Required parking spaces', 'Booking changes', 'Special requests']
months = ["January", "February", "March", "April",
          "May", "June", "July", "August", "September", 
          "October", "November", "December"]
years = [2015, 2016, 2017]

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
                        html.H4("Select the y-axis variable"),
                        dcc.Dropdown(
                            id="y-axis-dropdown",
                            options=[
                                {"label": column, "value": column} for column in columns
                            ],
                            value=columns[0],
                            multi=False,
                            searchable=False,
                            clearable=False,
                        ),
                        html.H4("Select a year"),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": year, "value": year} for year in years
                            ],
                            value=2016,
                            multi=False,
                            searchable=False,
                            clearable=False,
                        ),
                        html.H4("Select a month"),
                        dcc.Dropdown(
                            id="month-dropdown",
                            options=[
                                {"label": months[i], "value": i+1} for i in range(12)
                            ],
                            value=1,
                            multi=False,
                            searchable=False,
                            clearable=False,
                        ),
                        html.Br(),
                        html.H4("Select Hotel Type"),
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
                    ],
                    md=3,
                ),
        
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [             
                                    html.Iframe(
                                        id="year-plot",
                                        style={
                                            "border-width": "0",
                                            "width": "100%",
                                            "height": "500px",
                                        },
                                    ),
                                    ]
                                ),
                                dbc.Col(
                                    [               
                                    html.Iframe(
                                        id="month-plot",
                                        style={
                                            "border-width": "0",
                                            "width": "100%",
                                            "height": "500px",
                                        },
                                    )
                                    ]
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H4("Year summaries"),               
                                html.Iframe(
                                    id="year-summaries",
                                    style={
                                        "border-width": "0",
                                        "width": "50%",
                                        "height": "75px",
                                    },
                                ),
                                html.H4("Month summaries"),
                                html.Iframe(
                                    id="month-summaries",
                                    style={
                                        "border-width": "0",
                                        "width": "50%",
                                        "height": "75px",
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
    style={"max-width": "80%"},
)

app.layout = html.Div([jumbotron, html.Br(), info_area])

# # Callbacks and back-end
@app.callback(
    Output("year-plot", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("y-axis-dropdown", "value"),
    Input("year-dropdown", "value")
)
# Function to plot the year plot using selected hotel type and y variables, and year
def plot_year(hotel_type = "All", y_col = "Reservations", year = 2016):
    df = get_year_data(hotel_type, y_col, year)
    
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    df["Arrival month"] = df["Arrival month"].replace([1,2,3,4,5,6,7,8,9,10,11,12], months)
    
    lines = (
        alt.Chart(df, title=y_col + " for the year " + str(year))
        .mark_line(color="orange")
        .encode(alt.X("Arrival month", sort = months, title="Month", axis=alt.Axis(grid=False, labelAngle=-30)),
                             alt.Y(y_col, title = y_col, scale=alt.Scale(zero=True)),
                             alt.Color("Line"),
                             alt.Tooltip(y_col))
    )
    chart = (lines + lines.mark_point()
    ).properties(width=300, height=250).configure_axis(labelFontSize=13, titleFontSize=17
    ).configure_title(fontSize=23)
    return chart.to_html()

@app.callback(
    Output("month-plot", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("y-axis-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value")
)
# Function to plot the year plot using selected hotel type and y variables, and year
def plot_month(hotel_type = "All", y_col = "Reservations", year = 2016, month = 1):
    df = get_month_data(hotel_type, y_col, year, month)
    
    lines = (
        alt.Chart(df, title=y_col + " for the month of " + str(month))
        .mark_line(color="orange")
        .encode(alt.X("Arrival day", title="Date", axis=alt.Axis(grid=False, labelAngle=-30)),
                             alt.Y(y_col, title = y_col, scale=alt.Scale(zero=True)),
                             alt.Color("Line"),
                             alt.Tooltip(y_col))
    )
    chart = (lines + lines.mark_point()
    ).properties(width=300, height=250).configure_axis(labelFontSize=13, titleFontSize=17
    ).configure_title(fontSize=23)
    return chart.to_html()


# @app.callback(
#     Output("hist1", "srcDoc"),
#     Input("hotel-type-selection", "value"),
#     Input("week-selection", "value"),
# )
# # Function to plot the bottom left plot using selected hotel type
# def histogram_1(hotel_type, weeks):
#     df = left_plot(hotel_type, weeks)
#     top_countries = (
#         alt.Chart(df, title="Top 20 Home Countries of Guests")
#         .mark_bar(color="orange")
#         .encode(
#             alt.X("Country of origin", sort="-y", title="Countries"),
#             alt.Y("counts", title="Reservations"),
#             alt.Tooltip("Country of origin"),
#         )
#         .properties(width=300, height=200)
#         .configure_axis(labelFontSize=10, titleFontSize=15)
#         .configure_title(fontSize=19)
#     )
#     return top_countries.to_html()


# @app.callback(
#     Output("hist2", "srcDoc"),
#     Input("hotel-type-selection", "value"),
#     Input("week-selection", "value"),
# )
# # Function to plot the bottom right plot using selected hotel type
# def histogram_2(hotel_type, weeks):
#     df = right_plot(hotel_type, weeks)
#     stay = (
#         alt.Chart(df, title="Length of Guests Stay")
#         .mark_bar(clip=True, color="orange")
#         .encode(
#             alt.X(
#                 "Number of Nights of Stay",
#                 title="Number of nights of stay",
#                 scale=alt.Scale(domain=(0, 15)),
#                 bin=alt.Bin(maxbins=75),
#             ),
#             alt.Y("Percent of Reservations", title="Percent of Reservations"),
#             alt.Tooltip("Percent of Reservations"),
#         )
#         .properties(width=300, height=200)
#         .configure_axis(labelFontSize=10, titleFontSize=15)
#         .configure_title(fontSize=19)
#     )
#     return stay.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)