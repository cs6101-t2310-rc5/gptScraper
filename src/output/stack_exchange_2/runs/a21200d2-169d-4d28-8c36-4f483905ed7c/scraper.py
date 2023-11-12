# imports
import bs4
import requests
import json


def scraper(url: str) -> str:
    # Make a GET request to the specified URL
    response = requests.get(url)

    # Create a soup object from the response's text content
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # Find all div elements with the s-post-summary class
    question_items = soup.find_all('div', class_='s-post-summary')

    # Create an empty list to store the data
    data = []

    # Loop through each question item
    for item in question_items:

        # Find the question title, tags, and user name
        question_title = item.find('h3', class_='s-post-summary--content-title').text.strip()
        tags = [tag.text.strip() for tag in item.find_all('a', class_='post-tag')]

        # Check if the user-details span exists before attempting to find the user name
        # Assign a default value of None if it does not exist
        user_name = None
        if item.find('span', class_='user-details'):
            user_name = item.find('span', class_='user-details').find('a', class_='s-link').text.strip()

        # Create a dictionary to store the extracted data and append it to the list
        question_data = {'question_title': question_title, 'tags': tags, 'user_name': user_name}
        data.append(question_data)

    # Print out the data in JSON format
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    url = "https://math.stackexchange.com/questions"
    scraper(url)