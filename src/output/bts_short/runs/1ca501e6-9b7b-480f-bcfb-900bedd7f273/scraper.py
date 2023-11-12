# imports
import bs4 

def scraper(url: str) -> str:
  # retrieve page content
  res = requests.get(url)
  # create BeautifulSoup object
  soup = bs4.BeautifulSoup(res.text, "html.parser")
  
  # get title, rating, price, and in_stock for each book
  books_data = soup.find("ol", class_="row").find_all("article")
  
  # create empty list to store books
  books = []
  for book in books_data:
    # extract title
    title = book.find("h3").find("a")["title"]
    # extract rating
    rating = book.find("p", class_="star-rating")["class"][1]
    # extract price
    price = book.find("p", class_="price_color").text.strip("Â£")
    # extract in_stock
    in_stock = book.find("p", class_="instock availability").get_text(strip=True)
    # store book data in dictionary
    book_info = {
      "title": title,
      "rating": rating,
      "price": price,
      "in_stock": in_stock
    }
    # append book data to books list
    books.append(book_info)
    
  # convert books list to JSON format
  books_json = json.dumps(books, indent=4)
  # print out JSON data
  print(books_json)
  
if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)