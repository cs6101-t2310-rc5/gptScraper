# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> str:
    # send request to the provided url
    res = requests.get(url)
    # parse the html content using BeautifulSoup
    soup = BeautifulSoup(res.content, 'html.parser')
    # find all div tags with class 's-post-summary'
    posts = soup.find_all('div', class_='s-post-summary')
    # initialize lists to store the extracted data
    question_titles = []
    tags = []
    user_names = []
    # iterate through each post
    for post in posts:
        # extract question title
        question_title = post.find('h3', class_='s-post-summary--content-title').text.strip()
        # extract tags
        tags_list = []
        tags_container = post.find('ul', class_='js-post-tag-list-wrapper')
        for tag in tags_container.find_all('a', class_='post-tag'):
            tags_list.append(tag.text.strip())
        # extract user name
        meta_user = post.find('div', class_='s-post-summary--meta-user')
        if meta_user:
            link = meta_user.find('a', class_='s-link')
            if link:
                user_name = link.text.strip()
        else:
            user_name = ''

        # add the extracted data to respective lists
        question_titles.append(question_title)
        tags.append(tags_list)
        user_names.append(user_name)

    # combine the lists of data into a dictionary
    data = {
        "question_title": question_titles,
        "tags": tags,
        "user_name": user_names
    }

    # convert the dictionary to JSON
    json_data = json.dumps(data)

    # print out the JSON data for the top questions
    print(json_data)

if __name__ == '__main__':
    url = "https://math.stackexchange.com/questions"
    scraper(url)