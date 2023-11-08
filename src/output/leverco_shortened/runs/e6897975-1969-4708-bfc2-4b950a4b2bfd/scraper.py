# imports
import bs4
import json
import requests
from bs4 import BeautifulSoup

LIMIT = 20  # limits the number of job listings to retrieve


def get_jobs(url: str) -> list:
    # make GET request
    response = requests.get(url)
    # parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    # find all job postings
    postings = soup.find_all("div", class_="posting")
    # create empty list to store job listings
    job_listings = []
    # loop through postings and extract information
    for posting in postings[:LIMIT]:  # only retrieve specified number of job listings
        # extract title
        title = posting.find("h5", {"data-qa": "posting-name"}).text
        # extract workplace type
        workplace_type = posting.find("span", class_="workplaceTypes").find_next_sibling().text.strip()
        # extract commitment
        commitment = posting.find("span", class_="commitment").find_next_sibling().text.strip()
        # extract location
        try:
            location = posting.find("span", class_="location").find_next_sibling().text.strip()
        except:
            location = "N/A"
        # extract apply link
        apply_link = posting.find("div", {"data-qa": "btn-apply"}).find("a")['href']
        # create job listing dictionary
        job_listing = {"title": title, "tag": [workplace_type, commitment, location], "apply_link": apply_link}
        # append job listing to job listings list
        job_listings.append(job_listing)
    # return list of job listings
    return job_listings


def scraper(url: str):
    # call the get_jobs function with the specified url
    job_listings = get_jobs(url)
    # print job listings as JSON
    print(json.dumps(job_listings, indent=4))  # specify indent parameter for structured JSON output


if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)  # call the scraper function with the specified url