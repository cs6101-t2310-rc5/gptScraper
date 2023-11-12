# imports
import bs4 

def scraper(url: str) -> str:
  # make request to the url and parse the HTML
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  # get all the book listings on the page
  book_listings = soup.find_all('article', class_='product_pod')

  # create empty list to store data
  data_list = []

  # loop through each book listing and extract the desired data
  for book in book_listings:
    # extract title
    title = book.h3.a['title']

    # extract rating
    rating_class = book.p['class'][1]
    rating = rating_class[6:]

    # extract price
    price = book.find('p', class_='price_color').text

    # check for in stock
    in_stock = book.find('p', class_='instock availability').text.strip()

    # create dictionary with extracted data
    book_data = {
      'title': title,
      'rating': rating,
      'price': price,
      'in_stock': in_stock
    }

    # append dictionary to data_list
    data_list.append(book_data)

  # convert data_list to JSON format
  json_data = json.dumps(data_list)

  # print JSON data
  print(json_data)

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)