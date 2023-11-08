# imports
import requests
from bs4 import BeautifulSoup
import json 

def scraper(url: str) -> str:
  # request webpage
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')

  # extract paper_title
  paper_title = soup.find('h1', class_='title mathjax').text.strip()

  # extract authors
  authors = []
  author_elem = soup.find('div', class_='authors')
  for a in author_elem.find_all('a'):
    if a.get('title') == 'Author Profile Page':
      continue
    authors.append(a.text.strip())

  # extract abstract
  abstract = soup.find('blockquote', class_='abstract mathjax').text.strip()

  # create dictionary object
  data = {
    'paper_title': paper_title,
    'authors': authors,
    'abstract': abstract
  }

  # print json data
  print(json.dumps(data, indent=2))

  return "Data successfully scraped and printed as JSON"

if __name__ == '__main__':
  url = "https://arxiv.org/abs/2311.01449"
  scraper(url)