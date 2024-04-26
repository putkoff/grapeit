from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the webpage
driver.get('https://www.google.com/search?q=NEW+ENERGY+CONCEPTS+SOLAR%2C+2110+ARTESIA+BLVD+%23668+REDONDO+BEACH+++solar+install')

# Saving page to PDF
params = {
    'landscape': False,
    'printBackground': True,
    'pageSize': 'A4',
}
result = driver.execute_cdp_cmd("Page.printToPDF", params)

# Decode the PDF data from Base64
pdf = base64.b64decode(result['data'])

# Save the PDF
with open("webpage.pdf", "wb") as f:
    f.write(pdf)

# Close the browser
driver.quit()
