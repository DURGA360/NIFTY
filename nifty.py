# Import necessary libraries
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Define the URL to scrape
url = "https://www.moneycontrol.com/india/indexfutures/nifty/9/2023-08-17/OPTIDX/CE/17900.00/true"

@app.route('/api/nifty-options', methods=['GET'])
def get_nifty_options():
    # Fetch the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Define the CSS selector for the table
    table_selector = '#optchain_div'

    # Find the table using the selector
    table = soup.select_one(table_selector)

    if table:
        # Extract data from the table (excluding the first row)
        table_data = []
        for row in table.select('tr')[1:]:
            row_data = [cell.get_text(strip=True) for cell in row.select('th, td')]
            table_data.append(row_data)
    else:
        return jsonify({'error': 'Table not found using the specified selector.'}), 404

    # Get the timezone for Indian Standard Time (IST)
    ist = pytz.timezone('Asia/Kolkata')

    # Get the current time in IST
    current_time_ist = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

    # Add timestamp to the last row of the data
    table_data[-1].append(current_time_ist)

    return jsonify({'data': table_data})

if __name__ == '__main__':
    app.run(debug=True)
