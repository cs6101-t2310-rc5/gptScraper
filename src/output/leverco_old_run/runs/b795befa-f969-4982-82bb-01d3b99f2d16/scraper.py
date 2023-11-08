
# imports
import bs4 

def scraper(url: str) -> dict:
  # retrieve webpage content
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.text, 'html.parser')

  # find all job listings
  job_listings = soup.find_all('div', class_='posting')

  # initialize empty list for storing job data
  job_data = []

  # loop through each job listing
  for job in job_listings:
    # extract title
    title = job.find('h5', attrs={'data-qa': 'posting-name'}).text

    # extract tag
    tag = job.find('span', class_='sort-by-commitment').text

    # extract apply link
    apply_link = job.find('a', class_='posting-btn-submit')['href']

    # append job data to list
    job_data.append({
        'title': title,
        'tag': tag,
        'apply_link': apply_link
    })

  # print job data as JSON
  print(json.dumps(job_data))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)