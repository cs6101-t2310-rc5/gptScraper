# imports
import bs4 
import requests
import json

def scraper(url: str) -> str:
    # send get request to the url
    response = requests.get(url)

    # create a bs4 object from the response
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # find all divs with 'posting' class
    postings = soup.find_all('div', class_='posting')

    # create an empty list to store the data
    data = []

    # loop through each posting
    for posting in postings:

        # extract title by finding h5 tag
        title = posting.find('h5').text.strip()

        # extract tag by finding all span tags with class 'display-inline-block'
        tags = posting.find_all('span', class_='display-inline-block')

        # initialize an empty list to store the tags
        tag_list = []

        # loop through each tag and extract the text
        for tag in tags:
            tag_list.append(tag.text.strip())
        
        # join the tags in the list with a comma
        tag = ', '.join(tag_list)

        # extract apply_link by finding the 'a' tag
        apply_link = posting.find('a', class_='posting-btn-submit').get('href')

        # create a dictionary with the extracted data
        job = {
            'title': title,
            'tag': tag,
            'apply_link': apply_link
        }

        # append the dictionary to the data list
        data.append(job)

    # convert the data list to JSON format
    json_data = json.dumps(data)

    # print out the JSON data
    print(json_data)

if __name__ == '__main__':
    # replace the url with the actual url
    url = "https://jobs.lever.co/appboxo"
    scraper(url) 