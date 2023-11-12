# imports
from bs4 import BeautifulSoup
import requests
import json

def scraper(url: str) -> str:
  # function to extract the relevant data from a book article
  def extract_book_info(book_article):
    # extract the title
    title = book_article.h3.a['title']

    # extract the rating
    rating_classes = book_article.select('p.star-rating')[0]['class']
    rating = ''.join([x[6:] for x in rating_classes])

    # extract the price
    price = float(book_article.select('p.price_color')[0].text[1:])

    # extract the in_stock status
    if 'In stock' in book_article.select('p.instock.availability')[0].text.strip():
      in_stock = True
    else:
      in_stock = False

    # return the extracted data as a dictionary
    return {'title': title, 'rating': rating, 'price': price, 'in_stock': in_stock}

  # initialize an empty list to store the book data
  books = []

  # make a get request to the provided url
  response = requests.get(url)

  # check the status code of the response
  if response.status_code == 200:
    # parse the html response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # select all the book articles 
    book_articles = soup.find_all('article', {'class': 'product_pod'})

    # loop through each book article and extract the relevant data
    for book_article in book_articles:
      # extract the data using the helper function
      book_data = extract_book_info(book_article)

      # add the data to the books list
      books.append(book_data)

    # print the extracted data as a JSON object
    print(json.dumps(books))

  else:
    # print a message if the response was not successful
    print("Unable to retrieve book data.")

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)