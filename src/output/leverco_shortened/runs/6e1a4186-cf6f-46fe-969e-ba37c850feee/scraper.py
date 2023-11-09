# imports
import bs4 
import requests
import json 

def scraper(url):
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.content, 'html.parser')
  job_listings = soup.findAll('div', class_='posting')

  results = []
  for job in job_listings:
    title = job.find('h5', attrs={'data-qa': 'posting-name'}).get_text()
    tag = job.find('span', class_='sort-by-commitment posting-category small-category-label commitment').get_text()
    apply_link = job.find('div', class_='posting-apply').find('a').get('href')

    data = {
      'title': title,
      'tag': tag,
      'apply_link': apply_link
    }
    results.append(data)

  if len(results) > 0:
    print(json.dumps(results))
  else:
    return "No job listings found on this page."

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)