from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time, dotenv, os, pandas as pd

dotenv.load_dotenv()

os.makedirs('download', exist_ok=True)

# Initialize the WebDriver (ChromeDriver should be in your PATH)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
prefs = {
    "download.default_directory": os.path.abspath('download'),  # Set the download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "plugins.always_open_pdf_externally": True  # Open PDFs externally (not in Chrome)
}
options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver (ChromeDriver should be in your PATH)
driver = webdriver.Chrome(options=options)

# Open the browser and navigate to the login page
driver.get('https://ftp.ccohs.ca/Login')  # Change this to the URL of the login page

# Allow some time for the page to load
time.sleep(2)

# Find the login form elements and enter credentials
username_field = driver.find_element(By.NAME, 'RumpusLoginUserName')  # Change 'username' to the name or id of the username field
password_field = driver.find_element(By.NAME, 'RumpusLoginPassword')  # Change 'password' to the name or id of the password field

username_field.send_keys(os.getenv('RTECS_USERNAME'))  # Replace with your username
password_field.send_keys(os.getenv('RTECS_PASSWORD'))  # Replace with your password

# Submit the form
password_field.send_keys(Keys.RETURN)

# Allow some time for the login process to complete
time.sleep(3)

# List all the td fields
tds = driver.find_elements(By.TAG_NAME, 'td')

# list their text and find the field(s) ending in .xml.gz
dl_td = [td for td in tds if '.xml.gz' in td.text]

# send a click to each one
for td in dl_td:
    print(f"downloading...{td.text}")
    td.click()
    time.sleep(1)

# loop through download directory until there are no more .crdownload files
# print the current size of the dir (in mb) on each loop
# if it takes more than 20 minutes exit with exception
start = time.time()
while any([f.endswith('.crdownload') for f in os.listdir('download')]):
    mbdir = sum(os.path.getsize(os.path.join('download', f)) for f in os.listdir('download')) / 1024 / 1024
    print(f"Downloading...{mbdir:.2f}mb completed")
    elapsed = time.time() - start
    if elapsed > 1200:
        raise Exception("Download took too long")
    time.sleep(1)
     
driver.quit()