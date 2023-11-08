# imports
import requests
import bs4 
import json

# function to scrape data from given URL
def scraper(url: str):
  # send a GET request to the URL
  response = requests.get(url)
  # parse the HTML content using BeautifulSoup
  soup = bs4.BeautifulSoup(response.content, 'html.parser')
  # initialize lists to store data
  titles = []
  tags = []
  links = []
  # find all job listings on the page
  job_listings = soup.find_all('div', class_='posting')
  # loop through each job listing
  for job in job_listings:
    # extract title
    title = job.find('h5', class_='posting-name').text if job.find('h5', class_='posting-name') else 'N/A'
    # extract tag
    tag = job.find('span', class_='workplaceTypes').text if job.find('span', class_='workplaceTypes') else 'N/A'
    # extract apply link
    link = job.find('a', class_='posting-btn-submit').get('href') if job.find('a', class_='posting-btn-submit') else 'N/A'
    # append data to respective lists
    titles.append(title)
    tags.append(tag)
    links.append(link)
  # create a dictionary to store data
  data = {
      'title': titles,
      'tag': tags,
      'apply_link': links
  }
  # convert dictionary to JSON and print it out
  print(json.dumps(data, indent=2))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)