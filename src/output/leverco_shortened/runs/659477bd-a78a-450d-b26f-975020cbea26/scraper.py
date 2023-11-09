
# imports
import json
import requests
from bs4 import BeautifulSoup

def scraper(url):
  # load page
  page = requests.get(url)

  # parse HTML using BeautifulSoup
  soup = BeautifulSoup(page.content, 'html.parser')

  # find all job listings
  listings = soup.find_all('div', class_='posting')

  # loop through listings and extract data
  data = []
  for listing in listings:
    # check if title element exists
    if listing.find('title') is not None:
        # get title from <title> tag
        title = listing.find('title').get_text()
    else:
        # assign default value or skip extracting title
        title = ""

    # check if meta tag with property attribute equal to 'og:title' exists
    if listing.find('meta', {'property': 'og:title'}) is not None:
        # check if content attribute is not None
        if listing.find('meta', {'property': 'og:title'})['content'] is not None:
            # get tag from <meta> tag
            tag = listing.find('meta', {'property': 'og:title'})['content']
        else:
            # assign default value or skip extracting tag
            tag = ""
    else:
        # assign default value or skip extracting tag
        tag = ""

    # get apply link from listing <a> tag
    apply_link = listing.find('a', class_='posting-btn-submit')['href']

    # append data to list
    data.append({'title': title, 'tag': tag, 'apply_link': apply_link})

  # convert data to JSON and print
  json_data = json.dumps(data, indent=2)
  print(json_data)

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)  # call scraper function with provided URL to print out the extracted data as JSON