# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str):
  # get page content
  response = requests.get(url)
  # parse with BeautifulSoup
  soup = BeautifulSoup(response.content, 'html.parser')
  
  # find all postings
  postings = soup.find_all("div", {"class": "posting"})
  
  # loop through postings and extract desired data
  results = []
  for posting in postings:
    # extract title
    title = posting.find("h5", {"data-qa": "posting-name"}).get_text()
    # extract tag
    tags = posting.find_all("span", {"class": "small-category-label"})
    tag = tags[0].get_text().strip()
    # extract apply link
    apply_link = posting.find("a", {"class": "posting-btn-submit"})['href']
    
    # create dictionary with extracted data
    job = {
        "title": title,
        "tag": tag,
        "apply_link": apply_link
    }
    
    # append to results list
    results.append(job)
    
  # print results in JSON format
  print(json.dumps(results, indent=2))
  

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)