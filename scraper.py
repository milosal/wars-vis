import requests
from bs4 import BeautifulSoup
import json

# Helper functions
def process_date_range(date_range):
    # Split the date range into start and end dates
    if '–' in date_range:
        start_date, end_date = date_range.split('–', 1)
    elif '-' in date_range:
        start_date, end_date = date_range.split('-', 1)
    else:
        # If there's no range, both start and end dates are the same
        start_date = end_date = date_range

    # Further processing can be added here if needed

    return start_date.strip(), end_date.strip()

# URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_wars_by_death_toll'

# Sending a request to the URL
response = requests.get(url)
data = response.text

# Parsing the HTML content
soup = BeautifulSoup(data, 'html.parser')

# Find the tables that contain the data
tables = soup.find_all('table', {'class': 'wikitable'})

# Initialize an empty list to store war data
war_data = []

# Process the data from each table
for table in tables:
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skipping the header row
        cols = row.find_all('td')
        if len(cols) > 1:  # Ensure there are enough columns in the row
            war_name = cols[0].get_text(strip=True)
            date_range = cols[2].get_text(strip=True)
            death_toll = cols[1].get_text(strip=True).split('[')[0]  # Remove citations

            start_date, end_date = process_date_range(date_range)

            war_entry = {
                "name": war_name,
                "start_date": start_date,
                "end_date": end_date,
                "death_toll": death_toll
            }
            war_data.append(war_entry)

# Display the first few entries for review
print(war_data[:5])

war_data_json = json.dumps(war_data, indent=4)

# Write the JSON string to a file
with open('data.json', 'w') as file:
    file.write(war_data_json)
