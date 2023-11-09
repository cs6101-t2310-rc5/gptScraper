# imports
import bs4 

def scraper(url: str) -> str:
  # get request
  response = requests.get(url)

  # parse html
  soup = bs4.BeautifulSoup(response.content, 'html.parser')

  # create empty list
  job_listings = []

  # loop through all job postings
  for posting in soup.select('.posting'):

    # title
    title = posting.select_one('.posting-title h5').text.strip()

    # tag
    tags = posting.select('.posting-categories span')
    tag = [t.text.strip() for t in tags]

    # apply link
    apply_link = posting.select_one('a.posting-btn-submit').get('href')

    # create dictionary
    job_listing = {
      'title': title,
      'tag': tag,
      'apply_link': apply_link
    }

    # add dictionary to list
    job_listings.append(job_listing)

  # print out job listings as JSON
  print(json.dumps(job_listings))
  
if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)