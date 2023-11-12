
# imports
import requests
from bs4 import BeautifulSoup

def scraper(url: str):
    # make a GET request to the specified URL
    response = requests.get(url)

    # create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all the articles with class 'product_pod'
    articles = soup.find_all('article', class_='product_pod')

    # create a dictionary to store the extracted data
    data = {}

    # loop through the articles
    for article in articles:
        # extract the title
        title = article.find('h3').find('a')['title']

        # extract the rating
        rating = article.find('p', class_='star-rating')['class'][1]

        # extract the price
        price = article.find('p', class_='price_color').text.strip()[1:]

        # check if the book is in stock or not
        in_stock = article.find('p', class_='instock availability').find('i')['class'][0] == 'icon-ok'
        
        # add the extracted data to the dictionary
        data[title] = {
            'rating': rating,
            'price': price,
            'in_stock': in_stock
        }

    # print out the data in JSON format
    print(json.dumps(data, indent=4))
    
if __name__ == '__main__':
    url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    scraper(url)