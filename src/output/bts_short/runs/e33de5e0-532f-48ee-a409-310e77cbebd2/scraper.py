

# imports
import bs4 
import json
import requests

def scraper(url: str):
  # get webpage content
  res = requests.get(url)
  res.raise_for_status()
  # parse webpage content
  soup = bs4.BeautifulSoup(res.text, "html.parser")
  # create list to store book information
  books = []
  # iterate through each book on the page
  for book in soup.find_all("article", class_="product_pod"):
    # extract title
    title = book.h3.a.get("title")
    # extract rating
    rating = book.p.get("class")[1]
    # extract price
    price = None 
    try:
      price = float(book.find("p", class_="price_color").text.strip("£").replace("Â",""))
    except ValueError:
      print("Unable to convert price to float for book", title)
    # check if book is in stock
    in_stock = book.find("p", class_="instock availability").text.strip() != "In stock"
    # create a dictionary for each book and append to books list
    book = {
      "title": title,
      "rating": rating,
      "price": price, 
      "in_stock": in_stock
    }
    books.append(book)
  # print out list of books in JSON format
  print(json.dumps(books))

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)