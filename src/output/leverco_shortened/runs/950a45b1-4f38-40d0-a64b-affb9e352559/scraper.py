# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:
    # make GET request to URL
    req = requests.get(url)

    # create BeautifulSoup object to parse HTML
    soup = BeautifulSoup(req.content, 'html.parser')

    # find all job listings on webpage
    listings = soup.find_all('div', class_='posting')

    # create empty list to store job listings 
    job_listings = []
    
    # loop through each job listing
    for listing in listings:
        # extract title from job listing
        title = listing.find('h5').text.strip()

        # extract tag from job listing if it exists
        if listing.find('span', class_='sort-by-time sort-by-time-listing') is not None:
            tag = listing.find('span', class_='sort-by-time sort-by-time-listing').text.strip()
        else:
            # if tag does not exist, set it to None
            tag = None

        # extract apply link from job listing
        apply_link = listing.find('a', class_='posting-btn-submit')['href']

        # create dictionary for job listing
        job = {
            'title': title,
            'tag': tag,
            'apply_link': apply_link
        }

        # append job listing to list
        job_listings.append(job)

    # convert job_listings list to JSON and print out
    print(json.dumps(job_listings))

if __name__ == '__main__':
    # provide URL to scrape
    url = "https://jobs.lever.co/appboxo"
    scraper(url)