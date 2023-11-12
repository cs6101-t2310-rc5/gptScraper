# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:
  # send request to the url
  response = requests.get(url)

  # parse the HTML response using BeautifulSoup
  soup = BeautifulSoup(response.text, 'html.parser')

  # find all the top question items on the page
  top_questions = soup.find_all('div', class_="question-summary")

  # initialize empty list to store extracted data
  questions_data = []

  # loop through each top question
  if not top_questions:
    # handle empty list error
    print("No questions were found on the page.")
  else:
    for question in top_questions:
      # extract question_title
      question_title = question.find('h3', class_="s-post-summary--content-title").text.strip()

      # extract tags
      tags = [tag.text for tag in question.find_all('a', class_="post-tag")]

      # extract question_excerpt
      question_excerpt = question.find('div', class_="s-post-summary--content-excerpt").text.strip()

      # create dictionary with extracted data
      data = {
        "question_title": question_title,
        "tags": tags,
        "question_excerpt": question_excerpt
      }

      # append dictionary to questions_data list
      questions_data.append(data)

    # convert questions_data to json format
    questions_json = json.dumps(questions_data)

    # print out json data
    print(questions_json)

if __name__ == '__main__':
  url = "https://math.stackexchange.com/questions"
  scraper(url)