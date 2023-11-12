# imports
import requests
import bs4
import json 

def scraper(url: str) -> None:
    # send request
    response = requests.get(url)
    
    # create BeautifulSoup object
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    
    # initialize list to store book data
    books = []
    
    # find all book containers
    containers = soup.find_all('article', {'class':'product_pod'})
    
    # loop through each container
    for container in containers:
        # initialize dictionary to store data for current book
        book_data = {}
        
        # extract title
        title = container.find('h3').find('a').get('title')
        book_data['title'] = title
        
        # extract rating
        rating = container.find('p', {'class':'star-rating'})['class'][1]
        book_data['rating'] = rating
        
        # extract price
        price = container.find('p', {'class':'price_color'}).text[1:].strip()
        book_data['price'] = price
        
        # extract availability
        availability = container.find('p', {'class':'availability'}).text.strip()
        book_data['in_stock'] = availability
        
        # add book data to list of books
        books.append(book_data)
        
    # convert books list to JSON format
    books_json = json.dumps(books)
    
    # print books JSON
    print(books_json)
    

if __name__ == '__main__':
    url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    scraper(url)
    
    
    


