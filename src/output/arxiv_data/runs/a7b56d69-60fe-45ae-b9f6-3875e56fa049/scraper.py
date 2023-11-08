# imports
import bs4 
import requests

def print_json(title, authors, abstract):
    json = {
        "title": title,
        "authors": authors,
        "abstract": abstract
    }
    print(json)

def scraper(url: str) -> None:
    # Get webpage
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Extract title
    titleTag = soup.find("meta", {"name": "citation_title"})
    title = titleTag['content']

    # Extract authors
    authorsTag = soup.find_all("meta", {"name": "citation_author"})
    authors = []
    for authorTag in authorsTag:
        authors.append(authorTag['content'])

    # Extract abstract
    abstractTag = soup.find("meta", {"name": "twitter:description"})
    abstract = abstractTag['content']

    # Print JSON
    print_json(title, authors, abstract)

if __name__ == '__main__':
  url = "https://arxiv.org/abs/2311.01449"
  scraper(url)