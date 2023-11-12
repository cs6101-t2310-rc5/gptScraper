
# imports
import requests
import json
from bs4 import BeautifulSoup

def scraper(url: str) -> str:
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  book_list = []
  try:
    for book in soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'):
      title = book.find('h3').find('a')['title']
      rating = book.find('p', class_='star-rating')['class'][1]
      price = book.find('p', class_='price_color').get_text()[1:]
      if book.find('p', class_='instock availability').find('i')['class'][0] == 'icon-ok':
        in_stock = True
      else:
        in_stock = False
      book_data = {
        'title': title,
        'rating': rating,
        'price': price,
        'in_stock': in_stock
      }
      book_list.append(book_data)

    print(json.dumps(book_list, indent=2))
  except Exception as e:
    print("Exception: " + str(e))

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)