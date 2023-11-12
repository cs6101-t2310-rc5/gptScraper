# imports
import bs4
import requests
import json

def scraper(url: str) -> str:
    # make a get request to the url
    response = requests.get(url)

    # use BeautifulSoup to parse the html
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # find all the question-summary divs which contain all the information we need
    question_summaries = soup.find_all('div', {'class': 'question-summary'})

    # create an empty list to store the results
    results = []

    # check if the question_summaries list is not empty
    if len(question_summaries) > 0:

        # loop through each question-summary div
        for question in question_summaries:

            # extract the title
            question_title = question.find('a', {'class': 'question-hyperlink'}).text.strip()

            # extract the tags
            tags = [tag.text for tag in question.find_all('a', {'class': 'post-tag'})]

            # extract the user name
            user_name = question.find('a', {'class': 'user-details'}).text.strip()

            # extract the number of votes
            votes = int(question.find('span', {'class': 'vote-count-post'}).text)

            # extract the number of answers
            answers = int(question.find('div', {'class': 'status'}).text.strip().split()[0])

            # extract the number of views
            views = int(question.find('div', {'class': 'views'}).text.strip().split()[0])

            # extract the timestamp
            timestamp = question.find('span', {'class': 'relativetime'})['title']

            # create a dictionary with the extracted information
            result = {
                'question_title': question_title,
                'tags': tags,
                'user_name': user_name,
                'votes': votes,
                'answers': answers,
                'views': views,
                'timestamp': timestamp
            }

            # append the dictionary to the results list
            results.append(result)

        # convert the list to json
        results_json = json.dumps(results)

        # print out the json
        print(results_json)

    else:
        # if question_summaries list is empty, print an error message
        print("No data was extracted. Please check the scraping logic.")

if __name__ == '__main__':
    url = "https://math.stackexchange.com/questions"
    scraper(url)