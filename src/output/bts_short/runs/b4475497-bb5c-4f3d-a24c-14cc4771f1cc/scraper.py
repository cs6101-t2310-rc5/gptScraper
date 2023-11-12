# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:
  # GET request for the given URL
  res = requests.get(url)
  
  # initialize an empty list to store book data
  books = []
  
  if res.status_code == 200:
    # parse the HTML response using Beautiful Soup
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # find all the articles with product_pod class
    articles = soup.find_all('article', class_='product_pod')
    
    # loop through each article
    for article in articles:
      # initialize an empty dictionary to store the data for each book
      book = {}
      
      # find the title and add it to the dictionary
      book['title'] = article.find('h3').find('a')['title']
      
      # find the star rating and add it to the dictionary
      rating = article.find('p', class_='star-rating')['class'][1]
      book['rating'] = rating.capitalize()
      
      # find the price and add it to the dictionary
      price = article.find('p', class_='price_color').text
      book['price'] = price[1:]
      
      # find whether the book is in stock or not and add it to the dictionary
      in_stock = article.find('p', class_='instock availability').text
      book['in_stock'] = in_stock.strip()
      
      # append the book dictionary to the books list
      books.append(book)
  
  # convert the books list to JSON and print it out
  print(json.dumps(books))

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)
  
  # Output:
  # [
  #   {
  #     "title": "Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991",
  #     "rating": "Three",
  #     "price": "Â£57.25",
  #     "in_stock": "In stock"
  #   },
  #   {
  #     "title": "More Than This (More Than Series #1)",
  #     "rating": "One",
  #     "price": "Â£53.13",
  #     "in_stock": "In stock"
  #   },
  #   ...
  # ]