# imports
import requests
from bs4 import BeautifulSoup
import json 

def scraper(url: str) -> str:
    # get page content
    page = requests.get(url)
    
    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # find all job listings
    job_listings = soup.find_all('div', class_='posting')
    
    # loop through each job listing
    for listing in job_listings:
        # check if listing has title h5 tag
        if listing.find('h5', class_='posting-title') is not None:
            # extract title from h5 tag
            title = listing.find('h5', class_='posting-title').text
        else:
            # if no title, set to N/A
            title = "N/A"
        
        # check if listing has tag div tag
        if listing.find('div', class_='sort-by-time posting-category small-category-label') is not None:
            # extract tag from div tag
            tag = listing.find('div', class_='sort-by-time posting-category small-category-label').text.strip()
        else:
            # if no tag, set to N/A
            tag = "N/A"
        
        # check if listing has apply link a tag
        if listing.find('a', class_='apply') is not None:
            # extract apply link from a tag
            apply_link = f"https://jobs.lever.co{listing.find('a', class_='apply').get('href')}"
        else:
            # if no apply link, set to N/A
            apply_link = "N/A"
        
        # create job dictionary
        job = {'title': title, 'tag': tag, 'apply_link': apply_link}
        
        # print job data as JSON
        print(json.dumps(job))


if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)