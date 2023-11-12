
# imports
import bs4 
import requests
import json
from bs4 import BeautifulSoup

def scraper(url: str):
  # scraper logic goes here
  # request webpage
  response = requests.get(url)
  # create soup object
  soup = BeautifulSoup(response.content, 'html.parser')
  # find all articles with class product_pod
  articles = soup.find_all('article', class_="product_pod")
  # initialize empty list for data
  data_list = []
  # loop through articles and extract data
  for article in articles:
      # extract title
      title = article.find('h3').find('a')['title']
      # extract rating
      rating = article.find('p', class_="star-rating")['class'][1]
      # extract price
      price = article.find('p', class_="price_color").text
      # extract in_stock
      try:
        # extract data from article with class "instock availability"
        in_stock = article.find('p', class_="instock availability").find('i')['class'][1]
      except:
        try:
          # try to extract data from article with class "availability"
          in_stock = article.find('p', class_="availability").find('i')['class'][1]
        except:
          # if both fail, set default value of "in_stock"
          in_stock = "Out of Stock"
      # create dictionary for data
      data = {'title': title,
              'rating': rating,
              'price': price,
              'in_stock': in_stock}
      # append data to list
      data_list.append(data)
  # convert list to json
  json_data = json.dumps(data_list)
  # print json data
  print(json_data)

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)