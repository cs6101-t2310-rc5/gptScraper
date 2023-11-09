# imports
import bs4 
import requests
import json

def scraper(url: str) -> str:
  # Make request to the URL
  res = requests.get(url)

  # Use BeautifulSoup to parse the HTML
  soup = bs4.BeautifulSoup(res.text, 'html.parser')

  # Extract paper_title
  paper_title = soup.find('meta', attrs={'name': 'citation_title'})['content']

  # Extract authors
  author_names = []
  author_tags = soup.find_all('meta', attrs={'name': 'citation_author'})
  for tag in author_tags:
    author_names.append(tag['content'])

  # Extract abstract
  abstract = soup.find('meta', attrs={'name': 'citation_abstract'})['content']

  # Build dictionary with extracted data
  data = {
      'paper_title': paper_title,
      'authors': author_names,
      'abstract': abstract
  }

  # Convert dictionary to JSON and print out
  print(json.dumps(data, indent=4))

if __name__ == '__main__':
  url = "https://arxiv.org/abs/2311.01449"
  scraper(url)