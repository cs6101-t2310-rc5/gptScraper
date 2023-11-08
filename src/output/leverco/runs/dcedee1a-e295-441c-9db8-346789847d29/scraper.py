import requests
import bs4 

def scraper(url: str) -> str:
  # get webpage content
  response = requests.get(url)
  # parse webpage content
  webpage = bs4.BeautifulSoup(response.content, 'html.parser')
  
  # extract job listings 
  job_listings = webpage.find_all("div", class_="posting")

  # initialize list to store extracted data as dictionaries
  extracted_data = []
  # loop through job listings
  for listing in job_listings:
    # extract job title
    title = listing.find("h5", attrs={"data-qa": "posting-name"}).get_text()
    # extract workplace type
    workplace_type = listing.find("span", class_="workplaceTypes").get_text()
    # extract commitment
    commitment = listing.find("span", class_="commitment").get_text()
    # extract location
    location = listing.find("span", class_="location").get_text()
    # extract application link
    apply_link = listing.find("a", class_="posting-btn-submit").get("href")

    # create dictionary to store extracted data
    job_data = {"title": title,
                "workplace_type": workplace_type,
                "commitment": commitment,
                "location": location,
                "apply_link": apply_link}
    
    # append dictionary to list
    extracted_data.append(job_data)

  # print extracted data as JSON
  print(json.dumps(extracted_data))
  
  return "Successfully scraped and printed data in JSON format!"

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)