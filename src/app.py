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
from data_wrangling import (
    get_year_data,
    get_month_data,
    left_hist_data,
    right_hist_data,
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # to deploy the app.

# Global variables
columns = [
    "Reservations",
    "Average daily rate",
    "Adults",
    "Children",
    "Babies",
    "Required parking spaces",
    "Booking changes",
    "Special requests",
]
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
months_short = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
years = [2015, 2016, 2017]


info_area = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Super Hotel Management",
                    style={
                        "backgroundColor": "#e9ecef",
                        "padding": 10,
                        "color": "black",
                        "margin-top": 10,
                        "margin-bottom": 10,
                        "margin-left": -12,
                        "margin-right": -12,
                        "text-align": "left",
                        "font-size": "48px",
                        "border-radius": 5,
                    },
                )
            )
        ),
        dbc.Row(
            [
                # First column with control widgets
                dbc.Col(
                    [
                        html.H5("Global controls"),
                        html.Br(),
                        html.H6("Select variable to plot"),
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
                        html.Br(),
                        html.H6("Select year"),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[{"label": year, "value": year} for year in years],
                            value=2016,
                            multi=False,
                            searchable=False,
                            clearable=False,
                        ),
                        html.Br(),
                        html.H6("Select month"),
                        dcc.Dropdown(
                            id="month-dropdown",
                            options=[
                                {"label": months[i], "value": i + 1} for i in range(12)
                            ],
                            value=1,
                            multi=False,
                            searchable=False,
                            clearable=False,
                        ),
                        html.Br(),
                        html.H6("Select Hotel Type"),
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
                    md=2,
                    style={
                        "background-color": "#e9ecef",
                        "padding": 10,
                        "border-radius": 5,
                        "margin-right": "5px",
                    },
                ),
                # 2nd column with plots
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.Iframe(
                                                        id="year-plot",
                                                        style={
                                                            "border-width": "0",
                                                            "width": "110%",
                                                            "height": "375px",
                                                        },
                                                    ),
                                                    html.P(
                                                        children=[
                                                            "this is where i print \n important numbers",
                                                            years[0],
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            className="w-100 mb-3",
                                        )
                                    ),
                                    dbc.Row(
                                        dbc.Card(
                                            dbc.CardBody(
                                                html.Iframe(
                                                    id="hist1",
                                                    style={
                                                        "border-width": "0",
                                                        "width": "120%",
                                                        "height": "350px",
                                                    },
                                                ),
                                            ),
                                            className="w-100 mb-3",
                                        ),
                                    ),
                                ],
                                style={"margin-left": "5px", "margin-right": "5px"},
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.Iframe(
                                                        id="month-plot",
                                                        style={
                                                            "border-width": "0",
                                                            "width": "100%",
                                                            "height": "375px",
                                                        },
                                                    ),
                                                    html.P(children=["Nothing to see"]),
                                                ]
                                            ),
                                            className="w-100 mb-3",
                                        )
                                    ),
                                    dbc.Row(
                                        dbc.Card(
                                            dbc.CardBody(
                                                html.Iframe(
                                                    id="hist2",
                                                    style={
                                                        "border-width": "0",
                                                        "width": "100%",
                                                        "height": "350px",
                                                    },
                                                ),
                                            ),
                                            className="w-100 mb-3",
                                        ),
                                    ),
                                ],
                                style={"margin-left": "5px", "margin-right": "5px"},
                            ),
                        ]
                    )
                ),
            ]
        ),
    ]
)

# ,style={"max-width": "80%"},

# app.layout = html.Div([jumbotron, html.Br(), info_area])
app.layout = html.Div(info_area)


def get_stats(data, scope="all_time", ycol="Reservations"):
    if scope == "all_time":
        max_ind = data[data["Line"] == "Average"][ycol].argmax()
        min_ind = data[data["Line"] == "Average"][ycol].argmin()
    else:
        max_ind = data[data["Line"] != "Average"][ycol].argmax()
        min_ind = data[data["Line"] != "Average"][ycol].argmin()

    stats = {
        "ave": round(data[data["Line"] == "Average"][ycol].mean(), 1),
        "max": data.iloc[max_ind, 2],
        "max_date": data.iloc[max_ind, 0],
        "min": data.iloc[min_ind, 2],
        "min_date": data.iloc[min_ind, 0],
    }
    return stats


