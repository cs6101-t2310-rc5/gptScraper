# imports
import requests
import bs4 

def scraper(url: str) -> str:
  # fetch webpage
  response = requests.get(url)
  # initialize BeautifulSoup object
  soup = bs4.BeautifulSoup(response.text, 'html.parser')
  # find all job postings
  postings = soup.select('div.posting')
  # initialize empty list to store extracted data
  postings_data = []
  # loop through each job posting and extract the necessary data
  for posting in postings:
    # extract tags
    tags = [tag.text.strip() for tag in posting.select('span.small-category-label') if tag.text.strip()]
    # extract job title
    title = posting.select_one('h5[data-qa="posting-name"]').text.strip()
    # extract apply link
    apply_link = posting.select_one('a[class="posting-btn-submit template-btn-submit black"]')['href']
    # create a dictionary of extracted data
    data = {
      'title': title,
      'tags': tags,
      'apply_link': apply_link
    }
    # append to postings_data list
    postings_data.append(data)
  # print the extracted data in JSON format  
  print(json.dumps(postings_data, indent=2))
  return json.dumps(postings_data)

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)