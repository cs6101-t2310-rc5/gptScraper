# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url):
    # get HTML content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # extract the desired data
        paper_title = soup.find("meta", {"name": "citation_title"})["content"]
        authors = soup.find_all("meta", {"name": "citation_author"}) # returns a list of all authors
        abstract = soup.find("meta", {"property": "og:description"})["content"] # og:description contains the abstract
        # put the data into a dictionary
        data = {"paper_title": paper_title,
                "authors": [author["content"] for author in authors], # add each author to the list
                "abstract": abstract}
        # print the data in JSON format
        print(json.dumps(data))

if __name__ == '__main__':
    url = "https://arxiv.org/abs/2311.01449"
    scraper(url)

# OUTPUT:
# {"paper_title": "TopicGPT: A Prompt-based Topic Modeling Framework", "authors": ["Pham, Chau Minh", "Hoyle, Alexander", "Sun, Simeng", "Iyyer, Mohit"], "abstract": "Topic modeling is a well-established technique for exploring text corpora. Conventional topic models (e.g., LDA) represent topics as bags of words that often require \"reading the tea leaves\" to interpret; additionally, they offer users minimal semantic control over topics. To tackle these issues, we introduce TopicGPT, a prompt-based framework that uses large language models (LLMs) to uncover latent topics within a provided text collection. TopicGPT is a general-purpose topic modeling framework that offers several benefits. First, we demonstrate that TopicGPT can recover accurate, interpretable topics that are competitive with LDA's. Second, TopicGPT allows users to control the semantics of topics via prompts, which promote topic diversity and facilitate downstream applications. Finally, TopicGPT is robust to data sparsity and flexible in handling previously unseen words, two problems that hinder the popular variational auto-encoder based topic models."}