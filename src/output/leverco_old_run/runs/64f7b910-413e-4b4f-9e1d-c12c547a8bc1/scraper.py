# imports
import bs4

def scraper(url: str) -> str:
    # Make a GET request to the given URL
    response = requests.get(url)
    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all job listings
    job_listings = soup.find_all('div', class_='posting')
    # Initialize empty list to store extracted data
    data = []
    # Loop through each job listing
    for job in job_listings:
        # Extract job title
        title = job.find('h5', {'data-qa': 'posting-name'}).text
        # Extract job category
        # Check if category is present
        if job.find('div', {'class': 'posting-category-title'}) is not None:
            category = job.find('div', {'class': 'posting-category-title'}).text
        else:
            category = 'No category available'
        # Extract job commitment
        commitment = job.find('span', {'class': 'sort-by-commitment'}).text
        # Extract job location
        location = job.find('span', {'class': 'sort-by-location'}).text
        # Find and extract the apply link
        href = job.find('a', class_='posting-btn-submit').get('href')
        # Create a dictionary for the extracted data
        job_data = {
            'title': title,
            'category': category,
            'commitment': commitment,
            'location': location,
            'apply_link': href
        }
        # Append the dictionary to the data list
        data.append(job_data)
    # Convert data list to JSON format
    result = json.dumps(data)
    # Print out the result
    print(result)

if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)