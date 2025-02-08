import pandas as pd
from bs4 import BeautifulSoup
import os

# read csv file
# First save the csv file to an absolute path on your computer,
# and then perform subsequent file operations. 
# Be careful not to upload your own absolute path!!!

# csv_path = "Resume.csv"    

# Here is the absolute path while Resume.csv is in achieve/Resume folder
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "archive", "Resume", "Resume.csv")

print("CSV Path:", csv_path)

df = pd.read_csv(csv_path)
 
# View the previous rows of data
print(df.head())
html_col = df.iloc[:,2]
html_col.head()

