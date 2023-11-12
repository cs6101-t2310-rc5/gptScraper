
# imports
from bs4 import BeautifulSoup
import requests
import json

def scraper(url: str) -> None:
  # get the HTML content from the webpage
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')
  
  # create a list to store all the extracted data
  books_list = []
  
  # loop through each book and extract the desired data
  for book in soup.find_all('article', class_='product_pod'):
    
    # extract the title
    title = book.h3.a['title']
    
    # extract the rating
    rating = book.find('p', class_='star-rating')['class'][-1]
    
    # extract the price
    price = book.find('p', class_='price_color').text.strip()[1:]
    
    # extract the availability information
    in_stock = book.find('p', class_='instock availability').text.strip()
    
    # append the extracted data to the list as a dictionary
    books_list.append({'title': title, 'rating': rating, 'price': price, 'in_stock': in_stock})
  
  # convert the list into a JSON string and print it out
  print(json.dumps(books_list, indent=2))
  

if __name__ == '__main__':
  url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
  scraper(url)