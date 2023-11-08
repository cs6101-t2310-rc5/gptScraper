# Import necessary libraries
import bs4 
import requests
import json

def scraper(url: str) -> str:
  # Make a GET request to the provided URL
  response = requests.get(url)

  # Parse the content of the response using Beautiful Soup
  soup = bs4.BeautifulSoup(response.content, 'html.parser')

  # Find the relevant HTML elements containing the desired data and extract the text
  paper_title = soup.find('h1', class_='title mathjax').text.replace('Title:','').strip()
  authors = soup.find('div', class_='authors').text.replace('Authors:','').strip()
  abstract = soup.find('blockquote', class_='abstract mathjax').text.replace('Abstract:','').strip()

  # Create a dictionary with the extracted data
  data = {
      'paper_title': paper_title,
      'authors': authors,
      'abstract': abstract
  }

  # Convert the dictionary to JSON format and print it out
  print(json.dumps(data, indent=4))


if __name__ == '__main__':
  url = "https://arxiv.org/abs/2311.01449"
  scraper(url)