import openai
import requests
import logging
import time
import os
from typing import Tuple
from bs4 import BeautifulSoup

# Initialize the OpenAI API
# APIKEY IS SET VIA ENVIRONEMNT
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='web_scraper.log', filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# Define a logger for this script
logger = logging.getLogger(__name__)


def scrape(url: str) -> str:
    """
    Scrapes a website and returns the HTML.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise exception for bad responses
        return response.text
    except Exception as e:
        logger.error(f"Error while scraping {url}: {str(e)}")
        return ""


def generate_code(debugging_info: str, prompt: str, html_source: str) -> str:
    instruct_prompt = f"Given the debugging info:\n{debugging_info}\nGenerate Python code to scrape the website for: {prompt}\nBased on the following HTML snippet: {html_source[:5000]}..."
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruct_prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=150)
    code = response.choices[0].message['content'].strip()
    return code


def runner(code: str) -> Tuple[str, str]:
    """
    Runs the Python code and returns the output or error.
    """
    output = None
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        output = local_vars.get('result', "")
        return output, ""
    except Exception as e:
        logger.error(f"Error while running code: {str(e)}")
        return "", str(e)


def verifier(output: str, prompt: str) -> Tuple[bool, str]:
    instruct_prompt = f"Given the output:\n{output}\nVerify if it matches the required data format specified by: {prompt}\nIf not, explain why."
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruct_prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=150)
    answer_text = response.choices[0].message['content'].strip().lower()

    if "yes" in answer_text:
        return True, "Output matches the constraints of the prompt."
    else:
        return False, answer_text


def debugger(code: str, error: str) -> str:
    instruct_prompt = f"Given the code:\n{code}\nIdentify the issues and provide debugging insights based on the error: {error}."
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruct_prompt}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=150)
    debugging_info = response.choices[0].message['content'].strip()
    return debugging_info


def generate_scraper(prompt: str, website: str, retry: int = 3, verbose: bool = False, output: str = "json", api_key: str = None, model_id: str = "gpt-3.5-turbo", log: str = None) -> str:
    """
    Generates a web scraper using OpenAI's models.
    """
    html_source = scrape(website)
    debugging_info = ""
    for i in range(retry):
        code = generate_code(debugging_info, prompt, html_source)
        logger.info(f"Generated code (Attempt {i + 1}):\n{code}")

        result, error = runner(code)
        if error:
            # Passing the generated code and error to the debugger
            debugging_info = debugger(code, error)
            logger.error(f"Attempt {i + 1} failed. Error: {error}")
            logger.error(
                f"Debugging info (Attempt {i + 1}):\n{debugging_info}")
            if verbose:
                print(
                    f"Attempt {i + 1} failed. Debugging info: {debugging_info}")

            # Delay before the next retry
            if i < retry - 1:
                delay = (i + 1) * 1  # increasing delay with each retry
                logger.info(f"Waiting for {delay} seconds before retrying...")
                time.sleep(delay)
            continue

        verified, verifier_message = verifier(result, prompt)
        if verified:
            logger.info("Successfully generated a valid scraper.")
            logger.info(f"Generated result (Attempt {i + 1}):\n{result}")
            return result
        else:
            logger.warning(
                f"Output didn't match the prompt. Verifier Message (Attempt {i + 1}): {verifier_message}")
            debugging_info = f"Output didn't match the prompt. Expected: {prompt}. Got: {result}"
            logger.error(
                f"Debugging info (Attempt {i + 1}):\n{debugging_info}")
    logger.error("Failed to generate a valid scraper after max retries.")
    return "Failed to generate a valid scraper after max retries."


def main():
    prompt = "books data in json format"
    website = "http://books.toscrape.com/"
    result = generate_scraper(prompt, website, verbose=True)
    print(result)


if __name__ == "__main__":
    main()
