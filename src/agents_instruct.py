import io
import json
import logging
import os
import random
import re
import sys
import time
import traceback
from typing import Tuple

import openai
import requests
from bs4 import BeautifulSoup

# Initialize the OpenAI API
# APIKEY IS SET VIA ENVIRONEMNT
openai.api_key = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_NAME = "gpt-3.5-turbo-instruct"

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="web_scraper.log",
    filemode="a",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

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
    soup = BeautifulSoup(html_source, "html.parser")
    [s.decompose() for s in soup("script")]
    [s.decompose() for s in soup("style")]
    logger.info(f"Cleaned HTML Source:\n{html_source}\n")
    return str(soup)


def get_relevant_snippets(html_source: str, prompt: str, max_snippets: int = 3) -> list:
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

    while len(relevant_snippets) < max_snippets and attempts < max_snippets * 5:
        logger.info(
            f"Attempts: {attempts}, Found snippets: {len(relevant_snippets)}")
        # If the remaining text is shorter than 2000 characters, break
        if len(clean_html_source) <= 2000:
            break

        # Randomly select a start index for the snippet
        start_index = random.randint(0, len(clean_html_source) - 2000)
        snippet = clean_html_source[start_index: start_index + 2000]

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
        f"Determine if the following HTML snippet is relevant to the prompt: {prompt}\n "
        f'Reply "YES" or "NO" accordingly, and explain why.'
        f"\nHTML Snippet:\n{snippet}"
    )
    response = openai.Completion.create(
        model=OPENAI_MODEL_NAME, prompt=relevance_prompt, max_tokens=100
    )
    relevance_text = response.choices[0].text.strip()

    logger.info(f"Relevance check response:\n{relevance_text}")

    return "YES" in relevance_text


def generate_code(debugging_info: str, previous_code: str, prompt: str, website: str, relevant_snippets: list) -> str:
    if not relevant_snippets:
        logger.error("No relevant HTML snippets were provided.")
        return "No relevant HTML snippets were provided."

    # Randomly choose one of the relevant snippets
    relevant_snippet = random.choice(relevant_snippets)
    logger.info(f"Using Relevant Snippet:\n{str(relevant_snippet)}")

    # Proceed with code generation using the relevant snippet
    # instruct_prompt = (
    #     f"Please provide a Python function to scrape the website and extract: {prompt} as a JSON file.\n"
    #     f"The function should take in this HTML source as a string and print out the requested data in JSON format.\n"
    #     f"Generate only the process_source(html_source) function, and ensure the function declaration is included in your response.\n"
    #     f"**IMPORTANT**: You *MUST* wrap your code in a markdown code block. Like so: ```def blahblah```\n"
    #     f"You are provided the following relevant HTML snippet from somewhere in the webpage:\n{relevant_snippet}\n"
    #     f"**DO NOT** include example usages or outputs, I should only see the function definition.\n"
    #     f"This was the previous iteration of the code:\n{previous_code}\n"
    #     f"This is the debugging info as to why it didn't work:\n{debugging_info}\n"
    #     f"WRAP YOUR ANSWER IN A MARKDOWN CODE BLOCK!!\n"
    #     # f"Your code should *only* include the process_source function!\n"
    # )
    instruct_prompt = (
        f"Given the HTML snippet:\n{relevant_snippet}\n"
        f"and the debugging information:\n{debugging_info}\n"
        f"revise the previous code:\n{previous_code}\n"
        f"to define a Python function `process_source(html_source: str)` that processes the HTML source to extract {prompt}, "
        f"and prints the result as JSON."
        f"Reply in a Python markdown code block."
    )
    # log the prompt
    logger.info(f"Generation prompt:\n{instruct_prompt}")
    response = openai.Completion.create(
        model=OPENAI_MODEL_NAME, prompt=instruct_prompt, max_tokens=2000
    )

    # Log raw response
    logger.info(f"Raw response:\n{response}")

    stripped_response = response.choices[0].text.strip()
    # log the stripped response
    logger.info(f"Stripped response:\n{stripped_response}")

    patterns = [
        r"```python\n(.*?)```",  # Standard fenced code block
        r"```python\n(.*?)$",    # Code block without ending fence
        r"```\n(.*?)```",        # Fenced block without language specifier
        # Fenced block without ending fence or language specifier
        r"```\n(.*?)$"
        r"```(.*?)```",        # Fenced block without language specifier
        # Fenced block without ending fence or language specifier
        r"```(.*?)$"
    ]

    code = None
    for pattern in patterns:
        content_match = re.search(pattern, stripped_response, re.DOTALL)
        if content_match:
            code = content_match.group(1).strip()
            break

    if code:
        # Log the extracted code
        logger.info(f"Extracted Code:\n{code}")
        return code
    else:
        # If no code block is found, log the full response for manual inspection
        logger.error("Code block not found in response.")
        return "Failed to extract code from the AI's response."


