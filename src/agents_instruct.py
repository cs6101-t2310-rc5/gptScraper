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
import asyncio
import os
import logging
import openai
from playwright.async_api import async_playwright

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


def get_relevant_snippets_interactive(html_source: str, prompt: str, max_snippets: int = 3, max_attempts: int = 50) -> list:
    total_characters = len(html_source)
    log = []
    relevant_snippets = []
    attempts = 0
    snippet_length = 2000  # Define the length of each snippet

    # Initial start index
    current_start_index = 0

    while len(relevant_snippets) < max_snippets and attempts < max_attempts:
        current_end_index = min(current_start_index +
                                snippet_length, total_characters)
        snippet = html_source[current_start_index:current_end_index]
        logger.info(
            f"Analyzing snippet from index {current_start_index} to {current_end_index}.")
        # log the nsippet
        logger.info(f"Snippet:\n{snippet}")

        # GPT-3 prompt for checking relevance
        relevance_prompt = f"Does the following HTML snippet contain content directly relevant to the prompt: '{prompt}'? Please respond with 'YES' or 'NO' and provide a brief explanation.\nSnippet:\n{snippet}\n"

        response = openai.Completion.create(
            model=OPENAI_MODEL_NAME,
            prompt=relevance_prompt,
            max_tokens=150
        )

        output = response.choices[0].text.strip()
        logger.info(f"GPT-3 response to relevance: {output}")

        if "YES" in output:
            logger.info("GPT-3 determined the snippet is relevant.")
            relevant_snippets.append((current_start_index, snippet))

        relevance = "YES" if "YES" in output else "NO"
        # append to log regardless
        log.append({
            "start_index": current_start_index,
            "end_index": current_end_index,
            "relevance": relevance,
            "explanation": output
        })

        # format the log in lines
        log_str = ""
        for entry in log:
            log_str += f"Start index: {entry['start_index']}, End index: {entry['end_index']}, Relevance: {entry['relevance']}, Explanation: {entry['explanation']}\n"

        # If not enough relevant snippets found, ask for the next start index
        if len(relevant_snippets) < max_snippets:
            find_next_prompt = (
                f"Considering the HTML content and the prompt: '{prompt}', what should be the start index for the next snippet to examine?"
                f"For context, this is what you've found so far:\n"
                f"{log_str}\n"
                f"Try to explore the HTML, rather than going sequentially.\n"
                f"Try to avoid CSS & style tags, and focus on the content.\n"
                f"Please provide the next start index wrapped in backticks like so: `58`\n"
            )

            # log the find next prompt
            logger.info(f"Find next prompt:\n{find_next_prompt}")

            next_response = openai.Completion.create(
                model=OPENAI_MODEL_NAME,
                prompt=find_next_prompt,
                max_tokens=150
            )

            next_output = next_response.choices[0].text.strip()
            logger.info(f"GPT-3 response for the next index: {next_output}")

            # Extracting the start index using regex
            index_match = re.search(r"`(\d+)`", next_output)
            if index_match:
                suggested_start_index = int(index_match.group(1))
                if 0 <= suggested_start_index < total_characters - snippet_length:
                    current_start_index = suggested_start_index
                    logger.info(
                        f"Next start index suggested by GPT-3: {suggested_start_index}.")
                else:
                    logger.error(
                        "GPT-3 suggested an invalid start index. Choosing a random index.")
                    current_start_index = generate_random_start_index(
                        total_characters, snippet_length)
            else:
                logger.error(
                    "GPT-3 did not suggest a valid start index. Choosing a random index.")
                current_start_index = generate_random_start_index(
                    total_characters, snippet_length)

        attempts += 1

    if not relevant_snippets:
        logger.warning(
            "No relevant snippets found after the maximum number of attempts.")
    else:
        logger.info(f"Found {len(relevant_snippets)} relevant snippets.")

    return relevant_snippets


def generate_random_start_index(total_characters: int, snippet_length: int) -> int:
    """
    Generates a random start index for the snippet.
    """
    return random.randint(0, total_characters - snippet_length)


async def scrape_with_playwright(url: str) -> str:
    """
    Scrapes a website using Playwright and returns the HTML.
    This function is asynchronous and should be run within an asyncio event loop.
    """
    async with async_playwright() as p:
        # Launch the browser in headless mode
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        # Wait for the network to be idle (all resources loaded)
        await page.wait_for_load_state('networkidle')
        content = await page.content()  # Get the page content
        await browser.close()
        return content


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
    logger.info(f"Cleaned HTML Source:\n{str(soup)}\n")
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


