# imports
import requests
import bs4
import json

# function to scrape job listings for title, tag, and apply_link
def scraper(url: str) -> str:
    # use requests library to get the webpage html
    response = requests.get(url)

    # use bs4 to parse the html and find the job listings
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    job_listings = soup.find_all('div', class_='posting')

    # initialize empty dictionary to store job data
    job_data = {}

    # loop through job listings
    for job in job_listings:

        # find title
        title = job.find('h5').text.strip()

        # find tag
        tag = job.find('span', class_='sort-by-commitment posting-category small-category-label commitment').text.strip()

        # find apply link
        apply_link = job.find('a', class_='posting-btn-submit template-btn-submit black')['href'].strip()

        # add job data to dictionary
        job_data[title] = {
            'tag': tag,
            'apply_link': apply_link
        }

    # print job data in JSON format
    print(json.dumps(job_data, indent=4))

if __name__ == '__main__':
    url = 'https://jobs.lever.co/appboxo'
    scraper(url)