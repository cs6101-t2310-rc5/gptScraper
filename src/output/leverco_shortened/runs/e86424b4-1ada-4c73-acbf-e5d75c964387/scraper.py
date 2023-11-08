# imports
import bs4 
import requests
import json

def scraper(url: str) -> str:
    # make a GET request to the url
    response = requests.get(url)

    # check if the GET request was successful
    if response.status_code == 200:
        # use BeautifulSoup to parse the html
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        # find all the job listings by looking for the 'posting' class
        job_listings = soup.find_all('div', class_='posting')

        # create an empty list to store data
        results = []

        # loop through each job listing
        for job in job_listings:
            # extract the title by finding the 'posting-name' data-qa attribute
            title = job.find('h5', attrs={'data-qa':'posting-name'}).text

            # extract the tag by finding the 'posting-categories' class
            # and get the text of the first span element
            tag = job.find('span', class_='small-category-label').text

            # extract the apply_link by finding the 'posting-apply' class
            # and get the href attribute of the first 'a' element
            apply_link = job.find('div', class_='posting-apply').find('a')['href']

            # create a dictionary for each job listing
            job_dict = {
                'title': title,
                'tag': tag,
                'apply_link': apply_link
            }

            # append the dictionary to the results list
            results.append(job_dict)
        
        # convert the results list to JSON format and print it
        print(json.dumps(results))

    else:
        print('GET request was unsuccessful')

if __name__ == '__main__':
    url = "https://jobs.lever.co/appboxo"
    scraper(url)