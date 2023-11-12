# imports
import requests
import bs4

def scraper(url: str) -> str:
  # get page
  page = requests.get(url)
  # create soup object
  soup = bs4.BeautifulSoup(page.content, 'html.parser')
  # find all articles with class 'product_pod'
  articles = soup.find_all('article', class_='product_pod')
  # create empty list to store results
  results = []
  # loop through each article
  for article in articles:
    # extract title
    title = article.find('h3').find('a').get('title')
    # extract rating
    rating = article.find('p', class_='star-rating')['class'][1]
    # extract price
    price = article.find('p', class_='price_color').text[1:]
    # extract in_stock
    in_stock = article.find('p', class_='instock availability').text.strip()
    # append results to list
    results.append({'title': title,
                    'rating': rating,
                    'price': price,
                    'in_stock': in_stock})
  # print results as JSON
  print(json.dumps(results))
  # return results as JSON string
  return json.dumps(results)

if __name__ == '__main__':
  url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
  scraper(url)