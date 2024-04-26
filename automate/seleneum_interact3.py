from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64
import re

def extract_urls(text):
    pattern = r'\b(?:http|https):\/\/(?:www\.)?[a-zA-Z0-9\-_]+(?:\.[a-zA-Z]{2,})+(?::\d{2,5})?(?:\/[^\s]*)?\b'
    urls = re.findall(pattern, text)
    return urls

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the webpage
driver.get('https://www.google.com/search?q=NEW+ENERGY+CONCEPTS+SOLAR%2C+2110+ARTESIA+BLVD+%23668+REDONDO+BEACH+++solar+install')

def main():
    # Setup Chrome WebDriver

    
    try:
        # URL you want to open

        # Get page source
        page_source = driver.page_source

        # Print the page source
       
        input(extract_urls(page_source))
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
