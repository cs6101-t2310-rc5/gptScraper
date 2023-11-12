def scraper(url):
  # import necessary libraries
  import requests
  from bs4 import BeautifulSoup
  import json
  
  # make request to the url and get the HTML content
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html.parser')
  
  # find all the divs with class dno js-hidden and loop through them
  results = []
  for div in soup.find_all('div', {'class': 'dno js-hidden'}):
    # extract question title from the previous sibling of the div
    question_title = div.previous_sibling.text
    
    # find the a tag inside the div with class post-tag and get the tag name
    tags = div.find('a', {'class': 'post-tag'}).text
    
    # extract the user name from the previous sibling of the a tag
    user_name = div.find_previous_sibling().text
    
    # add the extracted data to the results list as a dictionary
    results.append({
        'question_title': question_title,
        'tags': tags,
        'user_name': user_name
    })
  
  # print the results in JSON format
  print(json.dumps(results, indent=2))
  
if __name__ == '__main__':
  url = "https://math.stackexchange.com/questions"
  scraper(url)