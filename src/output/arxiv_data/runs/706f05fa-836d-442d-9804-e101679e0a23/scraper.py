# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:
  # GET request
  response = requests.get(url)

  # parse html
  soup = BeautifulSoup(response.content, 'html.parser')

  # extract paper title
  paper_title = soup.find('h1', {'class': 'title mathjax'}).text.strip('Title:')

  # extract authors
  authors = [author.text for author in soup.find('div', {'class': 'authors'}).find_all('a')]

  # extract abstract
  abstract = soup.find('blockquote', {'class': 'abstract'}).text.strip('Abstract:')

  # create dictionary of extracted data
  data = {
    'paper_title': paper_title,
    'authors': authors,
    'abstract': abstract
  }

  # print data as JSON
  print(json.dumps(data, indent=2))

if __name__ == '__main__':
  url = "https://arxiv.org/abs/2311.01449"
  scraper(url)