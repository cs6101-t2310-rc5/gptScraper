# imports
import bs4 
import json

def scraper(url: str) -> str:
    # get the HTML from the webpage
    page = requests.get(url).content
    # create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(page, 'html.parser')
    # extract the relevant information from the HTML using the BeautifulSoup methods
    paper_title = soup.find('meta', {"name": "twitter:title"})['content'] # extract the paper's title
    authors = [author.text for author in soup.find_all('meta', {"name": "citation_author"})] # extract list of authors
    abstract = soup.find('meta', {"name": "twitter:description"})['content'] # extract the abstract
    # create a dictionary of the extracted information
    data = {"paper_title": paper_title, "authors": authors, "abstract": abstract}
    # convert the dictionary to JSON and print it out
    print(json.dumps(data))
    
if __name__ == '__main__':
    url = 'https://arxiv.org/abs/2311.01449'
    scraper(url)