def runner(process_source_code: str, html_source: str) -> Tuple[str, str]:
    """
    Runs the process_source function with the given HTML source and captures the printed output.
    Returns a tuple containing the output and the complete error stack trace, if any.
    """
    # Create a StringIO object to capture stdout
    captured_output = io.StringIO()
    # Initialize the error_message variable to capture stderr
    error_message = ""

    # Save the current stdout
    current_stdout = sys.stdout
    sys.stdout = captured_output

    try:
        # Define the scope where the process_source function will be executed
        local_scope = {}
        # Execute the generated code to define process_source in the local scope
        exec(process_source_code, globals(), local_scope)
        # Run the process_source function with the provided HTML source
        if 'process_source' in local_scope:
            local_scope['process_source'](html_source)
        else:
            raise Exception(
                "The process_source function is not defined in the generated code.")
    except Exception as e:
        # Capture any errors that occur during the execution of the process_source function
        error_message = traceback.format_exc()
        logger.error(f"Error during execution of process_source: {str(e)}")
    finally:
        # Restore stdout to its original state
        sys.stdout = current_stdout

        # Get the contents of the StringIO buffer
        output = captured_output.getvalue()
        # Close the StringIO buffer
        captured_output.close()

    # Check if the output is an empty list or an empty dictionary
    if output.strip() in ["[]", "{}", ""]:
        error_message = "Empty list or dictionary! No data returned, why?"
        output = "Empty list or dictionary! No data returned!"

    # Return the output and the error message
    return output, error_message


def verifier(output: str, prompt: str) -> Tuple[bool, str]:
    instruct_prompt = (
        f"Please verify if the following output snippet:\n```\n{output[:1000]}\n```\n"
        f"accurately fulfills the requirements based on the prompt:\n```\n{prompt}\n```\n"
        f"A valid output should be roughly JSON (not including braces is okay), and MUST NOT be an empty list and should have the content described by the prompt!"
        f"It must not be an empty list!"
        f'Respond with a brief explanation of your assessment, and then write either "YES" or "NO" in a markdown code block.'
    )
    response = openai.Completion.create(
        model=OPENAI_MODEL_NAME, prompt=instruct_prompt, max_tokens=1500
    )
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
    instruct_prompt = f"Given the code:\n{code}\nIdentify the issues and provide give one best guess for why this error occurs: {error}."
    response = openai.Completion.create(
        model=OPENAI_MODEL_NAME, prompt=instruct_prompt, max_tokens=2000
    )
    answer_text = response.choices[0].text
    return answer_text


def generate_scraper(
    prompt: str,
    website: str,
    output_dir: str,
    retry: int = 3,
    verbose: bool = False,
    output: str = "json",
    api_key: str = None,
    log: str = None,
) -> str:
    """
    Generates a web scraper using OpenAI's models.
    """
    html_source = scrape(website)
    # log original html source
    logger.info(f"Original HTML Source:\n{html_source}")
    debugging_info = "No debugging info."
    relevant_snippets = get_relevant_snippets(html_source, prompt)

    if not relevant_snippets:
        logger.error("No relevant HTML snippets were found.")
        return "No relevant HTML snippets were found."

    previous_code = "No previous code."
    for i in range(retry):
        code = generate_code(debugging_info, previous_code, prompt,
                             website, relevant_snippets)
        previous_code = code
        logger.info(f"Generated code (Attempt {i + 1}):\n{code}")

        result, error = runner(code, html_source)
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

            # # Delay before the next retry
            # if i < retry - 1:
            #     delay = (i + 1) * 1  # increasing delay with each retry
            #     logger.info(f"Waiting for {delay} seconds before retrying...")
            #     time.sleep(delay)
            continue

        verified, verifier_message = verifier(result, prompt)
        if verified:
            logger.info("Successfully generated a valid scraper.")
            logger.info(f"Generated result (Attempt {i + 1}):\n{result}")

            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(output_dir, "scraper.py")
            with open(filename, "w+") as f:
                f.write(code)

            return (
                f"Successfully generated a valid scraper in `{output_dir}/scraper.py`."
            )
        else:
            logger.warning(
                f"Output didn't match the prompt. Verifier Message (Attempt {i + 1}): {verifier_message}"
            )
            debugging_info = (
                f"Output didn't match the prompt. Expected: {prompt}. Got: {result}"
            )
            logger.error(
                f"Debugging info (Attempt {i + 1}):\n{debugging_info}")
    logger.error("Failed to generate a valid scraper after max retries.")
    return "Failed to generate a valid scraper after max retries."


def main():
    prompt = "job listings on this page"
    website = "https://jobs.lever.co/abridge"
    output_dir = "output/lever"
    result = generate_scraper(
        prompt, website, output_dir, verbose=True, retry=10)
    print(result)


if __name__ == "__main__":
    main()
