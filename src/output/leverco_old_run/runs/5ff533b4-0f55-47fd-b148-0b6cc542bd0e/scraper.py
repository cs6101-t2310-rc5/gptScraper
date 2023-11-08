import requests
from bs4 import BeautifulSoup
import json

def scraper(url):
  # make GET request
  response = requests.get(url)

  # parse HTML and find all job listings
  soup = BeautifulSoup(response.content, 'html.parser')
  job_listings = soup.find_all('div', class_='postings-group')
  
  # create empty list to store job information
  job_info = []

  # loop through job listings
  for job in job_listings:
    # extract title, tag, and apply link
    title = job.find('h5', attrs={'data-qa': 'posting-name'}).text
    tag = job.find('span', class_='display-inline-block small-category-label workplaceTypes').text.replace('— ', '')
    apply_link = job.find('a', class_='posting-btn-submit').get('href')

    # store job information in dictionary
    job_dict = {
        'title': title,
        'tag': tag,
        'apply_link': apply_link
    }

    # append job dictionary to job info list
    job_info.append(job_dict)

  # convert job info list to JSON and print
  print(json.dumps(job_info, indent=4))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)