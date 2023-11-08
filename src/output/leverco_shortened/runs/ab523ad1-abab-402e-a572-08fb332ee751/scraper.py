# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str):
    # make request to job listings page
    response = requests.get(url)

    # parse HTML using Beautiful Soup
    soup = BeautifulSoup(response.text, "html.parser")

    # find all job listings
    job_listings = soup.find_all("div", class_="posting")

    # loop through job listings
    for listing in job_listings:
        # extract title
        title = listing.find("h5", attrs={"data-qa": "posting-name"}).text.strip()

        # extract tag (work type)
        if listing.find("span", class_="sort-by-commitment posting-category") is None:
            # if class does not exist, assign empty string
            tag = ""
        else:
            # extract tag
            tag = listing.find("span", class_="sort-by-commitment posting-category").text.strip()

        # extract apply link
        apply_link = listing.find("a", class_="posting-btn-submit").get("href")

        # create dictionary with extracted data
        job_data = {"title": title, "tag": tag, "apply_link": apply_link}

        # print as JSON
        print(json.dumps(job_data, indent=2))

if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)