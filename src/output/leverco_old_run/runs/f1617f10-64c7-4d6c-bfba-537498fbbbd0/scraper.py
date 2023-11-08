# imports
import requests
from bs4 import BeautifulSoup
import json 

def scraper(url: str) -> str:
  # scraper logic goes here
  # get webpage content
  response = requests.get(url)
  # parse webpage content
  soup = BeautifulSoup(response.content, 'html.parser')
  # find all "posting" divs
  postings = soup.find_all(class_="posting")
  # create empty list to store data
  data = []
  # loop through "posting" divs
  for post in postings:
    # get title
    title = post.find('h5').text
    # get tag
    tags = post.find_all(class_="small-category-label")
    tag = ''
    for t in tags:
      if t.text != 'Full-time' and t.text != 'Remote':
        tag += t.text + " "
    # get apply link
    try:
      apply_link = post.find(class_="posting-apply").a['href']
    except:
      apply_link = ''
    # add data to list
    data.append({
        'title': title,
        'tag': tag,
        'apply_link': apply_link
    })
  # convert data to JSON and print
  print(json.dumps(data))

if __name__ == '__main__':
  url = 'https://jobs.lever.co/appboxo'
  scraper(url)