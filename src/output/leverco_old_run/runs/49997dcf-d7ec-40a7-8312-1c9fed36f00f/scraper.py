import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:

  # make request to the url
  response = requests.get(url)

  # create BeautifulSoup object
  soup = BeautifulSoup(response.text, "html.parser")

  # find all job listing containers
  job_listings = soup.find_all("div", {"class": "posting"})

  # iterate through each job listing and extract desired data
  job_info = []
  for job in job_listings:
    # extract title
    title = job.find("h5", {"data-qa": "posting-name"})
    if title is not None:
      title = title.text.strip()

    # extract tag
    tag = job.find("div", {"class": "posting-categories"})
    if tag is not None:
      tag = tag.text.strip()

    # extract apply_link
    apply_link = job.find("div", {"class": "posting-apply"})
    if apply_link is not None:
      apply_link = apply_link.find("a").get("href")

    # create dictionary to store job information
    job_dict = {"title": title, "tag": tag, "apply_link": apply_link}
    job_info.append(job_dict)

  # print out job information as JSON
  print(json.dumps(job_info, indent=4))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)