# imports
import requests
import json
from bs4 import BeautifulSoup

def scraper(url):
  # request webpage
  page = requests.get(url)
  # create BeautifulSoup object
  soup = BeautifulSoup(page.content, 'html.parser')

  # find all product elements
  products = soup.findAll(class_="product_pod")
  # create empty list to store books data
  books = []

  for product in products:
    # extract title
    title = product.find('h3').getText()
    # extract rating
    rating_class = product.find(class_="star-rating")['class'][1]
    rating = rating_class.replace('One', '1').replace('Two', '2').replace('Three', '3').replace('Four', '4').replace('Five', '5')
    # extract price
    price = product.find(class_="price_color").getText()
    # extract in stock status
    stock_status = product.find(class_="availability").find('i')['class'][0]
    if stock_status == 'icon-ok':
      in_stock = True
    else:
      in_stock = False
    # create dictionary for book data
    book = {
      'Title': title,
      'Rating': rating,
      'Price': price,
      'In Stock': in_stock
    }
    # add book to list
    books.append(book)

  # convert list to JSON and print
  print(json.dumps(books))

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)