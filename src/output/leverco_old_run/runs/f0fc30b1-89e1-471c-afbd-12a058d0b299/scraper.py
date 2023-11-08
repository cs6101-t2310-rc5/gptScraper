

# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url):
    """
    Function to scrape the given url and extract job listings with their title, tag and apply_link.
    
    Parameters:
        url (str): The url to be scraped.
        
    Returns:
        str (json): The extracted data in JSON format.
    """
    response = requests.get(url) # get the web page
    soup = BeautifulSoup(response.text, "html.parser") # parse the HTML
    listings = soup.find_all('div', {'class':'posting'}) # find all job listings on the page
    
    data = [] # create an empty list to store the extracted data
    
    # loop through each job listing and extract the required information
    for listing in listings:
        title = listing.find('h5').text # extract the job title
        tag = listing.find('span', {'class':'display-inline-block small-category-label workplaceTypes'}).text # extract the tag
        apply_link = listing.find('a', {'class':'posting-btn-submit'}).get('href') # extract the apply link
        
        # create a dictionary to store the extracted data
        job = {
            'title': title,
            'tag': tag,
            'apply_link': apply_link
        }
        
        data.append(job) # append the dictionary to the data list
    
    # print the extracted data in JSON format
    print(json.dumps(data, indent=4))
    
if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)
    
# Sample output:
# [
#     {
#         "title": "Senior Frontend Engineer (Fully Remote)",
#         "tag": "Remote\u200a—\u200a",
#         "apply_link": "https://jobs.lever.co/appboxo/70bf0681-36ed-4523-911d-12d1a69185fd"
#     },
#     {
#         "title": "Founder's Intern",
#         "tag": "On-site\u200a—\u200a",
#         "apply_link": "https://jobs.lever.co/appboxo/1487be26-4cfc-4f09-84fa-93ce86c3b0ee"
#     }
# ]