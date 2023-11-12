import bs4

def scraper(url):
    response = requests.get(url) #get html from url
    soup = bs4.BeautifulSoup(response.content, 'html.parser') #create soup object
    results = [] #list to store scraped data
    books = soup.find_all('article', class_='product_pod') #find all articles with class="product_pod"
    
    for book in books:
        title = book.h3.a.text #get title
        rating = book.p['class'][1] #get rating
        price = book.find('div', class_='product_price').find('p', class_='price_color').text #get price
        availability = book.find('div', class_='product_price').find('p', class_='instock availability').text.strip() #get availability
        
        #clean up scraped data
        availability = availability.replace('In stock (', '').replace(' available)', '')
        
        #add data to results list
        results.append({
            'title': title,
            'rating': rating,
            'price': price,
            'in_stock': availability
        })
    
    #print data as JSON
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    scraper(url)
