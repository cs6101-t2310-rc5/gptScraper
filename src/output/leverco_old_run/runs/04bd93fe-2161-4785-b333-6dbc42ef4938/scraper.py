# imports
import requests
from bs4 import BeautifulSoup
import json 

def scraper(url: str) -> str:
    # make a GET request to the url
    r = requests.get(url)
    # parse the html using BeautifulSoup
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # find all job postings
    postings = soup.find_all('div', class_="posting")

    # create a list to store job listings information
    job_listings = []

    # loop through the postings and extract the necessary information
    for posting in postings:
        # extract title
        title = posting.find('h5', {"data-qa": "posting-name"}).text.strip()
        # extract tag
        tag = posting.find('div', class_="posting-categories").find_all('span')[0].text.strip()
        # extract apply_link
        apply_link = posting.find('div', class_="posting-apply").find('a', class_="posting-btn-submit")['href']

        # create a dictionary to store the job listing information
        job_listing = {
            "title": title,
            "tag": tag,
            "apply_link": apply_link
        }
        # append the job listing to the list
        job_listings.append(job_listing)
        
    # convert the list to JSON format and print it out
    print(json.dumps(job_listings, indent=4))

if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)