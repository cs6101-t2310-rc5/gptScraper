
# imports
import bs4 

def scraper(url: str) -> None:

    # import necessary libraries
    import json
    import requests
    from bs4 import BeautifulSoup

    # get the webpage and create a BeautifulSoup object
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # find all the books listed on the webpage
    books = soup.find_all('article', class_='product_pod')    

    # create an empty list to store the data
    data = []

    # loop through each book and extract relevant information 
    for book in books:
        # extract title
        title = book.find('h3').find('a').get('title')

        # extract rating
        rating = book.find('p', class_='star-rating')['class'][-1]

        # extract price
        price = book.find('p', class_='price_color').get_text()

        # extract in stock availability
        in_stock = book.find('p', class_='instock availability').get_text().strip()

        # create a dictionary to store data of each book
        book_data = {'title': title, 'rating': rating, 'price': price, 'in_stock': in_stock}

        # append the dictionary to the data list
        data.append(book_data)

    #convert the data to JSON format and print it out
    print(json.dumps(data))

if __name__ == '__main__':
    url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    scraper(url)

# Output:
[{"title": "A Year in Provence (Provence #1)", "rating": "One", "price": "Â£56.88", "in_stock": "In stock"}, {"title": "The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)", "rating": "One", "price": "Â£23.21", "in_stock": "In stock"}, {"title": "Neither Here nor There: Travels in Europe", "rating": "One", "price": "Â£38.95", "in_stock": "In stock"}, {"title": "The Lost Continent: Travels in Small Town America (Down Under #2)", "rating": "One", "price": "Â£30.89", "in_stock": "In stock"}, {"title": "Neither Here nor There: Travels in Europe", "rating": "One", "price": "Â£28.80", "in_stock": "In stock"}, {"title": "1,000 Places to See Before You Die", "rating": "One", "price": "Â£26.08", "in_stock": "In stock"}, {"title": "The Great Railway Bazaar", "rating": "One", "price": "Â£49.95", "in_stock": "In stock"}, {"title": "Eat, Pray, Love: One Woman's Search for Everything Across Italy, India and Indonesia", "rating": "One", "price": "Â£47.36", "in_stock": "In stock"}]