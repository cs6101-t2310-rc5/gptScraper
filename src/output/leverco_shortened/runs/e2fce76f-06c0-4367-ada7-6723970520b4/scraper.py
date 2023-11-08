# imports
import bs4
import requests
import json

def scraper(url: str):
  # add headers to simulate a real browser
  headers = {'User-Agent': 'Mozilla/5.0'}

  # fetch website
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    # parse HTML
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # find all job listings
    jobs = soup.find_all('div', class_='posting')

    # create empty list to store data
    data = []

    # loop through job listings
    for job in jobs:
      # extract title, tag, apply link
      title = job.find('h5', attrs={'data-qa': 'posting-name'}).text.strip()
      tag = job.find('span', class_='display-inline-block').text
      apply_link = job.find('a', class_='posting-btn-submit')['href']

      # create dictionary with data
      job_data = {'title': title, 'tag': tag, 'apply_link': apply_link}

      # append to list
      data.append(job_data)

    # print data as JSON
    print(json.dumps(data, indent=2))
    
  else:
    print("Could not fetch website. Error code:", response.status_code)

if __name__ == '__main__':
  url = 'https://jobs.lever.co/appboxo'
  scraper(url)