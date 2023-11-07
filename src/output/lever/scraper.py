# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import json

# Define the website URL
url = "https://jobs.lever.co/abridge"

# Send a GET request to the website and store the response
response = requests.get(url)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all job postings by their class names
postings = soup.find_all("div", {"class": "posting"})

# Create an empty list to store the job listings
job_listings = []

# Loop through each job posting and extract the relevant information
for posting in postings:
    job = {}

    # Get the job title
    job_title = posting.find("h5", {"data-qa": "posting-name"}).text.strip()
    job['title'] = job_title

    # Get the job location
    job_location = posting.find("span", {"class": "sort-by-location"}).text.strip()
    job['location'] = job_location

    # Get the job type
    job_type = posting.find("span", {"class": "sort-by-commitment"}).text.strip()
    job['type'] = job_type

    # Get the application link
    apply_link = posting.find("a", {"class": "posting-btn-submit"})['href']
    job['apply_link'] = apply_link

    # Add the job listing to the list
    job_listings.append(job)

# Print the job listings as JSON
print(json.dumps(job_listings, indent=4))