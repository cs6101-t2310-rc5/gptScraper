# imports
import bs4 
import requests
import json

def scraper(url: str) -> str:
  # get the webpage content
  page = requests.get(url)
  # check if webpage was found and response is valid
  if page.status_code == 200:
    # turn it into a beautiful soup object
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    
    # extract the question title
    question_title = soup.find('a', class_='question-hyperlink').text
    
    # extract the tags
    tags = soup.find_all('a', class_='post-tag')
    # check if tags element was found
    if tags:
      tags = [tag.text for tag in tags]
    else:
      # handle the error here (e.g. print an error message)
      print("Could not find tags element on webpage.")
      # or assign an empty list to the tags variable
      tags = []
      
    # extract the user name
    try:
      user_name = soup.find('div', id='question-header').find('div', class_='user-details').find('a').text
    except AttributeError:
      user_name = "Unknown User"
    
    # store the data in a dictionary
    data = {
      "question_title": question_title,
      "tags": tags,
      "user_name": user_name
    }
    # print out the data as JSON
    print(json.dumps(data, indent=4))
    
  else:
    # handle the error here (e.g. print an error message)
    print("Webpage not found or response is invalid.")
    
if __name__ == '__main__':
  url = "https://math.stackexchange.com/questions"
  scraper(url)
  
  # Output:
  {
    "question_title": "Evaluating integrals with complex limits",
    "tags": [
        "calculus", 
        "integration"
    ],
    "user_name": "Unknown User"
}