
# imports
import bs4 
import json
import requests 

def scraper(url: str) -> str: 
    # fetch the page 
    response = requests.get(url) 

    # parse the HTML 
    soup = bs4.BeautifulSoup(response.text, 'html.parser') 

    # find the paper title 
    paper_title = soup.find('h1', class_='title mathjax').text 

    # find the authors 
    authors = soup.find('div', class_='authors').text.replace('Authors:','').split(',') 

    # find the abstract 
    abstract = soup.find('blockquote', class_='abstract mathjax').text.replace('Abstract:','').strip() 

    # create dictionary 
    paper_info = {'paper_title': paper_title, 'authors': authors, 'abstract': abstract} 

    # print as JSON 
    print(json.dumps(paper_info)) 

if __name__ == '__main__': 
    url = 'https://arxiv.org/abs/2311.01449' 
    scraper(url)