# # Callbacks and back-end
@app.callback(
    Output("year-plot", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("y-axis-dropdown", "value"),
    Input("year-dropdown", "value"),
)
# Function to plot the year plot using selected hotel type and y variables, and year
def plot_year(hotel_type="All", y_col="Reservations", year=2016):
    df = get_year_data(hotel_type, y_col, year)
    df["Arrival month"] = df["Arrival month"].replace(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], months_short
    )
    lines = (
        alt.Chart(df, title=y_col + " for " + str(year))
        .mark_line(color="orange")
        .encode(
            alt.X(
                "Arrival month",
                sort=months,
                title="Month",
                axis=alt.Axis(grid=False, labelAngle=-30),
            ),
            alt.Y(y_col, title=y_col, scale=alt.Scale(zero=True)),
            alt.Color("Line", legend=None),
            alt.Tooltip(y_col),
        )
    )
    chart = (
        (lines + lines.mark_circle())
        .properties(width=300, height=250)
        .configure_axis(labelFontSize=13, titleFontSize=17)
        .configure_title(fontSize=23)
    )
    return chart.to_html()


@app.callback(
    Output("month-plot", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("y-axis-dropdown", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value"),
)
# Function to plot the year plot using selected hotel type and y variables, and year
def plot_month(hotel_type="All", y_col="Reservations", year=2016, month=1):
    df = get_month_data(hotel_type, y_col, year, month)

    cur_mo = get_stats(df, "current", y_col)
    all_mo = get_stats(df, "all_time", y_col)

    lines = (
        alt.Chart(df, title=y_col + " for " + months[month - 1] + " " + str(year))
        .mark_line(color="orange")
        .encode(
            alt.X("Arrival day", title="Date", axis=alt.Axis(grid=False)),
            alt.Y(y_col, title=y_col, scale=alt.Scale(zero=True)),
            alt.Color("Line"),
            alt.Tooltip([y_col, "Arrival day of week"]),
        )
    )
    chart = (
        (lines + lines.mark_circle())
        .properties(width=300, height=250)
        .configure_axis(labelFontSize=13, titleFontSize=17)
        .configure_title(fontSize=23)
    )
    return chart.to_html()


############################################# Histograms ################################
@app.callback(
    Output("hist1", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value"),
)
# Function to plot the bottom left histogram using selected hotel type and dates
def histogram_1(hotel_type, year, month):
    df = left_hist_data(hotel_type, year, month)
    top_countries = (
        alt.Chart(
            df,
            title="Countries of origin "
            + str(months_short[month - 1])
            + " "
            + str(year),
        )
        .mark_bar(color="orange", size=15)
        .encode(
            alt.Y("Country of origin", sort="-x", title="Country"),
            alt.X("counts", title="Reservations"),
            alt.Tooltip("Country of origin"),
        )
        .properties(width=300, height=200)
        .configure_axis(labelFontSize=10, titleFontSize=15)
        .configure_title(fontSize=19)
    )
    return top_countries.to_html()


@app.callback(
    Output("hist2", "srcDoc"),
    Input("hotel-type-selection", "value"),
    Input("year-dropdown", "value"),
    Input("month-dropdown", "value"),
)

# Function to plot the bottom right plot using selected hotel type
def histogram_2(hotel_type, year, month):
    df = right_hist_data(hotel_type, year, month)
    stay = (
        alt.Chart(
            df,
            title="Lengths of Stay " + str(months_short[month - 1]) + " " + str(year),
        )
        .mark_bar(clip=True, color="orange", size=15)
        .encode(
            alt.X(
                "Total nights", title="Length of stay", scale=alt.Scale(domain=(2, 15))
            ),
            alt.Y("Percent of Reservations", title="Percent of Reservations"),
            alt.Tooltip("Percent of Reservations"),
        )
        .properties(width=300, height=200)
        .configure_axis(labelFontSize=10, titleFontSize=15)
        .configure_title(fontSize=19)
    )
    return stay.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)