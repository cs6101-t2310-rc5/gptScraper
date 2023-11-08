# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:
  # send GET request to the URL
  response = requests.get(url)

  # create BeautifulSoup object for parsing
  soup = BeautifulSoup(response.text, 'html.parser')

  # initialize empty list for job listings
  job_listings = []

  # scrape all job listings on the page
  listings = soup.find_all('div', class_='posting')

  # loop through each job listing and extract title, tag, and apply_link
  for listing in listings:
    # extract title
    title = None
    if listing.find('h5', class_='posting-title'):
        title = listing.find('h5', class_='posting-title').text.strip()

    # extract tag
    tag = None
    if listing.find('span', class_='sort-by-tag-wrapper'):
        tag = listing.find('span', class_='sort-by-tag-wrapper').text.strip()

    # extract apply_link
    apply_link = None
    if listing.find('a', class_='posting-btn-submit'):
        apply_link = listing.find('a', class_='posting-btn-submit')['href']

    # append data to job listings list
    job_listings.append({
        'title': title,
        'tag': tag,
        'apply_link': apply_link
    })

  # print job listings as JSON
  print(json.dumps(job_listings, indent=2))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)