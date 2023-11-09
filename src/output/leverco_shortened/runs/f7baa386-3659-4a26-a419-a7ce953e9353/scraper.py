# imports
import requests
from bs4 import BeautifulSoup
import json

# define scraper function
def scraper(url: str):
    # request page
    response = requests.get(url)

    # create BeautifulSoup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # find job listings
    job_listings = soup.find_all('div', class_='posting')

    # loop through job listings and extract relevant data
    for job in job_listings:
        # extract title
        title = job.find('h5').text.strip()

        # extract tag
        if job.find('a', class_='sort-by-time post-category') is not None:
            tag = job.find('a', class_='sort-by-time post-category').text.strip()
        else:
            tag = ''

        # extract apply_link
        if job.find('a', class_='apply-link') is not None:
            apply_link = job.find('a', class_='apply-link')['href'].strip()
        else:
            apply_link = ''

        # create dictionary to store data
        job_dict = {
            'title': title,
            'tag': tag,
            'apply_link': apply_link
        }

        # print data as JSON
        print(json.dumps(job_dict))

if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url) # calling the scraper function with given URL