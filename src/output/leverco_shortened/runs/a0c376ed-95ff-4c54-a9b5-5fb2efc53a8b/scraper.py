# imports
import bs4 
import requests
import json

def scraper(url: str) -> str:
  # get webpage content
  page = requests.get(url)

  # create BeautifulSoup object
  soup = BeautifulSoup(page.content, 'html.parser')

  # find all job listings
  listings = soup.find_all('div', class_="posting")

  # initialize empty list to store data
  data = []

  # loop through job listings
  for listing in listings:
    # check if listing is not None
    if listing is not None:
      # extract title, tag and apply link from the listing
      title_tag = listing.find('h5', class_="posting-name")
      # check if title_tag is not None
      if title_tag is not None:
        title = title_tag.text.strip()
        tag = listing.find('span', class_="sort-by-commitment").text.strip()
        apply_link = listing.find('a', class_="posting-btn-submit").get('href')

        # store data in a dictionary
        entry = {
          'title': title,
          'tag': tag,
          'apply_link': apply_link,
        }

        # append dictionary to data list
        data.append(entry)

  # check if data list is not empty
  if len(data) > 0:
    # print data in JSON format
    print(json.dumps(data, indent=4))
  else:
    print("No data was found.")

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)