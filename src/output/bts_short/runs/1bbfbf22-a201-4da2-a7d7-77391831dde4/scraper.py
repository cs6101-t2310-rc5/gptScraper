import requests
from bs4 import BeautifulSoup
import json

def scraper(url):
    # make request
    response = requests.get(url)
    
    # parse html
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # get all products on page
    products = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    
    # create empty list to store data
    data = []
    
    for product in products:
        # extract title
        title = product.find('h3').get_text()
        
        # extract rating
        rating = product.find('p', class_='star-rating').get('class')[1]
        
        # extract price
        price = product.find('p', class_='price_color').get_text()[2:]
        
        # extract in_stock
        in_stock = product.find('p', class_='instock availability').get_text().strip()
        
        # add data to list
        data.append({
            'title': title,
            'rating': rating,
            'price': price,
            'in_stock': in_stock
        })
        
    # print data as json
    print(json.dumps(data))
    
if __name__ == '__main__':
    url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    scraper(url)