def generate_code(
    debugging_info: str, prompt: str, website: str, relevant_snippets
) -> str:
    if not relevant_snippets:
        logger.error("No relevant HTML snippets were provided.")
        return "No relevant HTML snippets were provided."

    # Randomly choose one of the relevant snippets
    relevant_snippet = random.choice(relevant_snippets)
    logger.info(f"Using Relevant Snippet:\n{str(relevant_snippet)}")

    # Proceed with code generation using the relevant snippet
    instruct_prompt = (
        f"Given the debugging info:\n{debugging_info}\n"
        f"Please provide Python code to scrape the website and extract: {prompt} as a JSON file.\n"
        f"Based on the following relevant HTML snippet from somewhere in the webpage:\n{relevant_snippet}\n"
        f"The code should take in this link {website} and print out the requested data. "
        f"The website may be dynamically loaded, so use Playwright to wait for the page to load before scraping.\n"
        f"Generate only the code, you MUST wrap your answer in a markdown code block."
    )
    response = openai.Completion.create(
        model=OPENAI_MODEL_NAME, prompt=instruct_prompt, max_tokens=2500
    )

    # Log raw response
    logger.info(f"Raw response:\n{response}")

    # Extract content between backticks from the model's response
    content_match = re.search(
        r"```python\n(.*?)```", response.choices[0].text, re.DOTALL
    )

    if not content_match:
        logger.info("Code block not found. Trying without python syntax.")
        content_match = re.search(
            r"```python\n(.*?)$", response.choices[0].text, re.DOTALL
        )

    if not content_match:
        logger.info("Code block not found. Trying without python syntax.")
        content_match = re.search(
            r"```\n(.*?)```", response.choices[0].text, re.DOTALL)

    if not content_match:
        logger.info(
            "Code block not found. Trying without both ended backticks.")
        content_match = re.search(
            r"```\n(.*?)$", response.choices[0].text, re.DOTALL)

    if content_match:
        code = content_match.group(1).strip()
        # Log the extracted code
        logger.info(f"Extracted Code:\n{code}")

    else:
        logger.info("Code block not found. Giving raw response.")
        code = response.choices[0].text

        logger.info(f"Extracted Code:\n{code}")

    return code
    # else:
    #     # If no code block is found, log the full response for manual inspection
    #     logger.error(
    #         f"Code block not found in response:\n{response.choices[0].text}")
    #     return "Failed to extract code from the AI's response."


def runner(code: str, url: str) -> Tuple[str, str]:
    """
    Runs the Python code with the given website URL and captures the printed output.
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
        # Execute the code within the local scope
        exec(code, globals())
    except Exception as e:
        # Format the complete stack trace including the error within the executed code
        error_message = traceback.format_exc()
    finally:
        # Restore stdout to its original state
        sys.stdout = current_stdout

        # Get the contents of the StringIO buffer
        output = captured_output.getvalue()
        # Close the StringIO buffer
        captured_output.close()

    # Return the output and the error message
    if output == "":
        return "NO OUTPUT GIVEN!!", error_message
    # if output is empty list
    if output == "[]" or output == "[]\n":
        return "Empty list! No data returned!", "Empty list! No data returned, why?"
    if output == "\{\}" or output == "\{\}\n":
        return "Empty list! No data returned!", "Empty list! No data returned, why?"
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
    # html_source = scrape(website)
    html_source = asyncio.run(scrape_with_playwright(website))

    # log original html source
    logger.info(f"Original HTML Source:\n{html_source}")
    debugging_info = ""
    # relevant_snippets = get_relevant_snippets(html_source, prompt)
    relevant_snippets = get_relevant_snippets_interactive(html_source, prompt)

    if not relevant_snippets:
        logger.error("No relevant HTML snippets were found.")
        return "No relevant HTML snippets were found."

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
    prompt = "listing information on this page"
    website = "https://shopee.sg/CORSAIR-Vengeance-RGB-PRO-SL-16GB-(2-x-8GB)-DDR4-3200MHz-C16-DIMM-Desktop-Memory-Kit-White-CMH16GX4M2E3200C16W-i.287857235.9031119578?sp_atk=ad7440df-95ba-4df6-a396-162bf5cf2556&xptdk=ad7440df-95ba-4df6-a396-162bf5cf2556"
    output_dir = "output/lever"
    result = generate_scraper(
        prompt, website, output_dir, verbose=True, retry=10)
    print(result)


if __name__ == "__main__":
    main()
