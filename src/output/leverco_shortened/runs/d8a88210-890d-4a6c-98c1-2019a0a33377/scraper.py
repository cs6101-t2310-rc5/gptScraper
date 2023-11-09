# imports
import bs4 

def scraper(url: str) -> str:
  # make GET request to the url
  response = requests.get(url)

  # parse the HTML content
  soup = BeautifulSoup(response.content, 'html.parser')

  # find all the job posting divs
  job_divs = soup.find_all('div', class_='postings-wrapper')

  # loop through the job posting divs
  for div in job_divs:
    # extract the category title
    category_title = div.find('div', class_='posting-category-title').text
    # extract all job listings under the category
    job_list = div.find_all('div', class_='posting')
    # loop through the job listings
    for job in job_list:
      # extract the tag 
      tag = job.find('div', class_='posting-categories').text.strip()
      # extract the job title
      title = job.find('h5', {'data-qa' : 'posting-name'}).text.strip()
      # extract the application link
      apply_link = job.find('div', {'data-qa': 'btn-apply'}).find('a', {'class': 'posting-btn-submit'}).get('href')
      # create a dictionary with all the extracted data
      job_dict = {
          'title': title,
          'tag': tag,
          'apply_link': apply_link
      }
      # print out the job listings in JSON format
      print(json.dumps(job_dict, indent=2))

if __name__ == '__main__':
  url = "https://jobs.lever.co/appboxo"
  scraper(url)