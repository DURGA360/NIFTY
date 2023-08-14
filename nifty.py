import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime
import pytz

# URL of the website
url = "https://www.moneycontrol.com/india/indexfutures/nifty/9/2023-08-17/OPTIDX/CE/17900.00/true"  # Replace with the URL you want to scrape

# Fetch the HTML content
response = requests.get(url)
html_content = response.content

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Define the CSS selector for the table
table_selector = '#optchain_div'  # Replace with the appropriate CSS selector for the table

# Find the table using the selector
table = soup.select_one(table_selector)

if table:
    # Extract data from the table (excluding the first row)
    table_data = []
    for row in table.select('tr')[1:]:
        row_data = [cell.get_text(strip=True) for cell in row.select('th, td')]
        table_data.append(row_data)
else:
    print("Table not found using the specified selector.")

# Get the timezone for Indian Standard Time (IST)
ist = pytz.timezone('Asia/Kolkata')

# Get the current time in IST
current_time_ist = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

# Add timestamp to the last row of the data
table_data[-1].append(current_time_ist)

# Authenticate and access Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
sheet = client.open('NIFTY').sheet1  # Replace with your sheet title

# Convert table data to a 2D list format for updating the entire range
table_data_with_timestamp = table_data + [['']] * (sheet.row_count - len(table_data))  # Add empty rows if needed

# Update the entire table range with the converted table data
sheet.update('A1', table_data_with_timestamp)
