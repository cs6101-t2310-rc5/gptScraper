# imports
import requests
import bs4 
import json

def scraper(url: str) -> None:
    # request the webpage using the url
    response = requests.get(url)
    
    # check for successful request
    if response.status_code == 200:
        # use BeautifulSoup to parse the webpage
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        
        # create a list to store all book data
        books = []
        
        # loop through each book in the webpage
        for book in soup.find_all('article', class_='product_pod'): 
            # create a dictionary to store the current book's data
            book_info = {}
            
            # extract the book title and add to dictionary
            title = book.find('h3').find('a').get('title')
            book_info['title'] = title
            
            # extract the rating and add to dictionary
            rating = book.find('p', class_='star-rating').get('class')
            # extract only the number from the class name
            try:
                rating_num = int(rating[1])
            except:
                rating_num = None
            book_info['rating'] = rating_num
            
            # extract the price and add to dictionary
            price = book.find('p', class_='price_color').text
            book_info['price'] = price
            
            # extract the stock availability and add to dictionary
            in_stock = book.find('p', class_='availability').text.strip()
            book_info['in_stock'] = in_stock
            
            # add the book dictionary to the list of books
            books.append(book_info)
        
        # convert the list of books into JSON format
        books_json = json.dumps(books)
        
        # print out the data in JSON format
        print(books_json)
    
    else:
        print('Error: Could not access webpage.')
    
if __name__ == '__main__':
    url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html' 
    scraper(url)