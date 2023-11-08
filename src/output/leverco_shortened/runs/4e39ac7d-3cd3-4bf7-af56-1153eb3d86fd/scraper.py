# imports
import bs4 
import requests
import json
from bs4 import BeautifulSoup

def scraper(url):
  # make request to URL
  response = requests.get(url)
  
  # create BeautifulSoup object
  soup = BeautifulSoup(response.content, "html.parser")
  
  # find all postings
  postings = soup.findAll(class_="posting")
  
  # initialize empty list to store job listings
  job_listings = []
  
  # loop through postings and extract desired data
  for posting in postings:
    # extract title
    title = posting.find("h5", {"data-qa": "posting-name"}).text.strip()
    
    # extract tag (workplace type)
    try:
      tag = posting.find(class_="display-inline-block small-category-label workplaceTypes").text.strip()
    except:
      tag = "None"
    
    # extract apply link
    apply_link = posting.find("a", {"data-qa": "btn-apply"})
    if apply_link is not None:
      apply_link = apply_link['href']
    else:
      apply_link = None
    
    # create dictionary to store data for each job listing
    job_listing = {
      "title": title,
      "tag": tag,
      "apply_link": apply_link
    }
    
    # add job listing to list of job listings
    job_listings.append(job_listing)
  
  # convert list of job listings to JSON string
  job_listings = json.dumps(job_listings, indent=4)
  
  # print out job listings as JSON string
  print(job_listings)

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)