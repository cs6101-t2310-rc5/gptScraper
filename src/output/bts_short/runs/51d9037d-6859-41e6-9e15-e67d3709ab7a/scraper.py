
# imports
import requests
import bs4 
import json

def scraper(url: str) -> str:

  # use requests to get the page content
  response = requests.get(url)

  # use beautiful soup to parse the content
  soup = bs4.BeautifulSoup(response.text, "html.parser")

  # find all book elements
  books = soup.find_all("article", {"class": "product_pod"})

  # initialize empty list to store book data
  book_list = []

  # loop through each book element
  for book in books:

    # initialize dictionary to store book data
    book_data = {}

    # extract book title
    title = book.find("h3").find("a")["title"]
    book_data["title"] = title

    # extract book rating
    rating = book.find("p", {"class": "star-rating"})["class"][1]
    book_data["rating"] = rating

    # extract book price
    price = book.find("p", {"class": "price_color"}).text
    book_data["price"] = price

    # extract book availability
    availability = book.find("p", {"class": "instock availability"}).text
    book_data["in_stock"] = availability.strip()

    # add book data to list of books
    book_list.append(book_data)

  # print out book data in JSON format
  print(json.dumps(book_list))

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)
