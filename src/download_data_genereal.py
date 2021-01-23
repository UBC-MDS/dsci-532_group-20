# author: Trevor Kinsey
# date: 2021-01-19

'''This script downloads data from a url and stores it in a file.

Usage: download_data.py <url> <file_path>

# Options:
# --url=<url>               url of data source
# --file_path=<file_path>   Path to the data file output

'''
import pandas as pd
# import numpy as np
from docopt import docopt

opt = docopt(__doc__)

def main(url, file_path):
    data = pd.read_csv(url)
    data.to_csv(file_path)
    print("Download complete")
    
if __name__ == "__main__":
    main(opt["<url>"], opt["<file_path>"])