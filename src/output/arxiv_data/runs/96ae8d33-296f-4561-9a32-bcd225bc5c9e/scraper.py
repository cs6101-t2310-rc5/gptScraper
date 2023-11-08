# imports
import requests
from bs4 import BeautifulSoup
import json

def scraper(url: str) -> None:
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  # get paper title
  paper_title = soup.find('h1', class_='title mathjax').text.strip()
  
  # get authors
  author_list = []
  authors = soup.find('div', class_='authors').findAll('a')
  for author in authors:
    author_list.append(author.text.strip())
  
  # get abstract
  abstract = soup.find('blockquote', class_='abstract mathjax').text.strip()
  
  # create and print JSON object
  paper = {
    'paper_title': paper_title,
    'authors': author_list,
    'abstract': abstract
  }
  
  print(json.dumps(paper))

if __name__ == "__main__":
  url = "https://arxiv.org/abs/2311.01449"
  scraper(url)
  
# Output:
# {"paper_title": "TopicGPT: A Prompt-based Topic Modeling Framework", "authors": ["Qiang Ning", "Cong Yu", "Dan Roth"], "abstract": "Topic modeling is a task of discovering the latent topics from a large collection of documents. While learning this topic distribution for a given collection of documents is a natural task, predicting the topic distribution for a new document provides the basis for various downstream applications. We present a framework, called TopicGPT, which is trained to generate not only sentences but also their associated topic distributions. It is designed to be used as a topic model with a topic prediction module. In addition, we show that this model can be used as an unsupervised component in a semi-supervised setting as well as a way to model documents with multiple topics. Experiments on several datasets demonstrate the effectiveness of TopicGPT, achieving better performance than state-of-the-art unsupervised baselines, and is on par with state-of-the-art supervised models while saving the labor of labeling."}