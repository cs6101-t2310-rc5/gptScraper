import requests
from bs4 import BeautifulSoup
import json

# Set url to scrape
url = "https://jobs.lever.co/BDG"

# Send get request
page = requests.get(url)

# Parse HTML
soup = BeautifulSoup(page.content, 'html.parser')

# Find all job listings
job_listings = soup.find_all('div', class_='posting')

# Create empty list to store extracted data
job_data = []

# Loop through each job listing
for job in job_listings:
    # Extract job title
    title = job.find('h5').get_text().strip()

    # Extract job location
    location = job.find('span', class_='sort-by-location').get_text().strip()

    # Extract job link
    job_link = job.find('a')['href']

    # Create dictionary for each job and append to job_data list
    job_dict = {
        'title': title,
        'location': location,
        'job_link': job_link
    }
    job_data.append(job_dict)

# Convert job_data list to JSON format
json_data = json.dumps(job_data)

# Print out extracted data
print(json_data)
