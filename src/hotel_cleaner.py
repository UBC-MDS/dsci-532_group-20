# hotel_cleaner.py
# author: Trevor Kinsey
# date: 2021-01-19

'''This script cleans and wrangles the hotels.csv file to be used
   in a visualization dashboard app

Usage: python hotel_cleaner.py

'''
import numpy as np
import pandas as pd

# import the data
hotels = pd.read_csv("data/raw/hotels.csv")

# create `arrival_date` column from other columns
months = ["January", "February", "March", "April",
          "May", "June", "July", "August", "September", 
          "October", "November", "December"]
hotels["month"] = hotels["arrival_date_month"].replace(months,[1,2,3,4,5,6,7,8,9,10,11,12])
hotels["Arrival date"] = pd.to_datetime(hotels.arrival_date_year*10000 + hotels.month*100 + hotels.arrival_date_day_of_month, 
                                        format = '%Y%m%d')
# drop unused columns
hotels = hotels.drop(columns=['Unnamed: 0','agent', 'company', 'month'])
hotels.columns

# Change values to make more readable
hotels["hotel"] = hotels["hotel"].replace(["Resort Hotel", "City Hotel"], ["Resort", "City"])
hotels["is_canceled"] = hotels["is_canceled"].replace([0, 1], ["No", "Yes"])
hotels["meal"] = hotels["meal"].replace(["BB", "HB", "FB"], ["Bed & Breakfast", "Half board", "Full boar/d"])
hotels["distribution_channel"] = hotels["distribution_channel"].replace(["TA", "TO"], ["Travel agent", "Tour operator"])
hotels["is_repeated_guest"] = hotels["is_repeated_guest"].replace([0, 1], ["No", "Yes"])
hotels.head()

# change column names
hotels.columns = ['Hotel type', 'Canceled', 'Lead time (days)', 'Arrival year',
       'Arrival month', 'Arrival week',
       'Arrival date', 'Weekend nights',
       'Week nights', 'Adults', 'Children', 'Babies', 'Meal type',
       'Country of origin', 'Market segment', 'Distribution channel',
       'Repeated guest', 'Previous cancellations',
       'Previous bookings not canceled', 'Reserved room type',
       'Assigned room type', 'Booking changes', 'Deposit type',
       'Days in waiting list', 'Customer type', 'Average daily rate',
       'Required parking spaces', 'Special requests',
       'Reservation status', 'Reservation status date', 'Arrival date']

hotels.to_csv("data/processed/clean_hotels.csv")