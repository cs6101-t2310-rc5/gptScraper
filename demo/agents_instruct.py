import openai
import requests
import logging
import time
import os
import re
import io
import sys
import random
import traceback

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


def strip_scripts_and_styles(html_source: str) -> str:
    """
    Removes all script and style tags from the HTML source.
    """
    soup = BeautifulSoup(html_source, 'html.parser')
    [s.decompose() for s in soup('script')]
    [s.decompose() for s in soup('style')]
    return str(soup)


def get_relevant_snippets(html_source: str, prompt: str, max_snippets: int = 5) -> list:
    """
    Generates up to 'max_snippets' relevant snippets from the HTML source,
    after removing <script> and <style> tags, and only considering 2000 character long snippets.
    """
    relevant_snippets = []
    attempts = 0

    # Clean the HTML source by stripping <script> and <style> tags
    clean_html_source = strip_scripts_and_styles(html_source)
    # log the clean html source
    # logger.info(f"Clean HTML Source:\n{clean_html_source}")

    while len(relevant_snippets) < max_snippets and attempts < max_snippets * 2:
        logger.info(
            f"Attempts: {attempts}, Found snippets: {len(relevant_snippets)}")
        # If the remaining text is shorter than 2000 characters, break
        if len(clean_html_source) <= 2000:
            break

        # Randomly select a start index for the snippet
        start_index = random.randint(0, len(clean_html_source) - 2000)
        snippet = clean_html_source[start_index:start_index + 2000]

        logger.info(f"Snippet (Attempt {attempts + 1}):\n{snippet}")

        if is_relevant_snippet(snippet, prompt):
            relevant_snippets.append(snippet)

        attempts += 1

    if not relevant_snippets:
        logger.error("No relevant HTML snippets found after maximum attempts.")

    return relevant_snippets


def is_relevant_snippet(snippet: str, prompt: str) -> bool:
    """
    Check if a HTML snippet is relevant to the scraping prompt.
    """
    relevance_prompt = (
        f"Determine if the following HTML snippet is relevant to scraping "
        f"If it contains information that is relevant to a LLM trying to generate code to scrape for the given prompt, then it is relevant. Reply \"YES\" or \"NO\" accordingly, and explain why."
        f".\nPrompt: {prompt}\nHTML Snippet:\n{snippet}"
    )
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct", prompt=relevance_prompt, max_tokens=100
    )
    relevance_text = response.choices[0].text.strip()

    logger.info(f"Relevance check response:\n{relevance_text}")

    return "YES" in relevance_text


def generate_code(debugging_info: str, prompt: str, website: str, relevant_snippets) -> str:
    if not relevant_snippets:
        logger.error("No relevant HTML snippets were provided.")
        return "No relevant HTML snippets were provided."

    # Randomly choose one of the relevant snippets
    relevant_snippet = random.choice(relevant_snippets)
    logger.info(f"Using Relevant Snippet:\n{str(relevant_snippet)}")

    # Proceed with code generation using the relevant snippet
    instruct_prompt = (
        f"Given the debugging info:\n{debugging_info}\n"
        f"Please provide Python code to scrape the website and extract: {prompt}\n"
        f"Based on the following relevant HTML snippet from somewhere in the webpage:\n{relevant_snippet}\n"
        f"The code should take in this link {website} and print out the requested data. "
        f"Generate only the code, enclose your answer in triple backticks."
    )
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct", prompt=instruct_prompt, max_tokens=2500
    )

    # Log raw response
    logger.info(f"Raw response:\n{response}")

    # Extract content between backticks from the model's response
    content_match = re.search(
        r'```python\n(.*?)```', response.choices[0].text, re.DOTALL)

    if content_match:
        code = content_match.group(1).strip()
        # Log the extracted code
        logger.info(f"Extracted Code:\n{code}")
        return code
    else:
        # If no code block is found, log the full response for manual inspection
        logger.error(
            f"Code block not found in response:\n{response.choices[0].text}")
        return "Failed to extract code from the AI's response."


def runner(code: str, url: str) -> Tuple[str, str]:
    """
    Runs the Python code with the given website URL and captures the printed output.
    Returns a tuple containing the output and error messages, if any.
    """
    # Create a StringIO object to capture stdout
    captured_output = io.StringIO()
    error_message = ""

    # Save the current stdout so that we can restore it later
    current_stdout = sys.stdout
    sys.stdout = captured_output

    try:
        # Prepare the local variables with the URL included
        local_vars = {'url': url}
        # Execute the code within the local scope
        exec(code, globals(), local_vars)
    except Exception:
        # Use traceback to get a detailed stack trace
        error_message = traceback.format_exc()
        logger.error(
            f"Error while running code with URL {url}:\n{error_message}")
    finally:
        # Get the contents of the StringIO buffer
        output = captured_output.getvalue()
        # Restore stdout to its original state
        sys.stdout = current_stdout
        captured_output.close()

    return output, error_message


def verifier(output: str, prompt: str) -> Tuple[bool, str]:
    instruct_prompt = (
        f"Please verify if the following output:\n```\n{output}\n```\n"
        f"accurately fulfills the requirements based on the prompt:\n```\n{prompt}\n```\n"
        "A valid output should not be an empty list and must conform to the structure and content described by the prompt. "
        "Respond with either \"YES\" or \"NO\" in a markdown code block, followed by a brief explanation of your assessment."
    )
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct", prompt=instruct_prompt, max_tokens=1500)
    answer_text = response.choices[0].text
    # log the answer text
    logger.info(f"Verifier response:\n{answer_text}")

    if "YES" in answer_text:
        return True, answer_text
    elif "NO" in answer_text:
        return False, answer_text
    else:
        return False, "Invalid response."


def debugger(code: str, error: str) -> str:
    instruct_prompt = f"Given the code:\n{code}\nIdentify the issues and provide debugging insights based on the error: {error}."
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct", prompt=instruct_prompt, max_tokens=2000)
    answer_text = response.choices[0].text
    return answer_text


def generate_scraper(prompt: str, website: str, retry: int = 3, verbose: bool = False, output: str = "json", api_key: str = None, model_id: str = "gpt-3.5-turbo", log: str = None) -> str:
    """
    Generates a web scraper using OpenAI's models.
    """
    html_source = scrape(website)
    debugging_info = ""
    relevant_snippets = get_relevant_snippets(html_source, prompt)

    for i in range(retry):
        code = generate_code(debugging_info, prompt,
                             website, relevant_snippets)
        logger.info(f"Generated code (Attempt {i + 1}):\n{code}")

        result, error = runner(code, website)
        # log results and errors
        logger.info(f"Result (Attempt {i + 1}):\n{result}")
        logger.info(f"Error (Attempt {i + 1}):\n{error}")
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
            return code
        else:
            logger.warning(
                f"Output didn't match the prompt. Verifier Message (Attempt {i + 1}): {verifier_message}")
            debugging_info = f"Output didn't match the prompt. Expected: {prompt}. Got: {result}"
            logger.error(
                f"Debugging info (Attempt {i + 1}):\n{debugging_info}")
    logger.error("Failed to generate a valid scraper after max retries.")
    return "Failed to generate a valid scraper after max retries."


def main():
    prompt = "job listings in JSON format"
    website = "https://jobs.lever.co/h1"
    result = generate_scraper(prompt, website, verbose=True, retry=10)
    print(result)


if __name__ == "__main__":
    main()
