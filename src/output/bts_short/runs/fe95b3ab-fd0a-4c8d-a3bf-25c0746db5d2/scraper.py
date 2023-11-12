# imports
import bs4 

def scraper(url: str) -> str:
  # get html response from url
  response = requests.get(url)

  # use BeautifulSoup to parse the html response
  soup = BeautifulSoup(response.text, 'html.parser')

  # find all the necessary book elements
  books = soup.find_all('article', class_='product_pod')

  # initialize empty list to store book data
  book_data = []

  # loop through each book and extract the necessary data
  for book in books:
    # extract title
    title = book.find('h3').find('a').get('title')

    # extract rating
    rating = book.find('p', class_='star-rating').get('class')[-1]

    # extract price
    price = book.find('p', class_='price_color').text[2:]

    # extract in_stock
    if book.find('p', class_='instock availability').text.strip() == 'In stock':
      in_stock = True
    else:
      in_stock = False

    # add extracted data to book_data list as a dictionary
    book_data.append({
      'title': title,
      'rating': rating,
      'price': price,
      'in_stock': in_stock
    })

  # convert book_data list to JSON format
  book_data_json = json.dumps(book_data)

  # print JSON data
  print(book_data_json)

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)