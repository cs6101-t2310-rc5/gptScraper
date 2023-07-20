import time
import openai
import click
import json
from bs4 import BeautifulSoup
import requests
import logging

def get_html(url: str):
    logging.info(f"Fetching HTML from: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    logging.info(f"Finished fetching HTML from: {url}")
    html = BeautifulSoup(response.text, 'html.parser').prettify()
    #return the middle 5000 characters
    html = html[len(html)//2-2500:len(html)//2+2500]

    return html
        
@click.command()
@click.option('-p', '--prompt', type=str, required=True, help='A string to prompt GPT-4.')
@click.option('-w', '--website', type=str, required=True, help='Website URL to generate a scraper for.')
@click.option('-n', '--retry', type=int, default=3, help='Number of times to retry.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose logging.')
@click.option('-o', '--output', type=click.Path(), default='output.txt', help='Output file for the scraper.')
@click.option('--api_key', type=str, required=True, help='Your OpenAI API key.')
@click.option('--model_id', type=str, default="gpt-3.5-turbo", help='The ID of the OpenAI model to use.')
@click.option('--log', type=click.Path(), default='script.log', help='Log file.')
def generate_scraper(prompt, website, retry, verbose, output, api_key, model_id, log):
    """
    A command-line interface (CLI) to generate web scrapers using OpenAI's models.
    """
    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    file_handler = logging.FileHandler(log)
    file_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    openai.api_key = api_key

    logger.info(
        f"Generating a scraper for {website} with prompt '{prompt}', will retry {retry} times if there are errors.")
    logger.info(f"The scraper will be saved to {output}.")

    # get website html
    html = get_html(website)

    messages = [
        {"role": "system", "content": f"You are a helpful assistant tasked with generating a Python web scraper for the website: {website}. Here is the HTML structure: \n\n{html}"},
        {"role": "user", "content": f"{prompt}\n\nPlease generate a scraper for this website. Format your answer like this 'ADDITIONAL ICODE_SENTINEL'."},
    ]

    for i in range(retry):
        try:
            logger.info("Making API call to generate code.")
            logger.info(f"API request: {json.dumps(response.to_dict(), indent=2)}")  # Log the API request
            response = openai.ChatCompletion.create(
                model=model_id, messages=messages)
            logger.info(f"API response: {json.dumps(response.choices[0].message['content'], indent=2)}")  # Log the API response
            
            scraper_code = response.choices[0].message['content'].split('CODE_SENTINEL')[1]
            
            if 'WALRUS_OK' in scraper_code:
                with open(output, 'w') as f:
                    f.write(scraper_code.replace('WALRUS_OK', ''))
                logger.info("Scraper written successfully.")
                break
            else:
                logger.info("The generated code was incorrect. Retrying...")
                messages.append({"role": "user", "content": "The code was not correct. Please generate a new scraper. Remember to output 'WALRUS_OK' if the generated scraper is correct and works as intended."})

        except Exception as e:
            logger.error(f"Attempt {i+1} failed with error: {e}. Retrying...")
            time.sleep(1)  # add a 1-second delay before the next retry

    logger.info("Done generating the scraper.")

if __name__ == '__main__':
    generate_scraper()