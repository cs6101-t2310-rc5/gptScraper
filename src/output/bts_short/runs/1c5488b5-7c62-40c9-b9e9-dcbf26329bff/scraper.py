import bs4 
import json 

def scraper(url: str) -> str:
  # use the bs4 library to parse the HTML from the url
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.text, 'html.parser')

  # create an empty list to store the extracted data
  books = []

  # find all the products in the HTML snippet
  products = soup.find_all('article', class_='product_pod')

  # loop through each product and extract the relevant data
  for product in products:
    # extract title, rating, price, and in_stock from the HTML elements
    title = product.h3.a['title']

    # extract rating as a string and convert to integer
    rating = product.find('p', class_='star-rating')['class'][1]
    try:
      rating = int(rating)
    except ValueError:
      rating = 0 # default value in case rating cannot be converted

    price = product.find('p', class_='price_color').text

    # extract in_stock status by checking for the presence of the 'icon-ok' class
    in_stock = 'In stock' if product.find('p', class_='instock availability').find('i', class_='icon-ok') else 'Out of stock'

    # create a dictionary to store the extracted data for each book
    book = {
        'title': title,
        'rating': rating,
        'price': price,
        'in_stock': in_stock
    }

    # append the book dictionary to the list of books
    books.append(book)

  # print out the list of books as a JSON string
  print(json.dumps(books, indent=2))

  # return 'Success' if the scraper function successfully runs
  return 'Success'

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)