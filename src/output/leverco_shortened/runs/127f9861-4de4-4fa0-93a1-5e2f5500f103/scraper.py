import bs4
import requests

def scraper(url: str) -> str:
  # make GET request to the given URL
  response = requests.get(url)
  # parse the HTML using BeautifulSoup
  soup = bs4.BeautifulSoup(response.text, 'html.parser')
  # find all job posting div elements
  postings = soup.find_all('div', class_='posting')
  # create a list to store the extracted data
  data = []
  # loop through each job posting
  for posting in postings:
    # extract the job title
    title = posting.find('h5', attrs={'data-qa': 'posting-name'}).text.strip()
    # extract the job tag
    tag = posting.find('span', class_='sort-by-location posting-category small-category-label location').text.replace('Remote', ' ').strip()
    # change Singapore to Hybrid for consistency
    if tag == 'Singapore':
      tag = 'Hybrid'
    # extract the apply link
    apply_link = posting.find('a', class_='posting-btn-submit template-btn-submit black')['href']
    # create a dictionary to store the extracted data
    job = {
        'title': title,
        'tag': tag,
        'apply_link': apply_link
    }
    # add the job data to the list
    data.append(job)
  # print the data in JSON format
  print(json.dumps(data, indent=2))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)