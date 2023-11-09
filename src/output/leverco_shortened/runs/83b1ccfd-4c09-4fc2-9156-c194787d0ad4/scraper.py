# imports
import requests
import bs4 
import json

def scraper(url: str) -> str:
    """
    Scrapes job listings from the given URL and prints out the title, tag, and apply_link for each job listing as JSON.
    """
    # send get request to the URL
    response = requests.get(url)
    # convert response content into BeautifulSoup object
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    # find all job listings on the page
    listings = soup.find_all('div', {'class': 'posting'})
    # initialize empty list to store job listings data
    job_listings = []
    for listing in listings:
        # extract title
        title = listing.find('h5', {'data-qa': 'posting-name'}).text
        # extract tag
        tag = listing.find('span', {'class': 'sort-by-location'}).text
        # extract apply link
        apply_link = listing.find('a', {'class': 'posting-btn-submit'})['href']
        # add job listing data to the list
        job_listings.append({
            "title": title,
            "tag": tag,
            "apply_link": apply_link
        })
    
    # print job listings as JSON
    print(json.dumps(job_listings, indent=4, sort_keys=True))

if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)