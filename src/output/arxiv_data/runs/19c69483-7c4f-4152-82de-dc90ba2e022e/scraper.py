# imports
import bs4 
from bs4 import BeautifulSoup
import requests
import json

def scraper(url: str) -> str:
  # Scraping the webpage
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # Extracting the necessary data
  paper_title = soup.find("meta", {"name":"citation_title"})['content']
  authors = [author['content'] for author in soup.find_all("meta", {"name":"citation_author"})]
  date = soup.find("meta", {"name":"citation_online_date"})['content']
  abstract = soup.find("meta", {"name":"twitter:description"})['content']

  # Creating a dictionary with the data
  data = {
      "paper_title": paper_title,
      "authors": authors,
      "date": date,
      "abstract": abstract
  }

  # Printing out the data as JSON
  print(json.dumps(data))

if __name__ == '__main__':
  # Inputting the desired URL
  url = "https://arxiv.org/abs/2311.01449"
  scraper(url)