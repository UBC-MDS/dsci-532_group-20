import pandas as pd
import numpy as np

# Read in data from processed data
def getdata(hotel_type="All", weeks=[1, 53]):
    hotels = pd.read_csv("data/processed/clean_hotels.csv")
    hotels["Average daily rate per person"] = hotels["Average daily rate"] / (
        hotels["Adults"] + hotels["Children"]
    )
    hotel_trim = hotels[
        [
            "Hotel type",
            "Arrival week",
            "Average daily rate per person",
            "Country of origin",
            "Weekend nights",
            "Week nights",
            "Required parking spaces",
        ]
    ].copy()
    hotel_trim = hotel_trim.replace([np.inf, -np.inf], np.nan).dropna()

    if hotel_type == "Resort":
        hotel_trim = hotel_trim[hotel_trim["Hotel type"] == "Resort"]

    if hotel_type == "City":
        hotel_trim = hotel_trim[hotel_trim["Hotel type"] == "City"]

    hotel_trim = hotel_trim[hotel_trim["Arrival week"].between(weeks[0], weeks[1])]

    return hotel_trim


# Dataframe for main plots:
def main_plot(hotel_type="All", weeks=[1, 53]):
    df = getdata(hotel_type, weeks)
    guests_weekly = df.groupby("Arrival week")["Hotel type"].count()
    prices_weekly = df.groupby("Arrival week")["Average daily rate per person"].mean()
    parking_weekly = df.groupby("Arrival week")["Required parking spaces"].sum()
    data_weekly = pd.merge(guests_weekly, prices_weekly, on="Arrival week")
    data_weekly = pd.merge(data_weekly, parking_weekly, on="Arrival week")
    data_weekly = data_weekly.rename(
        columns={"Hotel type": "Guest Numbers"}
    ).reset_index()
    return data_weekly


# Dataframe for countries plot:
def left_plot(hotel_type="All", weeks=[1, 53]):
    df = getdata(hotel_type, weeks)
    top_20_countries = (
        df.groupby("Country of origin")
        .size()
        .reset_index(name="counts")
        .sort_values(by="counts", ascending=False)[:20]
    )
    return top_20_countries


# Dataframe for Stay Length plot:
def right_plot(hotel_type="All", weeks=[1, 53]):
    df = getdata(hotel_type, weeks)
    df["Total Nights of Stay"] = df["Weekend nights"] + df["Week nights"]
    num_nights = list(df["Total Nights of Stay"].value_counts().index)
    num_bookings = list(df["Total Nights of Stay"].value_counts())
    rel_bookings = (
        df["Total Nights of Stay"].value_counts() / sum(num_bookings) * 100
    )  # convert to percent
    stay_nights = pd.DataFrame(
        {
            "hotel": "Both Hotels",
            "Number of Nights of Stay": num_nights,
            "Percent of Guests": rel_bookings,
        }
    )
    return stay_nights


if __name__ == "__main__":
    main()