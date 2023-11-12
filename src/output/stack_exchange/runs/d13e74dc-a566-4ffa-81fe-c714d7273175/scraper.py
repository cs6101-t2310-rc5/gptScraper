
# Imports
import requests
import bs4
import json

# Function to scrape the website
def scraper(url: str) -> str:
  # Send get request to the URL
  response = requests.get(url)

  # Use BeautifulSoup to parse the response
  soup = bs4.BeautifulSoup(response.text, 'html.parser')

  # Check response status code
  if response.status_code != 200:
    print("Error: Response code is not 200.")
    print("Debugging info:")
    print(response.text)
    return

  # Find all div elements with class 'question-summary'
  question_list = soup.find_all('div', class_ = 'question-summary')

  # Create empty list to store question data
  questions = []

  # Loop through the list of div elements
  for question in question_list:
    # Get the title of the question
    question_title = question.find('a', class_ = 'question-hyperlink').text

    # Get the tags of the question
    tags = []
    for tag in question.find_all('a', class_ = 'post-tag'):
      tags.append(tag.text)

    # Get the username of the person who asked the question
    user_name = question.find('div', class_ = 'user-details').find_next('a').text

    # Get the number of votes for the question
    votes = question.find('span', class_ = 'vote-count-post').text

    # Get the number of answers for the question
    answers = question.find('div', class_ = 'status').find_next('strong').text

    # Get the number of views for the question
    views = question.find('div', class_ = 'views').find_next('div').text.strip()

    # Get the timestamp of when the question was asked
    timestamp = question.find('div', class_ = 'user-action-time').find_next('span', class_ = 'relativetime').text

    # Create a dictionary with the question data
    question_data = {
      'question_title': question_title,
      'tags': tags,
      'user_name': user_name,
      'votes': votes,
      'answers': answers,
      'views': views,
      'timestamp': timestamp
    }

    # Add the question data to the list
    questions.append(question_data)

  # Check if the list is not empty
  if questions:
    # Convert the list to JSON format
    json_output = json.dumps(questions)

    # Return the JSON data
    return json_output

  # If the list is empty, print an error message
  else:
    print("No data was scraped. Check if you are scraping correctly.")

# Main function to call the scraper function and pass in the URL
if __name__ == '__main__':
  url = 'https://math.stackexchange.com/questions'
  print(scraper(url))