import pandas as pd
import numpy as np

# Read in data and select hotel type
# Returns the main dataframe filtered by hotel type
def select_type(hotel_type="All"):
    hotels = pd.read_csv("data/processed/clean_hotels.csv")
    # hotels = hotels.replace([np.inf, -np.inf], np.nan).dropna()    
    # filter based on hotel type selection
    if hotel_type == "Resort":
        hotels = hotels[hotels["Hotel type"] == "Resort"]
    if hotel_type == "City":
        hotels = hotels[hotels["Hotel type"] == "City"]
    return hotels

# get data for `year-plot`
def get_year_data(hotel_type, y_col, year):
    hotels = select_type(hotel_type)
    data = pd.DataFrame()
    if y_col == "Reservations":
        # get average of all years
        data["Average"] = hotels.groupby("Arrival month")["Hotel type"].count() / hotels.groupby("Arrival month")["Arrival year"].nunique()
        # get values for selected year only
        data[str(year)] = hotels[hotels["Arrival year"] == year].groupby("Arrival month")["Hotel type"].count() 
    elif y_col == "Average daily rate":
        data["Average"] = hotels.groupby("Arrival month")[y_col].mean()
        data[str(year)] = hotels[hotels["Arrival year"] == year].groupby("Arrival month")[y_col].mean()

    else:
        data["Average"] = hotels.groupby("Arrival month")[y_col].sum() / hotels.groupby("Arrival month")["Arrival year"].nunique()
        data[str(year)] = hotels[hotels["Arrival year"] == year].groupby("Arrival month")[y_col].sum() 
          
    # make the month_no a column
    data = data.reset_index()
    data = pd.melt(data, 'Arrival month').rename(columns = {"variable": "Line", "value": y_col})

    return data

# Read in data data for `month-plot`
def get_month_data(hotel_type="All", y_col = "Reservations", year = 2016,  month = 1,):
    hotels = select_type(hotel_type)
    # for monthly plots, group data by day
    hotels = hotels[hotels["Arrival month"] == month]
    data = pd.DataFrame()
    if y_col == "Reservations":
        # get average of all years
        data["Average"] = hotels.groupby("Arrival day")["Hotel type"].count() / hotels.groupby("Arrival day")["Arrival year"].nunique()
        # get values for selected year only
        data[str(year)] = hotels[hotels["Arrival year"] == year].groupby("Arrival day")["Hotel type"].count() 
    elif y_col == "Average daily rate":
        data["Average"] = hotels.groupby("Arrival day")[y_col].mean()
        data[str(year)] = hotels[hotels["Arrival year"] == year].groupby("Arrival day")[y_col].mean()

    else:
        data["Average"] = df.groupby("Arrival day")[y_col].sum() / df.groupby("Arrival day")["Arrival year"].nunique()
        data[str(year)] = df[df["Arrival year"] == year].groupby("Arrival day")[y_col].sum() 
        
    data = data.reset_index()
    data = pd.melt(data, 'Arrival day').rename(columns = {"variable": "Line", "value": y_col})
    return data


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
            "Percent of Reservations": rel_bookings,
        }
    )
    return stay_nights


if __name__ == "__main__":
    main()