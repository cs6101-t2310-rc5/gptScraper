# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:
    # scrape the website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # find all job listings
    job_listings = soup.find_all('div', class_="posting")

    # loop through each job listing and extract title, tag, and apply_link
    job_list = []
    for job in job_listings:
        # get title
        title = job.find('h5', attrs={'data-qa': 'posting-name'}).text.strip()

        # get tag
        tag = job.find('span', class_='sort-by-location posting-category small-category-label location').text.strip()

        # get apply link
        apply_link = job.find('div', class_='posting-apply').find('a', class_='posting-btn-submit').get('href')

        # create a dictionary with job information
        job_dict = {'title': title,
                    'tag': tag,
                    'apply_link': apply_link}

        # add job dictionary to job list
        job_list.append(job_dict)

    # convert job list to JSON and print
    print(json.dumps(job_list, indent=4))

if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)

# OUTPUT:
# [
#     {
#         "title": "Senior Frontend Engineer (Fully Remote)",
#         "tag": "China",
#         "apply_link": "https://jobs.lever.co/appboxo/70bf0681-36ed-4523-911d-12d1a69185fd"
#     },
#     {
#         "title": "Founder's Intern",
#         "tag": "Singapore",
#         "apply_link": "https://jobs.lever.co/appboxo/1487be26-4cfc-4f09-84fa-93ce86c3b0ee"
#     }
# ]