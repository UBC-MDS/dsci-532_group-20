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
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Read in global data, once processed data is ready -> change URL path to load in processed data
hotels = pd.read_csv(
    "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv"
)

hotels["adr_ac"] = hotels["adr"] / (hotels["adults"] + hotels["children"])
hotel_trim = hotels[
    [
        "hotel",
        "arrival_date_month",
        "adr_ac",
        "country",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
    ]
].copy()
hotel_trim = hotel_trim.replace([np.inf, -np.inf], np.nan).dropna()

# Dataframe for main plot:
guests_monthly = hotel_trim.groupby("arrival_date_month")["hotel"].count()
prices_monthly = hotel_trim.groupby("arrival_date_month")["adr_ac"].mean()
data_monthly = pd.merge(guests_monthly, prices_monthly, on="arrival_date_month")
data_monthly = data_monthly.reset_index()
# order by month:
months_ordered = [
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

data_monthly["arrival_date_month"] = pd.Categorical(
    data_monthly["arrival_date_month"], categories=months_ordered, ordered=True
)
data_monthly = data_monthly.sort_values("arrival_date_month")

# Dataset contains July and August date from 3 years, the other month from 2 years. Normalize data:
data_monthly.loc[
    (data_monthly["arrival_date_month"] == "July")
    | (data_monthly["arrival_date_month"] == "August"),
    "hotel",
] /= 3
data_monthly.loc[
    ~(
        (data_monthly["arrival_date_month"] == "July")
        | (data_monthly["arrival_date_month"] == "August")
    ),
    "hotel",
] /= 2

# Dataframe for countries plot:
top_20_countries = (
    hotel_trim.groupby("country")
    .size()
    .reset_index(name="counts")
    .sort_values(by="counts", ascending=False)[:20]
)

# Dataframe for Stay Length plot:
hotel_trim["total_nights"] = (
    hotel_trim["stays_in_weekend_nights"] + hotel_trim["stays_in_week_nights"]
)
num_nights = list(hotel_trim["total_nights"].value_counts().index)
num_bookings = list(hotel_trim["total_nights"].value_counts())
rel_bookings = (
    hotel_trim["total_nights"].value_counts() / sum(num_bookings) * 100
)  # convert to percent
stay_nights = pd.DataFrame(
    {
        "hotel": "Both Hotels",
        "num_nights": num_nights,
        "rel_num_bookings": num_bookings,
    }
)


# Assign column names to a list for dropdown widget
columns = ["hotel", "adr_ac"]


def histogram_1():
    top_countries = (
        alt.Chart(top_20_countries, title="Top 20 Home Countries of Guests")
        .mark_bar()
        .encode(
            alt.X("country", sort="-y", title="Countries"),
            alt.Y("counts", title="Guests numbers"),
            alt.Tooltip("country"),
        )
    )
    return top_countries.to_html()


def histogram_2():
    stay = (
        alt.Chart(stay_nights)
        .mark_bar()
        .encode(
            alt.X("num_nights", title="Number of nights"),
            alt.Y("rel_num_bookings", title="Percent of guests"),
        )
    )
    return stay.to_html()


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

## Setup app layout and front-end
app.layout = dbc.Container(
    [
        html.H1("Super-Hotels-Happy-Manager-Info"),
        html.P("by Sakshi Jain, Trevor Kinsey, Cameron Harris, Chen Zhao"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Select variables"),
                        dcc.Dropdown(
                            id="y-axis-dropdown",
                            options=[
                                {"label": label, "value": label} for label in columns
                            ],
                            value=columns[1],
                            multi=False,
                            searchable=False,
                        ),
                    ],
                    md=3,
                    style={"border": "1px solid #d3d3d3", "border-radius": "10px"},
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
                                    srcDoc=histogram_1(),
                                    style={
                                        "border-width": "0",
                                        "width": "50%",
                                        "height": "500px",
                                    },
                                ),
                                html.Iframe(
                                    id="hist2",
                                    srcDoc=histogram_2(),
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
    ]
)

## Callbacks and back-end
@app.callback(Output("lines", "srcDoc"), Input("y-axis-dropdown", "value"))
# Function to plot cross-plot using dropdown x and y variables
def plot_altair(y_col):
    chart = (
        alt.Chart(data_monthly)
        .mark_line()
        .encode(
            alt.X("arrival_date_month", title="Month", sort=months_ordered),
            y=y_col,
            tooltip=y_col,
        )
        .properties(width=700, height=350)
        .interactive()
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)