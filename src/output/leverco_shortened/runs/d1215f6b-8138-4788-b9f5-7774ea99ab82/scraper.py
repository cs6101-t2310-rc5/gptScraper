# imports
import bs4 
import requests
import json

def scraper(url: str) -> str:
  # get webpage
  req = requests.get(url)
  # load webpage content into beautiful soup
  soup = bs4.BeautifulSoup(req.content, "html.parser")
  # find all job listings
  listings = soup.find_all("div", class_="posting")

  # loop through each job listing
  for listing in listings:
    # extract title
    title = listing.find("h5", class_="posting-name")
    if title:
      title = title.text
    else:
      title = ""
    # extract tag
    tag = listing.find("span", class_="sort-by-commitment")
    if tag:
      tag = tag.text
    else:
      tag = ""
    # extract apply link
    apply_link = listing.find("a", class_="posting-btn-submit")
    if apply_link:
      apply_link = apply_link["href"]
    else:
      apply_link = ""
    # create dictionary with extracted data
    job = {
      "title": title,
      "tag": tag,
      "apply_link": apply_link
    }
    # print job data as json
    print(json.dumps(job))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)