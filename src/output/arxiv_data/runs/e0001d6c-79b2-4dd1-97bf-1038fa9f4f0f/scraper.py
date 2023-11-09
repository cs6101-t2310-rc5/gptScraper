# imports
import requests
import bs4
import json

def scraper(url: str):
    """
    A function to scrape a webpage for paper title, authors, and abstract and print them out as JSON.
    
    Parameters:
    url (str): The URL of the webpage to be scraped
    
    Returns:
    None
    """
    
    # send a GET request to the URL
    response = requests.get(url)
    
    # check if the request was successful
    if response.status_code == 200:
        
        # use BeautifulSoup to parse the HTML content of the webpage
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        
        # extract the paper title using the 'citation_title' meta tag
        paper_title = soup.find('meta', {'name': 'citation_title'})['content']
        
        # extract the authors using the 'citation_author' meta tags 
        authors = []
        for tag in soup.findAll('meta', {'name': 'citation_author'}):
            authors.append(tag['content'])
        
        # extract the abstract using the 'property' meta tag
        abstract = soup.find('meta', {'property': 'og:description'})['content']
        
        # create a dictionary with the extracted data
        data = {'paper_title': paper_title, 'authors': authors, 'abstract': abstract}
        
        # print the dictionary as JSON
        print(json.dumps(data))
        
    else:
        # handle unsuccessful request
        print('Request was unsuccessful with status code: {}'.format(response.status_code))


if __name__ == '__main__':
    # specify the URL of the webpage to be scraped
    url = "https://arxiv.org/abs/2311.01449"
    
    # call the scraper function
    scraper(url)