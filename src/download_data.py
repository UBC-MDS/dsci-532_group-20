# author: Trevor Kinsey
# date: 2021-01-19

'''This script downloads the data needed for data visualization dashboard
   and from the web and stores it in data/raw/hotels2.csv

Usage: download_data.py 

'''
import pandas as pd

def main():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv"
    file_path = "data/raw/hotels.csv"
    data = pd.read_csv(url)
    data.to_csv(file_path)
    print("Download complete")
    
if __name__ == "__main__":
    main()