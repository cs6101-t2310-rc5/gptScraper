import bs4
import json

def scraper(url: str) -> dict:
    # Get the webpage content
    res = requests.get(url)
    # Use BeautifulSoup to parse the webpage
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the paper title
    paper_title = soup.find('h1').text

    # Find the list of authors
    authors = []
    authors_section = soup.find('div', {'class': 'authors'})
    for author in authors_section.find_all('a'):
        authors.append(author.text)

    # Find the abstract
    abstract = soup.find('blockquote', {'class': 'abstract mathjax'}).text

    # Create a dictionary with the extracted information
    result = {
        'paper_title': paper_title,
        'authors': authors,
        'abstract': abstract
    }

    # Print the result as JSON
    print(json.dumps(result))

if __name__ == '__main__':
    url = "https://arxiv.org/abs/2311.01449"
    scraper(url)