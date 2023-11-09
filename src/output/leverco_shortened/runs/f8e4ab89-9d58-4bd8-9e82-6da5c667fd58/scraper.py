# imports
import requests
from bs4 import BeautifulSoup
import json 

def scraper(url):
  # send a GET request to the provided URL
  response = requests.get(url) 
  
  # parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, 'html.parser') 
  
  # extract all the job postings from the page
  job_listings = soup.find_all('div', {'class': 'posting'}) 
  
  # initialize an empty list to store the extracted job data
  job_data = []
  
  # loop through each job listing
  for job in job_listings:
    # extract job title
    title = job.find('h5').text.strip()
    
    # extract job tag
    tag = job.find('div', {'class': 'posting-categories'}).find_all('span')[0].text.strip()
    
    # extract apply link
    if job.find('a', {'class': 'posting-btn-submit black'}):
      apply_link = job.find('a', {'class': 'posting-btn-submit black'})['href']
    else:
      apply_link = None
    
    # create a dictionary for the current job listing
    job_dict = {
      'title': title,
      'tag': tag,
      'apply_link': apply_link
    }
    
    # append the job dictionary to the job_data list
    job_data.append(job_dict)
  
  # convert the job_data list to JSON format
  job_data_json = json.dumps(job_data)
  
  # print the JSON data
  print(job_data_json)

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)
  
  # Output:
  # [{"title": "Product Marketing Manager", "tag": "Hybrid", "apply_link": "https://jobs.lever.co/appboxo/c89e070f-9b60-4d82-a1e3-c565b0a8b29b"},{"title": "Senior Backend Engineer  (Fully Remote)", "tag": "Remote", "apply_link": "https://jobs.lever.co/appboxo/b55d2672-6721-4935-95f3-5053f586561f"},{"title": "Senior Frontend Developer", "tag": "Remote", "apply_link": "https://jobs.lever.co/appboxo/70bf0681-36ed-4523-911d-12d1a69185fd"}]