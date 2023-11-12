# imports
import bs4 
import requests
import json

def scraper(url: str) -> str:
  # retrieve webpage content
  req = requests.get(url)
  content = req.content
  
  # parse html content
  soup = bs4.BeautifulSoup(content, 'html.parser')

  # find all product_pod elements
  products = soup.find_all(class_="product_pod")

  # initialize empty list to store data
  data = []

  # loop through each product element
  for product in products:
    # extract title
    title = product.find("h3").find("a").get("title")
    
    # extract rating
    rating_class = product.find("p").get("class")[-1]
    rating = rating_class.replace("star-rating", "").strip()

    # extract price
    price = product.find(class_="price_color").get_text()

    # check if in stock
    in_stock = product.find(class_="availability").get_text().strip()

    # create dictionary with extracted data
    book = {'title': title,
            'rating': rating,
            'price': price,
            'in_stock': in_stock}
    
    # append book to data list
    data.append(book)

  # convert data list to JSON
  json_data = json.dumps(data)

  # print JSON data
  print(json_data)

if __name__ == '__main__':
  # specify url
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  # call scraper function with url as argument
  scraper(url)