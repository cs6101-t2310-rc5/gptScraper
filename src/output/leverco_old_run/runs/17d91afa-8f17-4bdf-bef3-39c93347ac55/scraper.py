# imports
import requests
from bs4 import BeautifulSoup
import json 

def scraper(url: str) -> str:
  # Make a GET request to the provided url and store the response as a variable
  response = requests.get(url)
  
  # Use BeautifulSoup to parse the html
  soup = BeautifulSoup(response.content, 'html.parser')
  
  # Find all the job listings
  job_listings = soup.find_all('div', class_='posting')
  
  # Loop through each job listing and extract the title, tag, and apply link
  job_list = []
  for job in job_listings:
      title = job.find('h5', {'data-qa': 'posting-name'}).text
      tags = job.find_all('span', class_='small-category-label')
      # Check if job has a 'btn-apply' tag before trying to get the 'href' attribute
      if job.find('a', {'data-qa': 'btn-apply'}):
        apply_link = job.find('a', {'data-qa': 'btn-apply'}).get('href')
      else:
        apply_link = "N/A"
      job_dict = {
          'title': title,
          'tag': tags[0].text,
          'apply_link': apply_link
      }
      job_list.append(job_dict)
  
  # Convert the job list into a JSON format and print it out
  job_json = json.dumps(job_list)
  print(job_json)
  
if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)