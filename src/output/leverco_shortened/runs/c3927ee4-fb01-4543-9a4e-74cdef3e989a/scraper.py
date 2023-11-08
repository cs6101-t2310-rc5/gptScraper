# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> None:
  # send request to url
  response = requests.get(url)
  # parse HTML with BeautifulSoup
  soup = BeautifulSoup(response.content, 'html.parser')
  # find all postings on the webpage
  postings = soup.find_all(class_='posting')
  # create empty list for storing job listings
  job_listings = []
  # loop through each posting
  for posting in postings:
    # extract job title
    job_title = posting.find(class_='posting-title').find('h5').text.strip()
    # check if job tag exists
    if posting.find(class_='small-category-label workplaceTypes') is not None:
      # extract job tag
      job_tag = posting.find(class_='small-category-label workplaceTypes').text.strip()
    else:
      # assign None to job tag if it doesn't exist
      job_tag = None
    # extract apply link
    apply_link = posting.find(class_='posting-apply').find('a')['href']
    # create dictionary for job listing
    job_dict = {'title': job_title, 'tag': job_tag, 'apply_link': apply_link}
    # append dictionary to list
    job_listings.append(job_dict)
  # print out job listings as JSON
  print(json.dumps(job_listings, indent=2))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)