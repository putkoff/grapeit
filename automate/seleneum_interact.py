from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL you want to open
url = 'http://example.com'

# Open the URL
driver.get(url)

# Get page source
page_source = driver.page_source

# Print the page source
print(page_source)

# Close the browser
driver.quit()
